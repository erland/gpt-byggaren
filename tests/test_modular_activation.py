"""Regression: Novellskaparen-like migration must activate *actual* canonical Skills."""
import importlib.util
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("modular_activation", ROOT / "scripts/lib/activate_modular_skills.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _project(tmp_path):
    root = tmp_path
    (root / "canonical").mkdir()
    (root / "skills/write").mkdir(parents=True)
    (root / "skills/revise").mkdir(parents=True)
    parts = [("core", "canonical/intro.md", "Stay in Swedish.\n"),
             ("write", "skills/write/01.md", "Create an original novel.\n"),
             ("revise", "skills/revise/01.md", "Preserve continuity.\n")]
    for _, name, content in parts:
        (root / name).write_text(content)
    (root / "canonical/instructions.md").write_text("".join(p[2] for p in parts))
    (root / "canonical/assembly.json").write_text(json.dumps({"sections": [{"owner": o, "path": n} for o, n, _ in parts]}))
    cfg = {"project": {"id": "novellskaparen"}, "instructions": {"canonical": "canonical/instructions.md"},
           "skills": {"definitions": [{"id": "write", "name": "write", "description": "Write", "source": "skills/write/SKILL.md"},
                                      {"id": "revise", "name": "revise", "description": "Revise", "source": "skills/revise/SKILL.md"}]}}
    (root / "gpt-project.yaml").write_text(yaml.safe_dump(cfg))
    (root / "portable-skills.json").write_text(json.dumps({"core": "canonical/instructions.md"}))
    return root


def test_activation_uses_ownership_and_isolates_behaviors(tmp_path):
    root = _project(tmp_path)
    before = (root / "canonical/instructions.md").read_bytes()
    report = mod.activate(root)
    assert report["status"] == "activated_pending_behavior_review"
    assert (root / "canonical/instructions.md").read_bytes() == before
    cfg = yaml.safe_load((root / "gpt-project.yaml").read_text())
    assert cfg["instructions"]["mode"] == "modular_skills"
    assert cfg["instructions"]["core"] == "canonical/core.md"
    assert cfg["skills"]["definitions"][0]["source"] == "canonical/skills/write/behavior.md"
    assert json.loads((root / "portable-skills.json").read_text())["core"] == "canonical/core.md"
    helper_spec = importlib.util.spec_from_file_location("canonical_sources", ROOT / "scripts/lib/canonical_skill_sources.py")
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)
    write = helper.skill_instruction(root, cfg, cfg["skills"]["definitions"], cfg["skills"]["definitions"][0])
    revise = helper.skill_instruction(root, cfg, cfg["skills"]["definitions"], cfg["skills"]["definitions"][1])
    assert "Create an original novel." in write and "Preserve continuity." not in write
    assert "Preserve continuity." in revise and "Create an original novel." not in revise
    assert helper.projected_instruction(root, cfg, cfg["skills"]["definitions"]).count("Stay in Swedish.") == 1


def test_no_assembly_cannot_claim_activation(tmp_path):
    root = _project(tmp_path)
    (root / "canonical/assembly.json").unlink()
    report = mod.activate(root)
    assert report["status"] == "review_required"
    assert "mode" not in yaml.safe_load((root / "gpt-project.yaml").read_text())["instructions"]


def test_non_identical_assembly_rejected(tmp_path):
    root = _project(tmp_path)
    (root / "canonical/instructions.md").write_text("Different")
    assert mod.activate(root)["status"] == "review_required"
