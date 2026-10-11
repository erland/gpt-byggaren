"""Regression checks for standalone canonical-engine diagnostics."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "engine_selftest", ROOT / "scripts/selftest_distribution_engine.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_missing_source_reports_exact_stage(tmp_path):
    result = module.diagnose(tmp_path)
    assert result["ok"] is False
    assert result["stages"][0]["stage"] == "source"
    assert "scripts/build_distributions.py" in result["stages"][0]["missing"]


def test_selftest_present_in_packaged_plugin_skill(tmp_path):
    import yaml
    spec = importlib.util.spec_from_file_location(
        "build_distributions_selftest", ROOT / "scripts/build_distributions.py"
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    claude = builder.build_claude_skills(ROOT, cfg, tmp_path, "0.0.0-test")
    for runtime in (plugin, claude):
        assert (runtime / "skills/distribution-and-parity/scripts/selftest_distribution_engine.py").is_file()
    skill = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(encoding="utf-8")
    assert "selftest_distribution_engine.py" in skill
    assert "first failed stage" in skill


def test_canonical_source_selftest_succeeds():
    result = module.diagnose(ROOT)
    assert result["ok"], result
    assert [step["stage"] for step in result["stages"]] == list(module.STAGES)
