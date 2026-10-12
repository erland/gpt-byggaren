"""Activate canonical Skill sources from reviewed assembly ownership, never from summaries."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import yaml


def activate(project: Path) -> dict:
    profile = project / "gpt-project.yaml"
    if not profile.is_file():
        return {"status": "blocked", "reason": "Missing project model"}
    cfg = yaml.safe_load(profile.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        return {"status": "blocked", "reason": "Invalid project model"}
    instructions = cfg.get("instructions") or {}
    if instructions.get("mode") == "modular_skills":
        return {"status": "already_enabled"}
    assembly = project / "canonical/assembly.json"
    if not assembly.is_file():
        return {"status": "review_required", "reason": "No reviewed canonical/assembly.json with source ownership; cannot infer safe separation"}
    manifest = json.loads(assembly.read_text(encoding="utf-8"))
    sections = manifest.get("sections")
    skills = (cfg.get("skills") or {}).get("definitions") or []
    ids = {s.get("id") for s in skills if isinstance(s, dict)}
    if not isinstance(sections, list) or not sections or not ids:
        return {"status": "blocked", "reason": "Missing assembly sections or Skill definitions"}
    by_owner = {"core": []}
    for name in ids:
        by_owner[name] = []
    ordered = []
    for section in sections:
        owner, name = section.get("owner"), section.get("path")
        if owner not in by_owner or not isinstance(name, str):
            return {"status": "blocked", "reason": "Unknown owner or source", "section": section}
        rel = Path(name)
        source = (project / rel).resolve()
        if rel.is_absolute() or ".." in rel.parts or not source.is_relative_to(project.resolve()) or not source.is_file():
            return {"status": "blocked", "reason": "Unsafe or missing source", "source": name}
        body = source.read_text(encoding="utf-8")
        if not body.strip():
            return {"status": "blocked", "reason": "Empty source", "source": name}
        by_owner[owner].append(body)
        ordered.append(body)
    if not by_owner["core"] or any(not by_owner[s] for s in ids):
        return {"status": "blocked", "reason": "Each Skill and shared core require source content"}
    original = instructions.get("canonical")
    legacy = project / original if isinstance(original, str) else None
    if legacy is None or not legacy.is_file() or legacy.read_text(encoding="utf-8") != "".join(ordered):
        return {"status": "review_required", "reason": "Assembly is not byte-identical to legacy canonical instruction"}
    destination = project / "canonical/core.md"
    sources = {name: project / "canonical/skills" / name / "behavior.md" for name in ids}
    all_paths = [destination, *sources.values()]
    if any(p.exists() for p in all_paths):
        return {"status": "review_required", "reason": "Canonical module targets already exist; refusing overwrite"}
    new_cfg = copy.deepcopy(cfg)
    new_cfg["instructions"]["mode"] = "modular_skills"
    new_cfg["instructions"]["core"] = "canonical/core.md"
    # Keep the previous full canonical file as a compatibility artifact.
    for skill in new_cfg["skills"]["definitions"]:
        skill["source"] = f"canonical/skills/{skill['id']}/behavior.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(by_owner["core"]), encoding="utf-8")
    for owner, path in sources.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(by_owner[owner]), encoding="utf-8")
    portable_path = project / "portable-skills.json"
    if portable_path.is_file():
        portable = json.loads(portable_path.read_text(encoding="utf-8"))
        if isinstance(portable, dict) and portable.get("core") == original:
            portable["core"] = "canonical/core.md"
            portable_path.write_text(json.dumps(portable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    profile.write_text(yaml.safe_dump(new_cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {"status": "activated_pending_behavior_review", "core": "canonical/core.md",
            "skills": sorted(ids), "original_instruction_preserved": True,
            "source_coverage": "byte_exact_assembly", "runtime_parity_verified": False,
            "note": "Original interleaving preserved in legacy file; modular runtime projections group sections by owner and require behavioral review"}
