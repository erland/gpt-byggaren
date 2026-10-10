"""Prevent critical canonical rules from being silently moved out of the core."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

CORE_RULES = {
    "idea_first": "Analysera verksamhetsbehov före teknikval",
    "authoritative_status": "strukturerad status",
    "deterministic_gate": "Hoppa inte över gates",
    "runtime_parity": "runtime parity",
    "plugin_peer": "skills-first peer runtime",
    "release_gate": "Blockerande resultat stoppar release",
    "text_fallback": "textalternativ",
    "migration_safety": "Bevara domänbeteende",
    "tool_declaration": "Deklarera bara körbara verktyg",
}


def test_canonical_core_retains_all_mandatory_invariants():
    core = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    for name, phrase in CORE_RULES.items():
        assert phrase in core, f"Lost canonical rule: {name}"


def test_all_registered_skills_references_reachable():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    definitions = cfg["skills"]["definitions"]
    assert {s["id"] for s in definitions} >= {
        "gpt-project-workflow", "legacy-project-analysis", "distribution-and-parity"
    }
    for skill in definitions:
        for ref in skill.get("references", []):
            assert (ROOT / ref).is_file(), f"Missing canonical skill reference: {ref}"


def test_core_skill_boundary_review_exists():
    content = (ROOT / "docs/canonical-core-skill-boundaries.md").read_text(encoding="utf-8")
    for marker in ("gpt-project-workflow", "legacy-project-analysis",
                   "distribution-and-parity", "Chat ZIP", "Claude", "releasegates"):
        assert marker in content
