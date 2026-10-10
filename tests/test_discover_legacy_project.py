import importlib.util
import hashlib
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discover_legacy_project", ROOT / "scripts/discover_legacy_project.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_unknown_layout_generates_evidence_without_canonical_assumptions(tmp_path):
    nested = tmp_path / "my-old-gpt" / "materials"
    nested.mkdir(parents=True)
    (nested / "prompt.md").write_text("Research the market", encoding="utf-8")
    resources = tmp_path / "assets"
    resources.mkdir()
    (resources / "guide.txt").write_text("References", encoding="utf-8")
    result = module.discover(tmp_path)
    assert result["status"] == "analysis_required"
    assert result["release_ready"] is False
    assert "my-old-gpt/materials/prompt.md" in result["candidates"]["instruction_candidate"]
    assert "assets/guide.txt" in result["candidates"]["knowledge_candidate"]
    evidence = next(f for f in result["source_files"] if f["path"].endswith("prompt.md"))
    assert evidence["sha256"] == hashlib.sha256(b"Research the market").hexdigest()
    assert not (tmp_path / "gpt-project.yaml").exists()


def test_directory_with_only_unknown_names_still_inventoried(tmp_path):
    (tmp_path / "odd-file.xyz").write_bytes(b"contents")
    result = module.discover(tmp_path)
    assert len(result["source_files"]) == 1
    assert result["candidates"]["instruction_candidate"] == []


def test_symlink_rejected_without_following_external_file(tmp_path):
    external = tmp_path.parent / (tmp_path.name + "-external")
    external.write_text("secret")
    (tmp_path / "link.md").symlink_to(external)
    with pytest.raises(ValueError):
        module.discover(tmp_path)
