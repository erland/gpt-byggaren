"""Guard parity when detailed runtime suitability moves to a modular skill."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_requirements_retained_by_core_and_distribution_skill():
    core = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    skill = (ROOT / "docs/skills/distribution-and-parity.md").read_text(encoding="utf-8")
    for term in ("ChatGPT Chat", "Claude Projects", "OpenCode", "OpenAI Plugin",
                 "ChatGPT Custom", "distribution-and-parity", "verifierad kompatibilitet"):
        assert term in core
    for term in ("persistent workspace/state", "runtime parity", "OpenAI Plugin",
                 "skills-first", "UI-komponenter", "registrerad runtime"):
        assert term.lower() in skill.lower()
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    definitions = {d["id"]: d for d in cfg["skills"]["definitions"]}
    assert "docs/skills/distribution-and-parity.md" in definitions["distribution-and-parity"]["references"]
    for runtime in ("chat_zip", "claude", "opencode", "plugin"):
        assert cfg["runtime"][runtime]["enabled"] is True


def test_canonical_core_keeps_hard_release_and_tool_gates():
    core = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    assert "Hoppa inte över gates" in core
    assert "Kritiska beteenderegler" in core
    assert "runtime-specifika kontroller" in core
