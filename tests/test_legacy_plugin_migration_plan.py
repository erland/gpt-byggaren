import json
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_market_mapper_legacy_plugin_produces_review_plan_without_activation(tmp_path):
    source = tmp_path / "old.zip"
    project = {
        "project": {"id": "marknadskartlaggaren", "name": "Marknadskartläggaren"},
        "runtime": {
            "openai_plugin": {
                "enabled": True,
                "mode": "skills_first",
                "entrypoint": "skills/marknadskartlaggaren/SKILL.md",
                "web_dependency": "required_host_runtime",
                "mcp_generated": False,
            },
            "custom_gpt": {"enabled": True},
        },
    }
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("project/gpt-project.yaml", yaml.safe_dump(project))
        archive.writestr("project/skills/marknadskartlaggaren/SKILL.md", "# Research")
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"),
         "--source", str(source), "--destination", str(out)],
        text=True, capture_output=True
    )
    assert result.returncode == 0, result.stderr
    migrated = yaml.safe_load((out / "project/gpt-project.yaml").read_text())
    assert "plugin" not in migrated["runtime"]
    assert migrated["runtime"]["openai_plugin"]["enabled"] is True
    assert migrated["runtime"]["custom_gpt"]["enabled"] is False
    plan = json.loads((out / "project/reconstructed-canonical/plugin-migration-plan.json").read_text())
    assert plan["source_entrypoint_exists"] is True
    assert plan["host_capability_dependencies"]["web_dependency"] == "required_host_runtime"
    assert plan["proposed_config"]["enabled"] is False
    assert plan["release_ready"] is False
    assert plan["runtime_activated"] is False
    report = json.loads((out / "MIGRATION-REPORT.json").read_text())
    assert report["legacy_plugin_plan"]["result"] == "review_required"
