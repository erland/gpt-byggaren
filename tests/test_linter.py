from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_linter_current_project_has_no_errors():
    for p in [ROOT / ".pytest_cache", ROOT / "tests" / "__pycache__"]:
        if p.exists():
            shutil.rmtree(p)

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_gpt_project.py"),
         "--project-root", str(ROOT), "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    report = json.loads(r.stdout)
    assert report["summary"]["errors"] == 0
