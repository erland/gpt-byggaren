"""Ensure Claude Skills VERSION is a normal one-line text file."""
from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder_version_test", ROOT / "scripts/build_distributions.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_claude_skills_version_has_newline_not_literal_escape(tmp_path):
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    out = builder.build_claude_skills(ROOT, cfg, tmp_path, "2.3.4")
    assert (out / "VERSION").read_bytes() == b"2.3.4\n"


def test_release_engine_handoff_describes_download_and_upload():
    instruction = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    assert "ladda ned Engine ZIP" in instruction
    assert "bifoga den nedladdade ZIP-filen" in instruction
    assert "gpt-byggaren-engine-<VERSION>.zip" in instruction
