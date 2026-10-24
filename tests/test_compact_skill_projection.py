"""Modular Skill projections keep complete core for standalone hosts by default."""
import importlib.util
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/"scripts/lib/canonical_skill_sources.py"
spec=importlib.util.spec_from_file_location("canonical_skill_sources_test",SRC)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_workspace_and_portable_skill_core_policy(tmp_path):
    (tmp_path/"core.md").write_text("CORE RULE: never invent facts\n",encoding="utf-8")
    (tmp_path/"compact.md").write_text("SHORT RULE: require explicit approval\n",encoding="utf-8")
    (tmp_path/"skill.md").write_text("SKILL RULE: generate exactly one slide\n",encoding="utf-8")
    skill={"id":"slide-workflow","source":"skill.md"}
    cfg={"instructions":{"mode":"modular_skills","core":"core.md"}}
    assert "CORE RULE" in module.skill_instruction(tmp_path,cfg,[skill],skill)
    assert "SKILL RULE" in module.skill_instruction(tmp_path,cfg,[skill],skill)
    opencode=module.skill_instruction(tmp_path,cfg,[skill],skill,runtime="opencode")
    assert "SKILL RULE" in opencode
    assert "CORE RULE" not in opencode
    cfg["instructions"]["portable_skill_core"]="compact.md"
    standalone=module.skill_instruction(tmp_path,cfg,[skill],skill)
    assert "SHORT RULE" in standalone and "SKILL RULE" in standalone
    assert "CORE RULE" not in standalone
    assert "CORE RULE" in module.projected_instruction(tmp_path,cfg,[skill])

def test_missing_compact_core_fails_closed(tmp_path):
    (tmp_path/"core.md").write_text("CORE\n")
    (tmp_path/"skill.md").write_text("SKILL\n")
    skill={"id":"workflow","source":"skill.md"}
    cfg={"instructions":{"mode":"modular_skills","core":"core.md","portable_skill_core":"missing.md"}}
    import pytest
    with pytest.raises(ValueError,match="Unsafe or missing"):
        module.skill_instruction(tmp_path,cfg,[skill],skill)
