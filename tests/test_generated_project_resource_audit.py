"""Parity gate: the same declared-resource checks apply before Chat/Plugin builds."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "project_resource_audit", ROOT / "scripts/lib/project_resource_audit.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_missing_test_manifest_and_model_paths_are_blocking(tmp_path):
    cfg = {
        "testing": {"manifest": "test-manifest.yaml", "model": "docs/test-model.md"},
        "linting": {"script": "scripts/lint_gpt_project.py"},
        "model_robustness": {"model_compatibility": {
            "documentation": "docs/model-compatibility.md"
        }},
    }
    findings = audit.validate_project_resources(tmp_path, cfg)
    assert len(findings) == 4
    assert any("test-manifest.yaml" in f for f in findings)
    assert any("docs/model-compatibility.md" in f for f in findings)
    assert any("scripts/lint_gpt_project.py" in f for f in findings)


def test_complete_resources_pass_without_placeholder_generation(tmp_path):
    for name in ("test-manifest.yaml", "docs/test-model.md",
                 "scripts/lint_gpt_project.py", "docs/model-compatibility.md"):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("real declared resource")
    cfg = {"testing": {"manifest": "test-manifest.yaml", "model": "docs/test-model.md"},
           "linting": {"script": "scripts/lint_gpt_project.py"},
           "model_robustness": {"model_compatibility": {
               "documentation": "docs/model-compatibility.md"}}}
    assert audit.validate_project_resources(tmp_path, cfg) == []


def test_text_only_project_without_verification_paths_not_penalized(tmp_path):
    assert audit.validate_project_resources(tmp_path, {"project": {"id": "text-only"}}) == []


def test_path_traversal_rejected(tmp_path):
    assert "unsafe path" in audit.validate_project_resources(
        tmp_path, {"testing": {"manifest": "../outside.yaml"}}
    )[0]
