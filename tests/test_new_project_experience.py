from pathlib import Path
import json

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_analysis_recommendation_supports_peer_runtime_candidates():
    schema = json.loads(
        (ROOT / "schemas" / "analysis-recommendation.schema.json").read_text(encoding="utf-8")
    )
    recommendation = {
        "recommended_profile": "standard",
        "runtime": {
            "strategy": "peer_candidates",
            "candidates": [
                {
                    "runtime_id": "chatgpt_chat",
                    "suitability": "equivalent",
                    "rationale": "Passar det dokumentorienterade arbetsflödet.",
                    "activate_by_default": True,
                },
                {
                    "runtime_id": "chatgpt_custom",
                    "suitability": "equivalent",
                    "rationale": "Custom GPT kan bära kärnflödet.",
                    "activate_by_default": True,
                },
                {
                    "runtime_id": "claude_project",
                    "suitability": "equivalent",
                    "rationale": "Claude Projects kan bära samma canonical kontrakt.",
                    "activate_by_default": True,
                },
                {
                    "runtime_id": "opencode",
                    "suitability": "reduced",
                    "rationale": "Agentiskt workspace är möjligt men inte nödvändigt.",
                    "activate_by_default": False,
                },
                {
                    "runtime_id": "openai_plugin",
                    "suitability": "equivalent",
                    "rationale": "Skills-first distribution passar arbetsflödet.",
                    "activate_by_default": True,
                },
            ],
        },
        "model_robustness": {
            "level": "guided",
            "rationale": "Flerstegsflödet behöver en kort operativ kärna utan full state machine.",
            "operational_core": True,
            "explicit_workflow": False,
            "deterministic_gates": True,
            "model_compatibility_evals": True,
        },
        "capabilities": {},
        "project_features": {},
    }

    jsonschema.Draft202012Validator(schema).validate(recommendation)
    assert "primary" not in recommendation["runtime"]
    assert {c["runtime_id"] for c in recommendation["runtime"]["candidates"]} == {
        "chatgpt_chat", "chatgpt_custom", "claude_project", "opencode", "openai_plugin"
    }


def test_analysis_recommendation_rejects_missing_registered_runtime():
    schema = json.loads(
        (ROOT / "schemas" / "analysis-recommendation.schema.json").read_text(encoding="utf-8")
    )
    recommendation = {
        "recommended_profile": "standard",
        "runtime": {
            "strategy": "peer_candidates",
            "candidates": [
                {"runtime_id": "chatgpt_chat", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "chatgpt_custom", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
            ],
        },
        "capabilities": {},
        "project_features": {},
    }
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(recommendation))
    assert errors


def test_analysis_recommendation_requires_explicit_default_decision():
    schema = json.loads(
        (ROOT / "schemas" / "analysis-recommendation.schema.json").read_text(encoding="utf-8")
    )
    recommendation = {
        "recommended_profile": "standard",
        "runtime": {
            "strategy": "peer_candidates",
            "candidates": [
                {"runtime_id": "chatgpt_chat", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "chatgpt_custom", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "claude_project", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "opencode", "suitability": "reduced", "rationale": "ok"},
                {"runtime_id": "openai_plugin", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
            ],
        },
        "capabilities": {},
        "project_features": {},
    }
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(recommendation))
    assert errors


def test_reference_profiles_use_peer_candidate_strategy():
    for path in (ROOT / "profiles").glob("*.yaml"):
        profile = yaml.safe_load(path.read_text(encoding="utf-8"))
        runtime = profile["runtime_selection"]
        assert runtime["strategy"] == "peer_candidates"
        assert runtime["infer_from_canonical_contracts"] is True
        assert "primary_runtime" not in profile


def test_new_project_experience_is_registered():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    ux = cfg["new_project_experience"]
    assert ux["runtime_strategy"] == "peer_candidates"
    assert ux["infer_runtime_targets"] is True
    assert ux["ask_user_only_for_business_constraints"] is True


def test_active_new_project_guidance_does_not_assume_chat_custom_pair():
    analysis = (ROOT / "src" / "runtime-policy" / "analysis-policy.md").read_text(encoding="utf-8")
    planning = (ROOT / "src" / "runtime-policy" / "planning-policy.md").read_text(encoding="utf-8")
    profile_policy = (ROOT / "src" / "runtime-policy" / "profile-selection-policy.md").read_text(encoding="utf-8")
    advanced = yaml.safe_load((ROOT / "profiles" / "zip_first_advanced.yaml").read_text(encoding="utf-8"))

    assert "Advanced dual distribution" not in advanced["title"]
    assert "både Chat ZIP och Custom GPT" not in advanced["description"]
    assert "ChatGPT Chat" in analysis
    assert "Claude Projects" in analysis
    assert "OpenCode" in analysis
    assert "OpenAI Plugin" in analysis
    assert "activate_by_default: true" in planning
    assert "Chat ZIP och Custom GPT är de enda distributionsmålen" in planning
    assert "Profilen får inte i sig göra Chat/Custom till default" in profile_policy


def test_readme_describes_all_registered_runtime_families():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "ChatGPT Chat" in readme
    assert "Custom GPT" in readme
    assert "Claude Projects" in readme
    assert "OpenCode" in readme
    assert "Chat ZIP + Custom GPT är inte ett obligatoriskt standardpar" in readme



def test_canonical_instruction_knows_all_registered_runtime_families():
    instruction = (ROOT / "src" / "instructions" / "system.md").read_text(encoding="utf-8")

    for runtime_name in (
        "ChatGPT Chat",
        "ChatGPT Custom",
        "Claude Projects",
        "OpenCode",
        "OpenAI Plugin",
    ):
        assert runtime_name in instruction

    assert "skills-first peer runtime" in instruction
    assert "runtime parity" in instruction
    assert "genererad MCP-server" in instruction


def test_analysis_recommendation_requires_model_robustness():
    schema = json.loads(
        (ROOT / "schemas" / "analysis-recommendation.schema.json").read_text(encoding="utf-8")
    )
    recommendation = {
        "recommended_profile": "standard",
        "runtime": {
            "strategy": "peer_candidates",
            "candidates": [
                {"runtime_id": "chatgpt_chat", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "chatgpt_custom", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "claude_project", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
                {"runtime_id": "opencode", "suitability": "reduced", "rationale": "ok", "activate_by_default": False},
                {"runtime_id": "openai_plugin", "suitability": "equivalent", "rationale": "ok", "activate_by_default": True},
            ],
        },
        "capabilities": {},
        "project_features": {},
    }
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(recommendation))
    assert errors


def test_generated_gpt_model_robustness_policy_is_registered():
    instruction = (ROOT / "src" / "instructions" / "system.md").read_text(encoding="utf-8")
    policy = (ROOT / "src" / "runtime-policy" / "generated-gpt-model-robustness-policy.md").read_text(encoding="utf-8")
    planning = (ROOT / "src" / "runtime-policy" / "planning-policy.md").read_text(encoding="utf-8")

    assert "lightweight" in instruction
    assert "guided" in instruction
    assert "stateful" in instruction
    assert "Fråga inte användaren vilken robusthetsnivå" in policy
    assert "model_robustness" in planning
