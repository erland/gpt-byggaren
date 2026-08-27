from pathlib import Path
import ast, yaml
ROOT=Path(__file__).resolve().parents[1]

def test_stable_release_contract():
    for rel in [
        "docs/stable-release.md",
        "schemas/stable-release.schema.json",
        "scripts/validate_stable_release.py"
    ]:
        assert (ROOT/rel).exists()
    ast.parse((ROOT/"scripts"/"validate_stable_release.py").read_text(encoding="utf-8"))
    status=yaml.safe_load((ROOT/"project-status.yaml").read_text(encoding="utf-8"))
    assert status["release"]["state"]=="stable"
    assert status["release"]["version"]=="1.0.0"
