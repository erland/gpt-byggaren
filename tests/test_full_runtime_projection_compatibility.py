"""Protect Claude Project and Chat from portable per-Skill core optimization."""
import importlib.util
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "scripts/lib/canonical_skill_sources.py"
spec = importlib.util.spec_from_file_location("canonical_skill_sources_regression", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_portable_skill_core_never_shortens_projected_instruction(tmp_path):
    (tmp_path / "core.md").write_text("# Shared core\n\nREQUIRED CORE POLICY\n", encoding="utf-8")
    (tmp_path / "compact.md").write_text("# Short portable core\n\nSHORT CORE POLICY\n", encoding="utf-8")
    (tmp_path / "skill.md").write_text("## Domain workflow\n\nSPECIALIZED WORKFLOW POLICY\n", encoding="utf-8")
    skill={"id":"domain","source":"skill.md"}
    cfg={"instructions":{"mode":"modular_skills","core":"core.md"}}
    before=module.projected_instruction(tmp_path,cfg,[skill])
    cfg["instructions"]["portable_skill_core"]="compact.md"
    after=module.projected_instruction(tmp_path,cfg,[skill])
    assert after == before, "Full Chat/Claude Project projection must never depend on portable_skill_core"
    assert "REQUIRED CORE POLICY" in after
    assert "SPECIALIZED WORKFLOW POLICY" in after
    assert "SHORT CORE POLICY" not in after
    standalone=module.skill_instruction(tmp_path,cfg,[skill],skill)
    assert "SHORT CORE POLICY" in standalone and "SPECIALIZED WORKFLOW POLICY" in standalone
    workspace_skill=module.skill_instruction(tmp_path,cfg,[skill],skill,runtime="opencode")
    assert workspace_skill == "## Domain workflow\n\nSPECIALIZED WORKFLOW POLICY"

def test_runtime_builders_keep_full_projected_instruction():
    # Cross-check the real builder call sites, not only the projection helper.
    source=(SOURCE.parents[1] / "build_distributions.py").read_text(encoding="utf-8")
    for name in ("build_chat","build_claude","build_opencode"):
        start=source.index(f"def {name}(")
        end=source.find("\ndef ",start+5)
        block=source[start:end if end != -1 else None]
        assert "projected_instruction(root, cfg, canonical_skill_definitions(cfg))" in block
        assert "portable_skill_core" not in block
