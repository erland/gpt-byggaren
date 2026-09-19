#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

from lib.project_model import (
    normalize_capability_contract,
    capability_level,
    normalize_artifact_contract,
    normalize_workspace_state_contract,
    normalize_tool_contract,
    artifact_contract_id_for_delivery_type,
)

try:
    import yaml
except Exception as exc:
    raise SystemExit("PyYAML is required to run build_distributions.py") from exc


FIXED_ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def load_config(root: Path) -> dict:
    path = root / "gpt-project.yaml"
    if not path.exists():
        raise SystemExit(f"Missing config: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_write_zip(zip_path: Path, root: Path, files: list[Path]) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(files, key=lambda p: p.as_posix()):
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_filtered(src: Path, dst: Path, ignore_names: set[str] | None = None) -> None:
    # Runtime distributions must never contain local Python/cache artifacts.
    ignore_names = set(ignore_names or set()) | {
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"
    }
    if not src.exists():
        return
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        if any(part in ignore_names for part in rel.parts):
            continue
        if p.suffix in {".pyc", ".pyo"}:
            continue
        copy_file(p, dst / rel)


def render_template(text: str, replacements: dict[str, str]) -> str:
    for k, v in replacements.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def build_manifest(root: Path, runtime_id: str, version: str, entrypoint: str | None = None) -> dict:
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files.append({
                "path": p.relative_to(root).as_posix(),
                "sha256": sha256(p),
                "size": p.stat().st_size,
            })
    result = {
        "runtime_id": runtime_id,
        "version": version,
        "files": files,
    }
    if entrypoint:
        result["entrypoint"] = entrypoint
    return result


def write_manifest(root: Path, runtime_id: str, version: str, entrypoint: str | None = None) -> None:
    manifest = build_manifest(root, runtime_id, version, entrypoint)
    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def chat_runtime_contract(cfg: dict) -> dict:
    """Compile canonical assistant contracts into a Chat-runtime snapshot."""
    return {
        "schema_version": 1,
        "runtime_id": "chatgpt_chat",
        "capabilities": normalize_capability_contract(cfg),
        "artifacts": normalize_artifact_contract(cfg),
        "workspace_state": normalize_workspace_state_contract(cfg),
        "tools": normalize_tool_contract(cfg),
    }


def copy_declared_tool_scripts(root: Path, cfg: dict, target: Path) -> list[str]:
    """Copy only explicitly declared script tools plus their shared library."""
    copied = []
    contract = normalize_tool_contract(cfg)
    for tool in contract.get("tools", []):
        if tool.get("type") != "script":
            continue
        script_ref = tool.get("script")
        if not script_ref:
            continue
        src = root / script_ref
        if not src.exists():
            raise SystemExit(f"Declared runtime tool script missing: {script_ref}")
        rel = Path(script_ref)
        if rel.parts and rel.parts[0] == "scripts":
            rel = Path(*rel.parts[1:])
        copy_file(src, target / rel)
        copied.append(script_ref)

    shared_lib = root / "scripts" / "lib"
    if copied and shared_lib.exists():
        copy_tree_filtered(shared_lib, target / "lib")
    return copied


def build_chat(root: Path, cfg: dict, build_root: Path, version: str) -> Path:
    out = build_root / "chat"
    ensure_clean_dir(out)

    assistant = out / "assistant"
    policies = assistant / "policies"
    policies.mkdir(parents=True)

    instr_src = root / cfg["instructions"]["canonical"]
    copy_file(instr_src, assistant / "instructions.md")

    starters_root = root / cfg["structure"]["conversation_starters"]["path"]
    if starters_root.exists():
        starters = [p for p in starters_root.rglob("*") if p.is_file() and p.name != "README.md"]
        if starters:
            combined = "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(starters))
            (assistant / "conversation-starters.md").write_text(combined, encoding="utf-8")

    policy_root = root / cfg["structure"]["runtime_policy"]["path"]
    if policy_root.exists():
        for p in sorted(policy_root.rglob("*.md")):
            copy_file(p, policies / p.name)

    knowledge_root = root / cfg["knowledge_architecture"]["canonical_root"]
    if knowledge_root.exists():
        for p in sorted(knowledge_root.rglob("*")):
            if p.is_file() and p.name != "KNOWLEDGE.md":
                copy_file(p, out / "knowledge" / p.relative_to(knowledge_root))

    # Schemas/templates still follow the existing declarative Chat ZIP include model.
    # Runtime scripts are now selected from the canonical tool contract.
    for key in ["schemas", "templates"]:
        path = root / cfg["structure"][key]["path"]
        if path.exists():
            copy_tree_filtered(path, out / key, ignore_names={"README.md"})

    declared_tool_scripts = copy_declared_tool_scripts(root, cfg, out / "scripts")

    contract_snapshot = chat_runtime_contract(cfg)
    contract_snapshot["declared_tool_scripts"] = declared_tool_scripts
    (assistant / "runtime-contract.json").write_text(
        json.dumps(contract_snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    template_path = root / cfg["runtime"]["chat_zip"]["start_here_template"]
    template = template_path.read_text(encoding="utf-8")
    start_here = render_template(template, {
        "GPT_NAME": cfg["project"]["name"],
        "VERSION": version,
    })
    (out / "START-HERE.md").write_text(start_here, encoding="utf-8")
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")
    write_manifest(out, cfg["project"]["id"] + "-chat", version, "START-HERE.md")
    manifest_path = out / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_id"] = "chatgpt_chat"
    manifest["contract_snapshot"] = "assistant/runtime-contract.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def _knowledge_priority_patterns(cfg: dict) -> list[str]:
    return list(cfg.get("knowledge_architecture", {}).get("custom_gpt", {}).get("priority", []) or [])


def _rank_knowledge(files: list[Path], root: Path, cfg: dict) -> list[Path]:
    patterns = _knowledge_priority_patterns(cfg)
    ranked = []
    for p in files:
        rel_from_project = p.relative_to(root).as_posix()
        rank = len(patterns) + 1
        for idx, pattern in enumerate(patterns):
            if fnmatch.fnmatch(rel_from_project, pattern):
                rank = idx
                break
        ranked.append((rank, rel_from_project, p))
    return [p for _, _, p in sorted(ranked)]


def collect_custom_knowledge(root: Path, cfg: dict, target: Path) -> list[Path]:
    knowledge_root = root / cfg["knowledge_architecture"]["canonical_root"]
    files = [p for p in sorted(knowledge_root.rglob("*")) if p.is_file() and p.name != "KNOWLEDGE.md"] if knowledge_root.exists() else []
    max_files = int(cfg["runtime"]["custom_gpt"]["knowledge"]["max_files"])
    strategy = cfg["runtime"]["custom_gpt"]["knowledge"]["strategy"]

    if len(files) <= max_files:
        selected = files
    elif strategy in {"prioritize", "hybrid"}:
        selected = _rank_knowledge(files, root, cfg)[:max_files]
    else:
        raise SystemExit(
            f"Custom GPT Knowledge has {len(files)} files but max is {max_files}; "
            f"strategy {strategy!r} requires explicit consolidation support for overflow."
        )

    copied = []
    for p in selected:
        dst = target / p.relative_to(knowledge_root)
        copy_file(p, dst)
        copied.append(dst)
    return copied


def compile_custom_instruction(text: str, mode: str, max_chars: int, core_markers: list[str]) -> str:
    if mode == "identical":
        compiled = text
    elif mode in {"compressed", "compiled"}:
        # Conservative deterministic compression: preserve wording and headings,
        # remove trailing whitespace and collapse repeated blank lines.
        lines = [line.rstrip() for line in text.splitlines()]
        out = []
        blank = False
        for line in lines:
            if not line.strip():
                if blank:
                    continue
                blank = True
                out.append("")
            else:
                blank = False
                out.append(line)
        compiled = "\n".join(out).strip() + "\n"
    else:
        raise SystemExit(f"Unknown Custom GPT instruction mode: {mode!r}")

    missing = [marker for marker in core_markers if marker not in compiled]
    if missing:
        raise SystemExit(f"Custom GPT instruction compilation removed core behavior markers: {missing}")
    if len(compiled) > max_chars:
        raise SystemExit(
            f"Custom GPT instruction is {len(compiled)} characters after {mode!r} compilation; max is {max_chars}. "
            "Reduce or explicitly mark distribution-specific source material; do not move core behavior to Knowledge."
        )
    return compiled


def custom_runtime_contract(cfg: dict) -> dict:
    """Compile canonical assistant contracts into a Custom GPT adapter snapshot."""
    tool_contract = normalize_tool_contract(cfg)
    tool_states = []
    for tool in tool_contract.get("tools", []):
        fallback = tool.get("runtime_fallback", "not_applicable")
        state = "missing" if tool.get("requirement") == "required" and fallback == "block" else (
            "reduced" if tool.get("type") in {"script", "local_command"} else "not_applicable"
        )
        tool_states.append({
            "id": tool.get("id"),
            "type": tool.get("type"),
            "requirement": tool.get("requirement"),
            "state": state,
            "runtime_fallback": fallback,
        })

    return {
        "schema_version": 1,
        "runtime_id": "chatgpt_custom",
        "capabilities": normalize_capability_contract(cfg),
        "artifacts": normalize_artifact_contract(cfg),
        "workspace_state": normalize_workspace_state_contract(cfg),
        "tools": tool_contract,
        "adapter": {
            "tool_execution": "not_embedded",
            "tool_states": tool_states,
            "builder_package": True,
        },
    }


def build_custom(root: Path, cfg: dict, build_root: Path, version: str) -> Path:
    out = build_root / "custom-gpt"
    ensure_clean_dir(out)
    builder = out / "builder"
    kp = builder / "knowledge-package"
    kp.mkdir(parents=True)

    instr = (root / cfg["instructions"]["canonical"]).read_text(encoding="utf-8")
    max_chars = int(cfg["runtime"]["custom_gpt"]["instruction"]["max_characters"])
    mode = cfg["runtime"]["custom_gpt"]["instruction"]["mode"]
    core_markers = list(cfg.get("instructions", {}).get("core_contract", {}).get("required_markers", []) or [])
    compiled_instr = compile_custom_instruction(instr, mode, max_chars, core_markers)
    (builder / "instructions.md").write_text(compiled_instr, encoding="utf-8")

    starters_root = root / cfg["structure"]["conversation_starters"]["path"]
    starters = [p for p in starters_root.rglob("*") if p.is_file() and p.name != "README.md"] if starters_root.exists() else []
    combined = "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(starters))
    (builder / "conversation-starters.md").write_text(combined, encoding="utf-8")

    cap_tpl = (root / cfg["runtime"]["custom_gpt"]["templates"]["capabilities"]).read_text(encoding="utf-8")
    capability_contract = normalize_capability_contract(cfg)
    filesystem = capability_contract.get("requirements", {}).get("filesystem", {})
    filesystem_level = "required" if "required" in {filesystem.get("read"), filesystem.get("write")} else (
        "recommended" if "recommended" in {filesystem.get("read"), filesystem.get("write")} else "optional"
    )
    cap_text = render_template(cap_tpl, {
        "CAPABILITY_RECOMMENDATIONS": (
            f"- Webbsökning: {capability_level(capability_contract, 'web', 'optional')}\n"
            f"- Dataanalys/kodexekvering: {capability_level(capability_contract, 'code_execution', 'optional')}\n"
            f"- Bildgenerering: {capability_level(capability_contract, 'image_generation', 'optional')}\n"
            f"- Filhantering: {filesystem_level}"
        )
    })
    (builder / "capabilities.md").write_text(cap_text, encoding="utf-8")

    contract_snapshot = custom_runtime_contract(cfg)
    contract_ref = cfg["runtime"]["custom_gpt"]["builder"].get(
        "runtime_contract", "builder/runtime-contract.json"
    )
    contract_path = out / contract_ref
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(
        json.dumps(contract_snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    copied_knowledge = collect_custom_knowledge(root, cfg, kp)

    knowledge_root = root / cfg["knowledge_architecture"]["canonical_root"]
    canonical_knowledge = [p for p in sorted(knowledge_root.rglob("*")) if p.is_file() and p.name != "KNOWLEDGE.md"] if knowledge_root.exists() else []
    selected_rel = [p.relative_to(kp).as_posix() for p in copied_knowledge]
    selected_set = set(selected_rel)
    excluded_rel = [p.relative_to(knowledge_root).as_posix() for p in canonical_knowledge if p.relative_to(knowledge_root).as_posix() not in selected_set]
    compilation_report = {
        "runtime_id": "chatgpt_custom",
        "contract_snapshot": contract_ref,
        "instruction": {
            "mode": mode,
            "canonical_characters": len(instr),
            "compiled_characters": len(compiled_instr),
            "max_characters": max_chars,
            "core_markers_verified": len(core_markers),
        },
        "knowledge": {
            "strategy": cfg["runtime"]["custom_gpt"]["knowledge"]["strategy"],
            "canonical_files": len(canonical_knowledge),
            "selected_files": len(copied_knowledge),
            "max_files": int(cfg["runtime"]["custom_gpt"]["knowledge"]["max_files"]),
            "priority_patterns": _knowledge_priority_patterns(cfg),
            "selected": selected_rel,
            "excluded": excluded_rel,
        },
    }
    (builder / "compilation-report.json").write_text(json.dumps(compilation_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme_tpl = (root / cfg["runtime"]["custom_gpt"]["templates"]["readme"]).read_text(encoding="utf-8")
    (out / "README.md").write_text(
        render_template(readme_tpl, {"GPT_NAME": cfg["project"]["name"], "VERSION": version}),
        encoding="utf-8",
    )

    compat_tpl = (root / cfg["runtime"]["custom_gpt"]["templates"]["compatibility"]).read_text(encoding="utf-8")
    compat = render_template(compat_tpl, {
        "GPT_NAME": cfg["project"]["name"],
        "RUNTIME_RECOMMENDATION": "Ingen förvald primär runtime; välj endast utifrån faktisk capability/paritet.",
        "PARITY_TABLE": "Paritetsrapport genereras mer fullständigt i senare buildsteg.",
        "REDUCED_FEATURES": "Ej automatiskt analyserat ännu.",
        "MISSING_FEATURES": "Ej automatiskt analyserat ännu.",
    })
    (out / "COMPATIBILITY.md").write_text(compat, encoding="utf-8")
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")

    write_manifest(out, cfg["project"]["id"] + "-custom-gpt", version)
    manifest_path = out / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_id"] = "chatgpt_custom"
    manifest["contract_snapshot"] = contract_ref
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def claude_runtime_contract(cfg: dict) -> dict:
    """Compile canonical assistant contracts into a Claude Projects snapshot."""
    tool_contract = normalize_tool_contract(cfg)
    tool_states = []
    for tool in tool_contract.get("tools", []):
        state = "not_applicable"
        reason = None
        if tool.get("type") in {"script", "local_command"}:
            state = "reduced" if tool.get("runtime_fallback") == "manual" else "missing"
            reason = "Claude Projects package does not embed local command execution."
        elif tool.get("type") in {"mcp", "api_action"}:
            state = "reduced"
            reason = "Availability depends on the Claude account/project integration."

        item = {
            "id": tool.get("id"),
            "type": tool.get("type"),
            "requirement": tool.get("requirement"),
            "state": state,
        }
        if reason:
            item["reason"] = reason
        tool_states.append(item)

    return {
        "schema_version": 1,
        "runtime_id": "claude_project",
        "capabilities": normalize_capability_contract(cfg),
        "artifacts": normalize_artifact_contract(cfg),
        "workspace_state": normalize_workspace_state_contract(cfg),
        "tools": tool_contract,
        "adapter": {
            "mode": "claude_project",
            "project_instructions": True,
            "project_knowledge": True,
            "claude_code_conventions": False,
            "embedded_local_tools": False,
            "tool_states": tool_states,
        },
    }


def build_claude(root: Path, cfg: dict, build_root: Path, version: str) -> Path:
    out = build_root / "claude"
    ensure_clean_dir(out)

    runtime_cfg = cfg["runtime"]["claude"]
    project_dir = out / "project"
    project_dir.mkdir(parents=True)

    instr_src = root / cfg["instructions"]["canonical"]
    instructions_ref = runtime_cfg["project"]["instructions"]
    instructions_path = out / instructions_ref
    copy_file(instr_src, instructions_path)

    knowledge_root = root / cfg["knowledge_architecture"]["canonical_root"]
    knowledge_ref = runtime_cfg["project"]["knowledge"]
    knowledge_target = out / knowledge_ref
    if knowledge_root.exists():
        for p in sorted(knowledge_root.rglob("*")):
            if p.is_file() and p.name != "KNOWLEDGE.md":
                copy_file(p, knowledge_target / p.relative_to(knowledge_root))

    contract_ref = runtime_cfg["project"]["runtime_contract"]
    contract_path = out / contract_ref
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(
        json.dumps(claude_runtime_contract(cfg), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme_tpl = (root / runtime_cfg["templates"]["readme"]).read_text(encoding="utf-8")
    (out / "README.md").write_text(
        render_template(readme_tpl, {
            "GPT_NAME": cfg["project"]["name"],
            "VERSION": version,
        }),
        encoding="utf-8",
    )
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")

    write_manifest(out, cfg["project"]["id"] + "-claude", version, "README.md")
    manifest_path = out / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_id"] = "claude_project"
    manifest["contract_snapshot"] = contract_ref
    manifest["project_instructions"] = instructions_ref
    manifest["project_knowledge"] = knowledge_ref
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out


def build_opencode_skills(root: Path, cfg: dict, out: Path) -> list[str]:
    """Generate OpenCode skills from declared workflow/reference sources."""
    runtime_cfg = cfg["runtime"]["opencode"]
    skills_cfg = runtime_cfg.get("skills", {})
    if not skills_cfg.get("enabled"):
        return []

    skill_root = out / skills_cfg.get("directory", ".opencode/skills")
    built: list[str] = []
    for skill in skills_cfg.get("definitions", []):
        skill_id = skill["id"]
        skill_dir = skill_root / skill_id
        references_dir = skill_dir / "references"
        references_dir.mkdir(parents=True, exist_ok=True)

        reference_lines = []
        for ref in skill.get("references", []):
            src = root / ref
            if not src.exists():
                raise SystemExit(f"OpenCode skill reference missing: {ref}")
            dst = references_dir / src.name
            copy_file(src, dst)
            reference_lines.append(f"- Read `references/{src.name}` when that part of the workflow is relevant.")

        body = (
            "---\n"
            f"name: {skill['name']}\n"
            f"description: {skill['description']}\n"
            "compatibility: opencode\n"
            "metadata:\n"
            "  source: generated-from-canonical-project\n"
            "---\n\n"
            "## Purpose\n\n"
            f"{skill['description']}\n\n"
            "## Workflow\n\n"
            "1. Read the workspace state before choosing work.\n"
            "2. Prefer blockers, failed validation, hygiene, and missing dependencies before the next planned step.\n"
            "3. Treat the development plan as guiding rather than mechanical.\n"
            "4. After a change, validate, update project state, and rebuild the complete project package when applicable.\n"
            "5. Do not ask the user to repeat project history already present in workspace/state.\n\n"
            "## References\n\n"
            + "\n".join(reference_lines)
            + "\n"
        )
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
        built.append(skill_id)
    return built


def opencode_runtime_contract(cfg: dict, built_skills: list[str] | None = None) -> dict:
    """Compile canonical assistant contracts into an OpenCode workspace snapshot."""
    built_skills = list(built_skills or [])
    return {
        "schema_version": 1,
        "runtime_id": "opencode",
        "capabilities": normalize_capability_contract(cfg),
        "artifacts": normalize_artifact_contract(cfg),
        "workspace_state": normalize_workspace_state_contract(cfg),
        "tools": normalize_tool_contract(cfg),
        "adapter": {
            "mode": "opencode_workspace",
            "instructions": "AGENTS.md",
            "skills_included": bool(built_skills),
            "skills": built_skills,
            "tool_integration": "deferred",
            "workspace_first": True,
        },
    }


def build_opencode(root: Path, cfg: dict, build_root: Path, version: str) -> Path:
    out = build_root / "opencode"
    ensure_clean_dir(out)

    runtime_cfg = cfg["runtime"]["opencode"]

    canonical_instruction = (root / cfg["instructions"]["canonical"]).read_text(encoding="utf-8")
    agents_path = out / runtime_cfg["layout"]["instructions"]
    agents_path.write_text(
        canonical_instruction.rstrip()
        + "\n\n## OpenCode adapter\n\n"
        + "- Treat this AGENTS.md as a generated projection of the canonical assistant instructions.\n"
        + "- Work inside this repository/workspace.\n"
        + "- Reusable workflows may be available as project-local skills under .opencode/skills/.\n"
        + "- Load a skill when its description matches the current task instead of duplicating that workflow here.\n"
        + "- Tool integration is added in a later adapter step; do not infer undeclared tools.\n",
        encoding="utf-8",
    )

    knowledge_root = root / cfg["knowledge_architecture"]["canonical_root"]
    knowledge_target = out / runtime_cfg["layout"]["knowledge"]
    if knowledge_root.exists():
        for p in sorted(knowledge_root.rglob("*")):
            if p.is_file() and p.name != "KNOWLEDGE.md":
                copy_file(p, knowledge_target / p.relative_to(knowledge_root))

    built_skills = build_opencode_skills(root, cfg, out)

    contract_ref = runtime_cfg["layout"]["runtime_contract"]
    contract_path = out / contract_ref
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(
        json.dumps(opencode_runtime_contract(cfg, built_skills), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme_tpl = (root / runtime_cfg["templates"]["readme"]).read_text(encoding="utf-8")
    (out / "README.md").write_text(
        render_template(readme_tpl, {
            "GPT_NAME": cfg["project"]["name"],
            "VERSION": version,
        }),
        encoding="utf-8",
    )
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")

    write_manifest(out, cfg["project"]["id"] + "-opencode", version, "AGENTS.md")
    manifest_path = out / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_id"] = "opencode"
    manifest["contract_snapshot"] = contract_ref
    manifest["instructions"] = runtime_cfg["layout"]["instructions"]
    manifest["skills_included"] = bool(built_skills)
    manifest["skills"] = built_skills
    manifest["tool_integration"] = "deferred"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out


def project_files(root: Path) -> list[Path]:
    excluded_top = {"build", "dist", ".git"}
    result = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if rel.parts and rel.parts[0] in excluded_top:
            continue
        if "__pycache__" in rel.parts or ".pytest_cache" in rel.parts:
            continue
        result.append(p)
    return result


def write_checksums(dist: Path) -> None:
    lines = []
    for p in sorted(dist.glob("*.zip")):
        lines.append(f"{sha256(p)}  {p.name}")
    (dist / "SHA256SUMS.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_delivery_manifest(dist: Path, cfg: dict, version: str) -> None:
    artifacts = []
    for p in sorted(dist.iterdir()):
        if not p.is_file() or p.name in {"DELIVERY-MANIFEST.json"}:
            continue
        if p.suffix == ".zip":
            if "-project" in p.name:
                artifact_type = "project_zip"
            elif "-chat-" in p.name:
                artifact_type = "chat_zip"
            elif "-custom-gpt-" in p.name:
                artifact_type = "custom_gpt_zip"
            elif "-claude-" in p.name:
                artifact_type = "claude_zip"
            elif "-opencode-" in p.name:
                artifact_type = "opencode_zip"
            else:
                artifact_type = "zip"
        elif p.name == "SHA256SUMS.txt":
            artifact_type = "checksums"
        else:
            artifact_type = "file"
        artifact = {
            "type": artifact_type,
            "file": p.name,
            "sha256": sha256(p),
            "size": p.stat().st_size,
        }
        contract_id = artifact_contract_id_for_delivery_type(cfg, artifact_type)
        if contract_id:
            artifact["artifact_id"] = contract_id
        artifacts.append(artifact)

    payload = {
        "project": cfg["project"]["id"],
        "project_name": cfg["project"]["name"],
        "version": version,
        "primary_runtime": cfg.get("runtime", {}).get("primary", "none"),
        "runtime_strategy": "peer_distributions",
        "custom_gpt_enabled": bool(cfg["runtime"]["custom_gpt"]["enabled"]),
        "artifacts": artifacts,
    }
    (dist / "DELIVERY-MANIFEST.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--version", default="0.0.0-dev")
    parser.add_argument("--targets", default="project,chat,custom-gpt,claude,opencode")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cfg = load_config(root)
    build_root = root / "build"
    dist = root / "dist"
    build_root.mkdir(exist_ok=True)
    dist.mkdir(exist_ok=True)

    targets = {t.strip() for t in args.targets.split(",") if t.strip()}
    project_id = cfg["project"]["id"]
    version = args.version

    if "chat" in targets:
        chat_root = build_chat(root, cfg, build_root, version)
        chat_zip = dist / f"{project_id}-chat-{version}.zip"
        stable_write_zip(chat_zip, chat_root, [p for p in chat_root.rglob("*") if p.is_file()])

    if "custom-gpt" in targets and cfg["runtime"]["custom_gpt"]["enabled"]:
        custom_root = build_custom(root, cfg, build_root, version)
        custom_zip = dist / f"{project_id}-custom-gpt-{version}.zip"
        stable_write_zip(custom_zip, custom_root, [p for p in custom_root.rglob("*") if p.is_file()])

    if "claude" in targets and cfg.get("runtime", {}).get("claude", {}).get("enabled"):
        claude_root = build_claude(root, cfg, build_root, version)
        claude_zip = dist / f"{project_id}-claude-{version}.zip"
        stable_write_zip(claude_zip, claude_root, [p for p in claude_root.rglob("*") if p.is_file()])

    if "opencode" in targets and cfg.get("runtime", {}).get("opencode", {}).get("enabled"):
        opencode_root = build_opencode(root, cfg, build_root, version)
        opencode_zip = dist / f"{project_id}-opencode-{version}.zip"
        stable_write_zip(opencode_zip, opencode_root, [p for p in opencode_root.rglob("*") if p.is_file()])

    if "project" in targets:
        project_zip = dist / f"{project_id}-project.zip"
        stable_write_zip(project_zip, root, project_files(root))

    write_checksums(dist)
    write_delivery_manifest(dist, cfg, version)

    print(f"Build complete: {dist}")
    for p in sorted(dist.iterdir()):
        if p.is_file():
            print(p.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
