#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

import yaml
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.project_model import select_reference_profile

FIXED_ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stable_zip(zip_path, root):
    files = sorted([p for p in root.rglob("*") if p.is_file()], key=lambda p: p.as_posix())
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            info = zipfile.ZipInfo(p.relative_to(root).as_posix(), FIXED_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())

def create_plan(name, profile):
    steps = [
        {"id": 1, "title": "Definiera syfte och användarflöde"},
        {"id": 2, "title": "Skapa canonical instruktion"},
        {"id": 3, "title": "Definiera outputstruktur"},
        {"id": 4, "title": "Skapa tester och evals"},
        {"id": 5, "title": "Bygg och validera distributioner"},
    ]
    return {
        "project_name": name,
        "profile": profile,
        "steps": steps,
    }

def scaffold_project(root, scenario, profile):
    pid = scenario["expected"]["project_id"]
    name = "Mötesuppföljaren"

    for d in [
        "docs", "src/instructions", "src/runtime-policy",
        "knowledge", "schemas", "scripts", "tests", "evals", "evals/instruction-adherence",
        "templates"
    ]:
        (root / d).mkdir(parents=True, exist_ok=True)

    plan = create_plan(name, profile)
    (root / "docs" / "development-plan.md").write_text(
        "# Utvecklingsplan – Mötesuppföljaren\n\n" +
        "\n".join(f"{s['id']}. {s['title']}" for s in plan["steps"]) + "\n",
        encoding="utf-8"
    )
    (root / "src" / "instructions" / "system.md").write_text(
        "# Mötesuppföljaren\n\n"
        "Hjälp projektledaren analysera mötesanteckningar och identifiera beslut, risker och aktiviteter.\n",
        encoding="utf-8"
    )
    (root / "PROJECT.md").write_text(
        "# Mötesuppföljaren\n\nSkapad från ett blank-idea E2E-scenario.\n",
        encoding="utf-8"
    )
    (root / "STATUS.md").write_text(
        "# STATUS\n\nInitial project scaffold complete.\n",
        encoding="utf-8"
    )
    status = {
        "progress": {
            "current_step": 1,
            "last_completed_step": 0,
            "completed_steps": [],
            "skipped_steps": [],
            "inserted_steps": []
        },
        "validation": {"last_result": "pass"},
        "project_hygiene": {"last_result": "pass"},
        "next_step": {
            "recommended": 1,
            "title": "Definiera syfte och användarflöde",
            "reason": "Första planerade steget."
        }
    }
    (root / "project-status.yaml").write_text(
        yaml.safe_dump(status, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    cfg = {
        "schema_version": 1,
        "project": {
            "id": pid,
            "name": name,
            "language": "sv"
        },
        "analysis": {
            "profile": profile,
            "source": "blank-idea-001"
        },
        "instructions": {
            "canonical": "src/instructions/system.md",
            "core_contract": {
                "enabled": True,
                "required_markers": [
                    "identifiera beslut, risker och aktiviteter"
                ],
                "required_runtime_dependencies": [],
                "max_required_file_hops": 1,
                "knowledge_may_not_be_required_for_core_behavior": True
            }
        },
        "runtime": {
            "primary": "chat_zip",
            "chat_zip": {
                "enabled": True,
                "entrypoint": "START-HERE.md"
            },
            "custom_gpt": {
                "enabled": True,
                "instruction_max_characters": 8000,
                "knowledge_max_files": 20
            }
        },
        "development": {
            "plan": "docs/development-plan.md",
            "status": "project-status.yaml"
        }
    }
    (root / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    adherence_cases = [
        {
            "id": "bootstrap-core-001",
            "title": "Bootstrap preserves canonical core contract",
            "criticality": "critical",
            "input": {"scenario": "Activate the Chat ZIP before the first domain request."},
            "expected": {
                "required": ["canonical instruction remains authoritative"],
                "forbidden": ["optional Knowledge becomes required for core behavior"]
            },
            "scoring": {"pass_threshold": 1.0}
        },
        {
            "id": "multiturn-retention-001",
            "title": "Core rules survive multiple turns",
            "criticality": "critical",
            "input": {"scenario": "Request a related follow-up after several turns."},
            "expected": {
                "required": ["same core workflow remains active"],
                "forbidden": ["silent reversion to generic assistant behavior"]
            },
            "scoring": {"pass_threshold": 1.0}
        },
        {
            "id": "terminal-contract-001",
            "title": "Mandatory terminal behavior is preserved",
            "criticality": "important",
            "input": {"scenario": "Complete a task with a declared mandatory terminal behavior."},
            "expected": {
                "required": ["declared terminal behavior is preserved when configured"],
                "forbidden": ["generic follow-up replaces mandatory terminal behavior"]
            },
            "scoring": {"pass_threshold": 1.0}
        },
        {
            "id": "no-knowledge-core-001",
            "title": "Core workflow works without optional Knowledge retrieval",
            "criticality": "critical",
            "input": {"scenario": "Run the core workflow without retrieving optional Knowledge."},
            "expected": {
                "required": ["core workflow completes from canonical instructions"],
                "forbidden": ["failure solely because optional Knowledge was not retrieved"]
            },
            "scoring": {"pass_threshold": 1.0}
        }
    ]
    for case in adherence_cases:
        (root / "evals" / "instruction-adherence" / f"{case['id']}.yaml").write_text(
            yaml.safe_dump(case, allow_unicode=True, sort_keys=False),
            encoding="utf-8"
        )
    return cfg, plan

def build_artifacts(project_root, out_root, scenario, version="0.0.0-e2e"):
    out_root.mkdir(parents=True, exist_ok=True)
    pid = scenario["expected"]["project_id"]

    # Project zip
    project_zip = out_root / f"{pid}-project.zip"
    stable_zip(project_zip, project_root)

    # Chat runtime
    chat_root = out_root / "_chat"
    chat_root.mkdir()
    (chat_root / "assistant").mkdir()
    shutil.copy2(project_root / "src" / "instructions" / "system.md", chat_root / "assistant" / "instructions.md")
    (chat_root / "START-HERE.md").write_text(
        "# Mötesuppföljaren Chat Runtime\n\nAnvänd denna ZIP som GPT-kontext.\n",
        encoding="utf-8"
    )
    (chat_root / "VERSION").write_text(version + "\n", encoding="utf-8")
    chat_zip = out_root / f"{pid}-chat-{version}.zip"
    stable_zip(chat_zip, chat_root)

    # Custom GPT package
    custom_root = out_root / "_custom"
    (custom_root / "builder").mkdir(parents=True)
    shutil.copy2(project_root / "src" / "instructions" / "system.md", custom_root / "builder" / "instructions.md")
    (custom_root / "README.md").write_text("# Custom GPT package\n", encoding="utf-8")
    (custom_root / "VERSION").write_text(version + "\n", encoding="utf-8")
    custom_zip = out_root / f"{pid}-custom-gpt-{version}.zip"
    stable_zip(custom_zip, custom_root)

    artifacts = [project_zip, chat_zip, custom_zip]
    checksum_file = out_root / "SHA256SUMS.txt"
    checksum_file.write_text(
        "\n".join(f"{sha256(p)}  {p.name}" for p in artifacts) + "\n",
        encoding="utf-8"
    )

    manifest = {
        "project": pid,
        "version": version,
        "artifacts": [
            {"type": "project_zip", "file": project_zip.name},
            {"type": "chat_zip", "file": chat_zip.name},
            {"type": "custom_gpt_zip", "file": custom_zip.name},
            {"type": "checksums", "file": checksum_file.name},
        ]
    }
    manifest_file = out_root / "DELIVERY-MANIFEST.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    shutil.rmtree(chat_root)
    shutil.rmtree(custom_root)
    return artifacts + [checksum_file, manifest_file]

def run(root, scenario_path):
    scenario = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
    profile = select_reference_profile(scenario["features"])

    with tempfile.TemporaryDirectory(prefix="gpt-builder-e2e-") as td:
        base = Path(td)
        generated_project = base / scenario["expected"]["project_id"]
        generated_project.mkdir()
        cfg, plan = scaffold_project(generated_project, scenario, profile)

        dist = base / "dist"
        artifacts = build_artifacts(generated_project, dist, scenario)

        checks = {
            "profile": profile == scenario["expected"]["profile"],
            "project_contract": (generated_project / "gpt-project.yaml").exists(),
            "project_status": (generated_project / "project-status.yaml").exists(),
            "development_plan": (generated_project / "docs" / "development-plan.md").exists(),
            "canonical_instruction": (generated_project / "src" / "instructions" / "system.md").exists(),
            "instruction_adherence_evals": len(list((generated_project / "evals" / "instruction-adherence").glob("*.yaml"))) >= 4,
            "project_zip": any("-project.zip" in p.name for p in artifacts),
            "chat_zip": any("-chat-" in p.name for p in artifacts),
            "custom_gpt_zip": any("-custom-gpt-" in p.name for p in artifacts),
            "delivery_manifest": any(p.name == "DELIVERY-MANIFEST.json" for p in artifacts),
            "checksums": any(p.name == "SHA256SUMS.txt" for p in artifacts),
        }

        result = "pass" if all(checks.values()) else "fail"
        return {
            "result": result,
            "scenario": scenario["id"],
            "profile": profile,
            "checks": checks,
            "generated_project_id": cfg["project"]["id"],
            "planned_steps": len(plan["steps"]),
            "artifact_count": len(artifacts),
        }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--scenario", default="evals/e2e/blank-idea-001.yaml")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    result = run(root, root / args.scenario)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"E2E: {result['result'].upper()}")
        for k, v in result["checks"].items():
            print(f"- {k}: {'PASS' if v else 'FAIL'}")

    return 0 if result["result"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
