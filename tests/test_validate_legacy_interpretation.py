import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_legacy_interpretation", ROOT / "scripts/validate_legacy_interpretation.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def fixture():
    content = b"Original instruction text"
    digest = hashlib.sha256(content).hexdigest()
    discovery = {"status": "analysis_required", "source_files": [{
        "path": "unusual/location/my-file.txt", "sha256": digest,
        "size": len(content), "candidate_roles": [],
    }]}
    interpretation = {"schema_version": 1, "release_ready": False,
                      "runtime_activated": False, "unresolved": ["Tool access unknown"],
                      "claims": [{"role": "instructions", "confidence": "medium",
                                  "description": "Contains behavior instructions",
                                  "evidence": [{"path": "unusual/location/my-file.txt", "sha256": digest}]}]}
    return discovery, interpretation


def test_accepts_evidence_backed_interpretation_of_unknown_layout():
    discovery, interpretation = fixture()
    result = module.validate(discovery, interpretation)
    assert result["result"] == "accepted_for_review"
    assert result["canonical_contract_created"] is False
    assert result["release_ready"] is False


def test_rejects_unsupported_or_modified_evidence():
    discovery, interpretation = fixture()
    interpretation["claims"][0]["evidence"][0]["sha256"] = "wrong"
    result = module.validate(discovery, interpretation)
    assert result["result"] == "rejected"


def test_rejects_automatic_activation_and_missing_unresolved_list():
    discovery, interpretation = fixture()
    interpretation["runtime_activated"] = True
    interpretation.pop("unresolved")
    assert module.validate(discovery, interpretation)["result"] == "rejected"
