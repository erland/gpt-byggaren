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
