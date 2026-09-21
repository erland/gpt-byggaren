from pathlib import Path
import json
import subprocess
import sys
import tempfile

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_project_for_runtime.py"
SCHEMA = json.loads(
    (ROOT / "schemas" / "existing-project-migration-result.schema.json").read_text(encoding="utf-8")
)


def write_cfg(project: Path, cfg: dict):
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def run_workflow(project: Path, *, execute: bool, target: str = "opencode"):
    args = [
        sys.executable,
        str(SCRIPT),
        "--project-root",
        str(project),
        "--target-runtime",
        target,
        "--json",
    ]
    if execute:
        args.append("--execute")
    result = subprocess.run(args, capture_output=True, text=True)
    data = json.loads(result.stdout)
    jsonschema.Draft202012Validator(SCHEMA).validate(data)
    return result, data


def ready_project(project: Path):
    canonical = project / "src" / "instructions"
    canonical.mkdir(parents=True)
    (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")
    write_cfg(project, {
        "project": {"id": "legacy"},
        "instructions": {"canonical": "src/instructions/system.md"},
        "capabilities": {"web": "optional"},
        "workflow": {"resume_from_project_zip": True},
        "resume": {
            "supported": True,
            "requires_previous_chat_history": False,
        },
    })


def test_existing_project_migration_preview_hides_low_level_flags():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        ready_project(project)

        result, data = run_workflow(project, execute=False)

        assert result.returncode == 0
        assert data["status"] == "ready_to_migrate"
        assert data["compatibility"] == "ready"
        assert data["applied"] is False
        assert data["target_runtime"] == "opencode"


def test_existing_project_migration_executes_safe_changes_and_enables_opencode():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        ready_project(project)

        result, data = run_workflow(project, execute=True)
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert result.returncode == 0
        assert data["status"] == "completed"
        assert data["compatibility"] == "ready"
        assert data["applied"] is True
        assert migrated["runtime"]["opencode"]["enabled"] is True
        assert migrated["capabilities"]["contract_version"] == 1
        assert migrated["workspace_state"]["contract_version"] == 1


def test_existing_project_migration_needs_review_for_unclassified_scripts():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        ready_project(project)
        scripts = project / "scripts"
        scripts.mkdir()
        (scripts / "domain_helper.py").write_text("print('x')\n", encoding="utf-8")

        result, data = run_workflow(project, execute=True)
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert result.returncode == 0
        assert data["status"] == "needs_review"
        assert data["compatibility"] == "reduced"
        assert data["applied"] is False
        assert any("tool" in item.lower() for item in data["required_actions"])
        assert "runtime" not in migrated or "opencode" not in migrated.get("runtime", {})


def test_existing_project_migration_blocks_unknown_project_structure():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)

        result, data = run_workflow(project, execute=True)

        assert result.returncode == 1
        assert data["status"] == "blocked"
        assert data["compatibility"] == "blocked"
        assert data["applied"] is False


def test_existing_project_migration_ux_is_registered_in_canonical_project():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    ux = cfg["existing_project_migration"]

    assert ux["natural_language_intent"] is True
    assert ux["apply_safe_changes_when_explicitly_requested"] is True
    assert ux["ask_only_for_unresolved_business_or_semantic_choices"] is True
    assert "opencode" in ux["supported_targets"]
    assert "plugin" in ux["supported_targets"]

    instruction = (ROOT / "src" / "instructions" / "system.md").read_text(encoding="utf-8")
    assert "Migrering av befintliga projekt" in instruction
    assert "Exponera inte CLI-flaggor som ett krav för användaren" in instruction



def test_existing_project_migration_can_enable_plugin():
    with tempfile.TemporaryDirectory() as td:
        project = Path(td)
        canonical = project / "src" / "instructions"
        canonical.mkdir(parents=True)
        (canonical / "system.md").write_text("# Canonical\n", encoding="utf-8")

        write_cfg(project, {
            "project": {"id": "plugin-ready"},
            "instructions": {"canonical": "src/instructions/system.md"},
            "capabilities": {
                "contract_version": 1,
                "recommendation_mode": "explicit",
                "requirements": {"web": {"level": "optional"}},
            },
            "workspace_state": {
                "contract_version": 1,
                "workspace": {
                    "requirement": "optional",
                    "persistence": "optional",
                    "portable": True,
                    "separate_from_assistant": True,
                },
                "state": {
                    "requirement": "optional",
                    "persistence": "optional",
                    "authority": "conversation",
                },
            },
            "tools": {
                "contract_version": 1,
                "tools": [],
            },
        })

        result, data = run_workflow(project, execute=True, target="plugin")
        migrated = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))

        assert result.returncode == 0
        assert data["status"] == "completed"
        assert data["compatibility"] == "ready"
        assert data["target_runtime"] == "plugin"
        assert migrated["runtime"]["plugin"]["enabled"] is True
        assert (project / "schemas" / "plugin-runtime.schema.json").exists()
        assert (project / "templates" / "README.plugin.md.tpl").exists()
