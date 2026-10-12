"""Two GPT profiles: an executable Plugin engine and instructions-only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("generic_builder", ROOT / "scripts/build_distributions.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def config():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text())
    cfg["project"]["id"] = "sample-script-gpt"
    cfg["project"]["name"] = "Sample Script GPT"
    cfg["runtime"]["plugin"]["enabled"] = True
    return cfg


def test_opted_in_engine_manifest_and_plugin_handoff(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    (root / "scripts").mkdir()
    (root / "scripts" / "selftest.py").write_text("print('ok')\n")
    (root / "scripts" / "worker.py").write_text("print('work')\n")
    cfg = config()
    cfg["engine"] = {
        "enabled": True, "resources": ["scripts/worker.py", "scripts/selftest.py"],
        "selftest": "scripts/selftest.py",
        "release_repository": "example/sample-script-gpt",
    }
    from lib.engine_package import package_engine
    archive = package_engine(root, cfg, "1.2.3", root / "dist")
    assert archive.name == "sample-script-gpt-engine.zip"
    with zipfile.ZipFile(archive) as z:
        manifest = json.loads(z.read("engine-package.json"))
        assert manifest["engine_id"] == "sample-script-gpt"
        assert manifest["version"] == "1.2.3"
        assert z.testzip() is None
        for name, digest in manifest["files"].items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
    # Use the real repository's paths for skill resources during plugin packaging.
    plugin = builder.build_plugin(ROOT, cfg, tmp_path / "build", "1.2.3")
    skill_files = list(plugin.glob("skills/*/SKILL.md"))
    assert skill_files
    assert all("sample-script-gpt-engine.zip" in p.read_text() for p in skill_files)
    assert all(not (p.parent / "assets/sample-script-gpt-engine.zip").exists() for p in skill_files)


def test_text_only_gpt_has_no_engine_archive(tmp_path):
    cfg = config()
    cfg.pop("engine", None)
    from lib.engine_package import package_engine
    assert package_engine(tmp_path, cfg, "1.2.3", tmp_path / "dist") is None


def test_engine_rejects_missing_or_escaping_resource(tmp_path):
    from lib.engine_package import package_engine
    cfg = config()
    cfg["engine"] = {"enabled": True, "resources": ["../outside"], "selftest": "../outside"}
    try:
        package_engine(tmp_path, cfg, "1.2.3", tmp_path / "dist")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsafe path accepted")
