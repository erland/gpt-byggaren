from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_project_config(root: Path) -> dict[str, Any]:
    return load_yaml(root / "gpt-project.yaml")


def load_project_status(root: Path) -> dict[str, Any]:
    return load_yaml(root / "project-status.yaml")


def select_reference_profile(features: dict[str, Any]) -> str:
    """Return the canonical reference profile for a feature set."""
    if (
        features.get("research_heavy")
        or features.get("evidence_required")
        or features.get("multi_stage_workflow")
    ):
        return "workflow_research_heavy"

    if (
        features.get("project_zip_manipulation")
        or features.get("scripts_required")
        or features.get("rich_structured_runtime")
    ):
        return "zip_first_advanced"

    if (
        features.get("structured_knowledge")
        or features.get("repeatable_outputs")
        or features.get("moderate_workflow")
    ):
        return "standard"

    return "simple"


def get_registered_next_step(status: dict[str, Any]) -> dict[str, Any] | None:
    value = status.get("next_step")
    return value if isinstance(value, dict) and value else None


def get_blockers(status: dict[str, Any]) -> list[Any]:
    return list(status.get("blocking_issues") or status.get("blockers") or [])


CAPABILITY_LEVELS = {"required", "recommended", "optional", "not_required", "to_be_recommended"}

LEGACY_CAPABILITY_MAP = {
    "web": "web",
    "data_analysis": "code_execution",
    "image_generation": "image_generation",
    "structured_knowledge": "structured_data",
}


def _legacy_level(value: Any) -> str:
    if isinstance(value, str):
        aliases = {
            "likely_required": "recommended",
            "not_recommended": "not_required",
        }
        return aliases.get(value, value if value in CAPABILITY_LEVELS else "to_be_recommended")
    if isinstance(value, dict):
        return _legacy_level(value.get("state", value.get("level")))
    return "to_be_recommended"


def normalize_capability_contract(cfg: dict[str, Any]) -> dict[str, Any]:
    """Return the platform-neutral capability contract.

    Current projects use capabilities.requirements. Legacy projects using
    web/data_analysis/file_handling/etc. are mapped without mutating source data.
    """
    caps = cfg.get("capabilities") or {}
    requirements = caps.get("requirements")
    if isinstance(requirements, dict):
        return {
            "contract_version": caps.get("contract_version", 1),
            "recommendation_mode": caps.get("recommendation_mode", "inferred_from_use_case"),
            "ask_user_only_when_business_choice_is_ambiguous": caps.get(
                "ask_user_only_when_business_choice_is_ambiguous", True
            ),
            "requirements": requirements,
        }

    normalized: dict[str, Any] = {}
    for legacy, canonical in LEGACY_CAPABILITY_MAP.items():
        if legacy in caps:
            normalized[canonical] = {"level": _legacy_level(caps[legacy])}

    file_handling = caps.get("file_handling")
    if file_handling is not None:
        level = _legacy_level(file_handling)
        normalized["filesystem"] = {"read": level, "write": level}

    return {
        "contract_version": 1,
        "recommendation_mode": caps.get("recommendation_mode", "inferred_from_use_case"),
        "ask_user_only_when_business_choice_is_ambiguous": caps.get(
            "ask_user_only_when_business_choice_is_ambiguous", True
        ),
        "requirements": normalized,
    }


def capability_level(contract: dict[str, Any], capability: str, default: str = "optional") -> str:
    value = (contract.get("requirements") or {}).get(capability)
    if isinstance(value, dict):
        return str(value.get("level", default))
    return default
