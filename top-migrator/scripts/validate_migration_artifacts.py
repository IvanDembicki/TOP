#!/usr/bin/env python3
"""Lightweight structural checks for top-migrator JSON artifacts.

This script intentionally avoids third-party dependencies. It checks the
status vocabulary and required fields used by the skill references. It is not a
replacement for TOP validation from top-skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


LOG_ENTRY_TYPES = {
    "node_extracted",
    "checkpoint",
    "behavior_check",
    "top_validation",
    "failure",
    "repair",
    "rollback",
    "readiness",
    "escalation",
    "component_decision",
}

LOG_ENTRY_STATUSES = {"pending", "pass", "fail", "blocked", "not_verified", "deferred"}

DECOMPOSITION_STATUSES = {"pending", "decomposing", "leaf_irreducible", "children_ready", "blocked"}
BEHAVIOR_STATUSES = {"not_required", "not_tested", "tests_passed", "tests_failed", "behavior_not_verified"}
TOP_VALIDATION_STATUSES = {"not_required", "not_verified", "top_valid", "top_invalid", "contaminated"}
INTEGRATION_STATUSES = {"not_started", "pending", "integrated", "integration_failed", "stale_contract"}
READINESS_STATUSES = {"draft", "partial", "blocked", "ready_structural", "ready_verified"}

COMPONENT_ORIGINS = {"local", "external"}
COMPONENT_CLASSIFICATIONS = {
    "preserved_component",
    "black_box_component",
    "top_candidate",
    "temporary_residual",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_string(value: Any, label: str, errors: list[str]) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a non-empty string", errors)


def validate_migration_log(path: Path) -> list[str]:
    data = load_json(path)
    errors: list[str] = []
    require(isinstance(data, dict), "migration log must be an object", errors)
    if not isinstance(data, dict):
        return errors

    check_string(data.get("migrationId"), "migrationId", errors)
    require(data.get("profile") in {"strict-incremental", "draft-full-pass", "hybrid"}, "profile is invalid", errors)
    check_string(data.get("rootNode"), "rootNode", errors)
    require(isinstance(data.get("entries"), list), "entries must be an array", errors)

    for index, entry in enumerate(data.get("entries", [])):
        label = f"entries[{index}]"
        require(isinstance(entry, dict), f"{label} must be an object", errors)
        if not isinstance(entry, dict):
            continue
        check_string(entry.get("id"), f"{label}.id", errors)
        require(entry.get("type") in LOG_ENTRY_TYPES, f"{label}.type is invalid", errors)
        check_string(entry.get("nodePath"), f"{label}.nodePath", errors)
        check_string(entry.get("summary"), f"{label}.summary", errors)
        require(entry.get("status") in LOG_ENTRY_STATUSES, f"{label}.status is invalid", errors)
    return errors


def validate_node_readiness(path: Path) -> list[str]:
    data = load_json(path)
    errors: list[str] = []
    require(isinstance(data, dict), "node readiness must be an object", errors)
    if not isinstance(data, dict):
        return errors

    check_string(data.get("nodePath"), "nodePath", errors)
    require(data.get("decompositionStatus") in DECOMPOSITION_STATUSES, "decompositionStatus is invalid", errors)
    require(data.get("behaviorStatus") in BEHAVIOR_STATUSES, "behaviorStatus is invalid", errors)
    require(data.get("topValidationStatus") in TOP_VALIDATION_STATUSES, "topValidationStatus is invalid", errors)
    require(data.get("integrationStatus") in INTEGRATION_STATUSES, "integrationStatus is invalid", errors)
    require(data.get("readinessStatus") in READINESS_STATUSES, "readinessStatus is invalid", errors)
    return errors


def validate_component_inventory(path: Path) -> list[str]:
    data = load_json(path)
    errors: list[str] = []
    require(isinstance(data, dict), "component inventory must be an object", errors)
    if not isinstance(data, dict):
        return errors

    check_string(data.get("scope"), "scope", errors)
    require(isinstance(data.get("components"), list), "components must be an array", errors)
    for index, component in enumerate(data.get("components", [])):
        label = f"components[{index}]"
        require(isinstance(component, dict), f"{label} must be an object", errors)
        if not isinstance(component, dict):
            continue
        check_string(component.get("name"), f"{label}.name", errors)
        check_string(component.get("pathOrPackage"), f"{label}.pathOrPackage", errors)
        require(component.get("origin") in COMPONENT_ORIGINS, f"{label}.origin is invalid", errors)
        require(component.get("classification") in COMPONENT_CLASSIFICATIONS, f"{label}.classification is invalid", errors)
        check_string(component.get("reason"), f"{label}.reason", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate top-migrator JSON artifacts.")
    parser.add_argument("--migration-log", type=Path)
    parser.add_argument("--node-readiness", type=Path)
    parser.add_argument("--component-inventory", type=Path)
    args = parser.parse_args()

    checks = [
        ("migration log", args.migration_log, validate_migration_log),
        ("node readiness", args.node_readiness, validate_node_readiness),
        ("component inventory", args.component_inventory, validate_component_inventory),
    ]

    all_errors: list[str] = []
    ran_any = False
    for name, path, validator in checks:
        if path is None:
            continue
        ran_any = True
        try:
            errors = validator(path)
        except FileNotFoundError:
            errors = [f"{path}: file not found"]
        except json.JSONDecodeError as exc:
            errors = [f"{path}: invalid JSON: {exc}"]
        for error in errors:
            all_errors.append(f"{name}: {error}")

    if not ran_any:
        parser.error("provide at least one artifact path")

    if all_errors:
        for error in all_errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1

    print("PASS top-migrator artifact checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
