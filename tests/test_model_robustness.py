from pathlib import Path
import json
import subprocess
import sys

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_model_robustness_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_model_robustness.py", "--project-root", "."],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Model robustness contract OK" in result.stdout


def test_model_compatibility_eval_package():
    schema = json.loads((ROOT / "schemas" / "eval-case.schema.json").read_text(encoding="utf-8"))
    files = sorted((ROOT / "evals" / "model-compatibility").glob("*.yaml"))
    ids = set()
    for path in files:
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        jsonschema.validate(case, schema)
        ids.add(case["id"])

    assert {
        "simple-idea-001",
        "runtime-completeness-001",
        "multistep-recovery-001",
        "resume-state-001",
    }.issubset(ids)


def test_operational_policy_is_runtime_included():
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    policy = config["workflow"]["policy"]
    assert policy == "src/runtime-policy/operational-execution-policy.md"
    assert Path(ROOT / policy).is_file()
    assert any(
        pattern == "src/runtime-policy/*.md"
        for pattern in config["runtime"]["chat_zip"]["include"]["policies"]
    )
