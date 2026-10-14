"""Agent Skills technical names must match directory names in all runtimes."""
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_builder", ROOT / "scripts" / "build_distributions.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@pytest.mark.parametrize("id_,label", [
    ("bokplanering", "Bokplanering"),
    ("bokskrivande", "Bokskrivande och faktakontroll"),
    ("bokprojekt-publicering", "Bokprojekt, revision och publicering"),
])
def test_frontmatter_technical_name(id_, label):
    text = mod.compile_skill_markdown({"id": id_, "name": label, "description": "Test"})
    assert text.splitlines()[1] == "name: " + id_
    assert "name: " + label not in text.splitlines()[:4]

@pytest.mark.parametrize("bad", ["Uppercase", "innehåll", "space name", "-leading", "trailing-", "a"*65])
def test_invalid_id_rejected(bad):
    with pytest.raises(ValueError):
        mod.compile_skill_markdown({"id": bad, "name": "Label", "description": "Test"})
