"""Guard the generator instructions against a single-layout five-ZIP shortcut."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generated_projects_must_use_platform_specific_builders():
    policy = (ROOT / "docs/skills/distribution-and-parity.md").read_text(encoding="utf-8")
    assert "Generera **inte** ett förenklat" in policy
    assert "En identisk fillista" in policy
    for required in ("Chat ZIP", "OpenAI Plugin", "Claude Projects", "Claude Skills", "OpenCode"):
        assert required in policy


def test_canonical_builder_has_distinct_runtime_adapters():
    source = (ROOT / "scripts/build_distributions.py").read_text(encoding="utf-8")
    for fn in ("build_chat", "build_plugin", "build_claude", "build_claude_skills", "build_opencode"):
        assert f"def {fn}(" in source
    assert "def build_runtime_target(" in source
    assert 'target_cfg["builder"]' in source


def test_build_rejects_identical_runtime_archive_layouts():
    source = (ROOT / "scripts/build_distributions.py").read_text(encoding="utf-8")
    assert "layouts[target] = frozenset(zf.namelist())" in source
    assert "if len(set(layouts.values())) == 1:" in source
    assert "use platform-specific builders" in source
