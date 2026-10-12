"""Opt-in canonical core + Skill sources with legacy monolithic fallback."""
from pathlib import Path


def _read(root: Path, relative: str) -> str:
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or not (root / p).resolve().is_relative_to(root.resolve()) or not (root / p).is_file():
        raise ValueError(f"Unsafe or missing canonical source: {relative}")
    result = (root / p).read_text(encoding="utf-8").strip()
    if not result:
        raise ValueError(f"Empty canonical source: {relative}")
    return result


def is_modular(cfg: dict) -> bool:
    return (cfg.get("instructions") or {}).get("mode") == "modular_skills"


def modules(root: Path, cfg: dict, definitions: list[dict]) -> tuple[str, list[tuple[dict, str]]]:
    if not is_modular(cfg):
        return _read(root, cfg["instructions"]["canonical"]), []
    core = (cfg.get("instructions") or {}).get("core")
    if not isinstance(core, str):
        raise ValueError("modular_skills requires instructions.core")
    if not definitions:
        raise ValueError("modular_skills requires at least one canonical Skill")
    parts = []
    seen = set()
    source_paths = set()
    for skill in definitions:
        name = skill.get("id")
        source = skill.get("source")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("Canonical Skill IDs must be unique and nonempty")
        if not isinstance(source, str):
            raise ValueError(f"Canonical Skill {name} requires source")
        resolved_source = (root / source).resolve()
        if resolved_source == (root / core).resolve() or resolved_source in source_paths:
            raise ValueError(f"Canonical Skill {name} duplicates a core/Skill source")
        seen.add(name)
        source_paths.add(resolved_source)
        parts.append((skill, _read(root, source)))
    return _read(root, core), parts


def projected_instruction(root: Path, cfg: dict, definitions: list[dict]) -> str:
    core, parts = modules(root, cfg, definitions)
    if not is_modular(cfg):
        return (root / cfg["instructions"]["canonical"]).read_text(encoding="utf-8")
    return core + "\n\n" + "\n\n".join(
        f"## Skill: {item['id']}\n\n{body}" for item, body in parts
    ) + "\n"


def skill_instruction(root: Path, cfg: dict, definitions: list[dict], skill: dict) -> str:
    core, parts = modules(root, cfg, definitions)
    if not is_modular(cfg):
        return core
    for item, body in parts:
        if item["id"] == skill["id"]:
            return core + "\n\n" + body
    raise ValueError(f"Unknown Skill: {skill['id']}")
