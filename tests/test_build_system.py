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


def test_custom_build_compiles_canonical_contract_snapshot():
    import json
    import shutil

    for name in ["build", "dist"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-customcontract",
         "--targets", "custom-gpt"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    custom = ROOT / "build" / "custom-gpt"
    snapshot = json.loads((custom / "builder" / "runtime-contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((custom / "MANIFEST.json").read_text(encoding="utf-8"))
    report = json.loads((custom / "builder" / "compilation-report.json").read_text(encoding="utf-8"))

    assert snapshot["runtime_id"] == "chatgpt_custom"
    assert snapshot["capabilities"]["contract_version"] == 1
    assert snapshot["artifacts"]["contract_version"] == 1
    assert snapshot["workspace_state"]["contract_version"] == 1
    assert snapshot["tools"]["contract_version"] == 1
    assert snapshot["adapter"]["builder_package"] is True
    assert snapshot["adapter"]["tool_execution"] == "not_embedded"

    tool_states = {item["id"]: item for item in snapshot["adapter"]["tool_states"]}
    assert tool_states["lint-project"]["state"] == "missing"
    assert tool_states["project-hygiene"]["state"] == "reduced"

    assert manifest["adapter_id"] == "chatgpt_custom"
    assert manifest["contract_snapshot"] == "builder/runtime-contract.json"
    assert report["runtime_id"] == "chatgpt_custom"
    assert report["contract_snapshot"] == "builder/runtime-contract.json"


def test_claude_build_compiles_project_package_from_canonical_contracts():
    import json
    import shutil

    for name in ["build", "dist"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-claudecontract",
         "--targets", "claude"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    claude = ROOT / "build" / "claude"
    snapshot = json.loads((claude / "project" / "runtime-contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((claude / "MANIFEST.json").read_text(encoding="utf-8"))

    assert snapshot["runtime_id"] == "claude_project"
    assert snapshot["capabilities"]["contract_version"] == 1
    assert snapshot["artifacts"]["contract_version"] == 1
    assert snapshot["workspace_state"]["contract_version"] == 1
    assert snapshot["tools"]["contract_version"] == 1
    assert snapshot["adapter"]["claude_code_conventions"] is False
    assert snapshot["adapter"]["project_instructions"] is True
    assert snapshot["adapter"]["project_knowledge"] is True

    assert (claude / "project" / "instructions.md").exists()
    assert (claude / "README.md").exists()
    assert not (claude / "CLAUDE.md").exists()

    assert manifest["adapter_id"] == "claude_project"
    assert manifest["contract_snapshot"] == "project/runtime-contract.json"
    assert manifest["project_instructions"] == "project/instructions.md"


def test_opencode_build_compiles_base_workspace_from_canonical_contracts():
    import json
    import shutil

    for name in ["build", "dist"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-opencodecontract",
         "--targets", "opencode"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    opencode = ROOT / "build" / "opencode"
    snapshot = json.loads((opencode / ".opencode" / "runtime-contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((opencode / "MANIFEST.json").read_text(encoding="utf-8"))
    agents = (opencode / "AGENTS.md").read_text(encoding="utf-8")

    assert snapshot["runtime_id"] == "opencode"
    assert snapshot["capabilities"]["contract_version"] == 1
    assert snapshot["artifacts"]["contract_version"] == 1
    assert snapshot["workspace_state"]["contract_version"] == 1
    assert snapshot["tools"]["contract_version"] == 1
    assert snapshot["adapter"]["workspace_first"] is True
    assert snapshot["adapter"]["skills_included"] is True
    assert snapshot["adapter"]["skills"] == ["gpt-project-workflow"]
    assert snapshot["adapter"]["tool_integration"] == "custom_tools"

    assert "OpenCode adapter" in agents
    assert (opencode / "AGENTS.md").exists()
    assert not (opencode / "CLAUDE.md").exists()
    skill = opencode / ".opencode" / "skills" / "gpt-project-workflow" / "SKILL.md"
    assert skill.exists()
    skill_text = skill.read_text(encoding="utf-8")
    assert "name: gpt-project-workflow" in skill_text
    assert "description:" in skill_text
    assert (skill.parent / "references" / "dynamic-planning.md").exists()
    assert (skill.parent / "references" / "resume-flow.md").exists()
    assert (skill.parent / "references" / "next-step-recommendation.md").exists()

    assert manifest["adapter_id"] == "opencode"
    assert manifest["contract_snapshot"] == ".opencode/runtime-contract.json"
    assert manifest["instructions"] == "AGENTS.md"
    assert manifest["skills_included"] is True
    assert manifest["skills"] == ["gpt-project-workflow"]
    assert manifest["tool_integration"] == "custom_tools"

    integrations = {item["id"]: item for item in snapshot["adapter"]["tool_integrations"]}
    assert integrations["lint-project"]["opencode_tool"] == "gpt_lint_project"
    assert integrations["project-hygiene"]["permission"] == "ask"
    assert integrations["lint-project"]["permission"] == "allow"

    config = json.loads((opencode / "opencode.json").read_text(encoding="utf-8"))
    assert config["permission"]["gpt_lint_project"] == "allow"
    assert config["permission"]["gpt_project_hygiene"] == "ask"
    assert config["permission"]["bash"] == "ask"
    assert config["permission"]["edit"] == "ask"

    assert (opencode / ".opencode" / "tools" / "gpt_lint_project.ts").exists()
    assert (opencode / ".opencode" / "tools" / "gpt_recommend_next_step.ts").exists()
    assert (opencode / ".opencode" / "tools" / "gpt_project_hygiene.ts").exists()
    assert (opencode / "scripts" / "lint_gpt_project.py").exists()
    assert (opencode / "scripts" / "lib" / "project_model.py").exists()
    assert not (opencode / "scripts" / "validate_release_candidate.py").exists()
