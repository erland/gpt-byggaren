from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def test_release_readiness_fast():
    r=subprocess.run([sys.executable,str(ROOT/'scripts'/'assess_release_readiness.py'),'--project-root',str(ROOT),'--json'],capture_output=True,text=True)
    assert r.returncode==0, r.stdout+r.stderr
    data=json.loads(r.stdout)
    assert data['result'] in {'ready','ready_with_warnings'}


def test_release_readiness_covers_all_enabled_runtime_targets():
    import yaml
    cfg=yaml.safe_load((ROOT/'gpt-project.yaml').read_text(encoding='utf-8'))
    r=subprocess.run([sys.executable,str(ROOT/'scripts'/'assess_release_readiness.py'),'--project-root',str(ROOT),'--json'],capture_output=True,text=True)
    assert r.returncode==0, r.stdout+r.stderr
    data=json.loads(r.stdout)
    expected={'project_zip'}
    for target_cfg in cfg['build_system']['runtime_targets'].values():
        if cfg['runtime'][target_cfg['runtime_key']]['enabled']:
            expected.add(target_cfg['artifact_type'])
    assert expected <= set(data['distributions'])
