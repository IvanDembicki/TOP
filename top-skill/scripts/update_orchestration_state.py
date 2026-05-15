#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True


STATE_ORDER = {
    "scaffolded": 0,
    "passes-executed": 1,
    "runner-verified": 2,
    "judicial-validated": 3,
    "not-certified": 4,
    "certified": 5,
    "stale": 6,
}

TERMINAL_OR_RETRY_STATES = {"failed", "not-certified", "stale"}
PASS_STATUSES = {"done", "complete"}
DEFAULT_ARTIFACT_REFS = {
    "runnerWorkflow": "runner/runner-workflow.json",
    "runnerReport": "runner/runner-report.json",
    "judicialHandoff": "handoffs/judicial.handoff.json",
    "deliveryCertification": "reports/delivery-certification.json",
    "certificationSnapshot": "reports/certification-snapshot.json",
}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_optional_json(path):
    if not path.exists():
        return None
    return load_json(path)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def sha256_file(path):
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_inside(root, ref, label):
    if not is_nonempty_string(ref):
        raise ValueError(f"{label} must be a non-empty path")
    candidate = Path(ref)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes run root: {ref}") from exc
    return resolved


def evidence(check_id, status, details):
    return {
        "checkId": check_id,
        "status": status,
        "details": details if details else ["No evidence recorded."],
    }


def pass_results(runner_report):
    if not isinstance(runner_report, dict):
        return []
    return [item for item in runner_report.get("passResults", []) or [] if isinstance(item, dict)]


def runner_has_failed(runner_report):
    if not isinstance(runner_report, dict):
        return False
    if runner_report.get("runnerStatus") in {"fail", "blocked"}:
        return True
    for item in pass_results(runner_report):
        if item.get("status") in {"fail", "blocked"}:
            return True
    for item in runner_report.get("hardCheckResults", []) or []:
        if isinstance(item, dict) and item.get("requiredForComplete") is True and item.get("status") == "fail":
            return True
    return False


def runner_is_verified(runner_report):
    if not isinstance(runner_report, dict):
        return False
    required_results = [
        item for item in pass_results(runner_report)
        if item.get("role") in {"executive", "judicial", "certification"}
    ]
    return runner_report.get("runnerStatus") == "pass" and bool(required_results)


def passes_executed(run_root, runner_report):
    if isinstance(runner_report, dict) and pass_results(runner_report):
        return True
    handoffs_root = run_root / "handoffs"
    if not handoffs_root.exists():
        return False
    for handoff_path in handoffs_root.glob("*.handoff.json"):
        try:
            handoff = load_json(handoff_path)
        except Exception:
            continue
        if handoff.get("status") in PASS_STATUSES:
            return True
    return False


def judicial_is_valid(judicial_handoff):
    if not isinstance(judicial_handoff, dict):
        return False
    return (
        judicial_handoff.get("role") == "judicial"
        and judicial_handoff.get("status") in PASS_STATUSES
        and judicial_handoff.get("mayValidate") is True
        and judicial_handoff.get("mayEditFiles") is False
        and judicial_handoff.get("mayRepair") is False
        and judicial_handoff.get("mayCertifyDelivery") is False
    )


def snapshot_status(run_root, snapshot):
    if not isinstance(snapshot, dict):
        return "missing", ["Certification snapshot is missing."]
    artifacts = snapshot.get("artifacts", [])
    if not isinstance(artifacts, list) or not artifacts:
        return "missing", ["Certification snapshot contains no artifact hashes."]
    stale = []
    for item in artifacts:
        if not isinstance(item, dict):
            stale.append("Malformed snapshot artifact entry.")
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
    if stale:
        return "stale", stale
    return "current", ["Certification snapshot matches checked artifacts."]


def delivery_certification_state(delivery_certification):
    if not isinstance(delivery_certification, dict):
        return None
    return delivery_certification.get("deliveryStatus")


def certification_gate_has_run(delivery_certification):
    if not isinstance(delivery_certification, dict):
        return False
    evidence = delivery_certification.get("executionEvidence")
    if isinstance(evidence, dict):
        if evidence.get("executionIsolationLevel") != "protocol-defined":
            return True
        if evidence.get("verificationEvidenceLevel") != "none":
            return True
    if delivery_certification.get("generationOrRepairPassIds"):
        return True
    for item in delivery_certification.get("blockingChecks", []) or []:
        if isinstance(item, dict) and item.get("checkId") != "runner-evidence":
            return True
    return False


def derive_state(run_root, refs):
    runner_workflow = load_optional_json(resolve_inside(run_root, refs["runnerWorkflow"], "runner workflow"))
    runner_report = load_optional_json(resolve_inside(run_root, refs["runnerReport"], "runner report"))
    judicial_handoff = load_optional_json(resolve_inside(run_root, refs["judicialHandoff"], "judicial handoff"))
    delivery_certification = load_optional_json(resolve_inside(run_root, refs["deliveryCertification"], "delivery certification"))
    certification_snapshot = load_optional_json(resolve_inside(run_root, refs["certificationSnapshot"], "certification snapshot"))

    state_evidence = []
    workflow_id = None
    run_id = None
    if isinstance(runner_workflow, dict):
        workflow_id = runner_workflow.get("workflowId")
        run_id = runner_workflow.get("runId")
    if isinstance(runner_report, dict):
        workflow_id = workflow_id or runner_report.get("workflowId")
        run_id = run_id or runner_report.get("runId")
    if isinstance(delivery_certification, dict):
        workflow_id = workflow_id or delivery_certification.get("workflowId")
        certification_id = delivery_certification.get("certificationId")
        if not run_id and isinstance(certification_id, str) and certification_id.endswith("-delivery-certification"):
            run_id = certification_id.removesuffix("-delivery-certification")

    runner_status = runner_report.get("runnerStatus") if isinstance(runner_report, dict) else "missing"
    state_evidence.append(evidence("runner-report", "pass" if runner_status == "pass" else "not_verified", [f"runnerStatus={runner_status}"]))

    executed = passes_executed(run_root, runner_report)
    state_evidence.append(evidence("pass-execution", "pass" if executed else "not_verified", ["Pass results or completed handoffs found." if executed else "No completed pass evidence found."]))

    judicial_valid = judicial_is_valid(judicial_handoff)
    state_evidence.append(evidence("judicial-handoff", "pass" if judicial_valid else "not_verified", ["Judicial handoff is valid." if judicial_valid else "Valid judicial handoff not found."]))

    delivery_status = delivery_certification_state(delivery_certification)
    state_evidence.append(evidence("delivery-certification", "pass" if delivery_status == "complete" else "not_verified", [f"deliveryStatus={delivery_status or 'missing'}"]))

    snapshot_result, snapshot_details = snapshot_status(run_root, certification_snapshot)
    state_evidence.append(evidence("certification-snapshot", "pass" if snapshot_result == "current" else snapshot_result, snapshot_details))

    if delivery_status == "complete":
        current_state = "certified" if snapshot_result == "current" else "stale"
    elif runner_has_failed(runner_report):
        current_state = "failed"
    elif delivery_status == "not-certified" and certification_gate_has_run(delivery_certification):
        current_state = "not-certified"
    elif judicial_valid:
        current_state = "judicial-validated"
    elif runner_is_verified(runner_report):
        current_state = "runner-verified"
    elif executed:
        current_state = "passes-executed"
    else:
        current_state = "scaffolded"

    limitations = []
    if current_state == "stale":
        limitations.append("Certification exists but snapshot verification is stale.")
    if current_state == "not-certified":
        limitations.append("Run has certification output but does not satisfy delivery complete gates.")
    if current_state == "scaffolded":
        limitations.append("No executed pass, runner, judicial, or certification evidence has been recorded yet.")
    if current_state == "failed":
        limitations.append("Runner or required pass evidence reports failure or blocked status.")

    return {
        "schemaVersion": "1.0",
        "workflowId": workflow_id or "<unknown-workflow>",
        "runId": run_id or run_root.name,
        "currentState": current_state,
        "derivedAt": utc_now(),
        "derivedBy": "scripts/update_orchestration_state.py",
        "stateEvidence": state_evidence,
        "artifactRefs": refs,
        "limitations": limitations,
    }


def allowed_next_states(current_state):
    if current_state == "failed":
        return ["passes-executed", "runner-verified", "judicial-validated", "not-certified", "certified"]
    if current_state == "stale":
        return ["passes-executed", "runner-verified", "judicial-validated", "not-certified", "certified", "failed"]
    if current_state == "not-certified":
        return ["passes-executed", "runner-verified", "judicial-validated", "certified", "failed"]
    if current_state == "certified":
        return ["stale"]
    order = STATE_ORDER.get(current_state, 0)
    return [state for state, value in STATE_ORDER.items() if value > order] + ["failed"]


def transition_allowed(previous_state, next_state):
    if not previous_state or previous_state == next_state:
        return True
    if previous_state in TERMINAL_OR_RETRY_STATES:
        return next_state in allowed_next_states(previous_state)
    if previous_state == "certified":
        return next_state == "stale"
    previous_order = STATE_ORDER.get(previous_state)
    next_order = STATE_ORDER.get(next_state)
    if next_state == "failed":
        return True
    if previous_order is None or next_order is None:
        return False
    return next_order >= previous_order


def finalize_state(run_state, previous_state):
    run_state["previousState"] = previous_state
    run_state["allowedNextStates"] = allowed_next_states(run_state["currentState"])
    return run_state


def derive_and_write_state(root, state_ref="run-state.json", refs=None, verify=False, force=False):
    run_root = Path(root).resolve()
    resolved_refs = dict(DEFAULT_ARTIFACT_REFS)
    if refs:
        resolved_refs.update(refs)
    state_path = resolve_inside(run_root, state_ref, "run state")
    previous = load_optional_json(state_path)
    previous_state = previous.get("currentState") if isinstance(previous, dict) else None
    run_state = finalize_state(derive_state(run_root, resolved_refs), previous_state)
    next_state = run_state["currentState"]

    if not force and not transition_allowed(previous_state, next_state):
        raise ValueError(f"invalid run state transition: {previous_state} -> {next_state}")

    if not verify:
        write_json(state_path, run_state)
    return run_state


def update_state(args):
    refs = {
        "runnerWorkflow": args.runner_workflow,
        "runnerReport": args.runner_report,
        "judicialHandoff": args.judicial_handoff,
        "deliveryCertification": args.delivery_certification,
        "certificationSnapshot": args.certification_snapshot,
    }
    run_state = derive_and_write_state(
        args.root,
        state_ref=args.state,
        refs=refs,
        verify=args.verify,
        force=args.force,
    )
    current_state = run_state["currentState"]
    previous_state = run_state.get("previousState") or "none"

    if args.verify:
        print("update_orchestration_state: STATE_VALID")
        print(f"currentState: {current_state}")
        print(f"previousState: {previous_state}")
        return 0

    print("update_orchestration_state: STATE_WRITTEN")
    print(f"currentState: {current_state}")
    print(f"stateRef: {args.state}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Derive and write TOP orchestration run state.")
    parser.add_argument("--root", required=True, help="Run package root")
    parser.add_argument("--state", default="run-state.json")
    parser.add_argument("--runner-workflow", default="runner/runner-workflow.json")
    parser.add_argument("--runner-report", default="runner/runner-report.json")
    parser.add_argument("--judicial-handoff", default="handoffs/judicial.handoff.json")
    parser.add_argument("--delivery-certification", default="reports/delivery-certification.json")
    parser.add_argument("--certification-snapshot", default="reports/certification-snapshot.json")
    parser.add_argument("--verify", action="store_true", help="Derive and validate state without writing it")
    parser.add_argument("--force", action="store_true", help="Allow non-monotonic state rewrite")
    args = parser.parse_args()
    try:
        return update_state(args)
    except Exception as exc:
        print("update_orchestration_state: FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
