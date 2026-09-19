from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("project_model", ROOT / "scripts" / "lib" / "project_model.py")
project_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project_model)


def test_current_workspace_state_contract_is_portable_and_explicit():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    contract = project_model.normalize_workspace_state_contract(cfg)

    assert contract["contract_version"] == 1
    assert contract["workspace"]["requirement"] == "required"
    assert contract["workspace"]["portable"] is True
    assert contract["workspace"]["separate_from_assistant"] is True
    assert contract["workspace"]["artifact"] == "project_package"
    assert contract["state"]["authority"] == "workspace_file"
    assert contract["state"]["path"] == "project-status.yaml"
    assert contract["state"]["conversation_fallback"] is False


def test_legacy_resume_settings_infer_persistent_workspace_state():
    cfg = {
        "workflow": {
            "create_project_zip_on_first_execution_step": True,
            "resume_from_project_zip": True,
        },
        "resume": {
            "supported": True,
            "requires_previous_chat_history": False,
        },
    }

    contract = project_model.normalize_workspace_state_contract(cfg)

    assert contract["workspace"]["requirement"] == "required"
    assert contract["workspace"]["persistence"] == "required"
    assert contract["workspace"]["artifact"] == "project_package"
    assert contract["state"]["requirement"] == "required"
    assert contract["state"]["persistence"] == "required"
    assert contract["state"]["authority"] == "workspace_file"
    assert contract["state"]["format"] == "yaml"
    assert contract["state"]["path"] == "project-status.yaml"
    assert "workspace_state" not in cfg


def test_simple_legacy_project_does_not_force_persistent_state():
    cfg = {
        "workflow": {},
        "resume": {"supported": False},
    }

    contract = project_model.normalize_workspace_state_contract(cfg)

    assert contract["workspace"]["requirement"] == "optional"
    assert contract["state"]["requirement"] == "optional"
    assert contract["state"]["authority"] == "conversation"
    assert contract["state"]["conversation_fallback"] is True
