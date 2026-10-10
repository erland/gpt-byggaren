import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from project_legacy_analysis import project


def sample():
    digest = hashlib.sha256(b"unusual legacy content").hexdigest()
    discovery = {"status": "analysis_required", "source_files": [
        {"path": "odd/subfolder/notes.txt", "sha256": digest, "size": 22, "candidate_roles": []}
    ]}
    interpretation = {"schema_version": 1, "release_ready": False, "runtime_activated": False,
                      "claims": [{"role": "instructions", "confidence": "medium",
                                  "description": "Instructions for the legacy workflow",
                                  "evidence": [{"path": "odd/subfolder/notes.txt", "sha256": digest}]}],
                      "unresolved": ["Whether the source includes all required tools"]}
    return discovery, interpretation


def test_projects_unknown_layout_into_review_only_model():
    discovery, interpretation = sample()
    result = project(discovery, interpretation)
    assert result["status"] == "review_required"
    assert result["functional_evidence"]["instructions"][0]["evidence"][0]["path"] == "odd/subfolder/notes.txt"
    assert result["skills"]["status"] == "not_yet_classified"
    assert not any(result["runtime_targets"].values())
    assert result["canonical_contract_created"] is False
    assert result["release_ready"] is False


def test_rejects_claim_without_correct_hash():
    discovery, interpretation = sample()
    interpretation["claims"][0]["evidence"][0]["sha256"] = "tampered"
    with pytest.raises(ValueError):
        project(discovery, interpretation)
