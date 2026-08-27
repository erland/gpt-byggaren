from pathlib import Path
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_resume_current_project():
    status = yaml.safe_load((ROOT / "project-status.yaml").read_text(encoding="utf-8"))

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "resume_project.py"),
         "--project-root", str(ROOT), "--json", "--no-checks"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["status"] == "ready"
    assert data["project_id"] == "gpt-byggaren"
    assert data["last_completed_step"] == status["progress"]["last_completed_step"]
    assert data["recommended_next_step"] == status["next_step"]["recommended"]
    assert data["recommended_next_title"] == status["next_step"]["title"]
