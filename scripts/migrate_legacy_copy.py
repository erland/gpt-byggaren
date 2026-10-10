#!/usr/bin/env python3
"""Safely migrate a legacy project into a separate destination.

Accepts a project directory or ZIP. Never changes the input. Missing canonical
project files produce a review report rather than invented project metadata.
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import zipfile

import yaml
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


def retire_custom_gpt(project: Path) -> dict:
    """Retire only active Builder targets; preserve legacy configuration."""
    path = project / "gpt-project.yaml"
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        return {"result": "blocked", "reason": "Invalid project contract"}
    original = copy.deepcopy(cfg)
    runtime = cfg.get("runtime")
    previous_enabled = False
    if isinstance(runtime, dict) and isinstance(runtime.get("custom_gpt"), dict):
        previous_enabled = runtime["custom_gpt"].get("enabled") is True
        runtime["custom_gpt"]["enabled"] = False
    build = cfg.get("build")
    if isinstance(build, dict) and build.get("build_custom_gpt_zip") is True:
        build["build_custom_gpt_zip"] = False
    build_system = cfg.get("build_system")
    if isinstance(build_system, dict):
        if isinstance(build_system.get("targets"), list):
            build_system["targets"] = [t for t in build_system["targets"] if t != "custom-gpt"]
        if isinstance(build_system.get("runtime_targets"), dict):
            build_system["runtime_targets"].pop("custom-gpt", None)
    parity = cfg.get("runtime_parity")
    if isinstance(parity, dict) and isinstance(parity.get("registered_runtimes"), list):
        parity["registered_runtimes"] = [r for r in parity["registered_runtimes"] if r != "chatgpt_custom"]
    for section, key in (("direct_build", "deliver"), ("release", "artifacts")):
        obj = cfg.get(section)
        if section == "release" and isinstance(obj, dict):
            obj = obj.get("github")
        if isinstance(obj, dict) and isinstance(obj.get(key), list):
            obj[key] = [t for t in obj[key] if t != "custom_gpt_zip_when_enabled"]
    if cfg != original:
        path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {
        "result": "changed" if cfg != original else "no_changes",
        "previously_enabled": previous_enabled,
        "legacy_configuration_preserved": True,
        "automatic_plugin_conversion": False,
    }


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
        retired = retire_custom_gpt(project)
        report["custom_gpt_retirement"] = retired
        report["apply"] = {"result": "changed" if changed or retired["result"] == "changed" else "no_changes"}
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
