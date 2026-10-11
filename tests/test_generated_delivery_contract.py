from pathlib import Path
import importlib.util
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("delivery", ROOT / "scripts/validate_generated_delivery.py")
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


def test_rejects_missing_generated_contract(tmp_path):
    errors = delivery.validate(tmp_path)
    assert "Missing .gitignore" in errors
    assert "Missing gpt-project.yaml" in errors
    assert any("canonical engine" in error for error in errors)


def test_rejects_git_and_dist_in_project_zip(tmp_path):
    archive = tmp_path / "project.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("manualletaren/.git/config", "git metadata")
        zf.writestr("manualletaren/dist/runtime.zip", "generated")
    errors = delivery.validate(tmp_path, archive)
    assert any("Forbidden generated path" in error for error in errors)


def test_generated_gitignore_template():
    patterns = (ROOT / "templates/generated-project.gitignore").read_text(encoding="utf-8")
    assert "dist/" in patterns
    assert "build/" in patterns
    assert ".env" in patterns


def test_delivery_guard_bundled_in_canonical_engine():
    builder = (ROOT / "scripts/build_distributions.py").read_text(encoding="utf-8")
    assert 'for folder in ("scripts", "templates"):' in builder
    assert (ROOT / "scripts/validate_generated_delivery.py").is_file()


def test_rejects_missing_distribution_artifact(tmp_path):
    import json
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "DELIVERY-MANIFEST.json").write_text(json.dumps({
        "artifacts": [{"type": "runtime_zip", "file": f"runtime-{i}.zip"} for i in range(5)] + [{"type": "project_zip", "file": "project.zip"}]
    }), encoding="utf-8")
    errors = delivery.validate(tmp_path, dist_dir=dist)
    assert any("Missing or unsafe distribution file" in error for error in errors)


def test_rejects_incomplete_distribution_manifest(tmp_path):
    (tmp_path / "DELIVERY-MANIFEST.json").write_text('{"artifacts": []}', encoding="utf-8")
    errors = delivery.validate(tmp_path, dist_dir=tmp_path)
    assert "Expected five runtime distributions, found 0" in errors


def test_rejects_disabled_targets_or_enabled_custom_gpt(tmp_path):
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    cfg["build_system"]["targets"] = ["project", "chat", "plugin"]
    cfg["runtime"]["custom_gpt"]["enabled"] = True
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    errors = delivery.validate(tmp_path)
    assert "Expected project and all five canonical build targets" in errors
    assert "Custom GPT must be disabled" in errors


def test_rejects_gitignore_in_runtime_zip(tmp_path):
    import json
    dist = tmp_path / "dist"
    dist.mkdir()
    artifacts = [{"type": "project_zip", "file": "project.zip"}]
    (dist / "project.zip").write_bytes(b"placeholder")
    for index in range(5):
        name = f"runtime-{index}.zip"
        with zipfile.ZipFile(dist / name, "w") as zf:
            zf.writestr(".gitignore" if index == 0 else "SKILL.md", "content")
        artifacts.append({"type": "runtime_zip", "file": name})
    (dist / "DELIVERY-MANIFEST.json").write_text(json.dumps({"artifacts": artifacts}))
    errors = delivery.validate(tmp_path, dist_dir=dist)
    assert "Unexpected runtime root .gitignore: runtime-0.zip" in errors


def test_rejects_duplicate_runtime_types_even_with_five_zips(tmp_path):
    import hashlib
    import json
    dist = tmp_path / "dist"
    dist.mkdir()
    types = ["chat_zip", "chat_zip", "claude_project_zip", "claude_skills_zip", "opencode_zip"]
    artifacts = []
    for index, kind in enumerate(types):
        filename = f"runtime-{index}.zip"
        with zipfile.ZipFile(dist / filename, "w") as archive:
            archive.writestr("SKILL.md", "runtime")
        data = (dist / filename).read_bytes()
        artifacts.append({"type": kind, "file": filename,
                          "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    (dist / "DELIVERY-MANIFEST.json").write_text(json.dumps({"artifacts": artifacts}))
    errors = delivery.validate(tmp_path, dist_dir=dist)
    assert "Runtime distribution types must be exactly the canonical five, once each" in errors


def test_rejects_tampered_runtime_digest(tmp_path):
    import json
    dist = tmp_path / "dist"
    dist.mkdir()
    types = ["chat_zip", "plugin_zip", "claude_project_zip", "claude_skills_zip", "opencode_zip"]
    artifacts = []
    for index, kind in enumerate(types):
        filename = f"runtime-{index}.zip"
        with zipfile.ZipFile(dist / filename, "w") as archive:
            archive.writestr("SKILL.md", "runtime")
        artifacts.append({"type": kind, "file": filename,
                          "sha256": "0" * 64, "size": (dist / filename).stat().st_size})
    (dist / "DELIVERY-MANIFEST.json").write_text(json.dumps({"artifacts": artifacts}))
    errors = delivery.validate(tmp_path, dist_dir=dist)
    assert "SHA256 mismatch or missing digest: runtime-0.zip" in errors


def test_legacy_delivery_mode_rejected(tmp_path):
    (tmp_path / "project-status.yaml").write_text(
        "delivery_mode: zip\ngithub_allowed: false\n", encoding="utf-8"
    )
    errors = delivery.validate(tmp_path)
    assert "Legacy delivery_mode field is not allowed; use delivery.mode" in errors


def test_canonical_zip_delivery_mode_accepted(tmp_path):
    (tmp_path / "project-status.yaml").write_text(
        "delivery:\n  mode: zip\n", encoding="utf-8"
    )
    errors = delivery.validate(tmp_path)
    assert not any("delivery.mode" in error for error in errors)

def test_rejects_inherited_missing_reference_profiles(tmp_path):
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    cfg["reference_profiles"] = {"root": "profiles", "profiles": ["simple"]}
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    errors = delivery.validate(tmp_path)
    assert "Missing reference_profiles.root: profiles" in errors
    assert "Missing reference profile definition: simple" in errors


def test_project_without_reference_profiles_has_no_profile_errors(tmp_path):
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    cfg.pop("reference_profiles", None)
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    errors = delivery.validate(tmp_path)
    assert not any("reference profile" in error or "reference_profiles" in error for error in errors)
