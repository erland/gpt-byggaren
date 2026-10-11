"""Regression checks for canonical new-project workflow policy and runtime packaging."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_choice_is_persistent_and_zip_has_no_github_requirement():
    policy = (ROOT / "docs/skills/project-workflow-operations.md").read_text(encoding="utf-8")
    system = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    assert "delivery.mode: zip" in policy
    assert "delivery.mode: github" in policy
    assert "Föreslå inte GitHub igen" in policy
    assert "GitHub Actions" in system
    assert "ZIP är fullvärdigt" in system


def test_all_five_runtimes_from_first_build_and_no_custom_gpt():
    policy = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    operations = (ROOT / "docs/skills/project-workflow-operations.md").read_text(encoding="utf-8")
    for runtime in ("chat", "plugin", "claude_project", "claude_skills", "opencode"):
        assert runtime in policy
    assert "innan första" in operations
    assert "custom_gpt" in operations
    assert "enabled: false" in operations


def test_gitignore_is_project_only_not_runtime_root():
    operations = (ROOT / "docs/skills/project-workflow-operations.md").read_text(encoding="utf-8")
    assert "runtime-ZIP:arnas rot saknar" in operations
    assert "distribution-engine/" in operations
