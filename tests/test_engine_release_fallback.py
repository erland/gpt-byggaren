"""Regression checks for attached Engine ZIP workflow and peer-runtime parity."""
from pathlib import Path
import importlib.util
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "build_distributions_attached", ROOT / "scripts/build_distributions.py"
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_plugin_prefers_attached_engine_and_never_github_fallback(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    skill = plugin / "skills/distribution-and-parity"
    instructions = (skill / "SKILL.md").read_text(encoding="utf-8")
    assert "gpt-byggaren-engine.zip" in instructions
    assert "attach" in instructions
    assert "Never use a " in instructions
    assert (skill / "scripts/selftest_distribution_engine.py").is_file()
    assert not (skill / "scripts/fetch_distribution_engine.py").exists()


def test_plugin_is_thin_and_claude_skills_resources_remain(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    claude = builder.build_claude_skills(ROOT, cfg, tmp_path, "0.0.0-test")
    assert not (plugin / "distribution-engine").exists()
    plugin_skill = plugin / "skills/distribution-and-parity"
    assert not (plugin_skill / "assets/gpt-byggaren-engine.zip").exists()
    assert not (plugin_skill / "scripts/canonical-engine").exists()
    assert not (plugin_skill / "assets/canonical-engine").exists()
    assert (claude / "skills/distribution-and-parity/assets/gpt-byggaren-engine.zip").is_file()

def test_chat_zip_still_bundles_original_engine(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    chat = builder.build_chat(ROOT, cfg, tmp_path, "0.0.0-test")
    for relative in (
        "scripts/build_distributions.py",
        "scripts/install_distribution_engine.py",
        "scripts/lib/project_model.py",
    ):
        assert (chat / "distribution-engine" / relative).is_file()


def test_engine_package_script_is_preserved():
    assert (ROOT / "scripts/package_distribution_engine.py").is_file()


def test_ci_plugin_does_not_reference_actions_artifacts_or_release_url(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-ci")
    skill = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(encoding="utf-8")
    assert "one-time, non-blocking engine access preflight" in skill
    assert "Do not reference GitHub Actions" in skill
    assert "CI artifacts" in skill
    assert "releases/download/v0.0.0-ci/" not in skill
    assert "simply ask the user to attach" in skill


def test_released_plugin_direct_link_uses_exact_version(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "2.9.7")
    skill = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(encoding="utf-8")
    assert "https://github.com/erland/gpt-byggaren/releases/download/v2.9.7/gpt-byggaren-engine.zip" in skill
    assert "Do not use latest or a different release version" in skill
    assert "ci-distributions" not in skill
