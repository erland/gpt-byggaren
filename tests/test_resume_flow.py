from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]

def test_resume_current_project():
    r=subprocess.run(
        [sys.executable,str(ROOT/"scripts"/"resume_project.py"),
         "--project-root",str(ROOT),"--json","--no-checks"],
        capture_output=True,text=True
    )
    assert r.returncode==0, r.stdout+r.stderr
    data=json.loads(r.stdout)
    assert data["status"]=="ready"
    assert data["project_id"]=="gpt-byggaren"
    assert data["last_completed_step"]==21
    assert data["recommended_next_step"]==22
