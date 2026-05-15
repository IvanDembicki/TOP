#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_inside(root, ref):
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"artifact path escapes root: {ref}") from exc
    return resolved


def validate(path):
    data = load_json(path)
    errors = []
    if data.get("component") != "DriverStatusBadge":
        errors.append("component must be DriverStatusBadge")
    if data.get("statusLabel") != "Ready":
        errors.append("statusLabel must be Ready")
    if data.get("isValid") is not True:
        errors.append("isValid must be true")
    if data.get("repairedBy") != "repair-1":
        errors.append("repairedBy must be repair-1")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate the repair artifact dogfood fixture.")
    parser.add_argument("artifact", nargs="?", default="artifacts/repair-target.json")
    parser.add_argument("--root", default=".", help="Run package root")
    args = parser.parse_args()

    try:
        root = Path(args.root).resolve()
        artifact_path = resolve_inside(root, args.artifact)
        errors = validate(artifact_path)
    except Exception as exc:
        print("validate_repair_artifact_fixture: FAILED")
        print(f"- {exc}")
        return 1

    if errors:
        print("validate_repair_artifact_fixture: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("validate_repair_artifact_fixture: OK")
    print(f"artifact: {artifact_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
