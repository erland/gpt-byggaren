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
