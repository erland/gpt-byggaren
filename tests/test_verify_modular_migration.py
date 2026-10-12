"""Regression for v1.6.16: generated SKILL ZIPs must be genuinely specialized."""
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.verify_modular_migration import inspect


def _fixture(tmp_path):
    (tmp_path / "canonical/skills/a").mkdir(parents=True)
    (tmp_path / "canonical/skills/b").mkdir(parents=True)
    (tmp_path / "canonical/core.md").write_text("SHARED-CORE-UNIQUE\n")
    (tmp_path / "canonical/skills/a/behavior.md").write_text("WRITE-UNIQUE-BEHAVIOR\n")
    (tmp_path / "canonical/skills/b/behavior.md").write_text("REVISE-UNIQUE-BEHAVIOR\n")
    defs = [{"id":"a","source":"canonical/skills/a/behavior.md"},
            {"id":"b","source":"canonical/skills/b/behavior.md"}]
    cfg = {"project":{"id":"novellskaparen"}, "instructions":{"mode":"modular_skills","core":"canonical/core.md"}, "skills":{"definitions":defs}}
    return cfg


def _archives(tmp_path, cfg, duplicate=False):
    from lib.canonical_skill_sources import projected_instruction, skill_instruction
    (tmp_path / "dist").mkdir()
    assembled=projected_instruction(tmp_path,cfg,cfg["skills"]["definitions"])
    archives={
        "chat":{"assistant/instructions.md":assembled},
        "claude-project":{"project/instructions.md":assembled},
        "opencode":{"AGENTS.md":assembled+"\n## Adapter\n"},
        "plugin":{},
        "claude-skills":{},
    }
    for target in ["plugin","claude-skills"]:
        for sk in cfg["skills"]["definitions"]:
            body=skill_instruction(tmp_path,cfg,cfg["skills"]["definitions"],sk)
            if duplicate and sk["id"]=="a":
                body += "\nREVISE-UNIQUE-BEHAVIOR\n"
            archives[target][f"skills/{sk['id']}/SKILL.md"]="---\nname: sample\n---\n\n"+body
    for target, members in archives.items():
        with zipfile.ZipFile(tmp_path / "dist" / f"novellskaparen-{target}-0.1.0.zip","w") as z:
            for name, body in members.items():
                z.writestr(name,body)


def test_all_five_archives_verify(tmp_path):
    cfg=_fixture(tmp_path)
    _archives(tmp_path,cfg)
    result=inspect(tmp_path,cfg,"0.1.0")
    assert result["status"]=="archive_content_verified_pending_host",result
    assert len(result["checked_targets"])==5
    assert result["release_ready"] is False


def test_duplicate_specialized_behavior_blocks(tmp_path):
    cfg=_fixture(tmp_path)
    _archives(tmp_path,cfg,duplicate=True)
    result=inspect(tmp_path,cfg,"0.1.0")
    assert result["status"]=="blocked"
    assert any("duplicates behavior" in e for e in result["errors"])


def test_legacy_monolithic_mode_is_not_falsely_passed(tmp_path):
    cfg=_fixture(tmp_path)
    cfg["instructions"].pop("mode")
    assert inspect(tmp_path,cfg)["status"]=="blocked"


def test_missing_archive_blocks(tmp_path):
    cfg=_fixture(tmp_path)
    _archives(tmp_path,cfg)
    (tmp_path/"dist/novellskaparen-plugin-0.1.0.zip").unlink()
    result=inspect(tmp_path,cfg,"0.1.0")
    assert result["status"]=="blocked"
    assert any("plugin: missing" in e for e in result["errors"])
