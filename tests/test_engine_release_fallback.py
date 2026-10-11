from pathlib import Path
import importlib.util
import hashlib
import io
import json
import zipfile
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("engine_fetch", ROOT / "scripts/fetch_distribution_engine.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_version_match_precedes_fallback(monkeypatch, tmp_path):
    calls = []
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as z:
        for name in ("scripts/build_distributions.py", "scripts/install_distribution_engine.py",
                     "scripts/lib/project_model.py", "templates/example.tpl"):
            z.writestr(name, "test")
    blob = payload.getvalue()
    asset = {"name": "distribution-engine.zip",
             "digest": "sha256:" + hashlib.sha256(blob).hexdigest(),
             "browser_download_url": "https://github.com/erland/gpt-byggaren/releases/download/v2.3.4/distribution-engine.zip"}
    def fake_json(url):
        calls.append(url)
        return {"tag_name": "v2.3.4", "assets": [asset]}
    class Response(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *args): self.close()
    monkeypatch.setattr(module, "get_json", fake_json)
    monkeypatch.setattr(module.urllib.request, "urlopen", lambda *args, **kwargs: Response(blob))
    result = module.install("2.3.4", tmp_path / "engine")
    assert result["selected"] == "matching"
    assert calls == [module.API + "/tags/v2.3.4"]

def test_fallback_only_when_matching_asset_missing(monkeypatch):
    calls = []
    def fake_json(url):
        calls.append(url)
        if url.endswith("/tags/v1.2.3"):
            return {"tag_name": "v1.2.3", "assets": []}
        return {"tag_name": "v1.2.4", "assets": []}
    monkeypatch.setattr(module, "get_json", fake_json)
    with pytest.raises(module.MissingReleaseOrAsset):
        module.install("1.2.3", Path("/does-not-exist"))
    assert calls == [module.API + "/tags/v1.2.3", module.API + "/latest"]

def test_network_error_does_not_fallback(monkeypatch):
    def failed(_): raise TimeoutError("network failure")
    monkeypatch.setattr(module, "get_json", failed)
    with pytest.raises(TimeoutError):
        module.install("1.2.3", Path("/does-not-exist"))

def test_packaged_skill_has_resolver(tmp_path):
    import yaml
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT / "scripts/build_distributions.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    out = builder.build_plugin(ROOT, cfg, tmp_path, "2.3.4")
    for skill in builder.canonical_skill_definitions(cfg):
        directory = out / "skills" / skill["id"]
        assert (directory / "scripts" / "fetch_distribution_engine.py").is_file()
        instructions = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert "matching version" in instructions
        assert "latest" in instructions


def test_canonical_engine_direct_skill_files(tmp_path):
    import yaml
    spec = importlib.util.spec_from_file_location(
        "build_distributions_direct", ROOT / "scripts/build_distributions.py"
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    plugin = builder.build_plugin(ROOT, cfg, tmp_path, "0.0.0-test")
    claude = builder.build_claude_skills(ROOT, cfg, tmp_path, "0.0.0-test")
    for runtime in (plugin, claude):
        skill = runtime / "skills" / "distribution-and-parity"
        for relative in (
            "scripts/canonical-engine/scripts/build_distributions.py",
            "scripts/canonical-engine/scripts/install_distribution_engine.py",
            "scripts/canonical-engine/scripts/lib/project_model.py",
            "assets/canonical-engine/gpt-project.yaml",
        ):
            assert (skill / relative).is_file(), relative
        assert any((skill / "assets/canonical-engine/templates").rglob("*.tpl"))
    skill_text = (plugin / "skills/distribution-and-parity/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "scripts/canonical-engine/scripts/" in skill_text
    assert "assets/canonical-engine/" in skill_text
