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
