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
