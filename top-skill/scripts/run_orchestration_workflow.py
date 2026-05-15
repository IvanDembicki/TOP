#!/usr/bin/env python3
import argparse
import contextlib
import sys
from pathlib import Path
from types import SimpleNamespace


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from certify_orchestration_run import certify, verify_snapshot
from create_orchestration_run import parse_pass, scaffold
from top_protocol_runner import load_json, resolve_inside_root, run_workflow, update_run_state, write_json
from validate_orchestration_run import validate_run


DEFAULT_REFS = {
    "runner_workflow": "runner/runner-workflow.json",
    "runner_report": "runner/runner-report.json",
    "judicial_handoff": "handoffs/judicial.handoff.json",
    "validation_report": "reports/validation-report.json",
    "delivery_certification": "reports/delivery-certification.json",
    "final_audit": "reports/final-audit.md",
    "certification_snapshot": "reports/certification-snapshot.json",
    "state": "run-state.json",
}

FINAL_VERIFIER_STATUSES = [
    "RUN_VALID certified",
    "RUN_VALID not-certified",
    "RUN_STALE",
    "RUN_INVALID",
]


def driver_line(message):
    print(f"run_orchestration_workflow: {message}")


def resolve_run_root(args):
    if args.run_root:
        return Path(args.run_root).resolve()
    if not args.workflow_id or not args.run_id:
        raise ValueError("--workflow-id and --run-id are required when --run-root is not provided")
    return (Path(args.root).resolve() / "top" / "orchestration" / args.workflow_id / args.run_id).resolve()


def should_create(args):
    if args.create:
        return True
    if args.run_root:
        return False
    return not args.skip_create


def create_run_package(args, run_root):
    if not should_create(args):
        return None
    if not args.workflow_id or not args.run_id:
        raise ValueError("--workflow-id and --run-id are required to create a run package")
    create_args = SimpleNamespace(
        root=args.root,
        workflow_id=args.workflow_id,
        run_id=args.run_id,
        mode=args.mode,
        runner_name=args.runner_name,
        adapter_kind=args.adapter_kind,
        llm_smoke=args.llm_smoke,
        repair_loop=getattr(args, "repair_loop", False),
        repair_artifact_dogfood=getattr(args, "repair_artifact_dogfood", False),
        adapter_dry_run=args.adapter_dry_run,
        pass_=args.pass_,
        force=args.force,
    )
    with contextlib.redirect_stdout(sys.stderr):
        scaffold(create_args)
    return f"created {run_root}"


def run_protocol_runner(args, run_root):
    workflow_path = resolve_inside_root(run_root, args.runner_workflow, "runner workflow")
    runner_workflow = load_json(workflow_path)
    report, errors = run_workflow(
        runner_workflow,
        run_root,
        execute_passes=args.execute_passes,
        execute_hard_checks=args.execute_hard_checks,
        accept_external_runner_evidence=args.accept_external_runner_evidence,
    )
    report_path = resolve_inside_root(run_root, args.runner_report, "runner report")
    write_json(report_path, report)
    update_run_state(run_root, args.runner_workflow, args.runner_report)
    if errors:
        return "runner-failed", errors
    return report.get("runnerStatus", "unknown"), []


def certification_args(args, run_root, verify=False):
    return SimpleNamespace(
        root=str(run_root),
        runner_workflow=args.runner_workflow,
        runner_report=args.runner_report,
        judicial_handoff=args.judicial_handoff,
        validation_report=args.validation_report,
        delivery_certification=args.delivery_certification,
        final_audit=args.final_audit,
        snapshot=args.certification_snapshot,
        state=args.state,
        skip_state_update=False,
        verify_snapshot=verify,
    )


def run_certification(args, run_root):
    return certify(certification_args(args, run_root, verify=False))


def run_snapshot_verification(args, run_root):
    return verify_snapshot(certification_args(args, run_root, verify=True))


def verifier_args(args, run_root):
    return SimpleNamespace(
        root=str(run_root),
        runner_workflow=args.runner_workflow,
        runner_report=args.runner_report,
        judicial_handoff=args.judicial_handoff,
        delivery_certification=args.delivery_certification,
        certification_snapshot=args.certification_snapshot,
        state=args.state,
    )


def run_final_verifier(args, run_root):
    return validate_run(verifier_args(args, run_root))


def drive(args):
    run_root = resolve_run_root(args)
    step_errors = []

    create_result = create_run_package(args, run_root)
    if create_result:
        driver_line(f"CREATE_OK {run_root}")
    else:
        driver_line(f"CREATE_SKIPPED {run_root}")

    if args.skip_runner:
        driver_line("RUNNER_SKIPPED")
    else:
        runner_status, runner_errors = run_protocol_runner(args, run_root)
        if runner_errors:
            driver_line(f"RUNNER_FAILED status={runner_status}")
            for error in runner_errors:
                print(f"- runner: {error}")
            step_errors.extend(runner_errors)
            if args.stop_on_runner_failure:
                return "RUN_INVALID", None, step_errors, [], run_root
        else:
            driver_line(f"RUNNER_OK status={runner_status}")

    if args.skip_certification:
        driver_line("CERTIFICATION_SKIPPED")
    else:
        certification_result = run_certification(args, run_root)
        if certification_result == 0:
            driver_line("CERTIFICATION_COMPLETE")
        elif certification_result == 1:
            driver_line("CERTIFICATION_NOT_CERTIFIED")
        else:
            driver_line("CERTIFICATION_FAILED")
            step_errors.append(f"certification exited {certification_result}")

    if args.skip_snapshot_verify:
        driver_line("SNAPSHOT_VERIFY_SKIPPED")
    else:
        snapshot_result = run_snapshot_verification(args, run_root)
        if snapshot_result == 0:
            driver_line("SNAPSHOT_CURRENT")
        elif snapshot_result == 1:
            driver_line("SNAPSHOT_STALE")
        else:
            driver_line("SNAPSHOT_VERIFY_FAILED")
            step_errors.append(f"snapshot verification exited {snapshot_result}")

    status, delivery_status, invalid, stale = run_final_verifier(args, run_root)
    for item in stale:
        print(f"- stale: {item}")
    for item in invalid:
        print(f"- invalid: {item}")

    all_errors = step_errors + invalid
    return status, delivery_status, all_errors, stale, run_root


def main():
    parser = argparse.ArgumentParser(description="Run a TOP orchestration workflow driver.")
    parser.add_argument("--root", default=".", help="Skill or project root used when creating a run package")
    parser.add_argument("--run-root", help="Existing run package root. Creation is skipped by default when provided.")
    parser.add_argument("--workflow-id", help="Workflow id for a created run package")
    parser.add_argument("--run-id", help="Run id for a created run package")
    parser.add_argument("--mode", default="validation", help="Task mode for a created run package")
    parser.add_argument("--runner-name", default="top-protocol-runner", help="Runner name for a created run package")
    parser.add_argument("--adapter-kind", default="process", choices=["process", "llm-api"], help="Pass adapter kind for a created run package")
    parser.add_argument("--llm-smoke", action="store_true", help="Create a bounded two-pass llm-api smoke run")
    parser.add_argument("--repair-loop", action="store_true", help="Create a bounded executive, judicial, repair, judicial run")
    parser.add_argument("--repair-artifact-dogfood", action="store_true", help="Create a bounded repair loop with a real artifact write")
    parser.add_argument("--adapter-dry-run", action="store_true", help="Add --dry-run to llm-api adapter pass commands during creation")
    parser.add_argument("--pass", dest="pass_", action="append", type=parse_pass, help="Add pass as pass-id:role when creating a run package")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold files during creation")
    parser.add_argument("--create", action="store_true", help="Create or recreate the run package even when --run-root is provided")
    parser.add_argument("--skip-create", action="store_true", help="Skip run package creation")
    parser.add_argument("--skip-runner", action="store_true", help="Skip protocol runner execution")
    parser.add_argument("--skip-certification", action="store_true", help="Skip post-run certification")
    parser.add_argument("--skip-snapshot-verify", action="store_true", help="Skip certification snapshot verification")
    parser.add_argument("--execute-passes", action="store_true", help="Execute pass commands through the protocol runner")
    parser.add_argument("--execute-hard-checks", action="store_true", help="Execute hard-check commands through the protocol runner")
    parser.add_argument(
        "--accept-external-runner-evidence",
        action="store_true",
        help="Allow runner-enforced status only when external invocation evidence exists",
    )
    parser.add_argument("--stop-on-runner-failure", action="store_true", help="Stop before certification if the runner reports errors")
    parser.add_argument("--runner-workflow", default=DEFAULT_REFS["runner_workflow"])
    parser.add_argument("--runner-report", default=DEFAULT_REFS["runner_report"])
    parser.add_argument("--judicial-handoff", default=DEFAULT_REFS["judicial_handoff"])
    parser.add_argument("--validation-report", default=DEFAULT_REFS["validation_report"])
    parser.add_argument("--delivery-certification", default=DEFAULT_REFS["delivery_certification"])
    parser.add_argument("--final-audit", default=DEFAULT_REFS["final_audit"])
    parser.add_argument("--certification-snapshot", default=DEFAULT_REFS["certification_snapshot"])
    parser.add_argument("--state", default=DEFAULT_REFS["state"])
    args = parser.parse_args()

    try:
        status, delivery_status, errors, stale, run_root = drive(args)
    except Exception as exc:
        print("run_orchestration_workflow: FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 2

    driver_line(status)
    if delivery_status:
        print(f"deliveryStatus: {delivery_status}")
    print(f"runRoot: {run_root}")

    if status.startswith("RUN_VALID") and not errors:
        return 0
    if status == "RUN_STALE" or stale:
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
