import json
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_missing_legacy_skill_is_reported_with_recovery_sources(tmp_path):
    archive = tmp_path / "legacy.zip"
    cfg = {
        "project": {"id": "market", "name": "Market Mapper"},
        "instructions": {"canonical": "src/instructions/system.md"},
        "runtime": {
            "openai_plugin": {
                "enabled": True, "entrypoint": "skills/marknadskartlaggaren/SKILL.md",
                "mode": "skills_first",
            },
            "custom_gpt": {"enabled": True},
        },
    }
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("gpt-marknadskartlaggaren-main/gpt-project.yaml", yaml.safe_dump(cfg))
        z.writestr("gpt-marknadskartlaggaren-main/src/instructions/system.md", "Keep original workflow.")
        z.writestr("gpt-marknadskartlaggaren-main/knowledge/KNOWLEDGE.md", "Verified knowledge.")
    destination = tmp_path / "out"
    result = subprocess.run([
        sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"),
        "--source", str(archive), "--destination", str(destination),
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    project = destination / "gpt-marknadskartlaggaren-main"
    plan = json.loads((project / "reconstructed-canonical/plugin-migration-plan.json").read_text())
    assert plan["source_entrypoint_missing"] is True
    assert plan["source_entrypoint_exists"] is False
    assert plan["skill_reconstruction_required"] is True
    assert "src/instructions/system.md" in plan["recovery_sources"]
    assert "knowledge/KNOWLEDGE.md" in plan["recovery_sources"]
    assert plan["release_ready"] is False
    assert not (project / "skills/marknadskartlaggaren/SKILL.md").exists()
