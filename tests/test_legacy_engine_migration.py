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
