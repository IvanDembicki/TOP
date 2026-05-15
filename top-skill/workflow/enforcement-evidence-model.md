# Enforcement Evidence Model

## Purpose

This file is the root contract for delivery honesty in top-skill 2.0 protocol
mode. It separates execution isolation from validation evidence. These axes
must not be collapsed into one status.

Activation and operating steps are defined in
`workflow/activation-and-operating-procedure.md`.

## executionIsolationLevel

Describes how role separation was enforced.

- `protocol-defined` — the protocol exists in top-skill, but no execution
  evidence is provided.
- `protocol-followed-by-agent` — an agent claims it followed the protocol, but
  execution was not externally enforced.
- `schema-validated` — workflow artifacts passed JSON Schema validation. This
  does not prove physical role isolation.
- `runner-enforced` — an external runner launched separate passes with separate
  task capsules, separate contexts, and explicit handoff artifacts.

## verificationEvidenceLevel

Describes what evidence proves that validation checks were performed.

- `none` — no validation evidence.
- `agent-claimed` — an agent claims validation was performed.
- `schema-validated` — validation or report artifacts passed JSON Schema
  validation.
- `hard-check-verified` — required executable hard checks were actually run and
  all required gates passed.

## Protocol-Only Mode

When no external runner is used, top-skill operates in protocol-only mode. A
single LLM invocation may report `protocol-followed-by-agent` and may report
`schema-validated` only when schema validation was actually run. It must not
report `runner-enforced`.

## False Substitutes

- Schema validation is not role isolation.
- Hard checks are not role isolation.
- Multiple role headings in one answer are not role isolation.
- A single LLM invocation instructed to act as multiple agents is simulated
  separation, not enforced separation.
- Simulated separation cannot certify independent validation or delivery
  complete.

## Delivery Law

`deliveryStatus = complete` requires:

1. `executionIsolationLevel = runner-enforced`
2. `verificationEvidenceLevel = hard-check-verified`
3. valid independent judicial handoff artifact
4. no required gate is `fail` or `not_verified`

unless the active mode explicitly declares that it does not certify delivery.

If any condition is missing, the result may be useful, partial, or
protocol-followed, but it must not be reported as delivery complete.

## Hard Check / Judicial Handoff Symmetry

A hard check result without a judicial handoff is evidence, but not a judicial
verdict.

A judicial handoff without required hard-check evidence cannot certify delivery
complete.

## Required executionEvidence Fields

All delivery, handoff, and validation artifacts that affect certification must
include:

- `executionIsolationLevel`
- `verificationEvidenceLevel`
- `runnerName`
- `separateInvocationIds`
- `schemaValidationCommand`
- `hardCheckCommands`
- `limitations`

## Schema Limits and Runner Requirements

JSON Schema can validate artifact shape and some delivery gates. It cannot
prove that separate invocations actually occurred or that a runner restricted
context at runtime.

`scripts/validate_execution_evidence.py` is the protocol-layer hard validator
for delivery evidence artifacts. It provides a blocking exit code for false
`complete` claims, missing execution evidence, missing judicial handoff
references, and required gates with `fail` or `not_verified` status.

`scripts/top_protocol_runner.py` is the minimal protocol runner gate. It
validates runner workflow artifacts, task capsule to handoff consistency, and
hard-check exit codes. Its report is evidence, not a judicial verdict.

`scripts/create_orchestration_run.py` creates the canonical run package defined
in `workflow/run-package-layout.md`. The package starts as `protocol-defined`
and `not-certified`.

`scripts/certify_orchestration_run.py` is the post-run certification gate. It
reads runner evidence and the independent judicial handoff, writes validation
and delivery certification artifacts, and reports `deliveryStatus: complete`
only when all delivery law gates pass.

The certification gate also writes `reports/certification-snapshot.json`.
Snapshot verification detects whether any checked run-package artifact changed
after certification. A stale snapshot blocks treating an existing
`deliveryStatus: complete` claim as current.

Runner-enforced delivery still requires an external harness that verifies
invocation boundaries, task capsules, handoff artifacts, and hard-check command
results.
