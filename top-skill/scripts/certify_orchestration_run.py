#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_execution_evidence import validate_document
from update_orchestration_state import derive_and_write_state


PASS_STATUSES = {"done", "complete"}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path):
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


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


def command_text():
    return "python -B scripts/certify_orchestration_run.py --root <run-package>"


def default_ref(args, name, fallback):
    return getattr(args, name, None) or fallback


def hard_check_descriptions(runner_workflow):
    descriptions = {}
    for item in runner_workflow.get("hardChecks", []) or []:
        if isinstance(item, dict) and is_nonempty_string(item.get("id")):
            descriptions[item["id"]] = item.get("description") or item["id"]
    return descriptions


def normalize_hard_checks(runner_report, runner_workflow):
    descriptions = hard_check_descriptions(runner_workflow)
    result = []
    for item in runner_report.get("hardCheckResults", []) or []:
        if not isinstance(item, dict):
            continue
        check_id = item.get("id") or "<unknown-hard-check>"
        result.append(
            {
                "id": check_id,
                "description": descriptions.get(check_id, check_id),
                "requiredForComplete": item.get("requiredForComplete") is True,
                "status": item.get("status", "not_verified"),
                "command": item.get("command"),
                "evidence": item.get("evidence") if isinstance(item.get("evidence"), list) else [],
            }
        )
    return result


def gate(gate_id, status, evidence, violation_class="delivery-certification"):
    return {
        "gateId": gate_id,
        "violationClass": violation_class,
        "status": status,
        "evidence": evidence if evidence else ["No evidence recorded."],
    }


def blocking_check(gate_result):
    return {
        "checkId": gate_result["gateId"],
        "status": gate_result["status"],
        "evidence": gate_result["evidence"],
    }


def pass_results_by_role(runner_report):
    by_role = {}
    for item in runner_report.get("passResults", []) or []:
        if isinstance(item, dict):
            by_role.setdefault(item.get("role"), []).append(item)
    return by_role


def required_pass_ids(runner_workflow):
    return {
        item.get("passId")
        for item in runner_workflow.get("passes", []) or []
        if isinstance(item, dict) and item.get("requiredForDelivery") is True
    }


def pass_order(runner_workflow):
    return {
        item.get("passId"): index
        for index, item in enumerate(runner_workflow.get("passes", []) or [])
        if isinstance(item, dict) and is_nonempty_string(item.get("passId"))
    }


def repair_pass_ids(runner_report):
    return [
        item.get("passId")
        for item in runner_report.get("passResults", []) or []
        if isinstance(item, dict)
        and item.get("role") == "repair"
        and item.get("status") == "pass"
        and is_nonempty_string(item.get("passId"))
    ]


def validate_post_repair_judicial(run_root, runner_workflow, runner_report, judicial_handoff):
    repairs = repair_pass_ids(runner_report)
    if not repairs:
        return "not_applicable", ["No repair pass completed in this run."]

    order = pass_order(runner_workflow)
    judicial_pass_id = judicial_handoff.get("passId")
    judicial_index = order.get(judicial_pass_id)
    repair_indexes = [order.get(pass_id) for pass_id in repairs if order.get(pass_id) is not None]
    if judicial_index is None:
        return "fail", [f"judicial pass {judicial_pass_id!r} is not in runner workflow"]
    if not repair_indexes:
        return "fail", ["repair pass result exists but no repair pass order is known"]
    latest_repair = max(repair_indexes)
    if judicial_index <= latest_repair:
        return "fail", [
            f"judicial pass {judicial_pass_id} occurs before or at latest repair pass",
            f"repairPassIds={','.join(repairs)}",
        ]
    repaired_refs = []
    for pass_item in runner_workflow.get("passes", []) or []:
        if not isinstance(pass_item, dict) or pass_item.get("role") != "repair":
            continue
        if pass_item.get("passId") not in repairs:
            continue
        try:
            handoff = load_json(resolve_inside(run_root, pass_item.get("handoffArtifactRef"), "repair handoff"))
        except Exception:
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
            return "fail", [
                f"final judicial handoff did not read repaired refs: {', '.join(missing)}",
                f"repairPassIds={','.join(repairs)}",
            ]
    return "pass", [
        f"judicialPassId={judicial_pass_id}",
        f"postRepairPassIds={','.join(repairs)}",
        f"repairedRefs={','.join(repaired_refs) if repaired_refs else 'none'}",
    ]


def validate_judicial_handoff(handoff):
    errors = []
    if handoff.get("role") != "judicial":
        errors.append("judicial handoff role must be judicial")
    if handoff.get("status") not in PASS_STATUSES:
        errors.append("judicial handoff status must be done or complete")
    if handoff.get("mayValidate") is not True:
        errors.append("judicial handoff must have mayValidate true")
    if handoff.get("mayEditFiles") is not False:
        errors.append("judicial handoff must have mayEditFiles false")
    if handoff.get("mayRepair") is not False:
        errors.append("judicial handoff must have mayRepair false")
    if handoff.get("mayCertifyDelivery") is not False:
        errors.append("judicial handoff must not certify delivery")
    return errors


def build_gates(run_root, runner_report, runner_workflow, judicial_handoff):
    gates = []
    evidence = runner_report.get("executionEvidence", {}) if isinstance(runner_report.get("executionEvidence"), dict) else {}
    pass_results = runner_report.get("passResults", []) or []
    hard_checks = runner_report.get("hardCheckResults", []) or []
    required_ids = required_pass_ids(runner_workflow)
    required_results = [item for item in pass_results if item.get("passId") in required_ids]

    runner_ok = (
        runner_report.get("runnerStatus") == "pass"
        and evidence.get("executionIsolationLevel") == "runner-enforced"
        and evidence.get("verificationEvidenceLevel") == "hard-check-verified"
    )
    gates.append(
        gate(
            "runner-evidence",
            "pass" if runner_ok else "fail",
            [
                f"runnerStatus={runner_report.get('runnerStatus')}",
                f"executionIsolationLevel={evidence.get('executionIsolationLevel')}",
                f"verificationEvidenceLevel={evidence.get('verificationEvidenceLevel')}",
            ],
            "runner-evidence",
        )
    )

    required_passes_ok = bool(required_results) and all(item.get("status") == "pass" for item in required_results)
    gates.append(
        gate(
            "required-pass-status",
            "pass" if required_passes_ok else "fail",
            [
                f"{item.get('passId')}:{item.get('status')}"
                for item in required_results
            ],
            "runner-pass",
        )
    )

    adapter_evidence_ok = bool(required_results) and all(
        item.get("freshContext") is True
        and item.get("receivedOnlyContextPackage") is True
        and item.get("modelInvocationEvidence") is True
        for item in required_results
    )
    gates.append(
        gate(
            "adapter-invocation-evidence",
            "pass" if adapter_evidence_ok else "fail",
            [
                f"{item.get('passId')}:fresh={item.get('freshContext')},contextPackageOnly={item.get('receivedOnlyContextPackage')},modelEvidence={item.get('modelInvocationEvidence')}"
                for item in required_results
            ],
            "runner-invocation",
        )
    )

    invocation_ids = [item.get("invocationId") for item in required_results if is_nonempty_string(item.get("invocationId"))]
    context_ids = [item.get("contextId") for item in required_results if is_nonempty_string(item.get("contextId"))]
    separation_ok = len(set(invocation_ids)) >= 2 and len(set(context_ids)) >= 2
    gates.append(
        gate(
            "separate-invocation-and-context-ids",
            "pass" if separation_ok else "fail",
            [f"invocationIds={len(set(invocation_ids))}", f"contextIds={len(set(context_ids))}"],
            "runner-invocation",
        )
    )

    required_hard_checks = [item for item in hard_checks if item.get("requiredForComplete") is True]
    hard_checks_ok = bool(required_hard_checks) and all(item.get("status") == "pass" for item in required_hard_checks)
    gates.append(
        gate(
            "required-hard-checks",
            "pass" if hard_checks_ok else "fail",
            [f"{item.get('id')}:{item.get('status')}" for item in required_hard_checks],
            "hard-check",
        )
    )

    judicial_errors = validate_judicial_handoff(judicial_handoff)
    gates.append(
        gate(
            "independent-judicial-handoff",
            "pass" if not judicial_errors else "fail",
            judicial_errors or [
                f"judicialPassId={judicial_handoff.get('passId')}",
                "judicial handoff is independent from executive/repair authority",
            ],
            "judicial-validation",
        )
    )

    repair_status, repair_evidence = validate_post_repair_judicial(run_root, runner_workflow, runner_report, judicial_handoff)
    gates.append(
        gate(
            "post-repair-judicial-validation",
            repair_status,
            repair_evidence,
            "repair-loop",
        )
    )

    self_certification = any(
        item.get("role") in {"executive", "repair"} and item.get("mayCertifyDelivery") is True
        for item in [judicial_handoff]
    )
    gates.append(
        gate(
            "self-certification",
            "fail" if self_certification else "pass",
            ["No executive or repair handoff certified delivery."],
            "separation-of-powers",
        )
    )

    return gates


def certification_passed(gates):
    return all(item.get("status") in {"pass", "not_applicable"} for item in gates)


def validation_report(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks):
    workflow_id = runner_report.get("workflowId")
    run_id = runner_report.get("runId")
    blocking = [
        f"{item['gateId']}: {', '.join(item['evidence'])}"
        for item in gates
        if item.get("status") == "fail"
    ]
    return {
        "schemaVersion": "1.0",
        "reportId": f"{run_id}-validation-report",
        "workflowId": workflow_id,
        "judicialPassId": judicial_handoff.get("passId", "judicial"),
        "judicialHandoffRef": "handoffs/judicial.handoff.json",
        "repairAttemptIds": repair_pass_ids(runner_report),
        "executionEvidence": runner_report.get("executionEvidence"),
        "artifactScope": f"orchestration run package {run_root.name}",
        "checkedFiles": [
            "runner/runner-workflow.json",
            "runner/runner-report.json",
            "handoffs/judicial.handoff.json",
            *[
                item.get("invocationEvidenceRef")
                for item in runner_report.get("passResults", []) or []
                if is_nonempty_string(item.get("invocationEvidenceRef"))
            ],
        ],
        "commandsRun": [command_text()],
        "requiredHardChecks": hard_checks,
        "violationClassesChecked": [
            "runner-enforced-isolation",
            "hard-check-evidence",
            "independent-judicial-handoff",
            "required-pass-status",
            "self-certification",
            "post-repair-judicial-validation",
        ],
        "gateResults": gates,
        "blockingViolations": blocking,
        "unverifiedAreas": [] if not blocking else ["Delivery law gates did not all pass."],
        "finalValidationStatus": "pass" if not blocking else "fail",
        "independence": {
            "currentFilesRead": True,
            "executorClaimsIgnored": True,
            "samePassAsGenerationOrRepair": False,
            "selfCertificationDetected": False,
        },
    }


def delivery_certification(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks):
    workflow_id = runner_report.get("workflowId")
    run_id = runner_report.get("runId")
    complete = certification_passed(gates)
    generation_or_repair = [
        item.get("passId")
        for item in runner_report.get("passResults", []) or []
        if item.get("role") in {"executive", "repair"} and is_nonempty_string(item.get("passId"))
    ]
    repair_attempt_ids = [
        item.get("passId")
        for item in runner_report.get("passResults", []) or []
        if item.get("role") == "repair" and is_nonempty_string(item.get("passId"))
    ]
    return {
        "schemaVersion": "1.0",
        "certificationId": f"{run_id}-delivery-certification",
        "workflowId": workflow_id,
        "deliveryStatus": "complete" if complete else "not-certified",
        "executionEvidence": runner_report.get("executionEvidence"),
        "judicialValidationRef": "reports/validation-report.json",
        "judicialHandoffRef": "handoffs/judicial.handoff.json",
        "validationReportRef": "reports/validation-report.json",
        "finalAuditReportRef": "reports/final-audit.md",
        "generationOrRepairPassIds": generation_or_repair,
        "repairAttemptIds": repair_attempt_ids,
        "judicialPassId": judicial_handoff.get("passId", "judicial"),
        "separationOfPowersProof": [
            "Runner report records separate required pass invocation ids.",
            "Runner report records separate required pass context ids.",
            "Judicial handoff has validation authority and no edit/repair/certification authority.",
            "Required hard checks passed before certification.",
        ],
        "requiredHardChecks": hard_checks,
        "blockingChecks": [blocking_check(item) for item in gates],
        "knownExclusions": [
            "Certification scope is this orchestration run package only; it is not a general top-skill release claim."
        ],
        "noBlockingInScopeViolations": complete,
        "generationAndValidationSeparate": complete,
        "noUnverifiedRequiredGates": complete,
        "noRequiredGateFailedOrNotVerified": complete,
    }


def final_audit(run_root, validation, certification):
    return f"""# Final Audit

workflowId: {certification.get("workflowId")}
runId: {certification.get("certificationId", "").replace("-delivery-certification", "")}
deliveryStatus: {certification.get("deliveryStatus")}
executionIsolationLevel: {certification.get("executionEvidence", {}).get("executionIsolationLevel")}
verificationEvidenceLevel: {certification.get("executionEvidence", {}).get("verificationEvidenceLevel")}

Scope: orchestration run package `{run_root}`.

Validation status: {validation.get("finalValidationStatus")}

Blocking checks:
{chr(10).join(f"- {item['checkId']}: {item['status']}" for item in certification.get("blockingChecks", []))}

Known exclusions:
{chr(10).join(f"- {item}" for item in certification.get("knownExclusions", []))}
"""


def add_snapshot_artifact(artifacts, seen, run_root, ref, role):
    if not is_nonempty_string(ref) or ref in seen:
        return
    seen.add(ref)
    path = resolve_inside(run_root, ref, role)
    artifacts.append(
        {
            "ref": ref,
            "role": role,
            "sha256": sha256_file(path),
        }
    )


def certification_snapshot(
    run_root,
    runner_workflow,
    runner_report,
    certification,
    runner_workflow_ref,
    runner_report_ref,
    judicial_handoff_ref,
    validation_report_ref,
    delivery_certification_ref,
    final_audit_ref,
):
    artifacts = []
    seen = set()

    add_snapshot_artifact(artifacts, seen, run_root, runner_workflow_ref, "runner-workflow")
    add_snapshot_artifact(artifacts, seen, run_root, runner_report_ref, "runner-report")

    for item in runner_workflow.get("passes", []) or []:
        if not isinstance(item, dict):
            continue
        pass_id = item.get("passId") or "unknown-pass"
        add_snapshot_artifact(artifacts, seen, run_root, item.get("taskCapsuleRef"), f"{pass_id}:task-capsule")
        add_snapshot_artifact(artifacts, seen, run_root, item.get("contextPackageRef"), f"{pass_id}:context-package")
        add_snapshot_artifact(artifacts, seen, run_root, item.get("handoffArtifactRef"), f"{pass_id}:handoff")
        add_snapshot_artifact(artifacts, seen, run_root, item.get("invocationEvidenceRef"), f"{pass_id}:invocation-evidence")
        try:
            handoff = load_json(resolve_inside(run_root, item.get("handoffArtifactRef"), f"{pass_id}:handoff"))
        except Exception:
            handoff = {}
        for ref in handoff.get("filesChanged", []) or []:
            if isinstance(ref, str) and not ref.startswith("handoffs/"):
                add_snapshot_artifact(artifacts, seen, run_root, ref, f"{pass_id}:changed-artifact")

    for item in runner_report.get("passResults", []) or []:
        if not isinstance(item, dict):
            continue
        pass_id = item.get("passId") or "unknown-pass"
        add_snapshot_artifact(artifacts, seen, run_root, item.get("contextPackageRef"), f"{pass_id}:context-package")
        add_snapshot_artifact(artifacts, seen, run_root, item.get("invocationEvidenceRef"), f"{pass_id}:invocation-evidence")
        try:
            invocation = load_json(resolve_inside(run_root, item.get("invocationEvidenceRef"), f"{pass_id}:invocation-evidence"))
        except Exception:
            invocation = {}
        for artifact in invocation.get("artifactWrites", []) or []:
            if isinstance(artifact, dict):
                add_snapshot_artifact(artifacts, seen, run_root, artifact.get("ref"), f"{pass_id}:artifact-write")

    add_snapshot_artifact(artifacts, seen, run_root, judicial_handoff_ref, "judicial-handoff")
    add_snapshot_artifact(artifacts, seen, run_root, validation_report_ref, "validation-report")
    add_snapshot_artifact(artifacts, seen, run_root, delivery_certification_ref, "delivery-certification")
    add_snapshot_artifact(artifacts, seen, run_root, final_audit_ref, "final-audit")

    return {
        "schemaVersion": "1.0",
        "workflowId": certification.get("workflowId"),
        "runId": runner_report.get("runId"),
        "snapshotStatus": "current",
        "certifiedAt": utc_now(),
        "certifiedBy": "scripts/certify_orchestration_run.py",
        "deliveryStatus": certification.get("deliveryStatus"),
        "executionEvidence": certification.get("executionEvidence"),
        "artifacts": artifacts,
        "limitations": [
            "Snapshot detects accidental or ordinary post-certification artifact drift inside the run package.",
            "Snapshot does not protect against a privileged actor rewriting both artifacts and snapshot together.",
        ],
    }


def verify_snapshot(args):
    run_root = Path(args.root).resolve()
    snapshot_ref = default_ref(args, "snapshot", "reports/certification-snapshot.json")
    snapshot_path = resolve_inside(run_root, snapshot_ref, "certification snapshot")
    snapshot = load_json(snapshot_path)
    stale = []
    for item in snapshot.get("artifacts", []) or []:
        ref = item.get("ref")
        expected = item.get("sha256")
        path = resolve_inside(run_root, ref, "snapshot artifact")
        actual = sha256_file(path)
        if actual != expected:
            stale.append(
                {
                    "ref": ref,
                    "role": item.get("role"),
                    "expected": expected,
                    "actual": actual,
                }
            )

    state_error = None
    if not getattr(args, "skip_state_update", False):
        try:
            update_run_state(args)
        except Exception as exc:
            state_error = exc

    if stale:
        print("certify_orchestration_run: SNAPSHOT_STALE")
        for item in stale:
            print(f"- {item['ref']} ({item.get('role')}): expected {item.get('expected')}, actual {item.get('actual')}")
        if state_error:
            print(f"- failed to update run state: {state_error}")
        return 1

    if state_error:
        print("certify_orchestration_run: FAILED")
        print(f"- failed to update run state: {state_error}")
        return 2

    print("certify_orchestration_run: SNAPSHOT_CURRENT")
    print(f"deliveryStatus: {snapshot.get('deliveryStatus')}")
    return 0


def update_run_state(args):
    return derive_and_write_state(
        args.root,
        state_ref=getattr(args, "state", "run-state.json"),
        refs={
            "runnerWorkflow": args.runner_workflow,
            "runnerReport": args.runner_report,
            "judicialHandoff": args.judicial_handoff,
            "deliveryCertification": args.delivery_certification,
            "certificationSnapshot": default_ref(args, "snapshot", "reports/certification-snapshot.json"),
        },
    )


def certify(args):
    run_root = Path(args.root).resolve()
    runner_workflow_ref = args.runner_workflow
    runner_report_ref = args.runner_report
    judicial_handoff_ref = args.judicial_handoff
    validation_report_ref = args.validation_report
    delivery_certification_ref = args.delivery_certification
    final_audit_ref = args.final_audit
    snapshot_ref = default_ref(args, "snapshot", "reports/certification-snapshot.json")

    runner_workflow = load_json(resolve_inside(run_root, runner_workflow_ref, "runner workflow"))
    runner_report = load_json(resolve_inside(run_root, runner_report_ref, "runner report"))
    judicial_handoff = load_json(resolve_inside(run_root, judicial_handoff_ref, "judicial handoff"))

    gates = build_gates(run_root, runner_report, runner_workflow, judicial_handoff)
    hard_checks = normalize_hard_checks(runner_report, runner_workflow)
    validation = validation_report(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks)
    certification = delivery_certification(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks)

    validation_errors = validate_document(validation, validation_report_ref)
    certification_errors = validate_document(certification, delivery_certification_ref)
    if validation_errors or certification_errors:
        gates.append(gate("certification-artifact-validation", "fail", validation_errors + certification_errors, "artifact-schema"))
        validation = validation_report(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks)
        certification = delivery_certification(run_root, runner_report, runner_workflow, judicial_handoff, gates, hard_checks)

    write_json(resolve_inside(run_root, validation_report_ref, "validation report"), validation)
    write_json(resolve_inside(run_root, delivery_certification_ref, "delivery certification"), certification)
    write_text(resolve_inside(run_root, final_audit_ref, "final audit"), final_audit(run_root, validation, certification))
    snapshot = certification_snapshot(
        run_root,
        runner_workflow,
        runner_report,
        certification,
        runner_workflow_ref,
        runner_report_ref,
        judicial_handoff_ref,
        validation_report_ref,
        delivery_certification_ref,
        final_audit_ref,
    )
    write_json(resolve_inside(run_root, snapshot_ref, "certification snapshot"), snapshot)

    state_error = None
    if not getattr(args, "skip_state_update", False):
        try:
            update_run_state(args)
        except Exception as exc:
            state_error = exc

    if state_error:
        print("certify_orchestration_run: FAILED")
        print(f"- failed to update run state: {state_error}")
        return 2

    if certification.get("deliveryStatus") == "complete":
        print("certify_orchestration_run: COMPLETE")
        return 0

    print("certify_orchestration_run: NOT_CERTIFIED")
    for item in certification.get("blockingChecks", []):
        if item.get("status") == "fail":
            print(f"- {item.get('checkId')}: {', '.join(item.get('evidence') or [])}")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Certify a TOP orchestration run package.")
    parser.add_argument("--root", required=True, help="Run package root")
    parser.add_argument("--runner-workflow", default="runner/runner-workflow.json")
    parser.add_argument("--runner-report", default="runner/runner-report.json")
    parser.add_argument("--judicial-handoff", default="handoffs/judicial.handoff.json")
    parser.add_argument("--validation-report", default="reports/validation-report.json")
    parser.add_argument("--delivery-certification", default="reports/delivery-certification.json")
    parser.add_argument("--final-audit", default="reports/final-audit.md")
    parser.add_argument("--snapshot", default="reports/certification-snapshot.json")
    parser.add_argument("--state", default="run-state.json")
    parser.add_argument(
        "--skip-state-update",
        action="store_true",
        help="Do not refresh run-state.json after certification or snapshot verification",
    )
    parser.add_argument(
        "--verify-snapshot",
        action="store_true",
        help="Verify that the current run artifacts still match the certification snapshot.",
    )
    args = parser.parse_args()
    try:
        if args.verify_snapshot:
            return verify_snapshot(args)
        return certify(args)
    except Exception as exc:
        print("certify_orchestration_run: FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
