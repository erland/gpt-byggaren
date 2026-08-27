from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.project_model import select_reference_profile


def test_reference_projects():
    paths = sorted((ROOT / "evals" / "reference-projects").glob("*.yaml"))
    assert len(paths) == 3
    for path in paths:
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert select_reference_profile(case["characteristics"]) == case["expected"]["profile"]
