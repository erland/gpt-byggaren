#!/usr/bin/env python3
"""Validate explicit host acceptance evidence; never infer host execution from ZIP builds."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGETS = ("plugin", "claude", "opencode", "chat_zip")
SCENARIOS = ("skill_discovery", "skill_activation", "reference_access", "script_execution", "fallback")


def validate(payload: dict) -> dict:
    problems = []
    if payload.get("schema_version") != 1:
        problems.append("Unsupported schema_version")
    actual = payload.get("targets")
    if not isinstance(actual, dict):
        actual = {}
        problems.append("targets must be an object")
    summary = {}
    for target in TARGETS:
        entry = actual.get(target)
        if not isinstance(entry, dict):
            problems.append(f"{target}: missing target record")
            continue
        results = entry.get("scenarios")
        if not isinstance(results, dict):
            problems.append(f"{target}: missing scenarios")
            continue
        summary[target] = {}
        for scenario in SCENARIOS:
            evidence = results.get(scenario)
            if not isinstance(evidence, dict):
                problems.append(f"{target}/{scenario}: missing evidence")
                continue
            status = evidence.get("status")
            if status not in ("passed", "failed", "blocked", "not_tested", "not_applicable"):
                problems.append(f"{target}/{scenario}: invalid status")
                continue
            note = evidence.get("note")
            if not isinstance(note, str) or not note.strip():
                problems.append(f"{target}/{scenario}: explanation required")
            if status == "passed":
                if evidence.get("kind") != "host_observation":
                    problems.append(f"{target}/{scenario}: passed needs host_observation")
                if not isinstance(evidence.get("artifact"), str) or not evidence["artifact"].strip():
                    problems.append(f"{target}/{scenario}: passed needs evidence artifact reference")
            summary[target][scenario] = status
    host_ready = not problems and all(
        summary.get(t, {}).get(s) in ("passed", "not_applicable")
        for t in TARGETS for s in SCENARIOS
    )
    return {
        "result": "accepted" if not problems else "rejected",
        "errors": problems,
        "host_acceptance_verified": host_ready,
        "release_ready": False,
        "results": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    try:
        report = validate(json.loads(Path(args.evidence).read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Evidence unreadable: {exc}\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["errors"] or not report["host_acceptance_verified"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
