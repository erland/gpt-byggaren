from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_final_hygiene_current_project():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "project_hygiene.py"),
         "--project-root", str(ROOT), "--mode", "final", "--fix", "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["result"] in {"pass", "warning"}
    assert not any(f["severity"] == "blocked" for f in data["findings"])
