from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_legacy_project.py"


def run_migration(project: Path, *args: str):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(project), "--json", *args],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def write_cfg(project: Path, cfg: dict):
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def test_legacy_project_reports_warning_for_file_handling_and_does_not_promote_scripts():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        (project / "scripts").mkdir()
        (project / "scripts" / "helper.py").write_text("print('x')\n", encoding="utf-8")
        write_cfg(project, {
            "project": {"id": "legacy"},
            "capabilities": {
                "web": "required",
                "file_handling": "recommended",
            },
            "workflow": {
                "resume_from_project_zip": True,
            },
            "resume": {
                "supported": True,
                "requires_previous_chat_history": False,
            },
        })

        report = run_migration(project)

        assert report["migration"]["source_class"] == "L1"
        assert report["migration"]["status"] == "ready_with_manual_review"
        assert report["changes"]["capabilities"]["requirements"]["web"]["level"] == "required"
        assert report["changes"]["capabilities"]["requirements"]["filesystem"] == {
            "read": "recommended",
            "write": "recommended",
        }
        assert report["changes"]["workspace_state"]["state"]["authority"] == "workspace_file"
        assert report["changes"]["tools"] == {"contract_version": 1, "tools": []}
        tool_decisions = [d for d in report["decisions"] if d["area"] == "tools"]
        assert any(d["confidence"] == "manual_review" for d in tool_decisions)
        assert any("scripts/helper.py" in d.get("evidence", []) for d in tool_decisions)


def test_apply_adds_only_missing_contracts_and_preserves_domain_content():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        original = "# Domain behavior\nNever rewrite me.\n"
        (canonical / "system.md").write_text(original, encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "legacy"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {"web": "required"},
            "artifacts": {
                "project_zip": {"required": True},
                "chat_zip": {"required": True},
            },
            "workflow": {
                "resume_from_project_zip": True,
            },
            "resume": {
                "supported": True,
                "requires_previous_chat_history": False,
            },
        })

        report = run_migration(project, "--apply")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert report["apply"]["result"] == "changed"
        assert migrated["capabilities"]["contract_version"] == 1
        assert migrated["artifacts"]["contract_version"] == 1
        assert migrated["workspace_state"]["contract_version"] == 1
        assert migrated["tools"] == {
            "contract_version": 1,
            "tools": [],
            "schema": "schemas/tool-contract.schema.json",
        }
        assert (canonical / "system.md").read_text(encoding="utf-8") == original


def test_partial_migration_preserves_existing_new_contract():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        capabilities = {
            "contract_version": 1,
            "schema": "schemas/capability-contract.schema.json",
            "recommendation_mode": "explicit",
            "requirements": {"web": {"level": "optional"}},
        }
        write_cfg(project, {
            "project": {"id": "partial"},
            "capabilities": capabilities,
            "workflow": {"resume_from_project_zip": True},
        })

        report = run_migration(project, "--apply")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert report["migration"]["source_class"] == "L2"
        assert migrated["capabilities"] == capabilities
        assert migrated["workspace_state"]["contract_version"] == 1


def test_second_apply_is_idempotent():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        write_cfg(project, {
            "project": {"id": "legacy"},
            "capabilities": {"web": "required"},
            "workflow": {"resume_from_project_zip": True},
        })

        first = run_migration(project, "--apply")
        second = run_migration(project, "--apply")

        assert first["apply"]["result"] == "changed"
        assert second["apply"]["result"] == "no_changes"


def test_missing_project_contract_is_l0_and_apply_is_blocked():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        report = run_migration(project, "--apply")

        assert report["migration"]["source_class"] == "L0"
        assert report["migration"]["status"] == "manual_review"
        assert report["apply"]["result"] == "blocked"
        assert not (project / "gpt-project.yaml").exists()
