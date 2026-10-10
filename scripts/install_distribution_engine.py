#!/usr/bin/env python3
"""Install the canonical runtime distribution engine in a generated GPT project.

Does not rewrite project configuration or invent runtime-specific settings.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ENGINE_FILES = (
    "scripts/build_distributions.py",
    "scripts/lib/project_model.py",
    "scripts/validate_distributions.py",
    "scripts/validate_portable_skills.py",
)
REQUIRED_TARGETS = {"chat", "plugin", "claude_project", "claude_skills", "opencode"}


def install(source: Path, project: Path) -> list[str]:
    if source.resolve() == project.resolve():
        raise ValueError("Source and destination must be different")
    if not (project / "gpt-project.yaml").is_file():
        raise ValueError("Destination requires an existing gpt-project.yaml")
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required") from exc
    cfg = yaml.safe_load((project / "gpt-project.yaml").read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("Project configuration must be a YAML mapping")
    targets = cfg.get("build_system", {}).get("runtime_targets", {})
    missing = REQUIRED_TARGETS - set(targets)
    if missing:
        raise ValueError("Missing platform-specific runtime targets: " + ", ".join(sorted(missing)))
    missing_builders = [t for t in REQUIRED_TARGETS if not targets[t].get("builder")]
    if missing_builders:
        raise ValueError("Missing builder declarations: " + ", ".join(sorted(missing_builders)))
    declared_scripts = []
    for tool in cfg.get("tools", {}).get("tools", []):
        if tool.get("type") == "script" and tool.get("script"):
            declared_scripts.append(tool["script"])
    files_to_install = tuple(dict.fromkeys((*ENGINE_FILES, *declared_scripts)))
    template = cfg.get("runtime", {}).get("chat_zip", {}).get("start_here_template")
    declared_templates = [template] if template else []
    for runtime in ("plugin", "claude", "opencode"):
        templates = cfg.get("runtime", {}).get(runtime, {}).get("templates", {})
        if isinstance(templates, dict):
            declared_templates.extend(value for value in templates.values() if isinstance(value, str))
    files_to_install = tuple(dict.fromkeys((*files_to_install, *declared_templates)))
    for relative in files_to_install:
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError("Unsafe declared script path: " + relative)
        if not (source / relative).is_file() and not (project / relative).is_file():
            raise FileNotFoundError(source / relative)
    copied = []
    for relative in files_to_install:
        if not (source / relative).is_file():
            continue
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
        copied.append(relative)
    return copied


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    for name in install(args.source, args.project_root):
        print("Installed", name)


if __name__ == "__main__":
    main()
