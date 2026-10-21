from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_plugin_fallback_contract():
    policy = (ROOT / "docs/skills/plugin-declarative-fallback.md").read_text(encoding="utf-8")
    instructions = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    assert "declarative_fallback" in policy
    assert "pending_canonical_verification" in policy
    assert "release_ready: false" in policy
    assert "delivery.mode" in policy
    assert "Chat ZIP" in policy
    assert "plugin-declarative-fallback.md" in instructions


def test_chat_zip_builder_is_unchanged_in_fallback():
    builder = (ROOT / "scripts/build_distributions.py").read_text(encoding="utf-8")
    assert "def build_chat(" in builder
    assert 'get("bundle_distribution_engine", False)' in builder
