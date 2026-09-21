from pathlib import Path
import importlib.util
import json

import jsonschema

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("project_model", ROOT / "scripts" / "lib" / "project_model.py")
project_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project_model)


def _schema():
    return json.loads((ROOT / "schemas" / "runtime-parity.schema.json").read_text(encoding="utf-8"))


def test_generic_parity_schema_accepts_arbitrary_runtime_ids():
    report = {
        "schema_version": 2,
        "reference": {"type": "canonical_contract"},
        "runtimes": {
            "chatgpt_chat": {
                "level": "high",
                "weighted_score": 90,
                "release_recommendation": "publish",
            },
            "future_runtime": {
                "level": "moderate",
                "weighted_score": 70,
                "release_recommendation": "publish_with_warning",
            },
        },
        "requirements": [
            {
                "category": "tool",
                "id": "validate-model",
                "title": "Validate model",
                "criticality": "critical",
                "runtime_states": {
                    "chatgpt_chat": {"state": "reduced", "reason": "Limited local execution"},
                    "future_runtime": {"state": "equivalent"},
                },
            },
            {
                "category": "artifact",
                "id": "final-report",
                "title": "Final report",
                "criticality": "important",
                "runtime_states": {
                    "chatgpt_chat": {"state": "equivalent"},
                    "future_runtime": {"state": "equivalent"},
                },
            },
        ],
    }

    jsonschema.Draft202012Validator(_schema()).validate(report)


def test_legacy_two_runtime_report_normalizes_to_generic_model():
    legacy = {
        "schema_version": 1,
        "primary_runtime": "chat_zip",
        "summary": {
            "level": "moderate",
            "weighted_score": 75,
            "release_recommendation": "publish_with_warning",
        },
        "capabilities": [
            {
                "id": "core_workflow",
                "title": "Core workflow",
                "criticality": "critical",
                "chat_zip": "equivalent",
                "custom_gpt": "reduced",
                "reason": "Custom runtime is reduced",
            }
        ],
    }

    normalized = project_model.normalize_runtime_parity_report(legacy)

    assert normalized["schema_version"] == 2
    assert normalized["reference"]["type"] == "canonical_contract"
    assert project_model.runtime_ids_from_parity(normalized) == ["chat_zip", "custom_gpt"]
    requirement = normalized["requirements"][0]
    assert requirement["category"] == "capability"
    assert requirement["runtime_states"]["chat_zip"]["state"] == "equivalent"
    assert requirement["runtime_states"]["custom_gpt"]["state"] == "reduced"

    jsonschema.Draft202012Validator(_schema()).validate(normalized)


def test_generic_report_is_not_modified_by_normalizer():
    report = {
        "schema_version": 2,
        "reference": {"type": "canonical_contract"},
        "runtimes": {
            "opencode": {
                "level": "full",
                "release_recommendation": "publish",
            }
        },
        "requirements": [
            {
                "category": "workspace_state",
                "id": "persistent-workspace",
                "title": "Persistent workspace",
                "criticality": "critical",
                "runtime_states": {
                    "opencode": {"state": "equivalent"}
                },
            }
        ],
    }

    assert project_model.normalize_runtime_parity_report(report) is report


def test_parity_semantic_validation_requires_every_runtime_per_requirement():
    report = {
        "schema_version": 2,
        "reference": {"type": "canonical_contract"},
        "runtimes": {
            "chatgpt_chat": {
                "level": "high",
                "release_recommendation": "publish",
            },
            "opencode": {
                "level": "high",
                "release_recommendation": "publish",
            },
        },
        "requirements": [
            {
                "category": "tool",
                "id": "validate-model",
                "title": "Validate model",
                "criticality": "critical",
                "runtime_states": {
                    "chatgpt_chat": {"state": "reduced"}
                },
            }
        ],
    }

    errors = project_model.validate_runtime_parity_report(report)

    assert len(errors) == 1
    assert "opencode" in errors[0]


def test_openai_plugin_is_registered_for_runtime_parity():
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    assert "openai_plugin" in cfg["runtime_parity"]["registered_runtimes"]
    runtime_ids = {
        target["runtime_id"]
        for target in cfg["build_system"]["runtime_targets"].values()
    }
    assert "openai_plugin" in runtime_ids


def test_plugin_runtime_snapshot_exposes_v1_parity_limitations():
    import importlib.util
    import yaml

    spec_build = importlib.util.spec_from_file_location(
        "build_distributions", ROOT / "scripts" / "build_distributions.py"
    )
    build_distributions = importlib.util.module_from_spec(spec_build)
    spec_build.loader.exec_module(build_distributions)

    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    snapshot = build_distributions.plugin_runtime_contract(cfg, ["gpt-project-workflow"])
    notes = snapshot["adapter"]["parity_notes"]

    assert snapshot["runtime_id"] == "openai_plugin"
    assert set(notes) == {"behavior", "artifact", "workspace_state", "tool", "capability"}
    assert snapshot["adapter"]["mcp_generated"] is False
