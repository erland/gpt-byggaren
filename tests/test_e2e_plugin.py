from pathlib import Path
import json
import subprocess
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.0.0-plugin-e2e"


def run_script(script: str, *args: str):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), "--project-root", str(ROOT), *args],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def test_plugin_end_to_end_build_validate_and_verify():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    run_script("build_distributions.py", "--version", VERSION)
    run_script("validate_distributions.py")
    run_script("verify_distribution_outputs.py", "--version", VERSION)

    target = cfg["build_system"]["runtime_targets"]["plugin"]
    filename = (
        target["filename_pattern"]
        .replace("<project-id>", cfg["project"]["id"])
        .replace("<version>", VERSION)
    )
    plugin_zip = ROOT / "dist" / filename
    assert plugin_zip.is_file()

    with zipfile.ZipFile(plugin_zip) as zf:
        names = set(zf.namelist())
        assert "plugin.json" in names
        assert "README.md" in names
        assert "VERSION" in names
        assert "MANIFEST.json" in names
        assert "runtime-contract.json" in names
        assert any(name.startswith("skills/") and name.endswith("/SKILL.md") for name in names)

        plugin_manifest = json.loads(zf.read("plugin.json"))
        assert plugin_manifest["version"] == VERSION

        runtime_contract = json.loads(zf.read("runtime-contract.json"))
        assert runtime_contract["runtime_id"] == "openai_plugin"
        assert runtime_contract["adapter"]["skills_first"] is True

    delivery = json.loads((ROOT / "dist" / "DELIVERY-MANIFEST.json").read_text(encoding="utf-8"))
    plugin_artifacts = [
        item for item in delivery["artifacts"]
        if item.get("type") == "plugin_zip"
    ]
    assert len(plugin_artifacts) == 1
    assert plugin_artifacts[0]["file"] == filename
    assert plugin_artifacts[0]["artifact_id"] == "runtime_package"
