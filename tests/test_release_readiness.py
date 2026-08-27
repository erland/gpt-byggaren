from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def test_release_readiness_fast():
    r=subprocess.run([sys.executable,str(ROOT/'scripts'/'assess_release_readiness.py'),'--project-root',str(ROOT),'--json'],capture_output=True,text=True)
    assert r.returncode==0, r.stdout+r.stderr
    data=json.loads(r.stdout)
    assert data['result'] in {'ready','ready_with_warnings'}
