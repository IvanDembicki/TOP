# Activation and Operating Procedure

## Purpose

This file defines when top-skill 2.0 orchestration is active and how an agent
must operate it. It connects the evidence model, task capsules, handoffs, run
packages, runner gate, judicial validation, and delivery certification into one
working process.

## Activation Triggers

Use 2.0 orchestration when a task includes any of:

- migration;
- generation or regeneration;
- repair after validation;
- validation that may affect delivery status;
- final audit or delivery certification;
- top-skill maintenance;
- multi-pass workflow;
- any claim that work is complete, certified, ready, or delivery-ready.

If the task is a small discussion or analysis-only answer, 2.0 may remain
protocol-defined unless the answer claims delivery.

## First Action

Before implementation, validation, repair, or delivery certification begins,
the orchestrator must create or select a run package:

```text
top/orchestration/<workflow-id>/<run-id>/
```

Use `scripts/create_orchestration_run.py` when a package does not already exist.
Use `scripts/run_orchestration_workflow.py` when the current task should run the
standard ordered driver instead of manually chaining create, runner,
certification, snapshot verification, and verifier commands.

## Operating Loop

1. Orchestrator creates or updates one task capsule for the next pass.
2. The assigned pass receives only that capsule and required context slices.
3. The pass writes exactly one handoff artifact and stops.
4. Orchestrator accepts or rejects the handoff.
5. Runner validates handoff consistency and runs required hard checks when
   configured.
6. Judicial pass validates current artifacts and runner evidence.
7. Certification gate runs `scripts/certify_orchestration_run.py` and updates
   validation report, delivery certification, and final audit only when
   delivery law evidence exists.
8. Runner and certifier refresh `run-state.json` after runner, judicial,
   certification, or snapshot evidence changes. Manual refresh uses
   `scripts/update_orchestration_state.py`.
9. Run verifier checks the package read-only with
   `scripts/validate_orchestration_run.py` before a final validity claim.

`scripts/run_orchestration_workflow.py` may execute this sequence as one driver,
but it does not replace the verifier. The driver's final claim must be the
status returned by `scripts/validate_orchestration_run.py`.

## Protocol-Only Bridge

Until an external invocation runner exists, the workflow is protocol-only by
default. The agent may still create capsules, handoffs, runner workflows, and
reports, and may run hard checks through `scripts/top_protocol_runner.py`.

Protocol-only work may be useful and may be reported as `not-certified`, but it
must not be reported as `runner-enforced`, `hard-check-verified` unless hard
checks actually ran, or delivery `complete`.

## Status Reporting

Any final response for an orchestrated task must include:

- `executionIsolationLevel`
- `verificationEvidenceLevel`
- `deliveryStatus`
- runner report path, if any
- validation report path, if any
- delivery certification path, if any
- run state path, if any
- run verifier status, if any
- limitations

Avoid unqualified words such as `complete`, `certified`, `ready`, or `done`
unless the delivery law in `workflow/enforcement-evidence-model.md` is
satisfied.

## Mutation Ownership

- Orchestrator owns task capsules and runner workflow setup.
- Executive owns only its scoped implementation artifacts and handoff.
- Repair owns only scoped repair artifacts and handoff.
- Runner owns runner report.
- Judicial validation owns validation report.
- Certification owns delivery certification and final audit.
- State updater owns `run-state.json` as derived process evidence indexing.
- Run log is append-only.

## Stop Rule

Each pass stops after writing its handoff. It does not pick the next pass,
validate itself, repair itself, or certify delivery unless its task capsule
explicitly grants that authority.

## Adoption Rule

Do not wait for a perfect runner to use 2.0. Start with run packages and honest
evidence levels. The immediate goal is to eliminate hidden self-certification
and make missing enforcement visible.
