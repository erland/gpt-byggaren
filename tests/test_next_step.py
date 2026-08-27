from pathlib import Path
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_recommend_next_step_uses_project_status():
    status = yaml.safe_load((ROOT / "project-status.yaml").read_text(encoding="utf-8"))
    expected = status["next_step"]

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "recommend_next_step.py"),
         "--project-root", str(ROOT), "--json"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["recommended"]["type"] == "planned"
    assert data["recommended"]["step_id"] == expected["recommended"]
    assert data["recommended"]["title"] == expected["title"]
