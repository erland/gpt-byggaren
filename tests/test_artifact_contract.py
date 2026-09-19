from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("project_model", ROOT / "scripts" / "lib" / "project_model.py")
project_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project_model)


def test_current_artifact_contract_is_platform_neutral():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    contract = project_model.normalize_artifact_contract(cfg)
    outputs = contract["outputs"]

    assert contract["contract_version"] == 1
    assert outputs["development_plan"]["format"] == "markdown"
    assert outputs["project_package"]["format"] == "zip"
    assert outputs["runtime_package"]["multiplicity"] == "many"
    assert outputs["parity_report"]["requirement"] == "conditional"


def test_legacy_artifact_config_is_normalized_without_mutating_source():
    cfg = {
        "artifacts": {
            "project_zip": {"required": True},
            "chat_zip": {"required": True},
            "custom_gpt_zip": {"required_when_enabled": True},
            "validation_report": {"required_for_release": True},
            "parity_report": {"required_when_multiple_runtimes": True},
            "checksums": {"required_for_release": True},
        }
    }

    contract = project_model.normalize_artifact_contract(cfg)
    outputs = contract["outputs"]

    assert outputs["project_package"]["kind"] == "package"
    assert outputs["runtime_package"]["kind"] == "distribution"
    assert outputs["runtime_package"]["format"] == "zip"
    assert outputs["checksums"]["format"] == "sha256"
    assert "outputs" not in cfg["artifacts"]


def test_delivery_manifest_links_files_to_canonical_artifacts():
    r = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_distributions.py"),
            "--project-root", str(ROOT),
            "--version", "0.0.0-artifacttest",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr

    manifest = json.loads((ROOT / "dist" / "DELIVERY-MANIFEST.json").read_text(encoding="utf-8"))
    mapped = {item["type"]: item.get("artifact_id") for item in manifest["artifacts"]}

    assert mapped["project_zip"] == "project_package"
    assert mapped["chat_zip"] == "runtime_package"
    assert mapped["custom_gpt_zip"] == "runtime_package"
    assert mapped["checksums"] == "checksums"
