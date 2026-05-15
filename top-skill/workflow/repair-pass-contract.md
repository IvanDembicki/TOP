# Repair Pass Contract

## Purpose

A repair pass fixes scoped failures reported by a prior judicial pass. It is an
executor-family pass, not a validator, reporter, or certification authority.

## Authority

Repair pass authority:

- `mayEditFiles: true`
- `mayRepair: true`
- `mayValidate: false`
- `mayCertifyDelivery: false`

The repair pass may only change artifacts named by its task capsule or by the
prior judicial failure evidence.

## Bounded Artifact Writes

When a repair pass is allowed to materialize run-package artifacts, the task
capsule must list exact refs in `artifactWriteRequests`.

Each request must name:

- `ref`;
- `description`;
- `required`.

The adapter may write only those exact refs. The pass invocation evidence must
record every materialized write in `artifactWrites` with the ref and artifact
hash.

Unlisted artifact writes are invalid. Required artifact writes that are not
materialized are invalid.

## Required Inputs

A repair task capsule must receive bounded inputs:

- prior judicial handoff;
- runner report or validation evidence naming the failed gates;
- explicit file or artifact refs allowed for repair;
- stop condition and output handoff path.

The repair pass must not receive uncontrolled prior chat as hidden context.

## Required Handoff

A repair handoff must report:

- files read;
- files changed;
- commands run;
- failed gates addressed;
- gates intentionally not addressed;
- limitations;
- `handoffTo: judicial`.

## Post-Repair Judicial Law

A repair result is not a verdict.

If any repair pass runs and delivery is later reported as complete, the final
judicial handoff must come from a judicial pass that occurs after the latest
completed repair pass in the runner workflow.

Delivery complete is invalid when it relies on:

- a pre-repair judicial handoff;
- a repair handoff as a judicial verdict;
- a repair pass that validates or certifies its own output;
- stale certification from before the repair.

If a repair handoff or invocation evidence reports repaired artifact refs, the
post-repair judicial handoff must read those refs before delivery can be
certified complete.

## Attempt Limits

Runner workflows may define `repairPolicy`:

```json
{
  "maxRepairAttempts": 1,
  "repairPassIds": ["repair-1"],
  "finalJudicialPassId": "judicial",
  "requiresPostRepairJudicial": true,
  "limitations": []
}
```

The orchestrator must stop when `maxRepairAttempts` is exhausted or when the
same blocking failure repeats without new repair evidence.
