#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from update_orchestration_state import DEFAULT_ARTIFACT_REFS, derive_state, resolve_inside
from validate_execution_evidence import validate_document, validate_execution_evidence


VALID_NON_COMPLETE_STATES = {
    "runner-verified",
    "judicial-validated",
    "not-certified",
    "failed",
}
PASS_STATUSES = {"done", "complete"}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def sha256_file(path):
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(errors, message):
    errors.append(message)


def load_required_json(run_root, ref, label, errors):
    try:
        path = resolve_inside(run_root, ref, label)
    except Exception as exc:
        add(errors, f"{label}: {exc}")
        return None
    if not path.exists():
        add(errors, f"{label} missing: {ref}")
        return None
    try:
        return load_json(path)
    except Exception as exc:
        add(errors, f"{label} invalid JSON: {exc}")
        return None


def load_optional_json(run_root, ref, label, errors):
    try:
        path = resolve_inside(run_root, ref, label)
    except Exception as exc:
        add(errors, f"{label}: {exc}")
        return None
    if not path.exists():
        return None
    try:
        return load_json(path)
    except Exception as exc:
        add(errors, f"{label} invalid JSON: {exc}")
        return None


def refs_from_args(args):
    refs = dict(DEFAULT_ARTIFACT_REFS)
    refs.update(
        {
            "runnerWorkflow": args.runner_workflow,
            "runnerReport": args.runner_report,
            "judicialHandoff": args.judicial_handoff,
            "deliveryCertification": args.delivery_certification,
            "certificationSnapshot": args.certification_snapshot,
        }
    )
    return refs


def workflow_passes_by_id(runner_workflow):
    return {
        item.get("passId"): item
        for item in runner_workflow.get("passes", []) or []
        if isinstance(item, dict) and is_nonempty_string(item.get("passId"))
    }


def pass_results_by_id(runner_report):
    return {
        item.get("passId"): item
        for item in runner_report.get("passResults", []) or []
        if isinstance(item, dict) and is_nonempty_string(item.get("passId"))
    }


def required_pass_ids(runner_workflow):
    return {
        item.get("passId")
        for item in runner_workflow.get("passes", []) or []
        if isinstance(item, dict) and item.get("requiredForDelivery") is True
    }


def validate_identity(runner_workflow, runner_report, judicial_handoff, certification, run_state, snapshot, errors):
    workflow_id = runner_workflow.get("workflowId")
    run_id = runner_workflow.get("runId")
    checks = [
        ("runner report workflowId", runner_report.get("workflowId"), workflow_id),
        ("runner report runId", runner_report.get("runId"), run_id),
        ("judicial handoff workflowId", judicial_handoff.get("workflowId"), workflow_id),
        ("delivery certification workflowId", certification.get("workflowId"), workflow_id),
        ("run state workflowId", run_state.get("workflowId"), workflow_id),
        ("run state runId", run_state.get("runId"), run_id),
    ]
    if isinstance(snapshot, dict):
        checks.extend(
            [
                ("certification snapshot workflowId", snapshot.get("workflowId"), workflow_id),
                ("certification snapshot runId", snapshot.get("runId"), run_id),
            ]
        )
    for label, actual, expected in checks:
        if actual != expected:
            add(errors, f"{label} mismatch: expected {expected!r}, got {actual!r}")


def validate_runner_consistency(runner_workflow, runner_report, errors):
    if runner_report.get("runnerStatus") != "pass":
        add(errors, f"runner report status must be pass for a valid run package: {runner_report.get('runnerStatus')}")

    workflow_passes = workflow_passes_by_id(runner_workflow)
    results = pass_results_by_id(runner_report)
    for pass_id, pass_item in workflow_passes.items():
        result = results.get(pass_id)
        if not result:
            add(errors, f"runner report missing pass result for {pass_id}")
            continue
        if result.get("role") != pass_item.get("role"):
            add(errors, f"{pass_id}: role mismatch between workflow and runner report")
        if result.get("status") != "pass" and pass_item.get("requiredForDelivery") is True:
            add(errors, f"{pass_id}: required pass status is {result.get('status')}, expected pass")

    for pass_id in results:
        if pass_id not in workflow_passes:
            add(errors, f"runner report has pass result not listed in workflow: {pass_id}")

    required_results = [results.get(pass_id) for pass_id in required_pass_ids(runner_workflow) if pass_id in results]
    if required_pass_ids(runner_workflow) and not required_results:
        add(errors, "runner report has no results for delivery-required passes")


def validate_required_pass_invocation_evidence(runner_workflow, runner_report, delivery_status, errors):
    if delivery_status != "complete":
        return

    results = pass_results_by_id(runner_report)
    required_invocation_ids = []
    for pass_id in sorted(required_pass_ids(runner_workflow)):
        result = results.get(pass_id)
        if not result:
            continue
        if result.get("status") != "pass":
            continue

        invocation_id = result.get("invocationId")
        context_id = result.get("contextId")
        if not is_nonempty_string(invocation_id):
            add(errors, f"{pass_id}: delivery complete required pass lacks invocationId")
        else:
            required_invocation_ids.append(invocation_id)
        if not is_nonempty_string(context_id):
            add(errors, f"{pass_id}: delivery complete required pass lacks contextId")
        if not is_nonempty_string(result.get("invocationEvidenceRef")):
            add(errors, f"{pass_id}: delivery complete required pass lacks invocationEvidenceRef")
        if result.get("freshContext") is not True:
            add(errors, f"{pass_id}: delivery complete required pass must have freshContext true")
        if result.get("receivedOnlyContextPackage") is not True:
            add(errors, f"{pass_id}: delivery complete required pass must have receivedOnlyContextPackage true")
        if result.get("modelInvocationEvidence") is not True:
            add(errors, f"{pass_id}: delivery complete required pass must have modelInvocationEvidence true")

    if len(required_invocation_ids) >= 2 and len(set(required_invocation_ids)) != len(required_invocation_ids):
        add(errors, "delivery complete required passes must use distinct invocation ids")


def validate_post_repair_judicial(run_root, runner_workflow, runner_report, judicial_handoff, delivery_status, errors):
    if delivery_status != "complete":
        return

    pass_order = {
        item.get("passId"): index
        for index, item in enumerate(runner_workflow.get("passes", []) or [])
        if isinstance(item, dict) and is_nonempty_string(item.get("passId"))
    }
    completed_repairs = [
        item.get("passId")
        for item in runner_report.get("passResults", []) or []
        if isinstance(item, dict)
        and item.get("role") == "repair"
        and item.get("status") == "pass"
        and is_nonempty_string(item.get("passId"))
    ]
    if not completed_repairs:
        return

    repair_indexes = [pass_order.get(pass_id) for pass_id in completed_repairs if pass_order.get(pass_id) is not None]
    judicial_pass_id = judicial_handoff.get("passId")
    judicial_index = pass_order.get(judicial_pass_id)
    if judicial_index is None:
        add(errors, f"delivery complete after repair requires known final judicial pass, got {judicial_pass_id!r}")
        return
    if not repair_indexes:
        add(errors, "delivery complete after repair requires repair pass order evidence")
        return
    if judicial_index <= max(repair_indexes):
        add(errors, "delivery complete after repair requires a judicial handoff from a pass after the latest repair pass")
        return

    repaired_refs = []
    for pass_item in runner_workflow.get("passes", []) or []:
        if not isinstance(pass_item, dict) or pass_item.get("role") != "repair":
            continue
        if pass_item.get("passId") not in completed_repairs:
            continue
        handoff = load_optional_json(run_root, pass_item.get("handoffArtifactRef"), "repair handoff", errors)
        if not isinstance(handoff, dict):
            continue
        for ref in handoff.get("filesChanged", []) or []:
            if isinstance(ref, str) and not ref.startswith("handoffs/") and ref not in repaired_refs:
                repaired_refs.append(ref)

    if repaired_refs:
        judicial_inputs = set(judicial_handoff.get("inputReferences", []) or [])
        judicial_files_read = set(judicial_handoff.get("filesRead", []) or [])
        missing = [
            ref for ref in repaired_refs
            if ref not in judicial_inputs and ref not in judicial_files_read
        ]
        if missing:
            add(errors, f"delivery complete after repair requires final judicial handoff to read repaired refs: {', '.join(missing)}")


def validate_judicial_handoff(judicial_handoff, runner_workflow, errors):
    judicial_ids = {
        item.get("passId")
        for item in runner_workflow.get("passes", []) or []
        if isinstance(item, dict) and item.get("role") == "judicial"
    }
    if judicial_handoff.get("role") != "judicial":
        add(errors, "judicial handoff role must be judicial")
    if judicial_handoff.get("passId") not in judicial_ids:
        add(errors, "judicial handoff passId must match a judicial pass in runner workflow")
    if judicial_handoff.get("status") not in PASS_STATUSES:
        add(errors, "judicial handoff status must be done or complete")
    if judicial_handoff.get("mayValidate") is not True:
        add(errors, "judicial handoff must have mayValidate true")
    if judicial_handoff.get("mayEditFiles") is not False:
        add(errors, "judicial handoff must have mayEditFiles false")
    if judicial_handoff.get("mayRepair") is not False:
        add(errors, "judicial handoff must have mayRepair false")
    if judicial_handoff.get("mayCertifyDelivery") is not False:
        add(errors, "judicial handoff must not certify delivery")


def validate_snapshot(run_root, snapshot, delivery_status, stale, errors):
    if delivery_status == "complete" and not isinstance(snapshot, dict):
        add(errors, "delivery complete requires certification snapshot")
        return
    if not isinstance(snapshot, dict):
        return
    artifacts = snapshot.get("artifacts", [])
    if delivery_status == "complete" and not artifacts:
        add(errors, "delivery complete requires non-empty certification snapshot artifacts")
    if delivery_status == "complete" and snapshot.get("snapshotStatus") != "current":
        stale.append(f"certification snapshot status is {snapshot.get('snapshotStatus')}")
    for item in artifacts or []:
        if not isinstance(item, dict):
            add(errors, "certification snapshot artifact entry must be an object")
            continue
        ref = item.get("ref")
        expected = item.get("sha256")
        try:
            actual = sha256_file(resolve_inside(run_root, ref, "snapshot artifact"))
        except Exception as exc:
            stale.append(f"{ref}: {exc}")
            continue
        if actual != expected:
            stale.append(f"{ref}: expected {expected}, actual {actual}")


def validate_state(run_root, refs, run_state, stale, errors):
    try:
        derived = derive_state(run_root, refs)
    except Exception as exc:
        add(errors, f"could not derive run state: {exc}")
        return None

    persisted_state = run_state.get("currentState")
    derived_state = derived.get("currentState")
    if persisted_state != derived_state:
        if derived_state == "stale":
            stale.append(f"run-state.json currentState={persisted_state}, derived currentState=stale")
        else:
            add(errors, f"run-state.json currentState mismatch: persisted={persisted_state}, derived={derived_state}")
    if run_state.get("artifactRefs") != refs:
        add(errors, "run-state.json artifactRefs do not match verifier refs")
    return derived


def validate_run(args):
    run_root = Path(args.root).resolve()
    errors = []
    stale = []
    refs = refs_from_args(args)

    runner_workflow = load_required_json(run_root, refs["runnerWorkflow"], "runner workflow", errors)
    runner_report = load_required_json(run_root, refs["runnerReport"], "runner report", errors)
    judicial_handoff = load_required_json(run_root, refs["judicialHandoff"], "judicial handoff", errors)
    certification = load_required_json(run_root, refs["deliveryCertification"], "delivery certification", errors)
    run_state = load_required_json(run_root, args.state, "run state", errors)
    snapshot = load_optional_json(run_root, refs["certificationSnapshot"], "certification snapshot", errors)

    if errors:
        return "RUN_INVALID", None, errors, stale

    validate_identity(runner_workflow, runner_report, judicial_handoff, certification, run_state, snapshot, errors)
    validate_runner_consistency(runner_workflow, runner_report, errors)
    validate_judicial_handoff(judicial_handoff, runner_workflow, errors)

    for label, artifact in [
        ("runner-report", runner_report),
        ("delivery-certification", certification),
    ]:
        evidence_errors = validate_document(artifact, label)
        errors.extend(evidence_errors)
    if "executionEvidence" in judicial_handoff:
        errors.extend(validate_execution_evidence(judicial_handoff.get("executionEvidence"), "judicial-handoff"))

    delivery_status = certification.get("deliveryStatus")
    validate_required_pass_invocation_evidence(runner_workflow, runner_report, delivery_status, errors)
    validate_post_repair_judicial(run_root, runner_workflow, runner_report, judicial_handoff, delivery_status, errors)
    validate_snapshot(run_root, snapshot, delivery_status, stale, errors)
    derived_state = validate_state(run_root, refs, run_state, stale, errors)

    current_state = run_state.get("currentState")
    if delivery_status == "complete":
        if current_state != "certified":
            if current_state == "stale" or (derived_state and derived_state.get("currentState") == "stale"):
                stale.append("delivery complete run is stale")
            else:
                add(errors, f"delivery complete requires currentState certified, got {current_state}")
    elif delivery_status == "not-certified":
        if current_state not in VALID_NON_COMPLETE_STATES:
            add(errors, f"not-certified run has incompatible currentState: {current_state}")
    else:
        add(errors, f"unsupported deliveryStatus: {delivery_status!r}")

    if errors:
        return "RUN_INVALID", delivery_status, errors, stale
    if stale:
        return "RUN_STALE", delivery_status, errors, stale
    if delivery_status == "complete":
        return "RUN_VALID certified", delivery_status, errors, stale
    return "RUN_VALID not-certified", delivery_status, errors, stale


def main():
    parser = argparse.ArgumentParser(description="Validate one TOP orchestration run package.")
    parser.add_argument("--root", required=True, help="Run package root")
    parser.add_argument("--runner-workflow", default="runner/runner-workflow.json")
    parser.add_argument("--runner-report", default="runner/runner-report.json")
    parser.add_argument("--judicial-handoff", default="handoffs/judicial.handoff.json")
    parser.add_argument("--delivery-certification", default="reports/delivery-certification.json")
    parser.add_argument("--certification-snapshot", default="reports/certification-snapshot.json")
    parser.add_argument("--state", default="run-state.json")
    args = parser.parse_args()

    status, delivery_status, errors, stale = validate_run(args)
    print(f"validate_orchestration_run: {status}")
    if delivery_status:
        print(f"deliveryStatus: {delivery_status}")
    for item in stale:
        print(f"- stale: {item}")
    for item in errors:
        print(f"- invalid: {item}")

    if status.startswith("RUN_VALID"):
        return 0
    if status == "RUN_STALE":
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
