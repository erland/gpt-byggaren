"""Regression: offline Chat engine is opt-in without breaking GPT Byggaren."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from scripts.build_distributions import build_chat

ROOT = Path(__file__).resolve().parents[1]


def test_chat_engine_opt_in_and_default():
    original = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert original["runtime"]["chat_zip"]["bundle_distribution_engine"] is True
    with TemporaryDirectory() as directory:
        build_root = Path(directory)
        for setting, expected in [(None, False), (False, False), (True, True)]:
            cfg = deepcopy(original)
            if setting is None:
                cfg["runtime"]["chat_zip"].pop("bundle_distribution_engine", None)
            else:
                cfg["runtime"]["chat_zip"]["bundle_distribution_engine"] = setting
            runtime = build_chat(ROOT, cfg, build_root, "0.0.0-test")
            assert (runtime / "distribution-engine").exists() is expected
            assert (runtime / "assistant" / "instructions.md").is_file()
            assert (runtime / "MANIFEST.json").is_file()
