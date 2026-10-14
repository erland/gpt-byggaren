"""Regression checks for generically generated (non-Builder) runtime adapters."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("runtime_builder", ROOT / "scripts" / "build_distributions.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_opencode_book_tool_signatures():
    cases = {
        "book-build": ["--output-dir"],
        "book-export": ["--format", "--output-dir"],
        "project-integrity": ["verify", "projectRoot"],
        "project-validation": ["projectRoot"],
        "distribution-build": ["--version"],
        "distribution-validation": ["python3", "script"],
    }
    for kind, expected in cases.items():
        src = MOD._opencode_tool_wrapper({"id": kind, "purpose": "Test"}, "scripts/test.py")
        assert '"--project-root"' not in src, kind
        assert "cwd: projectRoot" in src, kind
        assert all(value in src for value in expected), kind


def test_plugin_does_not_copy_unrelated_builder_helpers(tmp_path):
    root = tmp_path / "generated-book-project"
    folder = root / "scripts"
    lib = folder / "lib"
    lib.mkdir(parents=True)
    (folder / "task.py").write_text("from lib.needed import helper\nhelper()\n", encoding="utf-8")
    (lib / "__init__.py").write_text("", encoding="utf-8")
    (lib / "needed.py").write_text("def helper(): return True\n", encoding="utf-8")
    (lib / "unrelated_builder.py").write_text("def heavy(): return False\n", encoding="utf-8")
    template = root / "templates" / "project"
    template.mkdir(parents=True)
    (template / "book.yaml").write_text("title: Example\n", encoding="utf-8")
    out = tmp_path / "compiled" / "skills" / "book"
    MOD._copy_skill_resources(root, out, {"scripts": ["scripts/task.py"], "references": [], "assets": ["templates/project"]})
    assert (out / "assets" / "project" / "book.yaml").read_text(encoding="utf-8") == "title: Example\n"
    assert (out / "scripts" / "task.py").exists()
    assert (out / "scripts" / "lib" / "needed.py").exists()
    assert not (out / "scripts" / "lib" / "unrelated_builder.py").exists()
