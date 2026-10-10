from pathlib import Path
import json
import subprocess
import sys

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "complete_reconstructed_contracts.py"


def fixture(tmp_path, enabled=False):
    cfg = {
        "project": {"id": "demo", "name": "Demo"},
        "reconstruction": {"status": "requires_runtime_validation", "release_ready": False},
        "runtime": {"plugin": {"enabled": enabled}, "custom_gpt": {"enabled": False}},
    }
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    (tmp_path / "project-status.yaml").write_text(
        yaml.safe_dump({"state": {"overall": "blocked"}}), encoding="utf-8"
    )
    folder = tmp_path / "reconstructed-canonical"
    folder.mkdir()
    (folder / "project-draft.json").write_text(
        json.dumps({"release_ready": False, "tool_candidates": ["scripts/legacy.py"],
                    "integration_candidates": ["mcp.json"]}), encoding="utf-8"
    )


def execute(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(path)],
        capture_output=True, text=True
    )


def test_validates_canonical_schemas_without_enabling_any_runtime(tmp_path):
    fixture(tmp_path)
    result = execute(tmp_path)
    assert result.returncode == 0, result.stderr
    cfg = yaml.safe_load((tmp_path / "gpt-project.yaml").read_text())
    for name in ("capabilities", "artifacts", "workspace_state", "tools"):
        schema = json.loads((tmp_path / cfg[name]["schema"]).read_text())
        jsonschema.Draft202012Validator(schema).validate(cfg[name])
    assert cfg["tools"]["tools"] == []
    assert cfg["capabilities"]["requirements"] == {}
    assert not cfg["runtime"]["plugin"]["enabled"]
    assert cfg["reconstruction"]["release_ready"] is False
    report = json.loads((tmp_path / "reconstructed-canonical/CONTRACT-VALIDATION.json").read_text())
    assert report["candidate_tools_unverified"] == ["scripts/legacy.py"]
    assert report["candidate_integrations_unverified"] == ["mcp.json"]
    assert report["runtime_parity_not_verified"] is True
    assert execute(tmp_path).returncode != 0


def test_blocks_runtime_activation_and_does_not_modify_source(tmp_path):
    fixture(tmp_path, enabled=True)
    original = (tmp_path / "gpt-project.yaml").read_bytes()
    result = execute(tmp_path)
    assert result.returncode != 0
    assert (tmp_path / "gpt-project.yaml").read_bytes() == original
    assert not (tmp_path / "schemas").exists()
