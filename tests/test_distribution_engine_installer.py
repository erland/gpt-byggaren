"""Regression checks for canonical engine installation in generated projects."""
from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "distribution_installer", ROOT / "scripts" / "install_distribution_engine.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_install_into_generated_project(tmp_path):
    project = tmp_path / "generated"
    project.mkdir()
    builders = {
        "chat": "chat",
        "plugin": "plugin",
        "claude_project": "claude",
        "claude_skills": "claude_skills",
        "opencode": "opencode",
    }
    config = {"build_system": {"runtime_targets": {
        name: {"builder": builder} for name, builder in builders.items()
    }}}
    before = yaml.safe_dump(config)
    (project / "gpt-project.yaml").write_text(before, encoding="utf-8")
    copied = module.install(ROOT, project)
    assert len(copied) == len(module.ENGINE_FILES)
    for relative in module.ENGINE_FILES:
        assert (project / relative).read_bytes() == (ROOT / relative).read_bytes()
    assert (project / "gpt-project.yaml").read_text(encoding="utf-8") == before


def test_missing_targets_rejected(tmp_path):
    project = tmp_path / "incomplete"
    project.mkdir()
    (project / "gpt-project.yaml").write_text(
        "build_system:\n  runtime_targets:\n    chat:\n      builder: chat\n",
        encoding="utf-8",
    )
    try:
        module.install(ROOT, project)
    except ValueError as exc:
        assert "Missing platform-specific runtime targets" in str(exc)
    else:
        raise AssertionError("Incomplete project must be rejected")


def test_installed_engine_builds_distinct_runtime_archives(tmp_path):
    import subprocess
    import sys
    import zipfile

    project = tmp_path / "generated"
    project.mkdir()
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    config["project"]["id"] = "generated-smoke"
    config["project"]["name"] = "Generated Smoke"
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(config, allow_unicode=True), encoding="utf-8"
    )
    module.install(ROOT, project)
    # Canonical build configuration is exercised against an isolated project root.
    # Minimal canonical instructions and one Skill are sufficient for the smoke run.
    instruction_path = project / config["instructions"]["canonical"]
    instruction_path.parent.mkdir(parents=True, exist_ok=True)
    instruction_path.write_text("You are a test assistant.\n", encoding="utf-8")
    for skill in config["skills"]["definitions"]:
        for key in ("references", "assets", "scripts"):
            for item in skill.get(key, []):
                relative = item if isinstance(item, str) else item.get("path")
                if not relative:
                    continue
                source = ROOT / relative
                if source.is_file():
                    destination = project / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(source.read_bytes())
    subprocess.run(
        [sys.executable, str(project / "scripts/build_distributions.py"),
         "--project-root", str(project), "--version", "0.1.0",
         "--targets", "chat,plugin,claude_project,claude_skills,opencode"],
        check=True, capture_output=True, text=True,
    )
    archives = list((project / "dist").glob("*.zip"))
    assert len(archives) == 5
    layouts = []
    for archive in archives:
        with zipfile.ZipFile(archive) as zf:
            layouts.append(frozenset(zf.namelist()))
    assert len(set(layouts)) > 1
