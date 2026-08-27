from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_build_and_validate():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-test"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    r2 = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_distributions.py"),
         "--project-root", str(ROOT)],
        capture_output=True, text=True
    )
    assert r2.returncode == 0, r2.stdout + r2.stderr
