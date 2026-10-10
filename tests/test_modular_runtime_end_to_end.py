"""End-to-end module packaging checks for the four peer distributions.

Validates real builders, not just declarative skill registrations.
"""
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("gpt-project-workflow", "legacy-project-analysis", "distribution-and-parity")


def test_modular_skills_in_all_four_real_builds(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert {s["id"] for s in cfg["skills"]["definitions"]} >= set(SKILLS)
    # Use a separate copied project to avoid modifying build/dist in the source checkout.
    import shutil
    project = tmp_path / "project"
    shutil.copytree(ROOT, project, ignore=shutil.ignore_patterns(".git", "build", "dist", "__pycache__", ".pytest_cache"))
    run = subprocess.run(
        [sys.executable, str(project / "scripts/build_distributions.py"),
         "--project-root", str(project), "--version", "0.0.0-module-parity",
         "--targets", "chat,claude,opencode,plugin"],
        text=True, capture_output=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    destinations = {
        "chat": project / "build/chat/assistant/skills",
        "claude": project / "build/claude/skills",
        "opencode": project / "build/opencode/.opencode/skills",
        "plugin": project / "build/plugin/skills",
    }
    for target, base in destinations.items():
        for skill in SKILLS:
            folder = base / skill
            assert (folder / "SKILL.md").is_file(), f"{target}: {skill} missing"
            body = (folder / "SKILL.md").read_text(encoding="utf-8")
            assert "name: " + skill in body, f"{target}: {skill} frontmatter missing"
    assert (project / "build/chat/assistant/instructions.md").read_bytes() == (
        project / "src/instructions/system.md").read_bytes()
    claude_path = cfg["runtime"]["claude"]["project"]["instructions"]
    assert (project / "build/claude" / claude_path).read_bytes() == (
        project / "src/instructions/system.md").read_bytes()
    assert (project / "build/plugin/skills/legacy-project-analysis/references/legacy-project-analysis.md").is_file()
    assert (project / "build/claude/skills/gpt-project-workflow/references/project-workflow-operations.md").is_file()
    assert (project / "build/chat/assistant/skills/gpt-project-workflow/references/project-workflow-operations.md").is_file()
    assert not list((project / "build/plugin").rglob("mcp.json"))


def test_workflow_core_and_detailed_skill_still_cover_resume_guards():
    core = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    detail = (ROOT / "docs/skills/project-workflow-operations.md").read_text(encoding="utf-8")
    for phrase in ("projektstatus", "project hygiene", "godkänd kontroll"):
        assert phrase.lower() in core.lower()
    for phrase in ("gpt-project.yaml", "project-status.yaml", "docs/development-plan.md", "STATUS.md", "PROJECT.md"):
        assert phrase in detail
    assert "Be inte användaren" in core
