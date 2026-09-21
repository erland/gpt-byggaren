from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_legacy_project.py"
REPORT_SCHEMA = json.loads((ROOT / "schemas" / "legacy-migration-report.schema.json").read_text(encoding="utf-8"))


def run_migration(project: Path, *args: str):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(project), "--json", *args],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    jsonschema.Draft202012Validator(REPORT_SCHEMA).validate(report)
    return report


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
        assert "tools" not in report["changes"]
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


def test_apply_does_not_overwrite_unknown_capabilities_or_domain_artifacts():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        original_caps = {
            "web": "required",
            "special_runtime_capability": "required",
        }
        original_artifacts = {
            "project_zip": {"required": True},
            "domain_model": {"required": True},
        }
        write_cfg(project, {
            "project": {"id": "uncertain"},
            "capabilities": original_caps,
            "artifacts": original_artifacts,
            "workflow": {"resume_from_project_zip": True},
        })

        report = run_migration(project, "--apply")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert report["migration"]["status"] == "ready_with_manual_review"
        assert migrated["capabilities"] == original_caps
        assert migrated["artifacts"] == original_artifacts
        assert migrated["workspace_state"]["contract_version"] == 1


def test_opencode_ready_project_can_be_enabled_and_receives_adapter_assets():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "ready"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {"web": "optional"},
            "workflow": {"resume_from_project_zip": True},
            "resume": {
                "supported": True,
                "requires_previous_chat_history": False,
            },
        })

        preview = run_migration(project)
        assert preview["opencode"]["status"] == "ready"
        assert preview["opencode"]["can_enable_automatically"] is True

        applied = run_migration(project, "--apply", "--enable-opencode")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert applied["apply"]["result"] == "changed"
        assert migrated["runtime"]["opencode"]["enabled"] is True
        assert migrated["runtime"]["opencode"]["layout"]["instructions"] == "AGENTS.md"
        assert (project / "schemas" / "opencode-runtime.schema.json").exists()
        assert (project / "src" / "runtime-policy" / "opencode-runtime-policy.md").exists()
        assert (project / "docs" / "opencode-runtime.md").exists()
        assert (project / "templates" / "README.opencode.md.tpl").exists()


def test_opencode_is_reduced_and_enablement_blocked_when_scripts_need_tool_review():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")
        scripts = project / "scripts"
        scripts.mkdir()
        (scripts / "domain_helper.py").write_text("print('x')\n", encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "scripted"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {"web": "optional"},
            "workflow": {"resume_from_project_zip": True},
            "resume": {
                "supported": True,
                "requires_previous_chat_history": False,
            },
        })

        preview = run_migration(project)
        assert preview["opencode"]["status"] == "reduced"
        assert preview["opencode"]["can_enable_automatically"] is False
        assert any("tool inventory" in reason.lower() for reason in preview["opencode"]["reasons"])

        applied = run_migration(project, "--apply", "--enable-opencode")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert applied["apply"]["result"] == "blocked"
        assert "runtime" not in migrated or "opencode" not in migrated.get("runtime", {})


def test_opencode_is_blocked_without_resolved_canonical_instruction():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        write_cfg(project, {
            "project": {"id": "blocked"},
            "capabilities": {"web": "optional"},
        })

        report = run_migration(project)

        assert report["opencode"]["status"] == "blocked"
        assert report["opencode"]["can_enable_automatically"] is False
        assert any("canonical instruction" in reason.lower() for reason in report["opencode"]["reasons"])


def test_opencode_can_be_enabled_on_already_migrated_project_without_other_changes():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "modern"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {
                "contract_version": 1,
                "recommendation_mode": "explicit",
                "requirements": {"web": {"level": "optional"}},
            },
            "artifacts": {
                "contract_version": 1,
                "outputs": {
                    "runtime_package": {
                        "kind": "distribution",
                        "format": "zip",
                        "requirement": "optional",
                        "persistence": "persistent",
                    }
                },
            },
            "workspace_state": {
                "contract_version": 1,
                "workspace": {
                    "requirement": "required",
                    "persistence": "required",
                    "portable": True,
                    "separate_from_assistant": True,
                },
                "state": {
                    "requirement": "optional",
                    "persistence": "preferred",
                    "authority": "workspace_file",
                    "format": "yaml",
                    "path": "project-status.yaml",
                },
            },
            "tools": {
                "contract_version": 1,
                "tools": [],
            },
            "runtime_parity": {
                "reference": {"type": "canonical_contract"},
                "registered_runtimes": ["chatgpt_chat"],
            },
        })

        report = run_migration(project, "--apply", "--enable-opencode")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert report["apply"]["result"] == "changed"
        assert migrated["runtime"]["opencode"]["enabled"] is True



def test_plugin_ready_project_can_be_enabled_and_receives_adapter_assets():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        original = "# Canonical behavior\nDo not rewrite me.\n"
        (canonical / "system.md").write_text(original, encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "ready-plugin", "name": "Ready Plugin", "description": "A portable assistant."},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {"web": "optional"},
        })

        preview = run_migration(project)
        assert preview["plugin"]["status"] == "ready"
        assert preview["plugin"]["can_enable_automatically"] is True

        applied = run_migration(project, "--apply", "--enable-plugin")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert applied["apply"]["result"] == "changed"
        assert migrated["runtime"]["plugin"]["enabled"] is True
        assert migrated["runtime"]["plugin"]["mode"] == "openai_plugin"
        assert (project / "schemas" / "plugin-runtime.schema.json").exists()
        assert (project / "schemas" / "skill-contract.schema.json").exists()
        assert (project / "src" / "runtime-policy" / "plugin-runtime-policy.md").exists()
        assert (project / "docs" / "plugin-runtime.md").exists()
        assert (project / "templates" / "README.plugin.md.tpl").exists()
        assert (canonical / "system.md").read_text(encoding="utf-8") == original


def test_plugin_enablement_is_reduced_when_required_tools_need_execution():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "tool-plugin"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "tools": {
                "contract_version": 1,
                "tools": [{
                    "id": "required-script",
                    "type": "script",
                    "requirement": "required",
                    "script": "scripts/run.py",
                }],
            },
        })

        preview = run_migration(project)
        assert preview["plugin"]["status"] == "reduced"
        assert preview["plugin"]["can_enable_automatically"] is False

        applied = run_migration(project, "--apply", "--enable-plugin")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))
        assert applied["apply"]["result"] == "blocked"
        assert "runtime" not in migrated or "plugin" not in migrated.get("runtime", {})
