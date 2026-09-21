from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ci_workflow():
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "pull_request:" in text
    assert "workflow_dispatch:" in text
    assert "scripts/build_distributions.py" in text
    assert "scripts/validate_distributions.py" in text
    assert "0.0.0-ci" in text
    assert "actions/upload-artifact@v4" in text
    assert "Project hygiene check failed" in text



def test_ci_covers_plugin_distribution_declaratively():
    import yaml

    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    assert cfg["runtime"]["plugin"]["enabled"] is True
    assert "plugin" in cfg["build_system"]["targets"]
    assert cfg["build_system"]["runtime_targets"]["plugin"]["runtime_id"] == "openai_plugin"
    assert cfg["build_system"]["runtime_targets"]["plugin"]["artifact_type"] == "plugin_zip"

    # CI must derive expected runtime artifacts from the project registry rather
    # than hard-code every runtime-specific filename.
    assert "scripts/verify_distribution_outputs.py" in workflow
    assert "dist/*.zip" in workflow
    assert "gpt-byggaren-plugin-" not in workflow
