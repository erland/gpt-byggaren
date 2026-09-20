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
                    "runtime_id": "opencode",
                    "suitability": "reduced",
                    "rationale": "Agentiskt workspace är möjligt men inte nödvändigt.",
                    "activate_by_default": False,
                },
            ],
        },
        "capabilities": {},
        "project_features": {},
    }

    jsonschema.Draft202012Validator(schema).validate(recommendation)
    assert "primary" not in recommendation["runtime"]


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
