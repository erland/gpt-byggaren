from pathlib import Path
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_direct_build():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_direct.py"),
            "--project-root", str(ROOT),
            "--version", "0.0.0-testdirect",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    dist = ROOT / "dist"
    manifest = json.loads((dist / "DELIVERY-MANIFEST.json").read_text(encoding="utf-8"))
    files = {a["file"] for a in manifest["artifacts"]}

    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    expected = {"gpt-byggaren-project.zip", "SHA256SUMS.txt"}
    for target in cfg["build_system"]["targets"]:
        if target == "project":
            continue
        target_cfg = cfg["build_system"]["runtime_targets"][target]
        if not cfg["runtime"][target_cfg["runtime_key"]]["enabled"]:
            continue
        expected.add(
            target_cfg["filename_pattern"]
            .replace("<project-id>", cfg["project"]["id"])
            .replace("<version>", "0.0.0-testdirect")
        )

    assert expected <= files
    assert (dist / "SHA256SUMS.txt").exists()
