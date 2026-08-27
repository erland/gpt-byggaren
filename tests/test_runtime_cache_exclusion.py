from pathlib import Path
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def test_chat_runtime_excludes_python_cache_artifacts():
    lib = ROOT / "scripts" / "lib"
    env = os.environ.copy()
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, 'scripts'); import lib.project_model"],
        cwd=ROOT, check=True, env=env
    )
    assert (lib / "__pycache__").exists()

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-cachetest",
         "--targets", "chat"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr

    chat_zip = ROOT / "dist" / "gpt-byggaren-chat-0.0.0-cachetest.zip"
    try:
        with zipfile.ZipFile(chat_zip) as zf:
            names = zf.namelist()
        assert not any("__pycache__" in name for name in names)
        assert not any(name.endswith((".pyc", ".pyo")) for name in names)
    finally:
        cache = lib / "__pycache__"
        if cache.exists():
            shutil.rmtree(cache)
