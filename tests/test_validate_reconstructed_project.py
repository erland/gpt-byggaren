from pathlib import Path
import importlib.util
import json
import shutil

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_reconstructed_project", ROOT / "scripts/validate_reconstructed_project.py")
import sys
sys.path.insert(0, str(ROOT / "scripts"))
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def create_fixture(tmp_path, include_status_schema=True):
    cfg = {
        "project": {"id": "recovered", "name": "Recovered"},
        "instructions": {"canonical": "src/instructions/system.md"},
        "reconstruction": {"status": "canonical_contracts_scaffolded", "release_ready": False},
        "runtime": {"plugin": {"enabled": False}, "custom_gpt": {"enabled": False}},
        "capabilities": {"contract_version": 1, "recommendation_mode": "inferred_from_use_case", "requirements": {},
                         "schema": "schemas/capability-contract.schema.json"},
        "artifacts": {"contract_version": 1, "outputs": {"project_package": {
            "kind": "package", "format": "zip", "requirement": "optional", "persistence": "persistent"}},
            "schema": "schemas/artifact-contract.schema.json"},
        "workspace_state": {"contract_version": 1, "workspace": {
            "requirement": "required", "persistence": "required", "portable": True, "separate_from_assistant": True},
            "state": {"requirement": "required", "persistence": "required", "authority": "workspace_file",
                      "format": "yaml", "path": "project-status.yaml"},
            "schema": "schemas/workspace-state-contract.schema.json"},
        "tools": {"contract_version": 1, "tools": [], "schema": "schemas/tool-contract.schema.json"},
    }
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    instruction = tmp_path / "src/instructions/system.md"
    instruction.parent.mkdir(parents=True)
    instruction.write_text("Recovered behavior", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Recovered project\\n", encoding="utf-8")
    (tmp_path / "PROJECT.md").write_text("# Project\\n", encoding="utf-8")
    (tmp_path / "STATUS.md").write_text("# Status: blocked\\n", encoding="utf-8")
    status = {"schema_version": 1, "project": {"id": "recovered", "name": "Recovered"},
              "plan": {"path": "docs/development-plan.md", "total_steps": 1},
              "progress": {"current_step": 1, "last_completed_step": 0, "completed_steps": []},
              "state": {"overall": "blocked", "blocking_issues": ["Runtime review"], "warnings": []},
              "next_step": {"recommended": 1, "title": "Review", "reason": "Pending"},
              "resume": {"supported": True, "required_files": ["gpt-project.yaml"]}}
    (tmp_path / "project-status.yaml").write_text(yaml.safe_dump(status), encoding="utf-8")
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    for name in ("capability-contract.schema.json", "artifact-contract.schema.json",
                 "workspace-state-contract.schema.json", "tool-contract.schema.json"):
        shutil.copyfile(ROOT / "schemas" / name, schemas / name)
    if include_status_schema:
        shutil.copyfile(ROOT / "schemas/project-status.schema.json", schemas / "project-status.schema.json")
    return cfg


def test_reconstructed_validation_is_never_release_ready(tmp_path):
    create_fixture(tmp_path)
    report = module.validate(tmp_path)
    assert report["result"] == "validated_pending_runtime_review"
    assert set(report["schema_checks"]) == {"capabilities", "artifacts", "workspace_state", "tools", "project_status"}
    assert report["release_ready"] is False
    assert report["runtimes_enabled"] == []


def test_missing_status_schema_blocks_even_when_lint_is_clean(tmp_path):
    create_fixture(tmp_path, include_status_schema=False)
    report = module.validate(tmp_path)
    assert report["result"] == "blocked"
    assert any("Project status schema" in reason for reason in report["errors"])


def test_activated_plugin_blocks_reconstruction(tmp_path):
    cfg = create_fixture(tmp_path)
    cfg["runtime"]["plugin"]["enabled"] = True
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    report = module.validate(tmp_path)
    assert report["result"] == "blocked"
    assert report["runtimes_enabled"] == ["plugin"]
