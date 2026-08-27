from pathlib import Path
import json
import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]

def test_test_manifest_schema():
    manifest = yaml.safe_load((ROOT / "test-manifest.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas" / "test-manifest.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(manifest, schema)

def test_reference_eval_schema():
    case = yaml.safe_load((ROOT / "evals" / "reference" / "analysis-zip-first-001.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas" / "eval-case.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(case, schema)
