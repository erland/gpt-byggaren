"""OpenCode projects modular canonical Skills without a legacy OpenCode skill toggle."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("engine_builder", ROOT / "scripts" / "build_distributions.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_modular_opencode_skills_are_on_by_default(monkeypatch, tmp_path):
    root = tmp_path
    (root / "knowledge").mkdir()
    (root / "knowledge" / "guide.md").write_text("Reference\n")
    (root / "sample.py").write_text("print('ok')\n")
    out = root / "out"
    cfg = {
        "runtime": {"opencode": {"skills": {}, "enabled": True}},
        "skills": {"mode": "modular", "resource_policy": "explicit"},
        "knowledge_architecture": {"canonical_root": "knowledge"},
    }
    definition = [{"id": "sample-skill", "name": "sample-skill",
                   "description": "Example skill", "references": ["knowledge/guide.md"],
                   "assets": [], "scripts": ["sample.py"]}]
    monkeypatch.setattr(module, "canonical_skill_definitions", lambda _cfg: definition)
    monkeypatch.setattr(module, "is_modular", lambda _cfg: True)
    monkeypatch.setattr(module, "skill_instruction", lambda *_args, **_kwargs: "## Instructions\nDo useful work.")
    monkeypatch.setattr(module, "plugin_script_runtime_requirements", lambda *_args: {})
    assert module.build_opencode_skills(root, cfg, out) == ["sample-skill"]
    path = out / ".opencode" / "skills" / "sample-skill"
    assert (path / "SKILL.md").exists()
    assert (path / "references" / "guide.md").read_text() == "Reference\n"
    assert (path / "scripts" / "sample.py").exists()


def test_explicitly_disabled_skills_stay_disabled(monkeypatch, tmp_path):
    cfg = {"runtime": {"opencode": {"skills": {"enabled": False}}}}
    monkeypatch.setattr(module, "is_modular", lambda _cfg: True)
    assert module.build_opencode_skills(tmp_path, cfg, tmp_path / "out") == []
