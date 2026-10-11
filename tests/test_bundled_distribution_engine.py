"""Offline distribution engine packaging regression checks."""
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def test_chat_and_plugin_bundle_engine(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-test",
         "--targets", "chat,plugin"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for target in ("chat", "plugin"):
        archives = list((ROOT / "dist").glob(f"*{target}*0.0.0-test.zip"))
        assert archives, f"No archive for {target}"
        with zipfile.ZipFile(archives[0]) as archive:
            names = set(archive.namelist())
            assert "distribution-engine/scripts/build_distributions.py" in names
            assert "distribution-engine/scripts/install_distribution_engine.py" in names
            assert "distribution-engine/scripts/lib/project_model.py" in names
            assert "distribution-engine/templates/START-HERE.chat.md.tpl" in names
