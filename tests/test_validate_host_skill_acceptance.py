import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_host_skill_acceptance import SCENARIOS, TARGETS, validate


def sample(status="not_tested"):
    return {"schema_version": 1, "targets": {
        target: {"scenarios": {
            scenario: {"status": status, "note": "No actual runtime session was executed"}
            for scenario in SCENARIOS
        }}
        for target in TARGETS
    }}


def test_offline_build_cannot_claim_runtime_success():
    result = validate(sample())
    assert result["result"] == "accepted"
    assert result["host_acceptance_verified"] is False
    assert result["release_ready"] is False


def test_pass_requires_actual_host_observation():
    data = sample()
    data["targets"]["plugin"]["scenarios"]["skill_activation"] = {
        "status": "passed", "note": "Observed in plugin host",
    }
    result = validate(data)
    assert result["result"] == "rejected"
    assert any("host_observation" in message for message in result["errors"])
    assert any("artifact" in message for message in result["errors"])


def test_all_host_evidence_is_accepted_but_never_grants_release():
    data = sample()
    for target in TARGETS:
        for scenario in SCENARIOS:
            data["targets"][target]["scenarios"][scenario] = {
                "status": "passed",
                "kind": "host_observation",
                "artifact": f"reports/{target}-{scenario}.txt",
                "note": "Host session was executed; inspect the linked artifact",
            }
    result = validate(data)
    assert result["result"] == "accepted"
    assert result["host_acceptance_verified"] is True
    assert result["release_ready"] is False


def test_missing_target_fails_closed():
    data = sample()
    del data["targets"]["claude"]
    assert validate(data)["result"] == "rejected"
