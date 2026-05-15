#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_execution_evidence import validate_document
from update_orchestration_state import derive_and_write_state


AUTHORITY_KEYS = [
    "mayEditFiles",
    "mayValidate",
    "mayRepair",
    "mayReport",
    "mayCertifyDelivery",
]

RUNNER_ENFORCED_ADAPTER_KINDS = {"llm-api", "external-agent-runtime"}
PLACEHOLDER_CONTEXT_SLICES = {
    "fill with minimal required context before launch",
    "not selected",
    "not_verified",
}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value):
    return sha256_text(canonical_json(value))


def sha256_file(path):
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def append(errors, message):
    errors.append(message)


def resolve_inside_root(root, ref, label):
    if not is_nonempty_string(ref):
        raise ValueError(f"{label} must be a non-empty path")
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes runner root: {ref}") from exc
    return resolved


def normalize_command(command):
    if command is None:
        return None
    if not isinstance(command, list) or not command:
        raise ValueError("command must be a non-empty argv array or null")
    if not all(is_nonempty_string(item) for item in command):
        raise ValueError("command argv items must be non-empty strings")
    return command


def find_skill_root(root):
    for candidate in [root, *root.parents]:
        if (candidate / "skill.json").exists() and (candidate / "scripts").exists():
            return candidate
    return root


def resolve_base_ref(root, ref, label):
    if ref is None or ref in {"runner-root", "run-package"}:
        return root
    if ref == "skill-root":
        return find_skill_root(root)
    return resolve_inside_root(root, ref, label)


def resolve_under_base(base, ref, label):
    if not is_nonempty_string(ref):
        raise ValueError(f"{label} must be a non-empty path")
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = base / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes base path: {ref}") from exc
    return resolved


def normalize_command_spec(item, root, label):
    command = item.get("command")
    if command is not None:
        argv = normalize_command(command)
        cwd = resolve_inside_root(root, item.get("cwd") or ".", f"{label} cwd")
        return argv, cwd, command_to_text(argv)

    command_type = item.get("commandType")
    if command_type is None:
        return None, resolve_base_ref(root, item.get("cwdRef"), f"{label} cwdRef"), None

    if command_type != "python-script":
        raise ValueError(f"{label} commandType must be python-script when structured command is used")

    script_ref = item.get("scriptRef")
    args = item.get("args", [])
    if not isinstance(args, list) or not all(is_nonempty_string(arg) for arg in args):
        raise ValueError(f"{label} args must be an array of non-empty strings")

    cwd = resolve_base_ref(root, item.get("cwdRef") or "runner-root", f"{label} cwdRef")
    script_base = resolve_base_ref(root, item.get("scriptBaseRef") or item.get("cwdRef") or "runner-root", f"{label} scriptBaseRef")
    script_path = resolve_under_base(script_base, script_ref, f"{label} scriptRef")
    argv = [sys.executable, "-B", str(script_path), *args]
    display = f"python -B {script_ref}"
    if args:
        display = f"{display} {' '.join(args)}"
    return argv, cwd, display


def run_command(command, cwd, timeout_seconds, env_extra):
    timeout = timeout_seconds if isinstance(timeout_seconds, int) and timeout_seconds > 0 else 300
    env = os.environ.copy()
    env.update(env_extra)
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
    )
    return {
        "exitCode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def validate_capsule_handoff(root, workflow_id, pass_item):
    errors = []
    capsule_ref = pass_item.get("taskCapsuleRef")
    handoff_ref = pass_item.get("handoffArtifactRef")
    try:
        capsule_path = resolve_inside_root(root, capsule_ref, "taskCapsuleRef")
        handoff_path = resolve_inside_root(root, handoff_ref, "handoffArtifactRef")
    except ValueError as exc:
        return [str(exc)]

    if not capsule_path.exists():
        append(errors, f"missing task capsule: {capsule_ref}")
        return errors
    if not handoff_path.exists():
        append(errors, f"missing handoff artifact: {handoff_ref}")
        return errors

    try:
        capsule = load_json(capsule_path)
    except Exception as exc:
        append(errors, f"{capsule_ref}: invalid JSON: {exc}")
        return errors
    try:
        handoff = load_json(handoff_path)
    except Exception as exc:
        append(errors, f"{handoff_ref}: invalid JSON: {exc}")
        return errors

    if capsule.get("workflowId") != workflow_id:
        append(errors, f"{capsule_ref}: workflowId does not match runner workflowId")
    if handoff.get("workflowId") != workflow_id:
        append(errors, f"{handoff_ref}: workflowId does not match runner workflowId")
    if capsule.get("taskId") != handoff.get("taskId"):
        append(errors, f"{handoff_ref}: taskId does not match task capsule")
    if capsule.get("role") != pass_item.get("role"):
        append(errors, f"{capsule_ref}: role does not match runner pass")
    if handoff.get("role") != pass_item.get("role"):
        append(errors, f"{handoff_ref}: role does not match runner pass")
    if handoff.get("passId") != pass_item.get("passId"):
        append(errors, f"{handoff_ref}: passId does not match runner pass")

    for key in AUTHORITY_KEYS:
        if key in capsule and key in handoff and handoff.get(key) and not capsule.get(key):
            append(errors, f"{handoff_ref}: {key} exceeds task capsule authority")

    role = pass_item.get("role")
    if role in {"executive", "repair"}:
        if handoff.get("mayValidate") is not False:
            append(errors, f"{handoff_ref}: {role} handoff must not validate")
        if handoff.get("mayCertifyDelivery") is not False:
            append(errors, f"{handoff_ref}: {role} handoff must not certify delivery")

    errors.extend(validate_document(handoff, str(handoff_path)))
    return errors


def default_context_package_ref(pass_item):
    return pass_item.get("contextPackageRef") or f"contexts/{pass_item.get('passId')}.context-package.json"


def default_invocation_evidence_ref(pass_item):
    return pass_item.get("invocationEvidenceRef") or f"invocations/{pass_item.get('passId')}.invocation-evidence.json"


def materialize_context_package(root, run, pass_item):
    context_ref = default_context_package_ref(pass_item)
    context_path = resolve_inside_root(root, context_ref, "contextPackageRef")
    capsule_ref = pass_item.get("taskCapsuleRef")
    capsule_path = resolve_inside_root(root, capsule_ref, "taskCapsuleRef")
    capsule = load_json(capsule_path)
    package = {
        "schemaVersion": "1.0",
        "workflowId": run.get("workflowId"),
        "runId": run.get("runId"),
        "passId": pass_item.get("passId"),
        "role": pass_item.get("role"),
        "taskCapsuleRef": capsule_ref,
        "handoffArtifactRef": pass_item.get("handoffArtifactRef"),
        "inputReferences": capsule.get("inputReferences", []),
        "contextSlices": capsule.get("contextSlices", []),
        "forbiddenInputs": [
            "full prior chat transcript unless explicitly listed in inputReferences",
            "unbounded agent memory",
            "implementation files outside task capsule scope unless explicitly referenced",
        ],
        "materializedBy": run.get("runnerName"),
        "materializedAt": utc_now(),
        "contextHash": None,
        "limitations": [
            "Context package records bounded inputs; it does not by itself prove LLM context isolation."
        ],
    }
    package["contextHash"] = sha256_json({key: value for key, value in package.items() if key != "contextHash"})
    write_json(context_path, package)
    return context_ref, package


def is_placeholder_context_slice(value):
    return isinstance(value, str) and value.strip().lower() in PLACEHOLDER_CONTEXT_SLICES


def validate_context_package_for_pass(pass_item, context_package):
    errors = []
    if pass_item.get("requiredForDelivery") is not True:
        return errors

    role = pass_item.get("role")
    context_slices = context_package.get("contextSlices") or []
    input_references = context_package.get("inputReferences") or []
    if any(is_placeholder_context_slice(item) for item in context_slices):
        errors.append(f"{pass_item.get('passId')}: required pass context package contains placeholder contextSlices")

    if role in {"judicial", "certification"} and not input_references:
        errors.append(f"{pass_item.get('passId')}: required {role} pass context package has empty inputReferences")

    return errors


def validate_invocation_evidence(evidence, run, pass_item, context_package):
    errors = []
    required = [
        "schemaVersion",
        "workflowId",
        "runId",
        "passId",
        "role",
        "adapterKind",
        "invocationId",
        "contextId",
        "runnerName",
        "taskCapsuleRef",
        "contextPackageRef",
        "handoffArtifactRef",
        "contextHash",
        "freshContext",
        "receivedOnlyContextPackage",
        "modelInvocationEvidence",
        "limitations",
    ]
    if not isinstance(evidence, dict):
        return ["invocation evidence must be an object"]
    for field in required:
        if field not in evidence:
            errors.append(f"invocation evidence missing required field `{field}`")
    if evidence.get("workflowId") != run.get("workflowId"):
        errors.append("invocation evidence workflowId does not match runner workflowId")
    if evidence.get("runId") != run.get("runId"):
        errors.append("invocation evidence runId does not match runner runId")
    if evidence.get("passId") != pass_item.get("passId"):
        errors.append("invocation evidence passId does not match runner pass")
    if evidence.get("role") != pass_item.get("role"):
        errors.append("invocation evidence role does not match runner pass")
    if evidence.get("taskCapsuleRef") != pass_item.get("taskCapsuleRef"):
        errors.append("invocation evidence taskCapsuleRef does not match runner pass")
    if evidence.get("handoffArtifactRef") != pass_item.get("handoffArtifactRef"):
        errors.append("invocation evidence handoffArtifactRef does not match runner pass")
    if evidence.get("contextHash") != context_package.get("contextHash"):
        errors.append("invocation evidence contextHash does not match materialized context package")
    for field in ["invocationId", "contextId", "adapterKind", "runnerName"]:
        if not is_nonempty_string(evidence.get(field)):
            errors.append(f"invocation evidence `{field}` must be a non-empty string")
    if not isinstance(evidence.get("limitations"), list):
        errors.append("invocation evidence limitations must be an array")
    for field in ["freshContext", "receivedOnlyContextPackage", "modelInvocationEvidence"]:
        if not isinstance(evidence.get(field), bool):
            errors.append(f"invocation evidence `{field}` must be a boolean")
    return errors


def build_runner_observed_invocation_evidence(
    root,
    run,
    pass_item,
    context_ref,
    context_package,
    command,
    started_at,
    ended_at,
    exit_code,
    executed,
):
    handoff_path = resolve_inside_root(root, pass_item.get("handoffArtifactRef"), "handoffArtifactRef")
    adapter_kind = pass_item.get("adapterKind") or "process"
    return {
        "schemaVersion": "1.0",
        "workflowId": run.get("workflowId"),
        "runId": run.get("runId"),
        "passId": pass_item.get("passId"),
        "role": pass_item.get("role"),
        "adapterKind": adapter_kind,
        "invocationId": pass_item.get("invocationId"),
        "contextId": pass_item.get("contextId"),
        "runnerName": run.get("runnerName"),
        "processId": None,
        "command": command_to_text(command),
        "startedAt": started_at,
        "endedAt": ended_at,
        "exitCode": exit_code,
        "taskCapsuleRef": pass_item.get("taskCapsuleRef"),
        "contextPackageRef": context_ref,
        "handoffArtifactRef": pass_item.get("handoffArtifactRef"),
        "contextHash": context_package.get("contextHash"),
        "handoffHash": sha256_file(handoff_path),
        "freshContext": bool(executed),
        "receivedOnlyContextPackage": False,
        "modelInvocationEvidence": False,
        "limitations": [
            "Runner-observed process evidence is not proof of separate LLM context.",
            "An adapter must write invocation evidence with modelInvocationEvidence=true to support runner-enforced isolation.",
        ],
    }


def load_or_write_invocation_evidence(
    root,
    run,
    pass_item,
    context_ref,
    context_package,
    command,
    started_at,
    ended_at,
    exit_code,
    executed,
):
    evidence_ref = default_invocation_evidence_ref(pass_item)
    evidence_path = resolve_inside_root(root, evidence_ref, "invocationEvidenceRef")
    if evidence_path.exists():
        evidence = load_json(evidence_path)
        if (
            evidence.get("modelInvocationEvidence") is not True
            and evidence.get("contextHash") != context_package.get("contextHash")
        ):
            evidence = build_runner_observed_invocation_evidence(
                root,
                run,
                pass_item,
                context_ref,
                context_package,
                command,
                started_at,
                ended_at,
                exit_code,
                executed,
            )
            write_json(evidence_path, evidence)
    else:
        evidence = build_runner_observed_invocation_evidence(
            root,
            run,
            pass_item,
            context_ref,
            context_package,
            command,
            started_at,
            ended_at,
            exit_code,
            executed,
        )
        write_json(evidence_path, evidence)
    errors = validate_invocation_evidence(evidence, run, pass_item, context_package)
    return evidence_ref, evidence, errors


def load_handoff_status(root, pass_item):
    try:
        handoff_path = resolve_inside_root(root, pass_item.get("handoffArtifactRef"), "handoffArtifactRef")
        handoff = load_json(handoff_path)
    except Exception:
        return None
    return handoff.get("status")


def handoff_status_to_pass_result(status):
    if status in {"done", "complete"}:
        return "pass"
    if status == "failed":
        return "fail"
    if status == "blocked":
        return "blocked"
    if status in {"not-started", "in-progress", "not-verified", "not-certified", "partial"}:
        return "not_verified"
    return "not_verified"


def validate_runner_shape(run):
    errors = []
    required_fields = [
        "schemaVersion",
        "workflowId",
        "runId",
        "runnerName",
        "mode",
        "runnerCapabilities",
        "passes",
        "hardChecks",
        "limitations",
    ]
    for field in required_fields:
        if field not in run:
            append(errors, f"runner workflow missing required field `{field}`")

    if not isinstance(run.get("passes"), list) or not run.get("passes"):
        append(errors, "passes must be a non-empty array")
    if not isinstance(run.get("hardChecks"), list):
        append(errors, "hardChecks must be an array")

    pass_ids = set()
    invocation_ids = set()
    context_ids = set()
    for index, pass_item in enumerate(run.get("passes", [])):
        path = f"passes[{index}]"
        for field in [
            "passId",
            "role",
            "taskCapsuleRef",
            "handoffArtifactRef",
            "invocationId",
            "contextId",
            "requiredForDelivery",
        ]:
            if field not in pass_item:
                append(errors, f"{path} missing required field `{field}`")
        pass_id = pass_item.get("passId")
        invocation_id = pass_item.get("invocationId")
        context_id = pass_item.get("contextId")
        adapter_kind = pass_item.get("adapterKind", "process")
        if adapter_kind not in {"process", "llm-api", "external-agent-runtime", "manual"}:
            append(errors, f"{path} invalid adapterKind: {adapter_kind!r}")
        if pass_id in pass_ids:
            append(errors, f"duplicate passId: {pass_id}")
        if invocation_id in invocation_ids:
            append(errors, f"duplicate invocationId: {invocation_id}")
        if context_id in context_ids:
            append(errors, f"duplicate contextId: {context_id}")
        pass_ids.add(pass_id)
        invocation_ids.add(invocation_id)
        context_ids.add(context_id)

    return errors


def runner_isolation_accepted(run, pass_results, accept_external_runner_evidence):
    capabilities = run.get("runnerCapabilities", {})
    required_pass_ids = {
        item.get("passId")
        for item in run.get("passes", [])
        if item.get("requiredForDelivery") is True
    }
    required_results = [
        item
        for item in pass_results
        if item.get("passId") in required_pass_ids
    ]
    invocation_ids = {
        item.get("invocationId")
        for item in required_results
        if is_nonempty_string(item.get("invocationId"))
    }
    context_ids = {
        item.get("contextId")
        for item in required_results
        if is_nonempty_string(item.get("contextId"))
    }
    required_evidence_is_strong = bool(required_results) and all(
        item.get("adapterKind") in RUNNER_ENFORCED_ADAPTER_KINDS
        and item.get("freshContext") is True
        and item.get("receivedOnlyContextPackage") is True
        and item.get("modelInvocationEvidence") is True
        for item in required_results
    )
    return (
        accept_external_runner_evidence
        and capabilities.get("launchesSeparateInvocations") is True
        and capabilities.get("isolatesContexts") is True
        and len(invocation_ids) >= len(required_results)
        and len(context_ids) >= len(required_results)
        and len(required_results) >= 2
        and required_evidence_is_strong
    )


def command_to_text(command):
    return None if command is None else " ".join(command)


def execute_or_verify_pass(root, run, pass_item, execute_passes):
    errors = []
    exit_code = None
    status = "pass"
    command = None
    command_text = None
    command_present = pass_item.get("command") is not None or pass_item.get("commandType") is not None
    started_at = None
    ended_at = None
    context_ref = default_context_package_ref(pass_item)
    evidence_ref = default_invocation_evidence_ref(pass_item)
    evidence = {}

    try:
        context_ref, context_package = materialize_context_package(root, run, pass_item)
        errors.extend(validate_context_package_for_pass(pass_item, context_package))
        if errors and status == "pass":
            status = "fail"
    except Exception as exc:
        context_package = {}
        errors.append(f"context package materialization failed: {exc}")
        status = "fail"

    if command_present:
        try:
            command, command_cwd, command_text = normalize_command_spec(pass_item, root, "pass")
        except ValueError as exc:
            errors.append(str(exc))
            status = "fail"

    if execute_passes:
        if command is None:
            errors.append("pass execution requested but pass command is missing")
            status = "not_verified"
        else:
            try:
                started_at = utc_now()
                result = run_command(
                    command,
                    command_cwd,
                    pass_item.get("timeoutSeconds"),
                    {
                        "TOP_WORKFLOW_ID": run.get("workflowId", ""),
                        "TOP_RUN_ID": run.get("runId", ""),
                        "TOP_PASS_ID": pass_item.get("passId", ""),
                        "TOP_ROLE": pass_item.get("role", ""),
                        "TOP_TASK_CAPSULE": pass_item.get("taskCapsuleRef", ""),
                        "TOP_HANDOFF_ARTIFACT": pass_item.get("handoffArtifactRef", ""),
                        "TOP_CONTEXT_PACKAGE": context_ref,
                        "TOP_INVOCATION_EVIDENCE": evidence_ref,
                    },
                )
                ended_at = utc_now()
                exit_code = result["exitCode"]
                if exit_code != 0:
                    status = "fail"
                    errors.append(f"pass command exited {exit_code}: {result['stderr'] or result['stdout']}")
            except Exception as exc:
                ended_at = utc_now()
                status = "fail"
                errors.append(f"pass command failed: {exc}")

    if context_package:
        try:
            evidence_ref, evidence, evidence_errors = load_or_write_invocation_evidence(
                root,
                run,
                pass_item,
                context_ref,
                context_package,
                command,
                started_at,
                ended_at,
                exit_code,
                execute_passes and command is not None,
            )
            errors.extend(evidence_errors)
            if evidence_errors and status == "pass":
                status = "fail"
        except Exception as exc:
            errors.append(f"invocation evidence failed: {exc}")
            if status == "pass":
                status = "fail"

    handoff_errors = validate_capsule_handoff(root, run.get("workflowId"), pass_item)
    if handoff_errors:
        status = "fail"
        errors.extend(handoff_errors)
    elif status == "pass":
        handoff_status = load_handoff_status(root, pass_item)
        mapped_status = handoff_status_to_pass_result(handoff_status)
        if mapped_status != "pass":
            status = mapped_status
            if mapped_status == "fail":
                errors.append(f"handoff status is failed for pass {pass_item.get('passId')}")

    if (
        pass_item.get("requiredForDelivery") is True
        and not command_present
        and evidence.get("modelInvocationEvidence") is not True
        and status == "pass"
    ):
        status = "not_verified"

    return {
        "passId": pass_item.get("passId"),
        "role": pass_item.get("role"),
        "invocationId": evidence.get("invocationId") or pass_item.get("invocationId"),
        "contextId": evidence.get("contextId") or pass_item.get("contextId"),
        "adapterKind": evidence.get("adapterKind") or pass_item.get("adapterKind") or "process",
        "contextPackageRef": context_ref,
        "invocationEvidenceRef": evidence_ref,
        "freshContext": evidence.get("freshContext") is True,
        "receivedOnlyContextPackage": evidence.get("receivedOnlyContextPackage") is True,
        "modelInvocationEvidence": evidence.get("modelInvocationEvidence") is True,
        "status": status,
        "exitCode": exit_code,
        "errors": errors,
    }


def execute_or_verify_hard_check(root, check, execute_hard_checks):
    errors = []
    exit_code = None
    evidence = []
    command_text = None
    status = "not_verified"

    try:
        command, command_cwd, command_text = normalize_command_spec(check, root, f"hard check {check.get('id')}")
    except ValueError as exc:
        command = None
        if check.get("requiredForComplete") is True:
            errors.append(str(exc))
            status = "fail"
        else:
            status = "not_applicable"

    if execute_hard_checks:
        if command is None:
            if check.get("requiredForComplete") is True:
                errors.append("required hard check command is missing")
                status = "fail"
            else:
                status = "not_applicable"
        else:
            try:
                result = run_command(command, command_cwd, check.get("timeoutSeconds"), {})
                exit_code = result["exitCode"]
                if result["stdout"]:
                    evidence.append(result["stdout"])
                if result["stderr"]:
                    evidence.append(result["stderr"])
                status = "pass" if exit_code == 0 else "fail"
                if exit_code != 0:
                    errors.append(f"hard check exited {exit_code}")
            except Exception as exc:
                status = "fail"
                errors.append(f"hard check failed: {exc}")
    elif check.get("requiredForComplete") is not True:
        status = "not_applicable"

    if check.get("requiredForComplete") is True and status != "pass":
        errors.append("required hard check did not pass")

    return {
        "id": check.get("id"),
        "requiredForComplete": check.get("requiredForComplete") is True,
        "status": status,
        "command": command_text,
        "exitCode": exit_code,
        "evidence": evidence + errors,
    }


def validate_delivery_certification(root, delivery_ref):
    if delivery_ref is None:
        return {
            "status": "not_applicable",
            "ref": None,
            "errors": [],
        }
    errors = []
    try:
        path = resolve_inside_root(root, delivery_ref, "deliveryCertificationRef")
        data = load_json(path)
        errors.extend(validate_document(data, str(path)))
    except Exception as exc:
        errors.append(str(exc))
    return {
        "status": "pass" if not errors else "fail",
        "ref": delivery_ref,
        "errors": errors,
    }


def build_execution_evidence(run, pass_results, hard_check_results, accept_external_runner_evidence, execute_hard_checks):
    required_checks = [item for item in hard_check_results if item.get("requiredForComplete")]
    required_checks_pass = bool(required_checks) and all(item.get("status") == "pass" for item in required_checks)
    hard_check_commands = [
        item.get("command")
        for item in hard_check_results
        if item.get("command") and item.get("status") == "pass"
    ]
    runner_isolation = runner_isolation_accepted(run, pass_results, accept_external_runner_evidence)

    if runner_isolation:
        execution_level = "runner-enforced"
    else:
        execution_level = "schema-validated"

    if execute_hard_checks and required_checks_pass:
        verification_level = "hard-check-verified"
    else:
        verification_level = "schema-validated"

    limitations = list(run.get("limitations") or [])
    if not runner_isolation:
        limitations.append("Runner isolation was not accepted as runner-enforced evidence.")
    if not execute_hard_checks:
        limitations.append("Hard checks were not executed in this runner pass.")

    return {
        "executionIsolationLevel": execution_level,
        "verificationEvidenceLevel": verification_level,
        "runnerName": run.get("runnerName"),
        "separateInvocationIds": [
            item.get("invocationId")
            for item in pass_results
            if is_nonempty_string(item.get("invocationId"))
        ],
        "schemaValidationCommand": "python scripts/top_protocol_runner.py <runner-workflow.json>",
        "hardCheckCommands": hard_check_commands,
        "limitations": limitations or ["No limitations reported."],
    }


def run_workflow(
    run,
    root,
    execute_passes=False,
    execute_hard_checks=False,
    accept_external_runner_evidence=False,
):
    errors = validate_runner_shape(run)
    pass_results = []
    hard_check_results = []

    if not errors:
        for pass_item in run.get("passes", []):
            pass_results.append(execute_or_verify_pass(root, run, pass_item, execute_passes))

        for check in run.get("hardChecks", []):
            hard_check_results.append(execute_or_verify_hard_check(root, check, execute_hard_checks))

    delivery_result = validate_delivery_certification(root, run.get("deliveryCertificationRef"))

    report = {
        "schemaVersion": run.get("schemaVersion", "1.0"),
        "workflowId": run.get("workflowId"),
        "runId": run.get("runId"),
        "runnerName": run.get("runnerName"),
        "runnerStatus": "pass",
        "executionEvidence": build_execution_evidence(
            run,
            pass_results,
            hard_check_results,
            accept_external_runner_evidence,
            execute_hard_checks,
        ),
        "passResults": pass_results,
        "hardCheckResults": hard_check_results,
        "deliveryCertificationResult": delivery_result,
        "limitations": list(run.get("limitations") or []),
    }

    for result in pass_results:
        errors.extend(result.get("errors", []))
    required_passes_by_id = {
        item.get("passId"): item.get("requiredForDelivery") is True
        for item in run.get("passes", [])
    }
    required_pass_not_verified = any(
        required_passes_by_id.get(result.get("passId")) and result.get("status") != "pass"
        for result in pass_results
    )
    for result in hard_check_results:
        if result.get("requiredForComplete") and result.get("status") != "pass":
            errors.append(f"required hard check failed or was not verified: {result.get('id')}")
    if delivery_result.get("status") == "fail":
        errors.extend(delivery_result.get("errors", []))

    evidence_errors = validate_document(report, "runner-report")
    errors.extend(evidence_errors)

    if errors:
        report["runnerStatus"] = "fail"
        report["limitations"].append("Runner failed with blocking errors.")
    elif required_pass_not_verified:
        report["runnerStatus"] = "not_verified"
        report["limitations"].append("One or more required pass handoffs are not pass/complete.")
    else:
        report["runnerStatus"] = "pass"

    return report, errors


def update_run_state(root, runner_workflow_ref, runner_report_ref):
    return derive_and_write_state(
        root,
        refs={
            "runnerWorkflow": runner_workflow_ref,
            "runnerReport": runner_report_ref,
        },
    )


def main():
    parser = argparse.ArgumentParser(description="Run or validate a TOP runner workflow.")
    parser.add_argument("runner_workflow", help="Path to runner workflow JSON")
    parser.add_argument("--root", default=".", help="Root directory for refs and commands")
    parser.add_argument("--execute-passes", action="store_true", help="Execute pass commands")
    parser.add_argument("--execute-hard-checks", action="store_true", help="Execute hard-check commands")
    parser.add_argument(
        "--accept-external-runner-evidence",
        action="store_true",
        help="Allow report executionIsolationLevel runner-enforced when invocation evidence is present",
    )
    parser.add_argument("--report-out", help="Write runner report JSON to this path")
    parser.add_argument(
        "--skip-state-update",
        action="store_true",
        help="Do not refresh run-state.json after writing the runner report",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        runner_workflow_path = resolve_inside_root(root, args.runner_workflow, "runner_workflow")
        run = load_json(runner_workflow_path)
    except Exception as exc:
        print(f"top_protocol_runner: FAILED\n- {exc}", file=sys.stderr)
        return 2

    report, errors = run_workflow(
        run,
        root,
        execute_passes=args.execute_passes,
        execute_hard_checks=args.execute_hard_checks,
        accept_external_runner_evidence=args.accept_external_runner_evidence,
    )

    if args.report_out:
        try:
            report_path = resolve_inside_root(root, args.report_out, "report_out")
            write_json(report_path, report)
        except Exception as exc:
            errors.append(f"failed to write report: {exc}")
        if not args.skip_state_update:
            try:
                update_run_state(root, args.runner_workflow, args.report_out)
            except Exception as exc:
                errors.append(f"failed to update run state: {exc}")

    if errors:
        print("top_protocol_runner: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("top_protocol_runner: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
