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


def test_modular_chat_skill_contains_canonical_behavior(tmp_path):
    source = tmp_path / "project"
    (source / "src" / "skills").mkdir(parents=True)
    (source / "src" / "instructions").mkdir(parents=True)
    (source / "src" / "instructions" / "core.md").write_text(
        "Core safety rules must always apply.\\n", encoding="utf-8"
    )
    (source / "src" / "skills" / "create.md").write_text(
        "Create the system and verify acceptance criteria.\\n", encoding="utf-8"
    )
    cfg = {
        "instructions": {"mode": "modular_skills", "core": "src/instructions/core.md"},
        "skills": {"definitions": [{
            "id": "create", "name": "create", "description": "Create new systems.",
            "source": "src/skills/create.md", "scripts": [], "references": []
        }]}
    }
    out = tmp_path / "runtime" / "skills"
    copy_portable_skill_modules(source, cfg, out)
    body = (out / "create" / "SKILL.md").read_text(encoding="utf-8")
    assert "## Canonical behavior" in body
    assert "Core safety rules must always apply." in body
    assert "Create the system and verify acceptance criteria." in body
    assert "## Scripts" not in body


def test_legacy_portable_skill_keeps_lightweight_fallback(tmp_path):
    source = tmp_path / "project"
    source.mkdir()
    cfg = {"skills": {"definitions": [{
        "id": "audit", "name": "audit", "description": "Audit projects."
    }]}}
    out = tmp_path / "runtime" / "skills"
    copy_portable_skill_modules(source, cfg, out)
    body = (out / "audit" / "SKILL.md").read_text(encoding="utf-8")
    assert "Audit projects." in body
    assert "## Canonical behavior" not in body
