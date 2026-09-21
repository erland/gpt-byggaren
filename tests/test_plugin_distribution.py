from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "build_distributions", ROOT / "scripts" / "build_distributions.py"
)
build_distributions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_distributions)


def load_cfg():
    return yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))


def test_plugin_manifest_uses_canonical_project_metadata():
    cfg = load_cfg()
    manifest = build_distributions.plugin_manifest(cfg, "1.2.3")

    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert manifest["name"] == cfg["project"]["id"]
    assert manifest["version"] == "1.2.3"
    assert manifest["description"] == cfg["project"]["description"].strip()


def test_build_plugin_has_required_structure_and_skill_resources():
    cfg = load_cfg()
    with tempfile.TemporaryDirectory() as td:
        build_root = Path(td)
        out = build_distributions.build_plugin(ROOT, cfg, build_root, "1.2.3")

        assert (out / "plugin.json").is_file()
        assert (out / "README.md").is_file()
        assert (out / "VERSION").read_text(encoding="utf-8") == "1.2.3\n"
        assert (out / "MANIFEST.json").is_file()
        assert (out / "runtime-contract.json").is_file()

        for skill in build_distributions.canonical_skill_definitions(cfg):
            skill_dir = out / "skills" / skill["id"]
            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            assert f"name: {skill['name']}" in skill_text
            assert f"description: {skill['description']}" in skill_text

            resources = build_distributions.resolve_plugin_skill_resources(ROOT, cfg, skill)
            for key in ("references", "assets", "scripts"):
                for ref in resources[key]:
                    assert (skill_dir / key / Path(ref).name).is_file()

        manifest = json.loads((out / "MANIFEST.json").read_text(encoding="utf-8"))
        assert manifest["adapter_id"] == "openai_plugin"
        assert manifest["plugin_manifest"] == "plugin.json"
        assert manifest["contract_snapshot"] == "runtime-contract.json"

        snapshot = json.loads((out / "runtime-contract.json").read_text(encoding="utf-8"))
        assert snapshot["runtime_id"] == "openai_plugin"
        assert snapshot["adapter"]["skills_first"] is True


def test_plugin_zip_is_deterministic():
    cfg = load_cfg()
    version = "9.9.9-test"

    def build_zip(base: Path) -> Path:
        out = build_distributions.build_plugin(ROOT, cfg, base / "build", version)
        zip_path = base / "plugin.zip"
        files = sorted(p for p in out.rglob("*") if p.is_file())
        build_distributions.stable_write_zip(zip_path, out, files)
        return zip_path

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        first_dir = root / "first"
        second_dir = root / "second"
        first_dir.mkdir()
        second_dir.mkdir()

        first_zip = build_zip(first_dir)
        second_zip = build_zip(second_dir)

        first_bytes = first_zip.read_bytes()
        second_bytes = second_zip.read_bytes()
        assert hashlib.sha256(first_bytes).hexdigest() == hashlib.sha256(second_bytes).hexdigest()
        assert first_bytes == second_bytes

        with zipfile.ZipFile(first_zip) as zf:
            names = zf.namelist()
            assert "plugin.json" in names
            assert "runtime-contract.json" in names
            assert any(name.endswith("/SKILL.md") for name in names)
            assert names == sorted(names)
