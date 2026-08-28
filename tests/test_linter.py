from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def _clean_generated_state():
    for name in ["build", "dist", ".pytest_cache"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)
    for p in sorted(ROOT.rglob("__pycache__"), key=lambda x: len(x.parts), reverse=True):
        if p.exists():
            shutil.rmtree(p)
    for p in ROOT.rglob("*.py[co]"):
        if p.exists():
            p.unlink()

def test_linter_current_project_has_no_errors():
    _clean_generated_state()
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_gpt_project.py"),
         "--project-root", str(ROOT), "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    report = json.loads(r.stdout)
    assert report["summary"]["errors"] == 0

def _write_minimal_project(tmp_path, canonical_text, core_contract):
    import yaml
    (tmp_path / "src" / "instructions").mkdir(parents=True)
    (tmp_path / "knowledge").mkdir(exist_ok=True)
    (tmp_path / "src" / "instructions" / "system.md").write_text(canonical_text, encoding="utf-8")
    for rel in ["README.md", "PROJECT.md", "STATUS.md", "project-status.yaml"]:
        (tmp_path / rel).write_text("ok\n", encoding="utf-8")
    cfg = {
        "schema_version": 1,
        "instructions": {
            "canonical": "src/instructions/system.md",
            "core_contract": core_contract,
        },
        "knowledge_architecture": {"canonical_root": "knowledge"},
    }
    (tmp_path / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def _run_linter(project_root):
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_gpt_project.py"),
         "--project-root", str(project_root), "--json"],
        capture_output=True, text=True
    )
    return r, json.loads(r.stdout)


def test_linter_rejects_missing_core_behavior_marker(tmp_path):
    _write_minimal_project(tmp_path, "# GPT\n", {
        "enabled": True,
        "required_markers": ["MANDATORY CORE RULE"],
        "required_runtime_dependencies": [],
        "max_required_file_hops": 1,
        "knowledge_may_not_be_required_for_core_behavior": True,
    })
    r, report = _run_linter(tmp_path)
    assert r.returncode == 1
    assert any(f["code"] == "GP502" for f in report["findings"])


def test_linter_rejects_knowledge_as_required_core_dependency(tmp_path):
    (tmp_path / "knowledge").mkdir(parents=True)
    (tmp_path / "knowledge" / "rules.md").write_text("rule\n", encoding="utf-8")
    _write_minimal_project(tmp_path, "# GPT\nMANDATORY CORE RULE\n", {
        "enabled": True,
        "required_markers": ["MANDATORY CORE RULE"],
        "required_runtime_dependencies": ["knowledge/rules.md"],
        "max_required_file_hops": 1,
        "knowledge_may_not_be_required_for_core_behavior": True,
    })
    r, report = _run_linter(tmp_path)
    assert r.returncode == 1
    assert any(f["code"] == "GP505" for f in report["findings"])


def test_linter_warns_when_required_file_hops_exceed_budget(tmp_path):
    _write_minimal_project(tmp_path, "# GPT\nMANDATORY CORE RULE\n", {
        "enabled": True,
        "required_markers": ["MANDATORY CORE RULE"],
        "required_runtime_dependencies": ["PROJECT.md", "STATUS.md"],
        "max_required_file_hops": 1,
        "knowledge_may_not_be_required_for_core_behavior": True,
    })
    r, report = _run_linter(tmp_path)
    assert r.returncode == 0
    assert any(f["code"] == "GP504" and f["severity"] == "warning" for f in report["findings"])

def test_linter_rejects_missing_readme(tmp_path):
    _write_minimal_project(tmp_path, "# GPT\nMANDATORY CORE RULE\n", {
        "enabled": True,
        "required_markers": ["MANDATORY CORE RULE"],
        "required_runtime_dependencies": [],
        "max_required_file_hops": 1,
        "knowledge_may_not_be_required_for_core_behavior": True,
    })
    (tmp_path / "README.md").unlink()
    r, report = _run_linter(tmp_path)
    assert r.returncode == 1
    assert any(f["code"] == "GP110" and f.get("path") == "README.md" for f in report["findings"])


def test_linter_requires_github_workflows_when_enabled(tmp_path):
    import yaml
    _write_minimal_project(tmp_path, "# GPT\nMANDATORY CORE RULE\n", {
        "enabled": True,
        "required_markers": ["MANDATORY CORE RULE"],
        "required_runtime_dependencies": [],
        "max_required_file_hops": 1,
        "knowledge_may_not_be_required_for_core_behavior": True,
    })
    cfg = yaml.safe_load((tmp_path / "gpt-project.yaml").read_text(encoding="utf-8"))
    cfg["ci"] = {"enabled": True, "workflow": ".github/workflows/ci.yml"}
    cfg["release"] = {"github": {"enabled": True, "workflow": ".github/workflows/release.yml"}}
    (tmp_path / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    r, report = _run_linter(tmp_path)
    assert r.returncode == 1
    codes = {f["code"] for f in report["findings"]}
    assert "GP400" in codes
    assert "GP410" in codes
