"""Regression: critical migration guarantees survive modularization."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_migration_behavior_remains_in_core_and_skill():
    core = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    skill = (ROOT / "docs/skills/legacy-project-analysis.md").read_text(encoding="utf-8")
    for required in ("Bevara domänbeteende", "aktivera aldrig en ny runtime", "CLI"):
        assert required in core
    for required in ("Inventera projektet", "Bevara domänbeteende", "manual-review", "Aktivera mål-runtimen"):
        assert required in skill
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    definitions = {item["id"]: item for item in cfg["skills"]["definitions"]}
    assert "docs/skills/legacy-project-analysis.md" in definitions["legacy-project-analysis"]["references"]


def test_all_four_build_targets_still_declared():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    for name in ("chat_zip", "plugin", "claude", "opencode"):
        assert name in cfg["runtime"]
    assert cfg["instructions"]["canonical"] == "src/instructions/system.md"
