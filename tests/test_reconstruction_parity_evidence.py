import importlib.util
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "collect_reconstruction_parity", ROOT / "scripts/collect_reconstruction_parity.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def fixture(tmp_path):
    recovered = tmp_path / "reconstructed-canonical"
    recovered.mkdir()
    (recovered / "instructions.md").write_bytes(b"Original instructions")
    (recovered / "project-draft.json").write_text(json.dumps({
        "instruction": "reconstructed-canonical/instructions.md",
        "source_instruction": "assistant/instructions.md",
        "knowledge_candidates": ["knowledge/rules.md"],
        "tool_candidates": ["scripts/legacy_tool.py"],
        "integration_candidates": ["mcp.json"],
    }))
    canonical = tmp_path / "src/instructions/system.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_bytes(b"Original instructions")
    knowledge = tmp_path / "knowledge/rules.md"
    knowledge.parent.mkdir()
    knowledge.write_text("Rules")
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump({
        "reconstruction": {"status": "canonical_contracts_scaffolded", "release_ready": False},
    }))
    return canonical


def test_reports_evidence_but_never_claims_runtime_parity(tmp_path):
    canonical = fixture(tmp_path)
    chat = tmp_path / "build/chat/assistant/instructions.md"
    chat.parent.mkdir(parents=True)
    chat.write_bytes(canonical.read_bytes())
    result = module.inspect(tmp_path)
    assert result["recovered_instruction_matches"]
    assert result["runtimes"]["chat"]["status"] == "matching_bytes"
    assert result["runtimes"]["claude"]["status"] == "not_tested"
    assert result["knowledge"][0]["present"]
    assert result["unresolved_dependencies"]["tool_candidates"] == ["scripts/legacy_tool.py"]
    assert result["automated_runtime_parity_verified"] is False
    assert result["release_ready"] is False


def test_detects_changed_reconstructed_instructions(tmp_path):
    canonical = fixture(tmp_path)
    canonical.write_text("Modified instructions")
    result = module.inspect(tmp_path)
    assert result["recovered_instruction_matches"] is False


def test_rejects_projects_already_marked_release_ready(tmp_path):
    fixture(tmp_path)
    cfg = {"reconstruction": {"status": "runtime_parity_verified", "release_ready": True}}
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg))
    import pytest
    with pytest.raises(ValueError):
        module.inspect(tmp_path)
