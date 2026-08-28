from pathlib import Path
import subprocess, sys, yaml, json, jsonschema

ROOT = Path(__file__).resolve().parents[1]

def test_instruction_adherence_eval_package():
    schema = json.loads((ROOT / "schemas" / "eval-case.schema.json").read_text(encoding="utf-8"))
    files = sorted((ROOT / "evals" / "instruction-adherence").glob("*.yaml"))
    ids = set()
    for path in files:
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        jsonschema.validate(case, schema)
        ids.add(case["id"])
    assert {
        "bootstrap-core-001",
        "multiturn-retention-001",
        "terminal-contract-001",
        "no-knowledge-core-001",
    }.issubset(ids)

def test_instruction_adherence_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_instruction_adherence.py", "--project-root", "."],
        cwd=ROOT, text=True, capture_output=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Instruction-adherence contract OK" in result.stdout
