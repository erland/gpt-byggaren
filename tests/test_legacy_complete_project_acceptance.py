"""Acceptance regression based on the older Marknadskartläggaren project layout."""
import json
import subprocess
import sys
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/migrate_legacy_copy.py"


def test_complete_legacy_project_reports_runtime_gap_and_preserves_source(tmp_path):
    archive = tmp_path / "market-mapper.zip"
    source = {
        "schema_version": 1,
        "project": {"id": "marknadskartlaggaren", "name": "Marknadskartläggaren"},
        "instructions": {"canonical": "src/instructions/system.md"},
        "runtime": {
            "chat_zip": {"enabled": True},
            "openai_plugin": {"enabled": True, "mode": "skills_first"},
            "custom_gpt": {"enabled": True},
        },
    }
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("gpt-marknadskartlaggaren-main/gpt-project.yaml",
                   yaml.safe_dump(source, allow_unicode=True))
        z.writestr("gpt-marknadskartlaggaren-main/src/instructions/system.md", "Research the market")
        z.writestr("gpt-marknadskartlaggaren-main/knowledge/KNOWLEDGE.md", "Reference")
        z.writestr("gpt-marknadskartlaggaren-main/scripts/build_distributions.py", "# legacy build")
    before = archive.read_bytes()
    output = tmp_path / "migrated"
    result = subprocess.run([sys.executable, str(SCRIPT), "--source", str(archive),
                             "--destination", str(output)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert archive.read_bytes() == before
    migrated = output / "gpt-marknadskartlaggaren-main"
    cfg = yaml.safe_load((migrated / "gpt-project.yaml").read_text())
    assert cfg["runtime"]["custom_gpt"]["enabled"] is False
    assert cfg["runtime"]["openai_plugin"]["enabled"] is True  # preserve old config, not modern activation
    assert cfg["runtime"]["custom_gpt"].get("mode") is None
    assert (migrated / "src/instructions/system.md").read_text() == "Research the market"
    report = json.loads((output / "MIGRATION-REPORT.json").read_text())
    assessment = report["existing_project_assessment"]
    assert assessment["ready_for_modern_distribution_build"] is False
    assert assessment["release_ready"] is False
    assert any("runtime.openai_plugin" in item for item in assessment["issues"])
    assert any("runtime_targets" in item for item in assessment["issues"])
    assert "knowledge/KNOWLEDGE.md" in assessment["dependency_inventory"]["knowledge_files"]
