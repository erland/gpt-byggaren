"""Migration Engine assessment must never activate an unverified runtime."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("legacy_engine_assessment", ROOT / "scripts/lib/legacy_engine_assessment.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_text_gpt_needs_no_engine(tmp_path):
    result = module.inspect_engine_migration(tmp_path, {"runtime": {"plugin": {"enabled": True}}})
    assert result["engine_required"] is False
    assert result["engine_status"] == "not_indicated"
    assert result["plugin_repair_status"] == "needs_rebuild_and_host_verification"
    assert result["release_ready"] is False


def test_script_gpt_requires_review_not_invented_selftest(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "summarize.py").write_text("print('source')\n")
    result = module.inspect_engine_migration(tmp_path, {"runtime": {"openai_plugin": {"enabled": True}}})
    assert result["engine_required"] == "needs_review"
    assert result["engine_candidates"] == ["scripts/summarize.py"]
    assert result["plugin_repair_status"] == "legacy_plugin_requires_mapping"
    assert result["automatic_engine_activation"] is False


def test_declared_engine_files_still_need_executable_verification(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "worker.py").write_text("print(1)\n")
    (tmp_path / "scripts" / "selftest.py").write_text("print('ok')\n")
    cfg = {"runtime": {"plugin": {"enabled": True}}, "engine": {
        "enabled": True, "resources": ["scripts/worker.py", "scripts/selftest.py"],
        "selftest": "scripts/selftest.py"}}
    result = module.inspect_engine_migration(tmp_path, cfg)
    assert result["engine_status"] == "configured_pending_integrity_and_execution"
    assert result["engine_selftest_verified"] is False
    assert result["runtime_parity_status"] == "unverified"


def test_missing_project_contract_blocks_engine_migration(tmp_path):
    assert module.inspect_engine_migration(tmp_path, None)["engine_status"] == "blocked"


def test_copy_migration_reports_engine_without_modifying_source(tmp_path):
    import sys, subprocess, yaml
    source = tmp_path / "legacy"
    source.mkdir()
    (source / "scripts").mkdir()
    (source / "scripts" / "summarize.py").write_text("print('hello')\n")
    (source / "gpt-project.yaml").write_text(yaml.safe_dump({"project": {"id": "legacy"},
        "runtime": {"openai_plugin": {"enabled": True}}}), encoding="utf-8")
    before = (source / "gpt-project.yaml").read_bytes()
    destination = tmp_path / "migrated"
    p = subprocess.run([sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"),
         "--source", str(source), "--destination", str(destination)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    report = json.loads((destination / "MIGRATION-REPORT.json").read_text())
    assert report["engine_migration"]["engine_required"] == "needs_review"
    assert report["engine_migration"]["plugin_repair_status"] == "legacy_plugin_requires_mapping"
    assert (source / "gpt-project.yaml").read_bytes() == before


def test_opt_in_upgrade_blocks_incomplete_project_without_touching_source(tmp_path):
    import sys, subprocess, yaml
    source = tmp_path / "legacy"
    source.mkdir()
    (source / "gpt-project.yaml").write_text(
        yaml.safe_dump({"project": {"id": "legacy"}, "runtime": {"plugin": {"enabled": True}}}),
        encoding="utf-8")
    original = (source / "gpt-project.yaml").read_bytes()
    out = tmp_path / "upgraded"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"), "--source",
         str(source), "--destination", str(out), "--upgrade-build", "--version", "0.1.0"],
        text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    report = json.loads((out / "MIGRATION-REPORT.json").read_text())
    assert report["canonical_build_upgrade"]["status"] == "blocked"
    assert report["canonical_build_upgrade"]["stage"] == "canonical_engine_install"
    assert report["canonical_build_upgrade"]["release_ready"] is False
    assert (source / "gpt-project.yaml").read_bytes() == original


def test_plugin_repair_from_authoritative_canonical_instructions(tmp_path):
    import yaml, subprocess, sys, json
    project = tmp_path / "project"
    project.mkdir()
    (project / "src/instructions").mkdir(parents=True)
    (project / "src/instructions/system.md").write_text("Summarize faithfully.\n")
    cfg = {"project": {"id": "summary", "description": "Summarize Swedish texts"},
           "runtime": {"plugin": {"enabled": True}},
           "instructions": {"canonical": "src/instructions/system.md"}}
    (project / "gpt-project.yaml").write_text(yaml.safe_dump(cfg))
    spec = importlib.util.spec_from_file_location(
        "migration_copy_test", ROOT / "scripts/migrate_legacy_copy.py"
    )
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    try:
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
    finally:
        _sys.path.pop(0)
    repair = migration._plugin_repair_preflight(project)
    assert repair["status"] == "repaired_from_canonical"
    assert repair["host_verified"] is False
    migrated_cfg = yaml.safe_load((project / "gpt-project.yaml").read_text())
    assert migrated_cfg["skills"]["definitions"][0]["id"] == "summary"
    assert (project / "src/instructions/system.md").read_text() == "Summarize faithfully.\n"
    assert migration._plugin_repair_preflight(project)["status"] == "already_declared"


def test_no_automatic_plugin_repair_without_canonical_source(tmp_path):
    import yaml
    project = tmp_path / "project"
    project.mkdir()
    (project / "gpt-project.yaml").write_text(yaml.safe_dump({
        "project": {"id": "legacy"},
        "runtime": {"plugin": {"enabled": True}},
        "instructions": {"canonical": "src/instructions/missing.md"}}))
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from migrate_legacy_copy import _plugin_repair_preflight
        assert _plugin_repair_preflight(project)["status"] == "blocked"
    finally:
        sys.path.pop(0)


def test_engine_recovery_only_from_required_declared_python_and_real_selftest(tmp_path):
    import yaml, sys
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    (project / "scripts/worker.py").write_text("print('work')\n")
    cfg = {"project": {"id": "demo"}, "tools": {"tools": [
        {"id": "worker", "type": "script", "requirement": "required", "script": "scripts/worker.py"}
    ]}}
    (project / "gpt-project.yaml").write_text(yaml.safe_dump(cfg))
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from migrate_legacy_copy import _recover_declared_engine
        no_selftest = _recover_declared_engine(project)
        assert no_selftest["status"] == "review_required"
        assert "engine" not in yaml.safe_load((project / "gpt-project.yaml").read_text())
        (project / "scripts/selftest.py").write_text("print('pass')\n")
        result = _recover_declared_engine(project)
        assert result["status"] == "configured_pending_execution"
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text())
        assert migrated["engine"]["enabled"] is True
        assert "scripts/worker.py" in migrated["engine"]["resources"]
        assert _recover_declared_engine(project)["status"] == "already_declared"
    finally:
        sys.path.pop(0)


def test_project_specific_engine_is_reported_without_automatic_conversion(tmp_path):
    import json, zipfile
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "package_runtime_engine.py").write_text("print('packaging')\n")
    with zipfile.ZipFile(tmp_path / "sample-engine-1.2.1.zip", "w") as z:
        z.writestr("MANIFEST.json", json.dumps({
            "project": "sample", "version": "1.2.1",
            "files": {"scripts/export.py": "a" * 64}}))
        z.writestr("scripts/export.py", "print('export')\n")
    result = module.inspect_engine_migration(
        tmp_path, {"runtime": {"plugin": {"enabled": True}}})
    package = result["existing_engine_package"]
    assert result["engine_required"] == "needs_review"
    assert result["engine_status"] == "review_required"
    assert package["detected"] is True
    assert package["project_specific_format_detected"] is True
    assert package["comparison"] == "compare_with_generic_engine_contract"
    assert package["archives"][0]["version"] == "1.2.1"
    assert package["archives"][0]["manifest_readable"] is True
    assert package["executable_verified"] is False
    assert package["integrity_verified"] is False
    assert result["automatic_engine_activation"] is False
    assert result["release_ready"] is False


def test_canonical_engine_archive_is_recognized(tmp_path):
    import json, zipfile
    with zipfile.ZipFile(tmp_path / "demo-engine-2.0.0.zip", "w") as z:
        z.writestr("engine-package.json", json.dumps({
            "schema_version": 1, "engine_id": "demo",
            "version": "2.0.0", "entrypoint": "scripts/selftest.py", "files": {}}))
    result = module.inspect_engine_migration(tmp_path, {"runtime": {}})
    package = result["existing_engine_package"]
    assert result["engine_required"] == "needs_review"
    assert package["canonical_format_detected"] is True
    assert package["comparison"] == "review_existing_canonical_engine"
    assert package["archives"][0]["entrypoint_declared"] is True


def test_invalid_engine_archive_is_only_an_inventory_warning(tmp_path):
    (tmp_path / "broken-engine.zip").write_bytes(b"not a zip")
    result = module.inspect_engine_migration(tmp_path, {"runtime": {}})
    assert result["release_ready"] is False
    archive = result["existing_engine_package"]["archives"][0]
    assert archive["error"] == "invalid_or_unreadable_archive"
    assert archive["manifest_readable"] is False


def test_build_and_dist_archives_are_excluded_from_engine_inventory(tmp_path):
    for folder in ("build", "dist"):
        directory = tmp_path / folder
        directory.mkdir()
        (directory / "sample-engine-1.2.1.zip").write_bytes(b"ignored")
    result = module.inspect_engine_migration(tmp_path, {"runtime": {}})
    assert result["existing_engine_package"]["detected"] is False
    assert result["engine_required"] is False


def test_copy_migration_recognizes_tullverket_style_engine_without_changing_source(tmp_path):
    """End-to-end reference case: Tullverket's MANIFEST.json Engine layout."""
    import json
    import subprocess
    import sys
    import zipfile
    import yaml

    source = tmp_path / "legacy_tullverket_style"
    (source / "scripts").mkdir(parents=True)
    (source / "scripts/package_runtime_engine.py").write_text(
        "# Project-specific Engine packager, preserved as source\n", encoding="utf-8")
    (source / "scripts/render_word.py").write_text("print('docx')\n", encoding="utf-8")
    (source / "scripts/render_pdf.py").write_text("print('pdf')\n", encoding="utf-8")
    cfg = {"project": {"id": "tullverket-omvarldsanalytiker"},
           "runtime": {"plugin": {"enabled": True}}}
    (source / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg), encoding="utf-8")
    archive = source / "tullverket-omvarldsanalytiker-engine-1.2.1.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("MANIFEST.json", json.dumps({
            "project": "tullverket-omvarldsanalytiker",
            "version": "1.2.1",
            "files": {"scripts/render_word.py": "0" * 64,
                      "scripts/render_pdf.py": "0" * 64}}))
        z.writestr("scripts/render_word.py", "print('docx')\n")
        z.writestr("scripts/render_pdf.py", "print('pdf')\n")
    before_cfg = (source / "gpt-project.yaml").read_bytes()
    before_zip = archive.read_bytes()
    destination = tmp_path / "migrated"
    command = [sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"),
               "--source", str(source), "--destination", str(destination)]
    completed = subprocess.run(command, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    report = json.loads((destination / "MIGRATION-REPORT.json").read_text())
    engine = report["engine_migration"]
    finding = engine["existing_engine_package"]
    assert finding["detected"] is True
    assert finding["project_specific_format_detected"] is True
    assert finding["comparison"] == "compare_with_generic_engine_contract"
    assert finding["archives"][0]["version"] == "1.2.1"
    assert engine["automatic_engine_activation"] is False
    assert engine["release_ready"] is False
    assert (source / "gpt-project.yaml").read_bytes() == before_cfg
    assert archive.read_bytes() == before_zip
    assert (destination / "scripts/package_runtime_engine.py").is_file()
