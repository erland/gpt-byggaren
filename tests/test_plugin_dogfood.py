from pathlib import Path
import importlib.util
import json
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "build_distributions", ROOT / "scripts" / "build_distributions.py"
)
build_distributions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_distributions)


def test_gpt_builder_dogfoods_plugin_with_explicit_reduced_parity():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    assert cfg["runtime"]["plugin"]["enabled"] is True
    assert cfg["workspace_state"]["workspace"]["requirement"] == "required"
    assert cfg["workspace_state"]["state"]["requirement"] == "required"
    assert any(
        tool.get("requirement") == "required"
        for tool in cfg["tools"]["tools"]
    )

    with tempfile.TemporaryDirectory() as td:
        out = build_distributions.build_plugin(ROOT, cfg, Path(td), "0.0.0-dogfood")

        skill = out / "skills" / "gpt-project-workflow" / "SKILL.md"
        assert skill.is_file()
        skill_text = skill.read_text(encoding="utf-8")
        assert "GPT Byggaren" in skill_text
        assert "Analysera verksamhetsbehov före teknikval." in skill_text

        for name in (
            "dynamic-planning.md",
            "resume-flow.md",
            "next-step-recommendation.md",
        ):
            assert (out / "skills" / "gpt-project-workflow" / "references" / name).is_file()

        snapshot = json.loads((out / "runtime-contract.json").read_text(encoding="utf-8"))
        notes = snapshot["adapter"]["parity_notes"]
        assert "host runtime" in notes["workspace_state"]
        assert "does not generate MCP execution" in notes["tool"]

        assert snapshot["tools"]["tools"]
        assert any(
            tool.get("requirement") == "required"
            for tool in snapshot["tools"]["tools"]
        )
