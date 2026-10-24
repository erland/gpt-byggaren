"""Regression: Claude Skills must not advertise an OpenAI Plugin adapter."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("distribution_builder_claude_contract", ROOT / "scripts" / "build_distributions.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_claude_skills_runtime_contract_has_claude_adapter():
    cfg = MODULE.load_config(ROOT)
    contract = MODULE.claude_skills_runtime_contract(cfg, ["metamodellering"])
    adapter = contract["adapter"]
    assert contract["runtime_id"] == "claude_skills"
    assert adapter["mode"] == "claude_skills"
    assert adapter["skills"] == ["metamodellering"]
    assert "Claude" in adapter["parity_notes"]["artifact"]
    assert not any("Plugin" in str(note) for note in adapter["parity_notes"].values())
