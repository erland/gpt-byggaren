from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("project_model", ROOT / "scripts" / "lib" / "project_model.py")
project_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project_model)


def test_current_tool_contract_declares_runtime_tools_explicitly():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    contract = project_model.normalize_tool_contract(cfg)
    tools = {tool["id"]: tool for tool in contract["tools"]}

    assert contract["contract_version"] == 1
    assert tools["lint-project"]["type"] == "script"
    assert tools["build-distributions"]["requirement"] == "required"
    assert tools["project-hygiene"]["mutates_workspace"] is True
    assert tools["validate-distributions"]["deterministic"] is True


def test_legacy_scripts_directory_is_not_implicitly_promoted_to_tools():
    cfg = {
        "structure": {
            "scripts": {"path": "scripts", "required": False}
        }
    }

    contract = project_model.normalize_tool_contract(cfg)

    assert contract == {"contract_version": 1, "tools": []}


def test_legacy_explicit_tooling_can_be_normalized():
    cfg = {
        "tooling": {
            "tools": [
                {
                    "id": "validate",
                    "type": "script",
                    "requirement": "required",
                    "purpose": "Validate project",
                    "script": "scripts/validate.py",
                }
            ]
        }
    }

    contract = project_model.normalize_tool_contract(cfg)

    assert contract["tools"][0]["id"] == "validate"
    assert contract["tools"][0]["script"] == "scripts/validate.py"
