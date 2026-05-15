# Orchestration Run State Machine

## Purpose

The run state machine records where one orchestration run package stands in the
execution-governance workflow. It is derived from artifacts, not from agent
claims.

The state machine does not certify delivery by itself. Certification remains
owned by `workflow/delivery-certification-procedure.md` and the delivery law in
`workflow/enforcement-evidence-model.md`.

## State Artifact

Each run package may contain:

```text
run-state.json
```

The artifact follows `top/schemas/run-state.schema.json` and is written by:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/<workflow-id>/<run-id>
```

Use `--verify` to derive and validate the state without rewriting the artifact.

`scripts/top_protocol_runner.py` refreshes `run-state.json` after it writes a
runner report. `scripts/certify_orchestration_run.py` refreshes it after
certification and after snapshot verification. Use `--skip-state-update` only
for diagnostics.

`scripts/validate_orchestration_run.py` independently derives state and compares
it to persisted `run-state.json` without rewriting artifacts.

## States

- `scaffolded` — run package exists, but no executed pass evidence exists.
- `passes-executed` — at least one pass result or completed handoff exists, but
  runner evidence is not yet verified.
- `runner-verified` — runner report exists and has `runnerStatus: pass`.
- `judicial-validated` — a valid judicial handoff exists.
- `not-certified` — certification output exists but delivery gates did not pass.
- `certified` — delivery certification is `complete` and the certification
  snapshot is current.
- `stale` — delivery certification was complete, but snapshot verification no
  longer matches current run-package artifacts.
- `failed` — runner or required pass evidence reports failure or blocked status.

## Transition Rule

The updater allows monotonic forward movement when later evidence already
implies earlier states. It blocks silent regression from a stronger state to a
weaker state unless `--force` is used.

Examples:

- `scaffolded -> judicial-validated` is allowed if a runner run already
  completed before state was updated.
- `certified -> stale` is allowed when snapshot verification fails.
- `certified -> runner-verified` is blocked unless forced, because deleting or
  rewriting certification artifacts must not silently downgrade a certified run.

## Evidence Sources

The updater derives state from:

- `runner/runner-workflow.json`
- `runner/runner-report.json`
- `handoffs/judicial.handoff.json`
- `reports/delivery-certification.json`
- `reports/certification-snapshot.json`

It records the evidence checks it used in `stateEvidence`.

## Non-Goals

The state machine does not:

- launch passes;
- run hard checks;
- validate JSON Schema by itself;
- write judicial verdicts;
- certify delivery complete;
- replace snapshot stale detection.

It only makes the process state explicit and searchable.
