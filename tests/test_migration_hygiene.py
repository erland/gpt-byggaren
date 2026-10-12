"""Migrationssteg, dokumentationshygien och skydd mot automatisk radering."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("migration_hygiene", ROOT / "scripts/lib/migration_hygiene.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_missing_docs_and_legacy_validators_are_detected_without_delete(tmp_path):
    (tmp_path / "scripts").mkdir()
    old = tmp_path / "scripts/validate_workflow_parity.py"
    old.write_text("print('legacy')\n")
    report = module.assess_hygiene(tmp_path)
    assert "README.md" in report["missing_documents"]
    assert "scripts/validate_workflow_parity.py" in report["legacy_validator_candidates"]
    assert old.is_file()
    assert report["files_deleted"] == []


def test_existing_docs_versions_and_ci_identifiers_are_flagged(tmp_path):
    (tmp_path / "README.md").write_text("Built with GPT Byggaren v1.5.0\n")
    (tmp_path / "PROJECT.md").write_text("Project\n")
    (tmp_path / "STATUS.md").write_text("CI #130 passed\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/development-plan.md").write_text("Development\n")
    report = module.assess_hygiene(tmp_path, engine_version="1.6.13")
    assert report["possible_stale_versions"][0]["file"] == "README.md"
    assert report["ci_references_to_reconcile"] == ["STATUS.md"]


def test_stepwise_report_marks_build_and_hygiene_separately():
    report = {"generic_discovery": {"status": "complete"}, "apply": {"result": "changed"},
              "canonical_build_upgrade": {"status": "built_pending_host_acceptance", "release_ready": False},
              "project_hygiene": {"status": "review_required"}}
    steps = module.migration_steps(report)
    assert steps[2]["status"] == "completed"
    assert steps[4]["status"] == "review_required"
    assert steps[5]["status"] == "pending"


def test_migration_copy_reports_next_step_without_changing_source(tmp_path):
    source = tmp_path / "old"
    source.mkdir()
    (source / "gpt-project.yaml").write_text(yaml.safe_dump({"project": {"id": "example"}}))
    original = (source / "gpt-project.yaml").read_bytes()
    destination = tmp_path / "new"
    result = subprocess.run([sys.executable, str(ROOT / "scripts/migrate_legacy_copy.py"),
                             "--source", str(source), "--destination", str(destination)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads((destination / "MIGRATION-REPORT.json").read_text())
    assert len(report["migration_steps"]) == 6
    assert report["next_step"]["id"] in {row["id"] for row in report["migration_steps"]}
    assert (source / "gpt-project.yaml").read_bytes() == original
