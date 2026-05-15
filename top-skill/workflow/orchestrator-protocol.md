# Orchestrator Protocol

## Purpose

The orchestrator controls workflow progression. It is a process controller, not
an executor, validator, repairer, or final evidence source.

Activation and the practical operating loop are defined in
`workflow/activation-and-operating-procedure.md`.

## Workflow, Not Free Agent Loop

TOP migration, validation, repair, reporting, and delivery certification are
workflows. The orchestrator owns control flow. Specialist micro-agents may make
local decisions only inside their assigned task capsule.

## Harness Context Operations

- Write: passes return handoff artifacts, logs, reports, and scratch evidence.
- Select: each task capsule receives only required context slices.
- Compress: downstream reporting and validation receive structured summaries
  and artifact references instead of uncontrolled full context.
- Isolate: executor, validator, repair, reporting, and certification roles run
  as separate passes when a runner exists; otherwise separation is protocol-only.

## Protocol-Only vs Runner-Enforced Execution

In protocol-only mode, the orchestrator may define capsules and evaluate
handoffs, but it cannot claim physical isolation. Runner-enforced execution
requires an external harness that launches separate passes with separate
contexts.

## Capsule Creation

For each pass, the orchestrator or context builder creates one task capsule with
one role, one objective, allowed actions, forbidden actions, context slices,
authority flags, output contract, and stop condition.

## Pass Launch

The orchestrator launches or requests one pass per capsule. A single pass must
not combine execution, validation, repair, reporting, and delivery
certification powers.

When a runner is available, the orchestrator writes or selects a runner workflow
artifact defined by `workflow/runner-contract.md`. The runner may launch pass
commands, validate capsule to handoff consistency, run hard checks, and return a
runner report.

For a new workflow, the orchestrator should create or select a run package using
`workflow/run-package-layout.md`. A scaffolded run package is only
`protocol-defined` and `not-certified` until actual pass, runner, judicial, and
hard-check evidence exists.

## Handoff Acceptance

The orchestrator accepts a handoff only when it matches the capsule, contains
required execution evidence, respects role authority, and identifies files,
commands, outputs, limitations, and powers not exercised.

## Repair Loop

When judicial validation fails, the orchestrator creates a repair capsule from
the validation failures. After repair, a separate judicial pass must revalidate.

Repair authority, attempt limits, and post-repair judicial requirements are
defined in `workflow/repair-pass-contract.md`.

## Delivery Certification Gate

Delivery certification must follow `workflow/enforcement-evidence-model.md`.
The orchestrator must not mark delivery complete unless the delivery law is
satisfied or the active mode explicitly does not certify delivery.

A runner report is evidence for the gate. It is not the final judicial verdict.
