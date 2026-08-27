from pathlib import Path
import json
import sys
import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.project_model import select_reference_profile


def test_profile_files_follow_schema():
    schema = json.loads((ROOT / "schemas" / "reference-profile.schema.json").read_text(encoding="utf-8"))
    for path in (ROOT / "profiles").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        jsonschema.validate(data, schema)


def test_selector_zip_first():
    assert select_reference_profile({"scripts_required": True}) == "zip_first_advanced"


def test_selector_standard():
    assert select_reference_profile({"structured_knowledge": True}) == "standard"


def test_selector_simple():
    assert select_reference_profile({}) == "simple"
