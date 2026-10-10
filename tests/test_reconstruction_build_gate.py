"""Reconstructed projects must not enter ordinary distribution builds prematurely."""
import subprocess
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def invoke(name, root):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / name),
                           "--project-root", str(root)],
                          capture_output=True, text=True)


def test_reconstruction_build_and_validation_block_before_output(tmp_path):
    cfg = {
        "project": {"id": "reconstructed", "name": "Reconstructed"},
        "runtime": {"custom_gpt": {"enabled": False}},
        "reconstruction": {"status": "canonical_contracts_scaffolded", "release_ready": False},
    }
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    for script in ("build_distributions.py", "validate_distributions.py"):
        result = invoke(script, tmp_path)
        assert result.returncode != 0, (script, result.stdout, result.stderr)
        assert "not release-ready" in result.stderr
    assert not (tmp_path / "build").exists()
    assert not (tmp_path / "dist").exists()


def test_disabling_reconstruction_gate_requires_both_release_and_parity_state(tmp_path):
    cfg = {
        "project": {"id": "reconstructed", "name": "Reconstructed"},
        "runtime": {"custom_gpt": {"enabled": False}},
        "reconstruction": {"status": "canonical_contracts_scaffolded", "release_ready": True},
    }
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    for script in ("build_distributions.py", "validate_distributions.py"):
        result = invoke(script, tmp_path)
        assert result.returncode != 0
        assert "not release-ready" in result.stderr
