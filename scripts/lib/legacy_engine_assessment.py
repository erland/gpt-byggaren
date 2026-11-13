"""Evidence-based Engine and Plugin recovery assessment for legacy GPT projects.

Do not manufacture selftests or claim runtime parity from package structure.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

SOURCE_EXCLUSIONS = {"dist", "build", ".git", "__pycache__", "reconstructed-canonical"}
BUILD_SCRIPTS = {"build_distributions.py", "install_distribution_engine.py", "validate_distributions.py", "lint_gpt_project.py", "migrate_legacy_copy.py", "migrate_legacy_project.py"}



ENGINE_PACKAGERS = {"package_runtime_engine.py", "package_distribution_engine.py"}


def inspect_existing_engine_package(root: Path) -> dict[str, Any]:
    """Inventory existing Engine implementations; do not execute untrusted code."""
    import json
    import zipfile

    packagers = sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*.py")
        if p.name in ENGINE_PACKAGERS
        and not set(p.relative_to(root).parts) & SOURCE_EXCLUSIONS
    )
    archives = []
    for path in sorted(root.rglob("*-engine*.zip")):
        if not path.is_file() or set(path.relative_to(root).parts) & SOURCE_EXCLUSIONS:
            continue
        finding = {"path": path.relative_to(root).as_posix(),
                   "format": "unknown", "manifest_readable": False}
        try:
            if path.stat().st_size > 50 * 1024 * 1024:
                finding["error"] = "archive_too_large"
            else:
                with zipfile.ZipFile(path) as archive:
                    for name, kind in (("engine-package.json", "canonical"),
                                       ("MANIFEST.json", "project_specific")):
                        info = next((i for i in archive.infolist()
                                     if i.filename == name), None)
                        if info is None:
                            continue
                        finding["format"] = kind
                        if info.file_size > 65536:
                            finding["error"] = "manifest_too_large"
                        else:
                            manifest = json.loads(archive.read(info))
                            if not isinstance(manifest, dict):
                                raise ValueError("Manifest is not an object")
                            finding["manifest_readable"] = True
                            finding["version"] = manifest.get("version")
                            finding["entrypoint_declared"] = bool(manifest.get("entrypoint"))
                            finding["file_count"] = len(manifest["files"]) if isinstance(manifest.get("files"), dict) else None
                        break
        except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
            finding["error"] = "invalid_or_unreadable_archive"
        archives.append(finding)
    local_manifests = [
        {"path": name, "format": kind}
        for name, kind in (("engine-package.json", "canonical"),
                           ("MANIFEST.json", "project_specific"))
        if (root / name).is_file()
    ]
    found = bool(packagers or archives or local_manifests)
    observed = [*archives, *local_manifests]
    canonical = any(item["format"] == "canonical" for item in observed)
    custom = bool(packagers or any(item["format"] == "project_specific" for item in observed))
    return {
        "detected": found,
        "packager_scripts": packagers,
        "archives": archives,
        "manifests": local_manifests,
        "canonical_format_detected": canonical,
        "project_specific_format_detected": custom,
        "comparison": ("review_existing_canonical_engine" if canonical
                       else "compare_with_generic_engine_contract" if custom
                       else "no_existing_package_evidence"),
        "integrity_verified": False,
        "executable_verified": False,
        "migration_automatic": False,
    }


def inspect_engine_migration(root: Path, cfg: dict | None) -> dict[str, Any]:
    if not isinstance(cfg, dict):
        return {"engine_required": "undetermined", "engine_status": "blocked",
                "plugin_repair_status": "source_contract_missing",
                "runtime_parity_status": "unverified", "release_ready": False,
                "required_actions": ["Recover and review canonical project contract before enabling Plugin or Engine."]}
    existing_package = inspect_existing_engine_package(root)
    runtime = cfg.get("runtime") or {}
    plugin = runtime.get("plugin") or runtime.get("openai_plugin") or {}
    plugin_present = isinstance(plugin, dict) and bool(plugin)
    declared = cfg.get("engine") or {}
    candidates = []
    for p in sorted(root.rglob("*.py")):
        rel = p.relative_to(root)
        if set(rel.parts) & SOURCE_EXCLUSIONS or p.name in BUILD_SCRIPTS:
            continue
        candidates.append(rel.as_posix())
    explicit = declared.get("enabled") is True
    resources = declared.get("resources") or []
    selftest = declared.get("selftest")
    configured = explicit and isinstance(resources, list) and bool(resources) and isinstance(selftest, str) and bool(selftest)
    verified_paths = configured and (root / selftest).is_file() and all(
        isinstance(v, str) and (root / v).exists() and not Path(v).is_absolute()
        and ".." not in Path(v).parts for v in resources
    )
    if explicit and verified_paths:
        engine_status = "configured_pending_integrity_and_execution"
    elif explicit:
        engine_status = "incomplete_configuration"
    elif candidates or existing_package["detected"]:
        engine_status = "review_required"
    else:
        engine_status = "not_indicated"
    if not plugin_present:
        plugin_status = "plugin_not_configured"
    elif "openai_plugin" in runtime and "plugin" not in runtime:
        plugin_status = "legacy_plugin_requires_mapping"
    else:
        plugin_status = "needs_rebuild_and_host_verification"
    actions = []
    if existing_package["detected"]:
        actions.append("Compare existing Engine package against generic engine.resources, selftest, dependencies and engine-package.json.")
        actions.append("Keep the existing Engine intact until integrity, execution and host regression tests succeed.")
    if candidates and not verified_paths:
        actions.append("Classify candidate Python scripts as Plugin runtime requirements, tests, or build-only tools.")
        actions.append("If executable Plugin scripts are required, declare engine.resources and a real engine.selftest.")
    if explicit and not verified_paths:
        actions.append("Correct engine resources/selftest paths; do not ship an unverified Engine ZIP.")
    if plugin_present:
        actions.append("Rebuild Plugin using the current canonical distribution builder; inspect Skills and resources.")
        actions.append("Validate all five distributions and test the Plugin in its actual host.")
    actions.append("Install/verify the current canonical builder only after reviewing the copied project schema and preserving project-specific files.")
    return {
        "engine_required": True if explicit else ("needs_review" if candidates or existing_package["detected"] else False),
        "engine_status": engine_status,
        "engine_candidates": candidates,
        "existing_engine_package": existing_package,
        "engine_configuration_present": explicit,
        "engine_selftest_verified": False,
        "plugin_repair_status": plugin_status,
        "runtime_parity_status": "unverified",
        "automatic_plugin_repair": False,
        "automatic_engine_activation": False,
        "release_ready": False,
        "required_actions": actions,
    }
