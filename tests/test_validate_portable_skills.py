import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_portable_skills import inspect


def _fixture(tmp_path):
    (tmp_path / "core.md").write_text("Mandatory safety, workflow and fallback")
    skill = tmp_path / "skills" / "audit"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: audit\ndescription: Check projects\n---\nCheck projects.")
    (skill / "run.py").write_text("print('ok')")
    contract = {
        "schema_version": 1, "core": "core.md",
        "modules": [{"id": "audit", "skill": "skills/audit/SKILL.md", "scripts": [{
            "path": "skills/audit/run.py", "engine": "python",
            "requirements": {
                "filesystem_read": "required", "filesystem_write": "none",
                "network": "none", "code_execution": "required", "persistent_state": "none",
            },
            "dependencies": [], "fallback": "manual",
        }]}],
        "fallback": {
            "chat_zip": "Read core and available skill references manually",
            "plugin": "Block unavailable scripts and retain core guidance",
            "claude": "Use skill when supported, otherwise core and manual procedure",
            "opencode": "Block unsupported execution and report limitations",
        },
    }
    return contract


def test_portable_skill_and_script_contract(tmp_path):
    result = inspect(_fixture(tmp_path), tmp_path)
    assert result["result"] == "review_ready"
    assert result["runtime_execution_verified"] is False
    assert result["release_ready"] is False


def test_missing_runtime_fallback_rejected(tmp_path):
    contract = _fixture(tmp_path)
    del contract["fallback"]["claude"]
    assert inspect(contract, tmp_path)["result"] == "rejected"


def test_unsafe_script_path_and_missing_requirements_rejected(tmp_path):
    contract = _fixture(tmp_path)
    contract["modules"][0]["scripts"][0]["path"] = "../outside.py"
    del contract["modules"][0]["scripts"][0]["requirements"]["network"]
    assert inspect(contract, tmp_path)["result"] == "rejected"


def test_existing_source_is_not_changed(tmp_path):
    contract = _fixture(tmp_path)
    before = (tmp_path / "core.md").read_bytes()
    inspect(contract, tmp_path)
    assert (tmp_path / "core.md").read_bytes() == before
