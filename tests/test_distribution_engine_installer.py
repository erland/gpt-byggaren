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
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    before = yaml.safe_dump(config)
    (project / "gpt-project.yaml").write_text(before, encoding="utf-8")
    copied = module.install(ROOT, project)
    assert set(module.ENGINE_FILES).issubset(copied)
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
    config["skills"]["definitions"] = []
    config["tools"]["tools"] = []
    config["runtime"]["chat_zip"]["include"]["knowledge"] = []
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
    result = subprocess.run(
        [sys.executable, str(project / "scripts/build_distributions.py"),
         "--project-root", str(project), "--version", "0.1.0",
         "--targets", "chat,plugin,claude_project,claude_skills,opencode"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + "\\n" + result.stderr
    archives = list((project / "dist").glob("*.zip"))
    assert len(archives) == 5
    layouts = []
    for archive in archives:
        with zipfile.ZipFile(archive) as zf:
            layouts.append(frozenset(zf.namelist()))
    assert len(set(layouts)) == 5
    assert config["project"]["id"] == "generated-smoke"
    assert not (project / "src/instructions/system.md").read_text(encoding="utf-8").startswith("GPT Byggaren")


def test_existing_project_script_is_preserved(tmp_path):
    project = tmp_path / "custom"
    project.mkdir()
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(config), encoding="utf-8"
    )
    own_script = project / "scripts" / "validate_model_robustness.py"
    own_script.parent.mkdir(parents=True)
    own_script.write_text("# Custom project validator\n", encoding="utf-8")
    module.install(ROOT, project)
    assert own_script.read_text(encoding="utf-8") == "# Custom project validator\n"


def test_wrong_runtime_builder_is_rejected(tmp_path):
    project = tmp_path / "wrong-builder"
    project.mkdir()
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    targets = config["build_system"]["runtime_targets"]
    targets["plugin"]["builder"] = "chat"
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(config),
        encoding="utf-8",
    )
    try:
        module.install(ROOT, project)
    except ValueError as exc:
        assert "Incorrect builder for plugin" in str(exc)
    else:
        raise AssertionError("Wrong runtime builder must be rejected")


def test_legacy_manualguiden_target_list_rejected(tmp_path):
    project = tmp_path / "manualguiden"
    project.mkdir()
    (project / "gpt-project.yaml").write_text(
        "build_system:\n  runtime_targets:\n  - chatgpt-chat\n  - openai-plugin\\n"
        "  - claude-projects\n  - claude-skills\n  - opencode\\n",
        encoding="utf-8",
    )
    try:
        module.install(ROOT, project)
    except ValueError as exc:
        assert "must be a mapping" in str(exc)
    else:
        raise AssertionError("Legacy target lists must fail with actionable error")


def test_project_specific_template_is_preserved(tmp_path):
    project = tmp_path / "manualguiden"
    project.mkdir()
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    config["project"]["id"] = "manualguiden"
    config["project"]["name"] = "Manualguiden"
    (project / "gpt-project.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    relative = config["runtime"]["chat_zip"]["start_here_template"]
    custom = project / relative
    custom.parent.mkdir(parents=True, exist_ok=True)
    custom.write_text("Manualguidens egen introduktion\n", encoding="utf-8")
    module.install(ROOT, project)
    assert custom.read_text(encoding="utf-8") == "Manualguidens egen introduktion\n"
    assert (project / "gpt-project.yaml").read_text(encoding="utf-8").find("manualguiden") != -1
