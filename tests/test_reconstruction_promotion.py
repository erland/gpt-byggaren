from pathlib import Path
import hashlib
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "promote_reconstructed_project.py"


def setup(tmp_path):
    recovered = tmp_path / "reconstructed-canonical"
    recovered.mkdir()
    raw = b"# Recovered instructions\nKeep source content.\n"
    (recovered / "instructions.md").write_bytes(raw)
    draft = {
        "status": "review_required",
        "release_ready": False,
        "instruction": "reconstructed-canonical/instructions.md",
        "source_instruction": "assistant/instructions.md",
    }
    (recovered / "project-draft.json").write_text(json.dumps(draft), encoding="utf-8")
    approval = {
        "project_id": "recovered-demo",
        "project_name": "Recovered Demo",
        "instruction_sha256": hashlib.sha256(raw).hexdigest(),
        "reviews": {
            "instruction_semantics": True,
            "knowledge_completeness": True,
            "tool_dependencies": True,
        },
    }
    review = tmp_path / "review.json"
    review.write_text(json.dumps(approval), encoding="utf-8")
    return raw, review, approval


def run(tmp_path, review):
    return subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(tmp_path),
                           "--review-file", str(review)], capture_output=True, text=True)


def test_reviewed_reconstruction_creates_disabled_canonical_draft(tmp_path):
    raw, review, _ = setup(tmp_path)
    result = run(tmp_path, review)
    assert result.returncode == 0, result.stderr
    cfg = yaml.safe_load((tmp_path / "gpt-project.yaml").read_text())
    assert (tmp_path / "src/instructions/system.md").read_bytes() == raw
    assert cfg["reconstruction"]["release_ready"] is False
    assert all(not x["enabled"] for key, x in cfg["runtime"].items() if isinstance(x, dict))
    assert run(tmp_path, review).returncode != 0


def test_unreviewed_or_modified_sources_cannot_promote(tmp_path):
    _, review, approval = setup(tmp_path)
    approval["reviews"]["knowledge_completeness"] = False
    review.write_text(json.dumps(approval))
    assert run(tmp_path, review).returncode != 0
    assert not (tmp_path / "gpt-project.yaml").exists()
    approval["reviews"]["knowledge_completeness"] = True
    review.write_text(json.dumps(approval))
    (tmp_path / "reconstructed-canonical/instructions.md").write_text("changed")
    assert run(tmp_path, review).returncode != 0
    assert not (tmp_path / "gpt-project.yaml").exists()
