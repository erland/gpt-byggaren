"""End-to-end smoke: historical Chat ZIP -> reviewed scaffold -> schema/lint validation."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def script(name, *args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / name), *map(str, args)],
                          capture_output=True, text=True)


def test_legacy_chat_zip_to_blocked_validated_project(tmp_path):
    original = tmp_path / "legacy-chat.zip"
    data = b"# Legacy GPT\nUse original behavior exactly.\n"
    with zipfile.ZipFile(original, "w") as archive:
        archive.writestr("START-HERE.md", "Legacy runtime")
        archive.writestr("assistant/instructions.md", data)
        archive.writestr("knowledge/rules.md", "Reference content")

    dest = tmp_path / "recovered"
    migrated = script("migrate_legacy_copy.py", "--source", original, "--destination", dest)
    assert migrated.returncode == 0, migrated.stderr
    assert (dest / "reconstructed-canonical/instructions.md").read_bytes() == data

    review = {
        "project_id": "legacy-recovered",
        "project_name": "Legacy Recovered",
        "instruction_sha256": hashlib.sha256(data).hexdigest(),
        "reviews": {
            "instruction_semantics": True,
            "knowledge_completeness": True,
            "tool_dependencies": True,
        },
    }
    attestation = tmp_path / "review.json"
    attestation.write_text(json.dumps(review), encoding="utf-8")
    promoted = script("promote_reconstructed_project.py", "--project-root", dest, "--review-file", attestation)
    assert promoted.returncode == 0, promoted.stderr
    assert (dest / "src/instructions/system.md").read_bytes() == data

    completed = script("complete_reconstructed_contracts.py", "--project-root", dest)
    assert completed.returncode == 0, completed.stderr
    validated = script("validate_reconstructed_project.py", "--project-root", dest)
    assert validated.returncode == 0, validated.stderr
    result = json.loads(validated.stdout)
    assert result["result"] == "validated_pending_runtime_review"
    assert result["release_ready"] is False
    assert result["runtimes_enabled"] == []
    assert original.is_file()
    assert original.read_bytes().startswith(b"PK")
