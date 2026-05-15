#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


EXECUTION_ISOLATION_LEVELS = {
    "protocol-defined",
    "protocol-followed-by-agent",
    "schema-validated",
    "runner-enforced",
}

VERIFICATION_EVIDENCE_LEVELS = {
    "none",
    "agent-claimed",
    "schema-validated",
    "hard-check-verified",
}

BLOCKING_GATE_STATUSES = {"fail", "not_verified"}

EXECUTION_EVIDENCE_FIELDS = {
    "executionIsolationLevel",
    "verificationEvidenceLevel",
    "runnerName",
    "separateInvocationIds",
    "schemaValidationCommand",
    "hardCheckCommands",
    "limitations",
}

JSON_SCHEMA_KEYS = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "type",
    "properties",
    "required",
    "allOf",
    "anyOf",
    "oneOf",
    "items",
    "enum",
    "const",
}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def is_nonempty_string_list(value):
    return isinstance(value, list) and all(is_nonempty_string(item) for item in value)


def is_schema_definition(value):
    if not isinstance(value, dict):
        return False
    has_schema_keys = any(key in value for key in JSON_SCHEMA_KEYS)
    has_evidence_fields = any(key in value for key in EXECUTION_EVIDENCE_FIELDS)
    return has_schema_keys and not has_evidence_fields


def append(errors, path, message):
    errors.append(f"{path}: {message}")


def validate_execution_evidence(evidence, path):
    errors = []
    required_fields = [
        "executionIsolationLevel",
        "verificationEvidenceLevel",
        "runnerName",
        "separateInvocationIds",
        "schemaValidationCommand",
        "hardCheckCommands",
        "limitations",
    ]
    if not isinstance(evidence, dict):
        return [f"{path}: executionEvidence must be an object"]

    for field in required_fields:
        if field not in evidence:
            append(errors, path, f"executionEvidence missing required field `{field}`")

    execution_level = evidence.get("executionIsolationLevel")
    verification_level = evidence.get("verificationEvidenceLevel")
    runner_name = evidence.get("runnerName")
    invocation_ids = evidence.get("separateInvocationIds")
    schema_command = evidence.get("schemaValidationCommand")
    hard_check_commands = evidence.get("hardCheckCommands")
    limitations = evidence.get("limitations")

    if execution_level not in EXECUTION_ISOLATION_LEVELS:
        append(errors, path, f"invalid executionIsolationLevel: {execution_level!r}")
    if verification_level not in VERIFICATION_EVIDENCE_LEVELS:
        append(errors, path, f"invalid verificationEvidenceLevel: {verification_level!r}")

    if runner_name is not None and not is_nonempty_string(runner_name):
        append(errors, path, "runnerName must be null or a non-empty string")
    if not isinstance(invocation_ids, list):
        append(errors, path, "separateInvocationIds must be an array")
    elif not all(is_nonempty_string(item) for item in invocation_ids):
        append(errors, path, "separateInvocationIds must contain only non-empty strings")
    if schema_command is not None and not is_nonempty_string(schema_command):
        append(errors, path, "schemaValidationCommand must be null or a non-empty string")
    if not isinstance(hard_check_commands, list):
        append(errors, path, "hardCheckCommands must be an array")
    elif not all(is_nonempty_string(item) for item in hard_check_commands):
        append(errors, path, "hardCheckCommands must contain only non-empty strings")
    if not isinstance(limitations, list):
        append(errors, path, "limitations must be an array")
    elif not all(is_nonempty_string(item) for item in limitations):
        append(errors, path, "limitations must contain only non-empty strings")

    if execution_level == "runner-enforced":
        if not is_nonempty_string(runner_name):
            append(errors, path, "runner-enforced requires a non-empty runnerName")
        if not is_nonempty_string_list(invocation_ids):
            append(errors, path, "runner-enforced requires separateInvocationIds")
        elif len(set(invocation_ids)) < 2:
            append(errors, path, "runner-enforced requires at least two distinct invocation ids")

    if execution_level == "schema-validated" and not is_nonempty_string(schema_command):
        append(errors, path, "schema-validated execution evidence requires schemaValidationCommand")

    if verification_level == "schema-validated" and not is_nonempty_string(schema_command):
        append(errors, path, "schema-validated verification evidence requires schemaValidationCommand")

    if verification_level == "hard-check-verified":
        if not is_nonempty_string_list(hard_check_commands):
            append(errors, path, "hard-check-verified requires hardCheckCommands")

    return errors


def object_status(item):
    if "deliveryStatus" in item:
        return item.get("deliveryStatus")
    if "status" in item:
        return item.get("status")
    return None


def get_any_string(item, keys):
    for key in keys:
        value = item.get(key)
        if is_nonempty_string(value):
            return value
    return None


def iter_named_objects(value, path="$"):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from iter_named_objects(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_named_objects(child, f"{path}[{index}]")


def validate_required_hard_checks(item, path):
    errors = []
    checks = item.get("requiredHardChecks", [])
    if checks is None:
        checks = []
    if not isinstance(checks, list):
        return [f"{path}.requiredHardChecks: must be an array"]

    for index, check in enumerate(checks):
        check_path = f"{path}.requiredHardChecks[{index}]"
        if not isinstance(check, dict):
            append(errors, check_path, "hard check must be an object")
            continue
        required = check.get("requiredForComplete") is True
        status = check.get("status")
        command = check.get("command")
        if required and status != "pass":
            append(errors, check_path, "required hard check must be pass for delivery complete")
        if required and not is_nonempty_string(command):
            append(errors, check_path, "required hard check must include command for delivery complete")
    return errors


def validate_gate_arrays(item, path):
    errors = []
    for key in ["blockingChecks", "gateResults"]:
        checks = item.get(key, [])
        if checks is None:
            checks = []
        if not isinstance(checks, list):
            append(errors, f"{path}.{key}", "must be an array")
            continue
        for index, check in enumerate(checks):
            check_path = f"{path}.{key}[{index}]"
            if not isinstance(check, dict):
                append(errors, check_path, "gate result must be an object")
                continue
            status = check.get("status")
            if status in BLOCKING_GATE_STATUSES:
                append(errors, check_path, f"status {status!r} blocks delivery complete")
    return errors


def validate_complete_delivery(item, path):
    errors = []
    evidence = item.get("executionEvidence")
    if not isinstance(evidence, dict):
        append(errors, path, "delivery complete requires executionEvidence")
        return errors

    if evidence.get("executionIsolationLevel") != "runner-enforced":
        append(errors, path, "delivery complete requires executionIsolationLevel runner-enforced")
    if evidence.get("verificationEvidenceLevel") != "hard-check-verified":
        append(errors, path, "delivery complete requires verificationEvidenceLevel hard-check-verified")

    if not get_any_string(item, ["judicialHandoffRef", "requiredJudicialHandoffRef"]):
        append(errors, path, "delivery complete requires judicial handoff artifact reference")
    if not get_any_string(item, ["judicialValidationRef", "validationReportRef", "requiredReportId"]):
        append(errors, path, "delivery complete requires judicial validation/report reference")

    for boolean_key in [
        "noBlockingInScopeViolations",
        "generationAndValidationSeparate",
        "noUnverifiedRequiredGates",
        "noRequiredGateFailedOrNotVerified",
    ]:
        if boolean_key in item and item.get(boolean_key) is not True:
            append(errors, path, f"{boolean_key} must be true for delivery complete")

    blocking_violations = item.get("blockingViolations")
    if isinstance(blocking_violations, list) and blocking_violations:
        append(errors, path, "blockingViolations must be empty for delivery complete")

    unverified_areas = item.get("unverifiedAreas")
    if isinstance(unverified_areas, list) and unverified_areas:
        append(errors, path, "unverifiedAreas must be empty for delivery complete")

    errors.extend(validate_required_hard_checks(item, path))
    errors.extend(validate_gate_arrays(item, path))
    return errors


def validate_document(data, source="<document>"):
    errors = []
    for path, item in iter_named_objects(data):
        evidence = item.get("executionEvidence")
        if evidence is not None and not is_schema_definition(evidence):
            errors.extend(validate_execution_evidence(evidence, f"{source}:{path}"))
        if object_status(item) == "complete":
            errors.extend(validate_complete_delivery(item, f"{source}:{path}"))
    return errors


def delivery_summaries(data, source):
    summaries = []
    for path, item in iter_named_objects(data):
        if "deliveryStatus" not in item:
            continue
        status = item.get("deliveryStatus")
        evidence = item.get("executionEvidence") if isinstance(item.get("executionEvidence"), dict) else {}
        reasons = []
        if status != "complete":
            if evidence.get("executionIsolationLevel") != "runner-enforced":
                reasons.append("runner-enforced isolation not verified")
            if evidence.get("verificationEvidenceLevel") != "hard-check-verified":
                reasons.append("hard-check verification not verified")
            for key in ["blockingChecks", "gateResults"]:
                for check in item.get(key, []) or []:
                    if isinstance(check, dict) and check.get("status") in BLOCKING_GATE_STATUSES:
                        check_id = check.get("checkId") or check.get("gateId") or "<unnamed>"
                        reasons.append(f"{check_id} is {check.get('status')}")
        summaries.append(
            {
                "source": source,
                "path": path,
                "deliveryStatus": status,
                "certification": "complete" if status == "complete" else "blocked",
                "reasons": reasons or ["delivery law evidence satisfied" if status == "complete" else "not complete"],
            }
        )
    return summaries


def main():
    parser = argparse.ArgumentParser(
        description="Validate TOP executionEvidence and delivery complete gates."
    )
    parser.add_argument("files", nargs="+", help="JSON files to validate")
    args = parser.parse_args()

    all_errors = []
    summaries = []
    for item in args.files:
        path = Path(item)
        try:
            data = load_json(path)
        except Exception as exc:
            all_errors.append(f"{path}: invalid JSON: {exc}")
            continue
        all_errors.extend(validate_document(data, str(path)))
        summaries.extend(delivery_summaries(data, str(path)))

    if all_errors:
        print("validate_execution_evidence: FAILED")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("validate_execution_evidence: ARTIFACT_VALID")
    for summary in summaries:
        print(f"{summary['source']}:{summary['path']}: deliveryStatus: {summary['deliveryStatus']}")
        print(f"{summary['source']}:{summary['path']}: certification: {summary['certification']}")
        for reason in summary["reasons"]:
            print(f"{summary['source']}:{summary['path']}: reason: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
