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
    assert "distribution-engine.zip" in instructions
    assert "Ask the user to attach the downloaded ZIP" in instructions
    assert "Never fetch an engine from GitHub inside Python" in instructions
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
    archive = plugin / "skills/distribution-and-parity/assets/distribution-engine.zip"
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
    assert "Plugin engine preflight and user handoff" in instructions
    assert "ci-distributions" in instructions
    assert "do not pretend to provide it as a download" in instructions


def test_early_engine_preflight_and_ci_handoff(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-ci")
    skill = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(encoding="utf-8")
    assert "At the beginning of the first GPT project creation or resumption" in skill
    assert "one-time, non-blocking access preflight" in skill
    assert "copy those bytes unchanged" in skill
    assert "ci-distributions" in skill
    assert "GitHub Actions" in skill
    assert "do not invent one" in skill
    assert "never guess a release for" in skill
    assert "0.0.0-ci" in skill
    assert "unverified declarative source draft" in skill
