"""Cross-runtime Skill isolation and canonical behavior regression checks."""
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_distributions import (build_chat, build_claude, build_claude_skills,
                                 build_opencode, build_plugin,
                                 canonical_skill_definitions, projected_instruction)


def test_skill_isolation_across_five_distributions(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    defs = canonical_skill_definitions(cfg)
    canonical = projected_instruction(ROOT, cfg, defs)
    chat = build_chat(ROOT, cfg, tmp_path / "chat-build", "1.6.20-test")
    claude = build_claude(ROOT, cfg, tmp_path / "claude-build", "1.6.20-test")
    plugin = build_plugin(ROOT, cfg, tmp_path / "plugin-build", "1.6.20-test")
    skills = build_claude_skills(ROOT, cfg, tmp_path / "skills-build", "1.6.20-test")
    opencode = build_opencode(ROOT, cfg, tmp_path / "opencode-build", "1.6.20-test")

    assert (chat / "assistant" / "instructions.md").read_text() == canonical
    assert (claude / "project" / "instructions.md").read_text() == canonical
    assert (opencode / "AGENTS.md").read_text().startswith(canonical.rstrip())
    assert not (claude / "skills").exists()
    for skill in defs:
        name = skill["id"]
        for root, prefix in ((chat, "assistant/skills"), (plugin, "skills"),
                             (skills, "skills"), (opencode, ".opencode/skills")):
            assert (root / prefix / name / "SKILL.md").is_file()
        if name != "distribution-and-parity":
            assert not (plugin / "skills" / name / "scripts").exists()
            assert not (skills / "skills" / name / "scripts").exists()
        for root, prefix in ((plugin, "skills"), (skills, "skills"), (opencode, ".opencode/skills")):
            body = (root / prefix / name / "SKILL.md").read_text()
            assert "## Canonical behavior" in body
            assert skill["description"] in body
    assert (plugin / "skills/distribution-and-parity/scripts/distribution-engine/scripts/build_distributions.py").is_file()
    assert (skills / "skills/distribution-and-parity/assets/gpt-byggaren-engine.zip").is_file()
    assert (opencode / ".opencode/runtime-contract.json").is_file() or (opencode / "AGENTS.md").is_file()


def test_explicit_resource_empty_is_preserved_in_portable_skill(tmp_path):
    from build_distributions import resolve_plugin_skill_resources
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    for skill in cfg["skills"]["definitions"]:
        resolved = resolve_plugin_skill_resources(ROOT, cfg, skill)
        if skill["id"] in ("gpt-project-workflow", "legacy-project-analysis"):
            assert resolved["scripts"] == []
        if skill["id"] == "distribution-and-parity":
            assert resolved["scripts"]


def test_skill_script_requirements_are_scoped_to_packaged_scripts():
    from build_distributions import plugin_script_runtime_requirements
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert plugin_script_runtime_requirements(cfg, [])["code_execution"]["level"] == "not_required"
    assert plugin_script_runtime_requirements(cfg)["code_execution"]["level"] == "required"
    script = next(tool["script"] for tool in cfg["tools"]["tools"] if tool.get("type") == "script")
    selected = plugin_script_runtime_requirements(cfg, [script])
    assert selected["code_execution"]["languages"] == ["python"]


def test_plugin_and_claude_skill_handoff_is_explicit_without_cross_skill_paths(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = build_plugin(ROOT, cfg, tmp_path / "plugin", "1.6.20-test")
    claude = build_claude_skills(ROOT, cfg, tmp_path / "claude", "1.6.20-test")
    for out in (plugin, claude):
        workflow = (out / "skills/gpt-project-workflow/SKILL.md").read_text()
        assert "## Skill dependencies" in workflow
        assert "`distribution-and-parity`" in workflow
        assert "Do not assume its files exist relative to this Skill" in workflow
        assert "## Scripts" not in workflow
        for skill_name in ("gpt-project-workflow", "legacy-project-analysis"):
            assert not (out / "skills" / skill_name / "scripts").exists()


def test_explicit_resource_policy_prevents_accidental_inheritance(tmp_path):
    import pytest
    from build_distributions import resolve_plugin_skill_resources
    root = tmp_path / "project"
    (root / "knowledge").mkdir(parents=True)
    (root / "knowledge" / "reference.md").write_text("Reference material.")
    cfg = {
        "skills": {"resource_policy": "explicit"},
        "knowledge_architecture": {"canonical_root": "knowledge"},
    }
    skill = {"id": "plan", "references": [], "assets": [], "scripts": []}
    assert resolve_plugin_skill_resources(root, cfg, skill) == {
        "references": [], "assets": [], "scripts": []
    }
    with pytest.raises(ValueError, match="must declare references"):
        resolve_plugin_skill_resources(root, cfg, {"id": "plan", "assets": [], "scripts": []})
    with pytest.raises(ValueError, match="must declare scripts"):
        resolve_plugin_skill_resources(root, cfg, {"id": "plan", "references": [], "assets": []})


def test_legacy_resource_inheritance_remains_supported(tmp_path):
    from build_distributions import resolve_plugin_skill_resources
    root = tmp_path / "project"
    (root / "knowledge").mkdir(parents=True)
    (root / "knowledge" / "reference.md").write_text("Reference material.")
    cfg = {"knowledge_architecture": {"canonical_root": "knowledge"}}
    result = resolve_plugin_skill_resources(root, cfg, {"id": "legacy"})
    assert result["references"] == ["knowledge/reference.md"]
    assert result["assets"] == []
