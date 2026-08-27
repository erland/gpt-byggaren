from pathlib import Path
import ast, yaml
ROOT=Path(__file__).resolve().parents[1]
def test_release_candidate_contract():
    for rel in ["docs/release-candidate.md","schemas/release-candidate.schema.json",
                "scripts/validate_release_candidate.py"]:
        assert (ROOT/rel).exists()
    ast.parse((ROOT/"scripts"/"validate_release_candidate.py").read_text(encoding="utf-8"))
    cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    assert cfg["release_candidate"]["version"]=="1.0.0-rc.1"
