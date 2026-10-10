from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_presentation_policy_is_explicit_and_model_independent():
    instruction = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    policy = (ROOT / "src/runtime-policy/adaptive-presentation-policy.md").read_text(encoding="utf-8")
    assert "adaptive-presentation-policy.md" in instruction
    assert "textalternativ" in instruction
    assert "Idé först" in policy
    assert "Text är fullvärdig fallback" in policy
    assert "Kapabilitet, inte modellnamn" in policy


def test_presentation_does_not_require_ui_or_extra_technical_questions():
    policy = (ROOT / "src/runtime-policy/adaptive-presentation-policy.md").read_text(encoding="utf-8")
    assert "utan obligatoriska formulär" in policy
    assert "Ingen viktig information får bara finnas" in policy
    assert "ingen `mcp.json`" in policy
    assert "Samma beslut och data" in policy


def test_plugin_policy_is_included_by_runtime_glob():
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert "src/runtime-policy/*.md" in cfg["runtime"]["chat_zip"]["include"]["policies"]
