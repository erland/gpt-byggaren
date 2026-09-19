from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("project_model", ROOT / "scripts" / "lib" / "project_model.py")
project_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project_model)


def test_current_capability_contract_is_platform_neutral():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    contract = project_model.normalize_capability_contract(cfg)
    requirements = contract["requirements"]

    assert contract["contract_version"] == 1
    assert requirements["filesystem"]["read"] == "required"
    assert requirements["filesystem"]["write"] == "required"
    assert requirements["code_execution"]["level"] == "recommended"
    assert "data_analysis" not in requirements
    assert "file_handling" not in requirements


def test_legacy_capabilities_are_normalized_without_mutating_source():
    cfg = {
        "capabilities": {
            "recommendation_mode": "inferred_from_use_case",
            "web": {"state": "required"},
            "data_analysis": {"state": "recommended"},
            "file_handling": {"state": "required"},
            "structured_knowledge": {"state": "likely_required"},
            "image_generation": {"state": "not_recommended"},
        }
    }

    contract = project_model.normalize_capability_contract(cfg)
    requirements = contract["requirements"]

    assert requirements["web"]["level"] == "required"
    assert requirements["code_execution"]["level"] == "recommended"
    assert requirements["filesystem"] == {"read": "required", "write": "required"}
    assert requirements["structured_data"]["level"] == "recommended"
    assert requirements["image_generation"]["level"] == "not_required"
    assert "requirements" not in cfg["capabilities"]
