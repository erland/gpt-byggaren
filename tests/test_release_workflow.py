from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_release_workflow_contract():
    p = ROOT / ".github" / "workflows" / "release.yml"
    text = p.read_text(encoding="utf-8")
    assert "types: [published]" in text
    assert "github.event.release.tag_name" in text
    assert "scripts/build_distributions.py" in text
    assert "scripts/validate_distributions.py" in text
    assert "gh release upload" in text


def test_release_workflow_uses_declarative_output_verifier():
    text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "verify_distribution_outputs.py" in text
    assert "mapfile -t FILES" in text
    assert "gpt-byggaren-chat-" not in text
    assert "gpt-byggaren-opencode-" not in text



def test_release_workflow_covers_plugin_declaratively():
    import yaml

    text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    assert cfg["runtime"]["plugin"]["enabled"] is True
    assert "plugin" in cfg["build_system"]["targets"]
    assert cfg["build_system"]["runtime_targets"]["plugin"]["artifact_type"] == "plugin_zip"

    assert "--print-files" in text
    assert "gh release upload" in text
    assert "FILES[@]" in text
    assert "gpt-byggaren-plugin-" not in text
