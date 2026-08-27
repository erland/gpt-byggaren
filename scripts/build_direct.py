#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and validate all direct-download GPT artifacts without GitHub."
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--version", default="0.0.0-dev")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    python = sys.executable

    run([
        python,
        str(root / "scripts" / "build_distributions.py"),
        "--project-root", str(root),
        "--version", args.version,
        "--targets", "project,chat,custom-gpt",
    ])

    run([
        python,
        str(root / "scripts" / "validate_distributions.py"),
        "--project-root", str(root),
    ])

    run([
        python,
        str(root / "scripts" / "assess_release_readiness.py"),
        "--project-root", str(root),
        "--include-build-state",
    ])

    manifest_path = root / "dist" / "DELIVERY-MANIFEST.json"
    if not manifest_path.exists():
        raise SystemExit("Delivery manifest was not created")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    print("DIRECT BUILD: PASS")
    print(f"Project: {manifest['project_name']}")
    print(f"Version: {manifest['version']}")
    print("Artifacts:")
    for artifact in manifest["artifacts"]:
        print(f"- {artifact['type']}: {artifact['file']}")
    print("- delivery_manifest: DELIVERY-MANIFEST.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
