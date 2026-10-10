import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_distributions import copy_portable_skill_modules


def test_portable_modules_copy_into_text_first_runtime(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    ref = source / "docs" / "skill.md"
    ref.parent.mkdir()
    ref.write_text("Read the verified project inventory.")
    cfg = {"skills": {"definitions": [{
        "id": "project-inventory", "name": "project-inventory",
        "description": "Analyze older projects.", "references": ["docs/skill.md"]
    }]}}
    out = tmp_path / "runtime" / "skills"
    built = copy_portable_skill_modules(source, cfg, out)
    assert built == ["project-inventory"]
    assert (out / "project-inventory" / "SKILL.md").is_file()
    assert "Analyze older projects." in (out / "project-inventory" / "SKILL.md").read_text()
    assert (out / "project-inventory" / "references" / "skill.md").read_text() == ref.read_text()


def test_skills_do_not_erase_canonical_core(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    core = source / "core.md"
    core.write_text("Core safety and workflow remain mandatory.")
    cfg = {"skills": {"definitions": [{"id": "audit", "name": "audit",
                                      "description": "Audit models."}]}}
    copy_portable_skill_modules(source, cfg, tmp_path / "out")
    assert core.read_text() == "Core safety and workflow remain mandatory."
