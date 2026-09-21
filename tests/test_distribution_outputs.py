from copy import deepcopy
from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "verify_distribution_outputs",
    ROOT / "scripts" / "verify_distribution_outputs.py",
)
verify_distribution_outputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_distribution_outputs)


def load_cfg():
    return yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))


def test_expected_files_include_enabled_plugin_distribution():
    cfg = load_cfg()
    version = "1.2.3"

    expected = set(verify_distribution_outputs.expected_files(cfg, version))

    assert f"{cfg['project']['id']}-plugin-{version}.zip" in expected


def test_expected_files_omit_disabled_plugin_distribution():
    cfg = deepcopy(load_cfg())
    cfg["runtime"]["plugin"]["enabled"] = False
    version = "1.2.3"

    expected = set(verify_distribution_outputs.expected_files(cfg, version))

    assert f"{cfg['project']['id']}-plugin-{version}.zip" not in expected
