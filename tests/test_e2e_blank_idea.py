from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_blank_idea_e2e():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_e2e_blank_idea.py"),
         "--project-root", str(ROOT), "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["result"] == "pass"
    assert data["profile"] == "standard"
    assert all(data["checks"].values())
