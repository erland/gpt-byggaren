from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_build_and_validate():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-test"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    r2 = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_distributions.py"),
         "--project-root", str(ROOT)],
        capture_output=True, text=True
    )
    assert r2.returncode == 0, r2.stdout + r2.stderr


def test_custom_knowledge_prioritizes_declared_globs(tmp_path):
    import importlib.util
    import yaml
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT / "scripts" / "build_distributions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    kroot = tmp_path / "knowledge"
    (kroot / "domain").mkdir(parents=True)
    (kroot / "reference").mkdir(parents=True)
    for i in range(3):
        (kroot / "domain" / f"critical-{i}.md").write_text("critical\n", encoding="utf-8")
    for i in range(25):
        (kroot / "reference" / f"ref-{i:02d}.md").write_text("ref\n", encoding="utf-8")

    cfg = {
        "knowledge_architecture": {
            "canonical_root": "knowledge",
            "custom_gpt": {"priority": ["knowledge/domain/**"]},
        },
        "runtime": {"custom_gpt": {"knowledge": {"max_files": 20, "strategy": "hybrid"}}},
    }
    target = tmp_path / "out"
    selected = mod.collect_custom_knowledge(tmp_path, cfg, target)
    rels = [p.relative_to(target).as_posix() for p in selected]
    assert len(rels) == 20
    assert all(f"domain/critical-{i}.md" in rels for i in range(3))


def test_custom_instruction_compiler_preserves_core_markers():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT / "scripts" / "build_distributions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text = "# GPT\n\n\nCORE RULE\n\n\nOther rule\n"
    compiled = mod.compile_custom_instruction(text, "compressed", 1000, ["CORE RULE"])
    assert "CORE RULE" in compiled
    assert "\n\n\n" not in compiled


def test_custom_instruction_compiler_blocks_overflow_after_safe_compression():
    import importlib.util
    import pytest
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT / "scripts" / "build_distributions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with pytest.raises(SystemExit) as exc:
        mod.compile_custom_instruction("CORE RULE\n" + ("x" * 200), "compressed", 50, ["CORE RULE"])
    assert "do not move core behavior to Knowledge" in str(exc.value)


def test_custom_build_emits_compilation_report():
    import json
    import shutil
    for name in ["build", "dist"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-reporttest"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    report_path = ROOT / "build" / "custom-gpt" / "builder" / "compilation-report.json"
    assert report_path.exists()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["instruction"]["compiled_characters"] <= report["instruction"]["max_characters"]
    assert report["knowledge"]["selected_files"] <= report["knowledge"]["max_files"]


def test_chat_build_compiles_canonical_contract_snapshot_and_declared_tools():
    import json
    import shutil

    for name in ["build", "dist"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-chatcontract",
         "--targets", "chat"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    chat = ROOT / "build" / "chat"
    snapshot = json.loads((chat / "assistant" / "runtime-contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((chat / "MANIFEST.json").read_text(encoding="utf-8"))

    assert snapshot["runtime_id"] == "chatgpt_chat"
    assert snapshot["capabilities"]["contract_version"] == 1
    assert snapshot["artifacts"]["contract_version"] == 1
    assert snapshot["workspace_state"]["contract_version"] == 1
    assert snapshot["tools"]["contract_version"] == 1

    declared = set(snapshot["declared_tool_scripts"])
    assert "scripts/lint_gpt_project.py" in declared
    assert "scripts/build_distributions.py" in declared

    assert (chat / "scripts" / "lint_gpt_project.py").exists()
    assert (chat / "scripts" / "build_distributions.py").exists()
    assert (chat / "scripts" / "lib" / "project_model.py").exists()

    # Development/release scripts are not runtime tools merely because they live under scripts/.
    assert not (chat / "scripts" / "validate_release_candidate.py").exists()
    assert not (chat / "scripts" / "validate_stable_release.py").exists()

    assert manifest["adapter_id"] == "chatgpt_chat"
    assert manifest["contract_snapshot"] == "assistant/runtime-contract.json"
