from pathlib import Path
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_legacy_copy.py"


def test_reconstructed_project_draft_tracks_evidence_without_activating_runtimes(tmp_path):
    archive = tmp_path / "legacy.zip"
    output = tmp_path / "reconstructed"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("START-HERE.md", "Start")
        z.writestr("assistant/instructions.md", "Keep original behavior.")
        z.writestr("knowledge/domain.md", "Facts")
        z.writestr("scripts/helper.py", "print('example')")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--source", str(archive), "--destination", str(output)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    draft = json.loads((output / "reconstructed-canonical" / "project-draft.json").read_text())
    assert draft["status"] == "review_required"
    assert draft["release_ready"] is False
    assert draft["source_instruction"] == "assistant/instructions.md"
    assert "knowledge/domain.md" in draft["knowledge_candidates"]
    assert "scripts/helper.py" in draft["tool_candidates"]
    assert not any(draft["runtime_activation"].values())
    assert not (output / "gpt-project.yaml").exists()
    assert json.loads((output / "MIGRATION-REPORT.json").read_text())["project_draft"]["result"] == "created_for_review"


def test_ambiguous_zip_does_not_create_project_draft(tmp_path):
    archive = tmp_path / "mixed.zip"
    output = tmp_path / "out"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("plugin.json", "{}")
        z.writestr("AGENTS.md", "One of two formats")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--source", str(archive), "--destination", str(output)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert not (output / "reconstructed-canonical" / "project-draft.json").exists()
    assert json.loads((output / "MIGRATION-REPORT.json").read_text())["project_draft"]["result"] == "not_created"
