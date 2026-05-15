#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ROLES = ["executive", "judicial", "certification"]


ROLE_AUTHORITY = {
    "orchestrator": {
        "mayEditFiles": False,
        "mayValidate": False,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": False,
        "allowedActions": ["create task capsules", "route workflow", "accept handoffs"],
        "forbiddenActions": ["implement artifacts", "validate artifacts", "certify delivery"],
        "handoffTo": "executive",
    },
    "context-builder": {
        "mayEditFiles": False,
        "mayValidate": False,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": False,
        "allowedActions": ["prepare task capsule context"],
        "forbiddenActions": ["implement artifacts", "validate artifacts", "certify delivery"],
        "handoffTo": "orchestrator",
    },
    "executive": {
        "mayEditFiles": True,
        "mayValidate": False,
        "mayRepair": False,
        "mayReport": False,
        "mayCertifyDelivery": False,
        "allowedActions": ["create or modify authorized artifacts"],
        "forbiddenActions": ["validate own output", "certify delivery", "write final audit"],
        "handoffTo": "judicial",
    },
    "judicial": {
        "mayEditFiles": False,
        "mayValidate": True,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": False,
        "allowedActions": ["validate current artifacts", "write judicial verdict"],
        "forbiddenActions": ["repair implementation", "certify delivery without hard-check evidence"],
        "handoffTo": "certification",
    },
    "repair": {
        "mayEditFiles": True,
        "mayValidate": False,
        "mayRepair": True,
        "mayReport": False,
        "mayCertifyDelivery": False,
        "allowedActions": ["repair scoped validation failures"],
        "forbiddenActions": ["validate own repair", "certify delivery"],
        "handoffTo": "judicial",
    },
    "reporting": {
        "mayEditFiles": False,
        "mayValidate": False,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": False,
        "allowedActions": ["summarize judicial findings"],
        "forbiddenActions": ["upgrade judicial verdict", "certify delivery"],
        "handoffTo": "certification",
    },
    "certification": {
        "mayEditFiles": False,
        "mayValidate": False,
        "mayRepair": False,
        "mayReport": True,
        "mayCertifyDelivery": True,
        "allowedActions": ["certify only when delivery law evidence exists"],
        "forbiddenActions": ["invent judicial verdict", "ignore hard-check failures"],
        "handoffTo": "done",
    },
}


def write_json(path, data, force):
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_text(path, text, force):
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_pass(value):
    if ":" not in value:
        raise argparse.ArgumentTypeError("pass must use pass-id:role")
    pass_id, role = value.split(":", 1)
    pass_id = pass_id.strip()
    role = role.strip()
    if not pass_id or not role:
        raise argparse.ArgumentTypeError("pass-id and role must be non-empty")
    if role not in ROLE_AUTHORITY:
        allowed = ", ".join(sorted(ROLE_AUTHORITY))
        raise argparse.ArgumentTypeError(f"unsupported role {role!r}; allowed: {allowed}")
    return pass_id, role


def protocol_defined_evidence():
    return {
        "executionIsolationLevel": "protocol-defined",
        "verificationEvidenceLevel": "none",
        "runnerName": None,
        "separateInvocationIds": [],
        "schemaValidationCommand": None,
        "hardCheckCommands": [],
        "limitations": ["Scaffolded artifact; no execution evidence yet."],
    }


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_input_references(pass_id, role, profile):
    if profile == "llm-smoke":
        if role == "judicial":
            return [
                "handoffs/executive.handoff.json",
                "invocations/executive.invocation-evidence.json",
            ]
        return []
    if profile == "repair-artifact-dogfood" and role == "judicial" and pass_id == "judicial":
        return [
            "handoffs/repair-1.handoff.json",
            "invocations/repair-1.invocation-evidence.json",
            "artifacts/repair-target.json",
        ]
    if profile == "repair-artifact-dogfood" and role == "judicial":
        return [
            "handoffs/executive.handoff.json",
            "invocations/executive.invocation-evidence.json",
            "artifacts/repair-target.json",
        ]
    if profile == "repair-artifact-dogfood" and role == "repair":
        return [
            "handoffs/judicial-initial.handoff.json",
            "artifacts/repair-target.json",
        ]
    if profile in {"repair-loop"} and role == "judicial" and pass_id == "judicial":
        return [
            "handoffs/repair-1.handoff.json",
            "invocations/repair-1.invocation-evidence.json",
        ]
    if profile in {"repair-loop"} and role == "judicial":
        return [
            "handoffs/executive.handoff.json",
            "invocations/executive.invocation-evidence.json",
        ]
    if role == "repair":
        return [
            "handoffs/judicial-initial.handoff.json",
        ]
    if role == "judicial":
        return [
            "handoffs/executive.handoff.json",
            "runner/runner-report.json",
        ]
    if role == "certification":
        return [
            "handoffs/judicial.handoff.json",
            "reports/validation-report.json",
            "runner/runner-report.json",
        ]
    return []


def default_context_slices(role, profile, pass_id=None):
    if profile == "llm-smoke":
        if role == "executive":
            return [
                "This is a bounded top-skill 2.0 runner smoke pass.",
                "Do not edit project files. Produce only the executive handoff artifact.",
                "Report status done if the supplied task capsule can be followed.",
                "Do not validate your own output and do not claim runner-enforced isolation.",
            ]
        if role == "judicial":
            return [
                "Independently inspect the supplied executive handoff and invocation evidence.",
                "Treat adapter invocation evidence as execution evidence only; do not certify delivery complete.",
                "Write a judicial handoff with status done when the executive handoff is structurally coherent and no self-certification claim is present.",
                "Do not repair implementation artifacts and do not certify delivery.",
            ]
        return [
            f"Run the {role} pass using only this task capsule and listed input references.",
            "Do not use unbounded prior chat or hidden memory.",
        ]
    if profile == "repair-artifact-dogfood" and role == "judicial" and pass_id == "judicial-initial":
        return [
            "Validate the explicitly referenced initial repair-target artifact and handoffs.",
            "This is the pre-repair judicial pass. If the artifact is invalid, use status done, record the blocking finding, and hand off to repair.",
            "Do not use status blocked merely because the pre-repair artifact is invalid; blocked means the judicial pass itself could not complete.",
            "Do not repair implementation artifacts and do not certify delivery.",
        ]
    if profile == "repair-artifact-dogfood" and role == "judicial":
        return [
            "Validate the explicitly referenced repair-target artifact and handoffs.",
            "This is the final post-repair judicial pass. Use status done only when artifacts/repair-target.json has statusLabel Ready, isValid true, and repairedBy repair-1.",
            "Use status blocked if the repaired artifact is missing or still invalid.",
            "Do not repair implementation artifacts and do not certify delivery.",
        ]
    if profile == "repair-loop" and role == "judicial":
        return [
            "Validate only the artifacts and handoffs explicitly listed in inputReferences.",
            "If this is the final judicial pass, validate post-repair artifacts and ignore repair self-claims.",
            "The runner report is produced after pass execution, so do not require it inside this judicial pass.",
            "Use status done when the judicial handoff is complete; done is not a delivery certification claim.",
            "Do not repair implementation artifacts and do not certify delivery.",
        ]
    if profile == "repair-artifact-dogfood" and role == "executive":
        return [
            "Inspect artifacts/repair-target.json and identify that it is intentionally invalid.",
            "Return an executive handoff only; do not repair the artifact in this pass.",
            "Use status done when the initial handoff records the broken artifact for judicial review.",
        ]
    if profile == "repair-loop" and role == "executive":
        return [
            "Execute the initial bounded repair-loop dogfood pass using only this task capsule.",
            "Return an executive handoff that identifies a small scoped output and at least one limitation for judicial review.",
            "Do not validate your own output and do not certify delivery.",
        ]
    if profile == "repair-artifact-dogfood" and role == "repair":
        return [
            "Repair only artifacts/repair-target.json using artifactWrites.",
            "Write JSON content with component DriverStatusBadge, statusLabel Ready, isValid true, and repairedBy repair-1.",
            "Do not validate your own repair and do not certify delivery.",
            "Return a repair handoff with status done and list artifacts/repair-target.json in filesChanged/outputReferences.",
        ]
    if role == "repair":
        return [
            "Repair only the failures listed by the prior judicial handoff and runner evidence.",
            "The runner report is produced after pass execution, so do not require it inside this repair pass.",
            "Do not validate your own repair and do not certify delivery.",
            "Return a repair handoff that identifies files changed, commands run, remaining limitations, and handoffTo judicial.",
        ]
    if role == "judicial":
        return [
            "Validate current artifacts, executive handoff, runner report, and required hard-check evidence.",
            "Do not use unbounded prior chat or executor claims as verdict evidence.",
        ]
    if role == "certification":
        return [
            "Read judicial handoff, validation report, runner report, and delivery certification gates.",
            "Keep delivery not-certified unless delivery law evidence exists.",
        ]
    return ["fill with minimal required context before launch"]


def task_capsule(workflow_id, pass_id, role, profile="scaffold"):
    authority = ROLE_AUTHORITY[role]
    allowed_actions = list(authority["allowedActions"])
    forbidden_actions = list(authority["forbiddenActions"])
    objective = f"Run {role} pass {pass_id}."
    may_edit_files = authority["mayEditFiles"]
    if profile == "llm-smoke":
        if role == "executive":
            objective = (
                "Execute a bounded LLM API smoke pass and write one executive "
                "handoff artifact without editing project files."
            )
            allowed_actions = ["read task capsule", "read context package", "write executive handoff"]
            forbidden_actions = [
                "edit project files",
                "validate own output",
                "certify delivery",
                "claim runner-enforced isolation",
                "use hidden prior chat",
            ]
            may_edit_files = False
        elif role == "judicial":
            objective = (
                "Independently review the executive handoff and invocation "
                "evidence from the bounded LLM API smoke pass."
            )
            allowed_actions = ["read executive handoff", "read invocation evidence", "write judicial verdict handoff"]
            forbidden_actions = [
                "repair implementation artifacts",
                "certify delivery complete",
                "ignore missing evidence",
                "use hidden prior chat",
            ]
    elif profile == "repair-artifact-dogfood":
        if role == "executive":
            objective = "Record the intentionally invalid repair-target artifact for judicial review."
            allowed_actions = ["read repair-target artifact", "write executive handoff"]
            forbidden_actions = ["edit artifacts", "validate own output", "certify delivery", "use hidden prior chat"]
            may_edit_files = False
        elif role == "judicial":
            objective = "Validate the explicitly referenced handoff and repair-target artifact for this pass."
            allowed_actions = ["read listed inputs", "write judicial handoff"]
            forbidden_actions = ["repair implementation artifacts", "certify delivery complete", "use hidden prior chat"]
        elif role == "repair":
            objective = "Repair the bounded repair-target artifact and write one repair handoff."
            allowed_actions = ["read prior judicial handoff", "write artifacts/repair-target.json", "write repair handoff"]
            forbidden_actions = ["validate own repair", "certify delivery", "write files outside artifactWriteRequests"]

    data = {
        "schemaVersion": "1.0",
        "workflowId": workflow_id,
        "taskId": f"{pass_id}-task",
        "role": role,
        "objective": objective,
        "allowedActions": allowed_actions,
        "forbiddenActions": forbidden_actions,
        "inputReferences": default_input_references(pass_id, role, profile),
        "contextSlices": default_context_slices(role, profile, pass_id),
        "outputContract": f"handoffs/{pass_id}.handoff.json",
        "requiredChecks": [],
        "stopCondition": "Write one handoff artifact and stop.",
    }
    if profile == "repair-artifact-dogfood" and role == "repair":
        data["artifactWriteRequests"] = [
            {
                "ref": "artifacts/repair-target.json",
                "description": "Rewrite the fixture JSON so statusLabel is Ready, isValid is true, and repairedBy is repair-1.",
                "required": True,
            }
        ]
    for key in ["mayEditFiles", "mayValidate", "mayRepair", "mayReport", "mayCertifyDelivery"]:
        data[key] = authority[key]
    data["mayEditFiles"] = may_edit_files
    return data


def handoff(workflow_id, pass_id, role, profile="scaffold"):
    authority = ROLE_AUTHORITY[role]
    data = {
        "schemaVersion": "1.0",
        "workflowId": workflow_id,
        "passId": pass_id,
        "taskId": f"{pass_id}-task",
        "role": role,
        "agentName": f"{role}-agent",
        "taskCapsuleRef": f"capsules/{pass_id}.task-capsule.json",
        "inputReferences": [],
        "outputReferences": [],
        "filesRead": [],
        "filesChanged": [],
        "commandsRun": [],
        "status": "not-started",
        "executionEvidence": protocol_defined_evidence(),
        "limitations": ["Scaffolded placeholder handoff; pass has not run."],
        "didNotDo": authority["forbiddenActions"],
        "handoffTo": authority["handoffTo"],
    }
    for key in ["mayEditFiles", "mayValidate", "mayRepair", "mayReport", "mayCertifyDelivery"]:
        data[key] = authority[key]
    if profile == "llm-smoke" and role == "executive":
        data["mayEditFiles"] = False
    return data


def hard_check_quick_validate():
    return {
        "id": "top-skill-quick-validate",
        "description": "Run top-skill package validation.",
        "requiredForComplete": True,
        "commandType": "python-script",
        "scriptRef": "scripts/quick_validate.py",
        "scriptBaseRef": "skill-root",
        "args": ["."],
        "cwdRef": "skill-root",
        "timeoutSeconds": 300,
    }


def hard_check_repair_artifact_fixture():
    return {
        "id": "repair-artifact-fixture",
        "description": "Validate the repaired artifact dogfood fixture.",
        "requiredForComplete": True,
        "commandType": "python-script",
        "scriptRef": "scripts/validate_repair_artifact_fixture.py",
        "scriptBaseRef": "skill-root",
        "args": ["artifacts/repair-target.json"],
        "cwdRef": "runner-root",
        "timeoutSeconds": 300,
    }


def pass_command_for_adapter(adapter_kind, adapter_dry_run):
    if adapter_kind != "llm-api":
        return {}
    args = ["--dry-run"] if adapter_dry_run else []
    return {
        "commandType": "python-script",
        "scriptRef": "scripts/adapters/llm_api_adapter.py",
        "scriptBaseRef": "skill-root",
        "args": args,
        "cwdRef": "runner-root",
    }


def runner_workflow(workflow_id, run_id, mode, runner_name, passes, adapter_kind, profile, adapter_dry_run):
    runner_enforced_adapter = adapter_kind in {"llm-api", "external-agent-runtime"}
    limitations = [
        "Scaffolded runner workflow.",
    ]
    if adapter_kind == "process":
        limitations.extend([
            "No pass commands are configured yet.",
            "No external runner-enforced invocation evidence is present.",
        ])
    elif adapter_dry_run:
        limitations.append("LLM API adapter is configured in dry-run mode and cannot provide model invocation evidence.")
    else:
        limitations.append("LLM API adapter is configured; runner-enforced evidence requires successful API credentials and separate model invocations.")

    required_roles = {"executive", "judicial", "certification"}
    if profile in {"repair-loop", "repair-artifact-dogfood"}:
        required_roles.add("repair")

    workflow = {
        "schemaVersion": "1.0",
        "workflowId": workflow_id,
        "runId": run_id,
        "runnerName": runner_name,
        "mode": mode,
        "runnerCapabilities": {
            "launchesSeparateProcesses": runner_enforced_adapter,
            "launchesSeparateInvocations": runner_enforced_adapter,
            "isolatesContexts": runner_enforced_adapter,
            "executesHardChecks": True,
            "validatesHandoffs": True,
        },
        "passes": [
            {
                "passId": pass_id,
                "role": role,
                "taskCapsuleRef": f"capsules/{pass_id}.task-capsule.json",
                "handoffArtifactRef": f"handoffs/{pass_id}.handoff.json",
                "invocationId": f"{run_id}-{pass_id}-invocation",
                "contextId": f"{run_id}-{pass_id}-context",
                "adapterKind": adapter_kind,
                "contextPackageRef": f"contexts/{pass_id}.context-package.json",
                "invocationEvidenceRef": f"invocations/{pass_id}.invocation-evidence.json",
                "freshContextRequired": True,
                "command": None if adapter_kind == "process" else None,
                "cwd": None,
                **pass_command_for_adapter(adapter_kind, adapter_dry_run),
                "timeoutSeconds": 300,
                "requiredForDelivery": role in required_roles,
            }
            for pass_id, role in passes
        ],
        "hardChecks": (
            [hard_check_quick_validate(), hard_check_repair_artifact_fixture()]
            if profile == "repair-artifact-dogfood"
            else [hard_check_quick_validate()] if profile in {"llm-smoke", "repair-loop"} else []
        ),
        "deliveryCertificationRef": "reports/delivery-certification.json",
        "limitations": limitations,
    }
    if profile in {"repair-loop", "repair-artifact-dogfood"}:
        workflow["repairPolicy"] = {
            "maxRepairAttempts": 1,
            "repairPassIds": ["repair-1"],
            "finalJudicialPassId": "judicial",
            "requiresPostRepairJudicial": True,
            "limitations": [
                "This scaffold creates one bounded repair attempt; additional attempts require explicit new pass ids or a new run."
            ],
        }
    return workflow


def delivery_certification(workflow_id, run_id, profile="scaffold"):
    return {
        "schemaVersion": "1.0",
        "certificationId": f"{run_id}-delivery-certification",
        "workflowId": workflow_id,
        "deliveryStatus": "not-certified",
        "executionEvidence": protocol_defined_evidence(),
        "judicialValidationRef": "reports/validation-report.json",
        "judicialHandoffRef": "handoffs/judicial.handoff.json",
        "validationReportRef": "reports/validation-report.json",
        "finalAuditReportRef": "reports/final-audit.md",
        "generationOrRepairPassIds": [],
        "repairAttemptIds": ["repair-1"] if profile == "repair-loop" else [],
        "judicialPassId": "judicial",
        "separationOfPowersProof": ["Scaffolded only; no passes have run."],
        "requiredHardChecks": [],
        "blockingChecks": [
            {
                "checkId": "runner-evidence",
                "status": "not_verified",
                "evidence": ["Runner has not produced evidence yet."],
            }
        ],
        "knownExclusions": [],
        "noBlockingInScopeViolations": False,
        "generationAndValidationSeparate": False,
        "noUnverifiedRequiredGates": False,
        "noRequiredGateFailedOrNotVerified": False,
    }


def run_state(workflow_id, run_id):
    return {
        "schemaVersion": "1.0",
        "workflowId": workflow_id,
        "runId": run_id,
        "currentState": "scaffolded",
        "previousState": None,
        "derivedAt": utc_now(),
        "derivedBy": "scripts/create_orchestration_run.py",
        "stateEvidence": [
            {
                "checkId": "initial-scaffold",
                "status": "not_verified",
                "details": ["Run package was scaffolded; no execution evidence exists yet."],
            }
        ],
        "artifactRefs": {
            "runnerWorkflow": "runner/runner-workflow.json",
            "runnerReport": "runner/runner-report.json",
            "judicialHandoff": "handoffs/judicial.handoff.json",
            "deliveryCertification": "reports/delivery-certification.json",
            "certificationSnapshot": "reports/certification-snapshot.json",
        },
        "allowedNextStates": ["passes-executed", "runner-verified", "judicial-validated", "not-certified", "certified", "stale", "failed"],
        "limitations": ["Scaffolded state; update with scripts/update_orchestration_state.py after execution evidence changes."],
    }


def validation_report(workflow_id, run_id):
    return {
        "schemaVersion": "1.0",
        "reportId": f"{run_id}-validation-report",
        "workflowId": workflow_id,
        "judicialPassId": "judicial",
        "judicialHandoffRef": "handoffs/judicial.handoff.json",
        "repairAttemptIds": [],
        "executionEvidence": protocol_defined_evidence(),
        "artifactScope": "not selected",
        "checkedFiles": ["not_verified"],
        "commandsRun": [],
        "requiredHardChecks": [],
        "violationClassesChecked": ["not_verified"],
        "gateResults": [
            {
                "gateId": "initial-scaffold",
                "violationClass": "workflow",
                "status": "not_verified",
                "evidence": ["Scaffolded validation report; validation has not run."],
            }
        ],
        "blockingViolations": [],
        "unverifiedAreas": ["All areas are unverified in scaffolded state."],
        "finalValidationStatus": "not_verified",
        "independence": {
            "currentFilesRead": False,
            "executorClaimsIgnored": False,
            "samePassAsGenerationOrRepair": False,
            "selfCertificationDetected": False,
        },
    }


def run_readme(workflow_id, run_id, mode, profile, adapter_kind):
    live_note = ""
    if profile == "llm-smoke":
        live_note = f"""
LLM smoke execution:

```text
$env:TOP_LLM_API_KEY = "<secret>"
$env:TOP_LLM_MODEL = "<model>"
python -B scripts/top_protocol_runner.py runner/runner-workflow.json --root top/orchestration/{workflow_id}/{run_id} --execute-passes --execute-hard-checks --accept-external-runner-evidence --report-out runner/runner-report.json
```

This run can prove runner-enforced isolation only after the LLM API adapter
writes model invocation evidence for each required pass.
"""
    if profile == "repair-loop":
        live_note = """
Repair loop profile:

```text
executive -> judicial-initial -> repair-1 -> judicial
```

Delivery complete is forbidden unless the final `judicial` pass validates
post-repair artifacts after `repair-1`.
"""
    if profile == "repair-artifact-dogfood":
        live_note = """
Repair artifact dogfood profile:

```text
executive -> judicial-initial -> repair-1 -> judicial
```

The repair pass may write only `artifacts/repair-target.json`. Delivery complete
requires the repaired artifact hard check and final post-repair judicial pass.
"""
    return f"""# Orchestration Run

workflowId: {workflow_id}
runId: {run_id}
mode: {mode}
profile: {profile}
adapterKind: {adapter_kind}

This package was scaffolded by `scripts/create_orchestration_run.py`.

Initial status:

- currentState: scaffolded
- executionIsolationLevel: protocol-defined
- verificationEvidenceLevel: none
- deliveryStatus: not-certified

Refresh `run-state.json` after runner, judicial, certification, or snapshot
changes:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/{workflow_id}/{run_id}
```

Do not report this run as runner-enforced, hard-check-verified, or delivery
complete until the runner, judicial validation, hard checks, and delivery
certification artifacts provide that evidence.
{live_note}
"""


def run_log(workflow_id, run_id):
    return f"""# Run Log

## created

- workflowId: {workflow_id}
- runId: {run_id}
- status: scaffolded
- delivery: not-certified
"""


def final_audit_report(workflow_id, run_id):
    return f"""# Final Audit

workflowId: {workflow_id}
runId: {run_id}
deliveryStatus: not-certified

This is a scaffolded final audit placeholder. It must not be rewritten as
complete or certified unless delivery law evidence exists:

- executionIsolationLevel: runner-enforced
- verificationEvidenceLevel: hard-check-verified
- valid independent judicial handoff artifact
- no required gate is fail or not_verified
"""


def scaffold(args):
    root = Path(args.root).resolve()
    package_root = root / "top" / "orchestration" / args.workflow_id / args.run_id
    repair_loop = getattr(args, "repair_loop", False)
    repair_artifact_dogfood = getattr(args, "repair_artifact_dogfood", False)
    profile = (
        "llm-smoke"
        if args.llm_smoke
        else "repair-artifact-dogfood" if repair_artifact_dogfood
        else "repair-loop" if repair_loop
        else "scaffold"
    )
    adapter_kind = args.adapter_kind
    if args.llm_smoke and adapter_kind == "process":
        adapter_kind = "llm-api"
    if args.llm_smoke and not args.pass_:
        passes = [("executive", "executive"), ("judicial", "judicial")]
    elif (repair_loop or repair_artifact_dogfood) and not args.pass_:
        passes = [
            ("executive", "executive"),
            ("judicial-initial", "judicial"),
            ("repair-1", "repair"),
            ("judicial", "judicial"),
        ]
    else:
        passes = args.pass_ or [(role, role) for role in DEFAULT_ROLES]

    for dirname in ["artifacts", "capsules", "contexts", "handoffs", "invocations", "runner", "reports", "logs", "scratch"]:
        (package_root / dirname).mkdir(parents=True, exist_ok=True)

    write_text(package_root / "RUN_README.md", run_readme(args.workflow_id, args.run_id, args.mode, profile, adapter_kind), args.force)
    write_text(package_root / "logs" / "RUN_LOG.md", run_log(args.workflow_id, args.run_id), args.force)
    write_text(package_root / "reports" / "final-audit.md", final_audit_report(args.workflow_id, args.run_id), args.force)
    write_json(package_root / "run-state.json", run_state(args.workflow_id, args.run_id), args.force)
    if profile == "repair-artifact-dogfood":
        write_json(
            package_root / "artifacts" / "repair-target.json",
            {
                "component": "DriverStatusBadge",
                "statusLabel": "Broken",
                "isValid": False,
                "issue": "statusLabel must be Ready and isValid must be true.",
            },
            args.force,
        )

    for pass_id, role in passes:
        write_json(
            package_root / "capsules" / f"{pass_id}.task-capsule.json",
            task_capsule(args.workflow_id, pass_id, role, profile),
            args.force,
        )
        write_json(
            package_root / "handoffs" / f"{pass_id}.handoff.json",
            handoff(args.workflow_id, pass_id, role, profile),
            args.force,
        )

    write_json(
        package_root / "runner" / "runner-workflow.json",
        runner_workflow(
            args.workflow_id,
            args.run_id,
            args.mode,
            args.runner_name,
            passes,
            adapter_kind,
            profile,
            args.adapter_dry_run,
        ),
        args.force,
    )
    write_json(
        package_root / "reports" / "validation-report.json",
        validation_report(args.workflow_id, args.run_id),
        args.force,
    )
    write_json(
        package_root / "reports" / "delivery-certification.json",
        delivery_certification(args.workflow_id, args.run_id, profile),
        args.force,
    )
    print(package_root)


def main():
    parser = argparse.ArgumentParser(description="Create a TOP orchestration run package.")
    parser.add_argument("--root", default=".", help="Project or skill root")
    parser.add_argument("--workflow-id", required=True, help="Workflow id")
    parser.add_argument("--run-id", required=True, help="Run id")
    parser.add_argument("--mode", default="validation", help="Task mode")
    parser.add_argument("--runner-name", default="top-protocol-runner", help="Runner name")
    parser.add_argument(
        "--adapter-kind",
        default="process",
        choices=["process", "llm-api"],
        help="Pass adapter kind to configure in the runner workflow.",
    )
    parser.add_argument(
        "--llm-smoke",
        action="store_true",
        help="Create a concrete two-pass llm-api smoke run instead of placeholder protocol scaffold.",
    )
    parser.add_argument(
        "--repair-loop",
        action="store_true",
        help="Create a bounded executive -> judicial -> repair -> judicial workflow profile.",
    )
    parser.add_argument(
        "--repair-artifact-dogfood",
        action="store_true",
        help="Create a repair-loop profile with a real bounded artifact write.",
    )
    parser.add_argument(
        "--adapter-dry-run",
        action="store_true",
        help="Add --dry-run to llm-api adapter pass commands.",
    )
    parser.add_argument(
        "--pass",
        dest="pass_",
        action="append",
        type=parse_pass,
        help="Add pass as pass-id:role. Can be repeated.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()
    try:
        scaffold(args)
    except Exception as exc:
        print(f"create_orchestration_run: FAILED\n- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
