from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def _clean_generated_state():
    for name in ["build", "dist", ".pytest_cache"]:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)
    for p in sorted(ROOT.rglob("__pycache__"), key=lambda x: len(x.parts), reverse=True):
        if p.exists():
            shutil.rmtree(p)
    for p in ROOT.rglob("*.py[co]"):
        if p.exists():
            p.unlink()

def test_linter_current_project_has_no_errors():
    _clean_generated_state()
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_gpt_project.py"),
         "--project-root", str(ROOT), "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    report = json.loads(r.stdout)
    assert report["summary"]["errors"] == 0
