from pathlib import Path
import importlib.util
import json

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec_model = importlib.util.spec_from_file_location(
    "project_model", ROOT / "scripts" / "lib" / "project_model.py"
)
project_model = importlib.util.module_from_spec(spec_model)
spec_model.loader.exec_module(project_model)

spec_build = importlib.util.spec_from_file_location(
    "build_distributions", ROOT / "scripts" / "build_distributions.py"
)
build_distributions = importlib.util.module_from_spec(spec_build)
spec_build.loader.exec_module(build_distributions)


def load_cfg():
    return yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))


def canonical_contracts(cfg):
    return {
        "capabilities": project_model.normalize_capability_contract(cfg),
        "artifacts": project_model.normalize_artifact_contract(cfg),
        "workspace_state": project_model.normalize_workspace_state_contract(cfg),
        "tools": project_model.normalize_tool_contract(cfg),
    }


def test_canonical_contracts_validate_without_runtime_assumptions():
    cfg = load_cfg()
    contracts = canonical_contracts(cfg)
    schema_map = {
        "capabilities": "capability-contract.schema.json",
        "artifacts": "artifact-contract.schema.json",
        "workspace_state": "workspace-state-contract.schema.json",
        "tools": "tool-contract.schema.json",
    }

    for name, contract in contracts.items():
        schema = json.loads((ROOT / "schemas" / schema_map[name]).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(contract)


def test_all_runtime_snapshots_project_the_same_canonical_contracts():
    cfg = load_cfg()
    canonical = canonical_contracts(cfg)

    snapshots = {
        "chatgpt_chat": build_distributions.chat_runtime_contract(cfg),
        "chatgpt_custom": build_distributions.custom_runtime_contract(cfg),
        "claude_project": build_distributions.claude_runtime_contract(cfg),
        "opencode": build_distributions.opencode_runtime_contract(cfg, [], []),
    }

    assert set(snapshots) == set(cfg["runtime_parity"]["registered_runtimes"])

    for runtime_id, snapshot in snapshots.items():
        assert snapshot["runtime_id"] == runtime_id
        for contract_name, expected in canonical.items():
            assert snapshot[contract_name] == expected


def test_every_registered_runtime_has_an_enabled_adapter_and_build_target():
    cfg = load_cfg()

    runtime_targets = cfg["build_system"]["runtime_targets"]
    registered = set(cfg["runtime_parity"]["registered_runtimes"])
    declared_runtime_ids = {item["runtime_id"] for item in runtime_targets.values()}

    assert registered == declared_runtime_ids

    build_targets = set(cfg["build_system"]["targets"])
    for build_target, target_cfg in runtime_targets.items():
        assert build_target in build_targets
        assert cfg["runtime"][target_cfg["runtime_key"]]["enabled"] is True
        assert target_cfg["builder"] in build_distributions.RUNTIME_BUILDERS


def test_core_behavior_contract_is_runtime_neutral():
    cfg = load_cfg()
    instruction = (ROOT / cfg["instructions"]["canonical"]).read_text(encoding="utf-8")
    markers = cfg["instructions"]["core_contract"]["required_markers"]

    assert "Bygg aktiverade runtime-distributioner från samma canonical kontrakt." in markers
    assert "Bygg normalt både Chat ZIP och Custom GPT från samma canonical kontrakt." not in markers

    for marker in markers:
        assert marker in instruction

    runtime_section = instruction.split("## Runtime", 1)[1].split("## ", 1)[0]
    assert "aktiverat" in runtime_section or "aktiverade" in runtime_section
    assert "Alla runtimes ska härledas från samma canonical" in runtime_section
