#!/usr/bin/env python3
"""Safely migrate a legacy project into a separate destination.

Accepts a project directory or ZIP. Never changes the input. Missing canonical
project files produce a review report rather than invented project metadata.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path

from migrate_legacy_project import apply_changes, build_report, load_cfg

SKIP = {".git", "build", "dist", "__pycache__", ".pytest_cache"}


def _assert_separate(source: Path, destination: Path) -> None:
    source = source.resolve()
    destination = destination.resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Destination must be separate from the source tree")
    if destination.exists():
        raise FileExistsError(f"Destination already exists: {destination}")


def _safe_unpack(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        entries = zf.infolist()
        if len(entries) > 5000:
            raise ValueError("Archive has too many entries")
        for entry in entries:
            name = entry.filename.replace("\\", "/")
            parts = Path(name).parts
            if not parts or name.startswith("/") or ".." in parts or ":" in parts[0]:
                raise ValueError(f"Unsafe archive entry: {name}")
            # Reject symbolic links.
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"Archive contains symlink: {name}")
            if entry.file_size > 100 * 1024 * 1024:
                raise ValueError(f"Archive member too large: {name}")
            target = destination.joinpath(*parts)
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError(f"Unsafe archive destination: {name}")
        for entry in entries:
            name = entry.filename.replace("\\", "/")
            parts = Path(name).parts
            if any(p in SKIP for p in parts):
                continue
            target = destination.joinpath(*parts)
            if entry.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(entry) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)


def _project_root(dest: Path) -> Path:
    if (dest / "gpt-project.yaml").exists():
        return dest
    candidates = list(dest.rglob("gpt-project.yaml"))
    if len(candidates) == 1:
        return candidates[0].parent
    return dest


def migrate(source: Path, destination: Path) -> dict:
    source, destination = source.resolve(), destination.resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    if source.is_dir():
        _assert_separate(source, destination)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns(*SKIP))
    elif source.is_file() and zipfile.is_zipfile(source):
        if destination.exists():
            raise FileExistsError(destination)
        destination.mkdir(parents=True)
        try:
            _safe_unpack(source, destination)
        except Exception:
            shutil.rmtree(destination)
            raise
    else:
        raise ValueError("Source must be a directory or ZIP archive")

    project = _project_root(destination)
    cfg = load_cfg(project)
    report = build_report(project, cfg)
    report["safe_copy"] = {
        "source_type": "zip" if source.is_file() else "directory",
        "source_unchanged": True,
        "project_root": project.relative_to(destination).as_posix(),
        "destination": str(destination),
    }
    if cfg is None:
        report["apply"] = {"result": "blocked", "reason": "No gpt-project.yaml; reconstruction requires review"}
    else:
        changed = apply_changes(project, cfg, report)
        report["apply"] = {"result": "changed" if changed else "no_changes"}
    (destination / "MIGRATION-REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate a legacy GPT project without modifying the source")
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args()
    try:
        report = migrate(Path(args.source), Path(args.destination))
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
