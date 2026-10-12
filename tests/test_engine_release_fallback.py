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


def test_canonical_engine_direct_skill_files(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    claude = builder.build_claude_skills(ROOT, cfg, tmp_path, "0.0.0-test")
    for runtime in (plugin, claude):
        skill = runtime / "skills" / "distribution-and-parity"
        for relative in (
            "scripts/canonical-engine/scripts/build_distributions.py",
            "scripts/canonical-engine/scripts/install_distribution_engine.py",
            "scripts/canonical-engine/scripts/lib/project_model.py",
            "assets/canonical-engine/gpt-project.yaml",
        ):
            assert (skill / relative).is_file(), relative
        assert any((skill / "assets/canonical-engine/templates").rglob("*.tpl"))
        assert not (skill / "scripts/fetch_distribution_engine.py").exists()


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


def test_embedded_engine_archive_matches_canonical_source(tmp_path):
    import hashlib
    import zipfile
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    archive = plugin / "skills/distribution-and-parity/assets/gpt-byggaren-engine.zip"
    assert archive.is_file()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for relative in (
            "scripts/build_distributions.py",
            "scripts/install_distribution_engine.py",
            "scripts/lib/project_model.py",
            "gpt-project.yaml",
        ):
            assert z.read(relative) == (ROOT / relative).read_bytes()
    instructions = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(encoding="utf-8")
    assert "Plugin engine preflight and handoff" in instructions
    assert "Never invent a sandbox path" in instructions


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
