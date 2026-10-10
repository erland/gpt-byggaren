import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from exercise_reconstructed_runtimes import exercise


def test_isolated_chat_builder_uses_real_adapter_and_preserves_original(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    instruction = project / "src/instructions/system.md"
    instruction.parent.mkdir(parents=True)
    instruction.write_bytes(b"Canonical instructions\n")
    draft = project / "reconstructed-canonical"
    draft.mkdir()
    (draft / "project-draft.json").write_text(json.dumps({
        "instruction": "reconstructed-canonical/instructions.md",
        "source_instruction": "assistant/instructions.md",
    }))
    (draft / "instructions.md").write_bytes(instruction.read_bytes())
    config = {
        "project": {"id": "legacy-demo", "name": "Legacy Demo"},
        "instructions": {"canonical": "src/instructions/system.md"},
        "reconstruction": {"status": "canonical_contracts_scaffolded", "release_ready": False},
        "runtime": {"chat_zip": {"enabled": False}, "custom_gpt": {"enabled": False}},
        "structure": {"conversation_starters": {"path": "src/conversation-starters"}},
    }
    (project / "gpt-project.yaml").write_text(yaml.safe_dump(config))
    before = hashlib.sha256((project / "gpt-project.yaml").read_bytes()).hexdigest()
    report = exercise(project, ["chat"])
    assert report["release_ready"] is False
    assert report["isolated"] is True
    assert report["attempted"] == ["chat"]
    assert hashlib.sha256((project / "gpt-project.yaml").read_bytes()).hexdigest() == before
    assert not (project / "build").exists()
    assert not (project / "dist").exists()


def test_rejects_non_reconstructed_projects(tmp_path):
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump({"project": {"id": "demo"}}))
    with pytest.raises(ValueError):
        exercise(tmp_path, ["chat"])
