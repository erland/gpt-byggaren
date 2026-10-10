from pathlib import Path
import subprocess
import sys
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_split_claude_artifacts_and_skill_resources(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    targets = cfg["build_system"]["runtime_targets"]
    assert "claude" not in targets
    assert "claude_project" in targets and "claude_skills" in targets
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-split-test",
         "--targets", "claude_project,claude_skills,plugin"],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    dist = ROOT / "dist"
    project_id = cfg["project"]["id"]
    def entries(suffix):
        with zipfile.ZipFile(dist / f"{project_id}-{suffix}-0.0.0-split-test.zip") as z:
            return set(z.namelist())
    project = entries("claude-project")
    skills = entries("claude-skills")
    plugin = entries("plugin")
    assert "project/instructions.md" in project
    assert not any(p.startswith("skills/") for p in project)
    assert "project/instructions.md" not in skills
    for name in ("gpt-project-workflow", "legacy-project-analysis", "distribution-and-parity"):
        assert f"skills/{name}/SKILL.md" in skills
        assert f"skills/{name}/SKILL.md" in plugin
    for name in plugin:
        if name.startswith("skills/") and ("/scripts/" in name or "/assets/" in name or "/references/" in name):
            assert name in skills, f"Claude Skills missing canonical resource: {name}"
    assert not any(p.endswith("mcp.json") for p in skills)
