"""Executable plugin engine preflight regression coverage."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/detect_plugin_engine_runtime.py"
spec = importlib.util.spec_from_file_location("engine_detector", SCRIPT)
detector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detector)


def test_direct_with_real_canonical_source():
    result = detector.detect(ROOT)
    assert result["mode"] == "direct"
    assert not result["missing"]


def test_zip_fallback_only_if_original_engine_files_unavailable(tmp_path):
    absent = tmp_path / "missing"
    fallback = tmp_path / "original-engine.zip"
    fallback.write_bytes(b"placeholder-not-executed")
    result = detector.detect(absent, fallback)
    assert result["mode"] == "zip_fallback"
    assert result["fallback_zip"] == str(fallback.resolve())


def test_blocked_without_original_engine_or_zip(tmp_path):
    result = detector.detect(tmp_path / "missing")
    assert result["mode"] == "blocked"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--engine-root", str(tmp_path / "missing")],
        text=True, capture_output=True,
    )
    assert completed.returncode == 2
    assert json.loads(completed.stdout)["mode"] == "blocked"


def test_cli_direct_from_original_source():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--engine-root", str(ROOT)],
        text=True, capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["mode"] == "direct"


def test_direct_precedes_fallback_when_both_available(tmp_path):
    fallback = tmp_path / "engine.zip"
    fallback.write_bytes(b"placeholder-not-executed")
    assert detector.detect(ROOT, fallback)["mode"] == "direct"
