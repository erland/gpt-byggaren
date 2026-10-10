#!/usr/bin/env python3
"""Recover a review-only Plugin SKILL candidate from canonical instructions.

Never mutate the legacy entrypoint or activate a distribution.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml


def recover(root: Path) -> dict:
    root = root.resolve()
    cfg = yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))
    legacy = (cfg.get("runtime") or {}).get("openai_plugin")
    if not isinstance(legacy, dict):
        raise ValueError("No legacy openai_plugin contract")
    entry = legacy.get("entrypoint")
    if not isinstance(entry, str) or not entry.strip():
        raise ValueError("Missing legacy entrypoint")
    relative = Path(entry)
    if relative.is_absolute() or ".." in relative.parts or relative.name != "SKILL.md":
        raise ValueError("Unsafe or unsupported skill entrypoint")
    if (root / relative).exists():
        raise ValueError("Legacy skill already exists: do not replace it")
    instruction = (cfg.get("instructions") or {}).get("canonical")
    if not isinstance(instruction, str):
        raise ValueError("Missing canonical instruction reference")
    source_ref = Path(instruction)
    if source_ref.is_absolute() or ".." in source_ref.parts:
        raise ValueError("Unsafe canonical instruction path")
    source = (root / source_ref).resolve()
    if not source.is_relative_to(root) or not source.is_file():
        raise ValueError("Canonical instruction not available")
    original = source.read_bytes()
    if not original.strip():
        raise ValueError("Canonical instruction empty")
    try:
        text = original.decode("utf-8")
    except UnicodeError as exc:
        raise ValueError("Canonical instruction must be valid UTF-8") from exc
    name = relative.parent.name
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise ValueError("Skill name is not valid")
    output = root / "reconstructed-canonical" / "plugin-skill-candidate"
    target = output / "skills" / name / "SKILL.md"
    evidence = output / "RECOVERY.json"
    if target.exists() or evidence.exists():
        raise FileExistsError("Candidate already exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "---\nname: " + name + "\ndescription: Granskningsutkast återställt från canonical instruktioner\n---\n\n"
        "# Återställda instruktioner\n\n" + text + ("\n" if not text.endswith("\n") else ""),
        encoding="utf-8",
    )
    report = {
        "status": "review_required",
        "candidate": target.relative_to(root).as_posix(),
        "source": source_ref.as_posix(),
        "source_sha256": hashlib.sha256(original).hexdigest(),
        "original_bytes_preserved_in_canonical_source": True,
        "original_entrypoint_created": False,
        "plugin_activated": False,
        "release_ready": False,
        "review_needed": ["Check adapted instruction semantics", "Map Knowledge and required host tools",
                          "Run real Plugin builder and mobile import test"],
    }
    evidence.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        result = recover(Path(args.project_root))
    except (ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"Plugin recovery blocked: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
