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


def test_custom_gpt_is_retired_only_in_migrated_copy(tmp_path):
    source = tmp_path / "legacy"
    dest = tmp_path / "updated"
    source.mkdir()
    cfg = {
        "project": {"id": "old"},
        "runtime": {
            "custom_gpt": {"enabled": True, "instruction": {"max_characters": 8000}},
            "chat_zip": {"enabled": True},
        },
        "build": {"build_custom_gpt_zip": True},
        "build_system": {
            "targets": ["project", "chat", "custom-gpt", "plugin"],
            "runtime_targets": {
                "custom-gpt": {"runtime_id": "chatgpt_custom", "runtime_key": "custom_gpt"},
                "plugin": {"runtime_id": "openai_plugin", "runtime_key": "plugin"},
            },
        },
        "runtime_parity": {"registered_runtimes": ["chatgpt_custom", "openai_plugin"]},
        "direct_build": {"deliver": ["custom_gpt_zip_when_enabled", "plugin_zip_when_enabled"]},
        "release": {"github": {"artifacts": ["custom_gpt_zip_when_enabled", "plugin_zip_when_enabled"]}},
    }
    (source / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    result = invoke(source, dest)
    assert result.returncode == 0, result.stderr
    migrated = yaml.safe_load((dest / "gpt-project.yaml").read_text())
    untouched = yaml.safe_load((source / "gpt-project.yaml").read_text())
    assert untouched == cfg
    assert migrated["runtime"]["custom_gpt"]["enabled"] is False
    assert migrated["runtime"]["custom_gpt"]["instruction"]["max_characters"] == 8000
    assert migrated["build_system"]["targets"] == ["project", "chat", "plugin"]
    assert "custom-gpt" not in migrated["build_system"]["runtime_targets"]
    assert migrated["runtime_parity"]["registered_runtimes"] == ["openai_plugin"]
    assert migrated["direct_build"]["deliver"] == ["plugin_zip_when_enabled"]
    assert migrated["release"]["github"]["artifacts"] == ["plugin_zip_when_enabled"]
    assert json.loads((dest / "MIGRATION-REPORT.json").read_text())["custom_gpt_retirement"]["legacy_configuration_preserved"]


def test_distribution_inventory_identifies_legacy_chat_zip(tmp_path):
    archive = tmp_path / "chat.zip"
    dest = tmp_path / "converted"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("START-HERE.md", "Start")
        z.writestr("assistant/instructions.md", "Canonical text unavailable")
        z.writestr("knowledge/domain.md", "Domain rules")
    result = invoke(archive, dest)
    assert result.returncode == 0, result.stderr
    report = json.loads((dest / "MIGRATION-REPORT.json").read_text())
    inv = report["distribution_inventory"]
    assert inv["classification"] == "chat_zip"
    assert inv["knowledge_file_count"] == 1
    assert inv["reconstruction"] == "review_required"
    assert report["apply"]["result"] == "blocked"


def test_distribution_inventory_identifies_plugin_without_mcp_dependency(tmp_path):
    archive = tmp_path / "plugin.zip"
    dest = tmp_path / "converted"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("plugin.json", "{}")
        z.writestr("skills/example/SKILL.md", "# Skill")
    result = invoke(archive, dest)
    assert result.returncode == 0, result.stderr
    inv = json.loads((dest / "MIGRATION-REPORT.json").read_text())["distribution_inventory"]
    assert inv["classification"] == "openai_plugin"
    assert "skills/example/SKILL.md" in inv["evidence"]


def test_distribution_inventory_reports_ambiguity(tmp_path):
    archive = tmp_path / "mixed.zip"
    dest = tmp_path / "converted"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("plugin.json", "{}")
        z.writestr("AGENTS.md", "Agent")
    result = invoke(archive, dest)
    assert result.returncode == 0, result.stderr
    inv = json.loads((dest / "MIGRATION-REPORT.json").read_text())["distribution_inventory"]
    assert inv["classification"] == "ambiguous"


def test_reconstructs_reviewable_snapshot_from_chat_distribution(tmp_path):
    archive = tmp_path / "chat.zip"
    destination = tmp_path / "output"
    raw = b"# Original instructions\\nKeep every word.\\n"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("START-HERE.md", "Start")
        z.writestr("assistant/instructions.md", raw)
        z.writestr("knowledge/facts.md", "Important knowledge")
    result = invoke(archive, destination)
    assert result.returncode == 0, result.stderr
    recovery = json.loads((destination / "reconstructed-canonical" / "RECOVERY.json").read_text())
    assert recovery["status"] == "review_required"
    assert recovery["provenance"] == "assistant/instructions.md"
    assert recovery["canonical_contract_created"] is False
    assert recovery["release_ready"] is False
    assert (destination / recovery["recovered_instruction"]).read_bytes() == raw
    assert (destination / "knowledge" / "facts.md").read_text() == "Important knowledge"


def test_ambiguous_distribution_does_not_invent_canonical_instructions(tmp_path):
    archive = tmp_path / "ambiguous.zip"
    destination = tmp_path / "output"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("plugin.json", "{}")
        z.writestr("AGENTS.md", "Agent content")
    result = invoke(archive, destination)
    assert result.returncode == 0, result.stderr
    report = json.loads((destination / "MIGRATION-REPORT.json").read_text())
    assert report["reconstruction"]["result"] == "review_required"
    assert not (destination / "reconstructed-canonical").exists()
