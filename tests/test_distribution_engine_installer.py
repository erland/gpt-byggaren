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
