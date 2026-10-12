"""Canonical Skill sources stay modular in Skill runtimes and complete elsewhere."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("canonical_skill_sources", ROOT / "scripts/lib/canonical_skill_sources.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _fixture(tmp_path):
    (tmp_path / "canonical/skills/write").mkdir(parents=True)
    (tmp_path / "canonical/skills/revise").mkdir(parents=True)
    (tmp_path / "canonical/core.md").write_text("Use Swedish. Keep user intent.\n", encoding="utf-8")
    (tmp_path / "canonical/skills/write/behavior.md").write_text("Compose original stories.\n", encoding="utf-8")
    (tmp_path / "canonical/skills/revise/behavior.md").write_text("Preserve established continuity.\n", encoding="utf-8")
    skills = [{"id": "write", "name": "write", "description": "Write", "source": "canonical/skills/write/behavior.md"},
              {"id": "revise", "name": "revise", "description": "Revise", "source": "canonical/skills/revise/behavior.md"}]
    cfg = {"instructions": {"mode": "modular_skills", "canonical": "canonical/core.md",
                             "core": "canonical/core.md"}, "skills": {"definitions": skills}}
    return cfg, skills


def test_modular_skills_share_only_core(tmp_path):
    cfg, skills = _fixture(tmp_path)
    write = module.skill_instruction(tmp_path, cfg, skills, skills[0])
    revise = module.skill_instruction(tmp_path, cfg, skills, skills[1])
    assert "Use Swedish." in write and "Use Swedish." in revise
    assert "Compose original stories." in write
    assert "Preserve established continuity." not in write
    assert "Preserve established continuity." in revise
    assert "Compose original stories." not in revise
    combined = module.projected_instruction(tmp_path, cfg, skills)
    assert combined.count("Use Swedish.") == 1
    assert combined.count("Compose original stories.") == 1
    assert combined.count("Preserve established continuity.") == 1


def test_monolithic_projects_keep_old_behavior(tmp_path):
    (tmp_path / "canonical").mkdir()
    (tmp_path / "canonical/instructions.md").write_text("One complete instruction.\n")
    cfg = {"instructions": {"canonical": "canonical/instructions.md"}}
    assert module.projected_instruction(tmp_path, cfg, []) == "One complete instruction.\n"
    assert module.skill_instruction(tmp_path, cfg, [{"id": "a"}], {"id": "a"}) == "One complete instruction."


def test_missing_or_unsafe_modular_source_is_rejected(tmp_path):
    cfg, skills = _fixture(tmp_path)
    skills[0]["source"] = "../escape.md"
    import pytest
    with pytest.raises(ValueError):
        module.projected_instruction(tmp_path, cfg, skills)


def test_skill_architecture_defaults_to_one_reviewed_skill():
    spec = importlib.util.spec_from_file_location("skill_architecture_analysis", ROOT / "scripts/lib/skill_architecture_analysis.py")
    analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analyzer)
    proposal = analyzer.propose("## Write\nCreate story\n\n## Revise\nChange prose", "novellskaparen")
    assert len(proposal["suggested_skills"]) == 1
    assert len(proposal["candidate_boundaries"]) == 2
    assert proposal["approval_required_for_split"] is True
    assert proposal["source_text_preserved"] is True
