#!/usr/bin/env python3
"""Run TOP orchestration regression fixtures.

Fixtures cover missing judicial handoff, process-only false complete,
required hard check not_verified, stale snapshots, and RUN_VALID not-certified
output.
"""
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from update_orchestration_state import derive_and_write_state
from validate_orchestration_run import validate_run


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execution_evidence(level="runner-enforced", verification="hard-check-verified"):
    return {
        "executionIsolationLevel": level,
        "verificationEvidenceLevel": verification,
        "runnerName": "top-protocol-runner" if level == "runner-enforced" else "process-runner",
        "separateInvocationIds": ["executive-invocation", "judicial-invocation"],
        "schemaValidationCommand": "python -B scripts/top_protocol_runner.py runner/runner-workflow.json",
        "hardCheckCommands": ["python -B scripts/quick_validate.py ."] if verification == "hard-check-verified" else [],
        "limitations": ["Regression fixture evidence."],
    }


def runner_workflow():
    return {
        "schemaVersion": "1.0",
        "workflowId": "orchestration-regression",
        "runId": "regression-run",
        "runnerName": "top-protocol-runner",
        "mode": "validation",
        "runnerCapabilities": {
            "launchesSeparateProcesses": True,
            "launchesSeparateInvocations": True,
            "isolatesContexts": True,
            "executesHardChecks": True,
            "validatesHandoffs": True,
        },
        "passes": [
            {
                "passId": "executive",
                "role": "executive",
                "taskCapsuleRef": "capsules/executive.task-capsule.json",
                "handoffArtifactRef": "handoffs/executive.handoff.json",
                "invocationId": "executive-invocation",
                "contextId": "executive-context",
                "adapterKind": "llm-api",
                "contextPackageRef": "contexts/executive.context-package.json",
                "invocationEvidenceRef": "invocations/executive.invocation-evidence.json",
                "freshContextRequired": True,
                "command": None,
                "cwd": None,
                "timeoutSeconds": 300,
                "requiredForDelivery": True,
            },
            {
                "passId": "judicial",
                "role": "judicial",
                "taskCapsuleRef": "capsules/judicial.task-capsule.json",
                "handoffArtifactRef": "handoffs/judicial.handoff.json",
                "invocationId": "judicial-invocation",
                "contextId": "judicial-context",
                "adapterKind": "llm-api",
                "contextPackageRef": "contexts/judicial.context-package.json",
                "invocationEvidenceRef": "invocations/judicial.invocation-evidence.json",
                "freshContextRequired": True,
                "command": None,
                "cwd": None,
                "timeoutSeconds": 300,
                "requiredForDelivery": True,
            },
        ],
        "hardChecks": [
            {
                "id": "quick-validate",
                "description": "Package validation",
                "requiredForComplete": True,
                "commandType": "python-script",
                "scriptRef": "scripts/quick_validate.py",
                "scriptBaseRef": "skill-root",
                "args": ["."],
                "cwdRef": "skill-root",
                "timeoutSeconds": 300,
            }
        ],
        "deliveryCertificationRef": "reports/delivery-certification.json",
        "limitations": ["Regression runner workflow."],
    }


def runner_report(evidence=None, hard_check_status="pass", process_only=False):
    evidence = evidence or execution_evidence()
    adapter_kind = "process" if process_only else "llm-api"
    model_evidence = not process_only
    context_only = not process_only
    return {
        "schemaVersion": "1.0",
        "workflowId": "orchestration-regression",
        "runId": "regression-run",
        "runnerName": "top-protocol-runner",
        "runnerStatus": "pass",
        "executionEvidence": evidence,
        "passResults": [
            {
                "passId": "executive",
                "role": "executive",
                "invocationId": "executive-invocation",
                "contextId": "executive-context",
                "adapterKind": adapter_kind,
                "contextPackageRef": "contexts/executive.context-package.json",
                "invocationEvidenceRef": "invocations/executive.invocation-evidence.json",
                "freshContext": True,
                "receivedOnlyContextPackage": context_only,
                "modelInvocationEvidence": model_evidence,
                "status": "pass",
                "exitCode": 0,
                "errors": [],
            },
            {
                "passId": "judicial",
                "role": "judicial",
                "invocationId": "judicial-invocation",
                "contextId": "judicial-context",
                "adapterKind": adapter_kind,
                "contextPackageRef": "contexts/judicial.context-package.json",
                "invocationEvidenceRef": "invocations/judicial.invocation-evidence.json",
                "freshContext": True,
                "receivedOnlyContextPackage": context_only,
                "modelInvocationEvidence": model_evidence,
                "status": "pass",
                "exitCode": 0,
                "errors": [],
            },
        ],
        "hardCheckResults": [
            {
                "id": "quick-validate",
                "requiredForComplete": True,
                "status": hard_check_status,
                "command": "python -B scripts/quick_validate.py .",
                "exitCode": 0 if hard_check_status == "pass" else None,
                "evidence": [f"quick-validate:{hard_check_status}"],
            }
        ],
        "deliveryCertificationResult": {
            "status": "pass",
            "ref": "reports/delivery-certification.json",
            "errors": [],
        },
        "limitations": ["Regression runner report."],
    }


def judicial_handoff(status="done"):
    return {
        "schemaVersion": "1.0",
        "workflowId": "orchestration-regression",
        "passId": "judicial",
        "taskId": "judicial-task",
        "role": "judicial",
        "agentName": "judicial-regression",
        "taskCapsuleRef": "capsules/judicial.task-capsule.json",
        "inputReferences": ["handoffs/executive.handoff.json", "runner/runner-report.json"],
        "outputReferences": ["handoffs/judicial.handoff.json"],
        "filesRead": ["runner/runner-report.json"],
        "filesChanged": ["handoffs/judicial.handoff.json"],
        "commandsRun": [],
        "status": status,
        "executionEvidence": execution_evidence("protocol-followed-by-agent", "agent-claimed"),
        "mayEditFiles": False,
        "mayValidate": True,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": False,
        "limitations": ["Regression judicial handoff."],
        "didNotDo": ["did not repair", "did not certify delivery"],
        "handoffTo": "certification",
    }


def delivery_certification(status="complete", evidence=None, hard_check_status="pass"):
    evidence = evidence or execution_evidence()
    complete = status == "complete"
    return {
        "schemaVersion": "1.0",
        "certificationId": "regression-run-delivery-certification",
        "workflowId": "orchestration-regression",
        "deliveryStatus": status,
        "executionEvidence": evidence,
        "judicialValidationRef": "reports/validation-report.json",
        "judicialHandoffRef": "handoffs/judicial.handoff.json",
        "validationReportRef": "reports/validation-report.json",
        "finalAuditReportRef": "reports/final-audit.md",
        "generationOrRepairPassIds": ["executive"],
        "judicialPassId": "judicial",
        "separationOfPowersProof": ["Regression fixture proof."],
        "requiredHardChecks": [
            {
                "id": "quick-validate",
                "description": "Package validation",
                "requiredForComplete": True,
                "status": hard_check_status,
                "command": "python -B scripts/quick_validate.py .",
                "evidence": [f"quick-validate:{hard_check_status}"],
            }
        ],
        "blockingChecks": [
            {
                "checkId": "runner-evidence",
                "status": "pass" if complete else "not_verified",
                "evidence": ["Regression fixture runner evidence."],
            }
        ],
        "knownExclusions": [],
        "noBlockingInScopeViolations": complete,
        "generationAndValidationSeparate": complete,
        "noUnverifiedRequiredGates": complete,
        "noRequiredGateFailedOrNotVerified": complete,
    }


def write_snapshot(run_root):
    artifacts = []
    for ref, role in [
        ("runner/runner-workflow.json", "runner-workflow"),
        ("runner/runner-report.json", "runner-report"),
        ("handoffs/judicial.handoff.json", "judicial-handoff"),
        ("reports/delivery-certification.json", "delivery-certification"),
    ]:
        path = run_root / ref
        if path.exists():
            artifacts.append({"ref": ref, "role": role, "sha256": sha256_file(path)})
    delivery = json.loads((run_root / "reports" / "delivery-certification.json").read_text(encoding="utf-8"))
    write_json(
        run_root / "reports" / "certification-snapshot.json",
        {
            "schemaVersion": "1.0",
            "workflowId": "orchestration-regression",
            "runId": "regression-run",
            "snapshotStatus": "current",
            "certifiedAt": "2026-05-14T00:00:00Z",
            "certifiedBy": "scripts/validate_orchestration_regressions.py",
            "deliveryStatus": delivery.get("deliveryStatus"),
            "executionEvidence": delivery.get("executionEvidence"),
            "artifacts": artifacts,
            "limitations": ["Regression snapshot."],
        },
    )


def base_run_package(run_root, *, delivery_status="complete", evidence=None, hard_check_status="pass", process_only=False):
    evidence = evidence or execution_evidence()
    write_json(run_root / "runner" / "runner-workflow.json", runner_workflow())
    write_json(
        run_root / "runner" / "runner-report.json",
        runner_report(evidence=evidence, hard_check_status=hard_check_status, process_only=process_only),
    )
    write_json(run_root / "handoffs" / "judicial.handoff.json", judicial_handoff())
    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status=delivery_status, evidence=evidence, hard_check_status=hard_check_status),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root)


def verify(run_root):
    args = SimpleNamespace(
        root=str(run_root),
        runner_workflow="runner/runner-workflow.json",
        runner_report="runner/runner-report.json",
        judicial_handoff="handoffs/judicial.handoff.json",
        delivery_certification="reports/delivery-certification.json",
        certification_snapshot="reports/certification-snapshot.json",
        state="run-state.json",
    )
    return validate_run(args)


def run_case(name, configure, expected_status, expected_delivery):
    with tempfile.TemporaryDirectory(prefix=f"top-orchestration-regression-{name}-") as temp_name:
        run_root = Path(temp_name).resolve()
        base_run_package(run_root)
        configure(run_root)
        status, delivery_status, errors, stale = verify(run_root)
        case_errors = []
        if status != expected_status:
            case_errors.append(f"{name}: expected {expected_status}, got {status}")
        if delivery_status != expected_delivery:
            case_errors.append(f"{name}: expected deliveryStatus {expected_delivery}, got {delivery_status}")
        if expected_status == "RUN_STALE" and not stale:
            case_errors.append(f"{name}: expected stale evidence")
        if expected_status == "RUN_INVALID" and not errors:
            case_errors.append(f"{name}: expected invalid evidence")
        return case_errors


def no_change(_run_root):
    return None


def not_certified(run_root):
    evidence = execution_evidence("schema-validated", "hard-check-verified")
    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status="not-certified", evidence=evidence, hard_check_status="pass"),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def missing_judicial_handoff(run_root):
    (run_root / "handoffs" / "judicial.handoff.json").unlink()
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def hard_check_not_verified(run_root):
    evidence = execution_evidence("runner-enforced", "hard-check-verified")
    write_json(
        run_root / "runner" / "runner-report.json",
        runner_report(evidence=evidence, hard_check_status="not_verified"),
    )
    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status="complete", evidence=evidence, hard_check_status="not_verified"),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def schema_validated_false_complete(run_root):
    evidence = execution_evidence("schema-validated", "hard-check-verified")
    write_json(
        run_root / "runner" / "runner-report.json",
        runner_report(evidence=evidence, hard_check_status="pass"),
    )
    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status="complete", evidence=evidence, hard_check_status="pass"),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def process_only_false_complete(run_root):
    evidence = execution_evidence("runner-enforced", "hard-check-verified")
    write_json(
        run_root / "runner" / "runner-report.json",
        runner_report(evidence=evidence, hard_check_status="pass", process_only=True),
    )
    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status="complete", evidence=evidence, hard_check_status="pass"),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def repair_without_post_judicial(run_root):
    workflow = json.loads((run_root / "runner" / "runner-workflow.json").read_text(encoding="utf-8"))
    repair_pass = {
        "passId": "repair-1",
        "role": "repair",
        "taskCapsuleRef": "capsules/repair-1.task-capsule.json",
        "handoffArtifactRef": "handoffs/repair-1.handoff.json",
        "invocationId": "repair-invocation",
        "contextId": "repair-context",
        "adapterKind": "llm-api",
        "contextPackageRef": "contexts/repair-1.context-package.json",
        "invocationEvidenceRef": "invocations/repair-1.invocation-evidence.json",
        "freshContextRequired": True,
        "command": None,
        "cwd": None,
        "timeoutSeconds": 300,
        "requiredForDelivery": True,
    }
    workflow["passes"].append(repair_pass)
    workflow["repairPolicy"] = {
        "maxRepairAttempts": 1,
        "repairPassIds": ["repair-1"],
        "finalJudicialPassId": "judicial",
        "requiresPostRepairJudicial": True,
        "limitations": ["Regression fixture repair policy."],
    }
    write_json(run_root / "runner" / "runner-workflow.json", workflow)

    report = json.loads((run_root / "runner" / "runner-report.json").read_text(encoding="utf-8"))
    report["passResults"].append(
        {
            "passId": "repair-1",
            "role": "repair",
            "invocationId": "repair-invocation",
            "contextId": "repair-context",
            "adapterKind": "llm-api",
            "contextPackageRef": "contexts/repair-1.context-package.json",
            "invocationEvidenceRef": "invocations/repair-1.invocation-evidence.json",
            "freshContext": True,
            "receivedOnlyContextPackage": True,
            "modelInvocationEvidence": True,
            "status": "pass",
            "exitCode": 0,
            "errors": [],
        }
    )
    report["executionEvidence"]["separateInvocationIds"].append("repair-invocation")
    write_json(run_root / "runner" / "runner-report.json", report)

    write_json(
        run_root / "reports" / "delivery-certification.json",
        delivery_certification(status="complete", evidence=execution_evidence(), hard_check_status="pass"),
    )
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def repair_handoff_cannot_certify(run_root):
    handoff = judicial_handoff()
    handoff["passId"] = "repair-1"
    handoff["role"] = "repair"
    handoff["mayValidate"] = False
    handoff["mayRepair"] = True
    handoff["mayCertifyDelivery"] = True
    handoff["limitations"] = ["Regression repair handoff tried to certify."]
    write_json(run_root / "handoffs" / "judicial.handoff.json", handoff)
    write_snapshot(run_root)
    derive_and_write_state(run_root, force=True)


def stale_after_certification(run_root):
    handoff = copy.deepcopy(judicial_handoff())
    handoff["limitations"] = ["Regression handoff changed after certification."]
    write_json(run_root / "handoffs" / "judicial.handoff.json", handoff)


def run_regressions():
    cases = [
        ("valid_certified", no_change, "RUN_VALID certified", "complete"),
        ("valid_not_certified", not_certified, "RUN_VALID not-certified", "not-certified"),
        ("missing_judicial_handoff_blocks_complete", missing_judicial_handoff, "RUN_INVALID", None),
        ("hard_check_not_verified_blocks_complete", hard_check_not_verified, "RUN_INVALID", "complete"),
        ("schema_validated_false_complete_blocks", schema_validated_false_complete, "RUN_INVALID", "complete"),
        ("process_only_false_complete_blocks", process_only_false_complete, "RUN_INVALID", "complete"),
        ("repair_without_post_judicial_blocks_complete", repair_without_post_judicial, "RUN_INVALID", "complete"),
        ("repair_handoff_cannot_certify", repair_handoff_cannot_certify, "RUN_INVALID", "complete"),
        ("stale_snapshot_blocks_current_complete", stale_after_certification, "RUN_STALE", "complete"),
    ]
    errors = []
    for name, configure, expected_status, expected_delivery in cases:
        errors.extend(run_case(name, configure, expected_status, expected_delivery))
    return errors


def main():
    errors = run_regressions()
    if errors:
        print("validate_orchestration_regressions: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("validate_orchestration_regressions: OK")
    print("fixtures: valid_certified, valid_not_certified, missing_judicial_handoff, hard_check_not_verified, schema_validated_false_complete, process_only_false_complete, repair_without_post_judicial, repair_handoff_cannot_certify, stale_snapshot")
    return 0


if __name__ == "__main__":
    sys.exit(main())
