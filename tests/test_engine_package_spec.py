"""GPT-specific Engine ZIP inventory, integrity and CI compatibility."""
import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "gpt_engine_package", ROOT / "scripts/package_distribution_engine.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_manifest_and_archive_integrity(tmp_path):
    output = module.package(root=ROOT, version="2.4.6", output=tmp_path / module.ARCHIVE_NAME)
    assert output.name == "gpt-byggaren-engine.zip"
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        manifest = json.loads(z.read("engine-package.json"))
        assert manifest["engine_id"] == "gpt-byggaren"
        assert manifest["version"] == "2.4.6"
        assert manifest["entrypoint"] in manifest["required_files"]
        assert set(manifest["required_files"]) <= set(manifest["files"])
        assert set(manifest["files"]) == set(z.namelist()) - {"engine-package.json"}
        for name, digest in manifest["files"].items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
        assert "scripts/build_distributions.py" in manifest["files"]
        assert any(name.startswith("templates/") for name in manifest["files"])


def test_archive_build_is_reproducible(tmp_path):
    a = module.package(root=ROOT, version="0.0.0-ci", output=tmp_path / "a.zip")
    b = module.package(root=ROOT, version="0.0.0-ci", output=tmp_path / "b.zip")
    assert a.read_bytes() == b.read_bytes()


def test_workflows_publish_matching_engine_filename():
    for name in ("ci.yml", "release.yml"):
        text = (ROOT / ".github/workflows" / name).read_text()
        assert "gpt-byggaren-engine.zip" in text
        assert "dist/distribution-engine.zip" not in text
        assert "scripts/package_distribution_engine.py --version" in text
