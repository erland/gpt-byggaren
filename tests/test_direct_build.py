from pathlib import Path
import json
import subprocess
import sys

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

    assert "gpt-byggaren-project.zip" in files
    assert "gpt-byggaren-chat-0.0.0-testdirect.zip" in files
    assert "gpt-byggaren-custom-gpt-0.0.0-testdirect.zip" in files
    assert (dist / "SHA256SUMS.txt").exists()
