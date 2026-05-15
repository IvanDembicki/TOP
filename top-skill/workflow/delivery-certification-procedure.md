# Delivery Certification Procedure

## Purpose

This file defines the executable post-run certification step for top-skill 2.0
orchestration. The runner proves execution evidence, the judicial pass provides
an independent verdict handoff, and the certification gate decides whether the
run package can honestly report `deliveryStatus: complete`.

This procedure is scope-limited to one orchestration run package. Certifying a
smoke run does not certify an entire top-skill release.

## Certification Script

```text
scripts/certify_orchestration_run.py
```

The script reads:

- `runner/runner-workflow.json`
- `runner/runner-report.json`
- `handoffs/judicial.handoff.json`

It writes:

- `reports/validation-report.json`
- `reports/delivery-certification.json`
- `reports/final-audit.md`
- `reports/certification-snapshot.json`

After this script writes certification artifacts, it refreshes `run-state.json`
unless `--skip-state-update` is used. Manual refresh remains available:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/<workflow-id>/<run-id>
```

The state update is process evidence indexing only. It does not replace the
delivery certification gate.

## Required Gates

The script may write `deliveryStatus: complete` only when all gates pass:

- runner report status is `pass`;
- runner report execution evidence is `runner-enforced`;
- runner report verification evidence is `hard-check-verified`;
- all delivery-required passes are `pass`;
- all delivery-required passes have fresh context, context-package-only input,
  and model invocation evidence;
- at least two distinct required invocation ids and context ids exist;
- all required hard checks are `pass`;
- judicial handoff is present, has role `judicial`, status `done` or
  `complete`, validation authority, and no edit/repair/certification authority;
- no executive or repair pass certified delivery.

If any gate fails, the script writes `not-certified` with blocking evidence.

## Evidence Ownership

The script does not create runner evidence and does not replace judicial
validation. It only composes existing runner evidence, hard-check results, and a
judicial handoff into validation and certification artifacts.

Runner report is evidence. Judicial handoff is verdict. Certification is the
delivery gate.

## Certification Snapshot

Certification also writes a snapshot of the artifacts used to produce the
delivery verdict. The snapshot records `sha256` for run-package artifacts such
as task capsules, context packages, handoffs, invocation evidence, runner
workflow/report, validation report, delivery certification, and final audit.

The snapshot answers one question:

```text
Did any checked artifact change after certification?
```

Verify it with:

```text
python -B scripts/certify_orchestration_run.py --root top/orchestration/<workflow-id>/<run-id> --verify-snapshot
```

If verification reports `SNAPSHOT_STALE`, the existing delivery certification
must not be treated as current. Re-run runner/judicial/certification as needed.
Snapshot verification also refreshes `run-state.json`; stale verification is
reflected as `currentState: stale`.

This is not a cryptographic supply-chain guarantee. It is stale certification
detection for ordinary run-package drift.
