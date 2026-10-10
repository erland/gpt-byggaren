from pathlib import Path
import json
import subprocess
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_legacy_copy.py"


def invoke(source, destination):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--source", str(source), "--destination", str(destination)],
        capture_output=True, text=True
    )


def test_directory_migration_does_not_change_source(tmp_path):
    source = tmp_path / "old"
    dest = tmp_path / "new"
    (source / "src" / "instructions").mkdir(parents=True)
    (source / "src" / "instructions" / "system.md").write_text("Keep this behavior", encoding="utf-8")
    old = {"project": {"id": "example"}, "capabilities": {"web": "required"},
           "instructions": {"canonical": "src/instructions/system.md"}}
    (source / "gpt-project.yaml").write_text(yaml.safe_dump(old), encoding="utf-8")
    before = (source / "gpt-project.yaml").read_bytes()
    result = invoke(source, dest)
    assert result.returncode == 0, result.stderr
    assert (source / "gpt-project.yaml").read_bytes() == before
    assert yaml.safe_load((dest / "gpt-project.yaml").read_text())["capabilities"]["contract_version"] == 1
    assert (dest / "src" / "instructions" / "system.md").read_text() == "Keep this behavior"
    assert json.loads((dest / "MIGRATION-REPORT.json").read_text())["safe_copy"]["source_unchanged"]


def test_zip_with_top_directory_is_migrated(tmp_path):
    source = tmp_path / "old.zip"
    dest = tmp_path / "new"
    with zipfile.ZipFile(source, "w") as z:
        z.writestr("project/gpt-project.yaml", yaml.safe_dump({"project": {"id": "legacy"}, "capabilities": {"web": "required"}}))
        z.writestr("project/knowledge/rules.md", "Original rules")
    assert invoke(source, dest).returncode == 0
    assert (dest / "project" / "knowledge" / "rules.md").read_text() == "Original rules"
    assert (dest / "MIGRATION-REPORT.json").exists()


def test_distribution_only_zip_requires_review(tmp_path):
    source = tmp_path / "chat.zip"
    dest = tmp_path / "out"
    with zipfile.ZipFile(source, "w") as z:
        z.writestr("assistant/instructions.md", "Preserve")
    result = invoke(source, dest)
    assert result.returncode == 0
    report = json.loads((dest / "MIGRATION-REPORT.json").read_text())
    assert report["apply"]["result"] == "blocked"
    assert (dest / "assistant" / "instructions.md").read_text() == "Preserve"


def test_unsafe_zip_and_existing_destination_are_rejected(tmp_path):
    source = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(source, "w") as z:
        z.writestr("../escape.txt", "bad")
    dest = tmp_path / "out"
    assert invoke(source, dest).returncode != 0
    assert not dest.exists()
    good = tmp_path / "good"
    good.mkdir()
    assert invoke(good, tmp_path).returncode != 0
