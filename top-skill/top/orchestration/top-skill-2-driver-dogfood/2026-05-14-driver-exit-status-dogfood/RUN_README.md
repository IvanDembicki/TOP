# Orchestration Run

workflowId: top-skill-2-driver-dogfood
runId: 2026-05-14-driver-exit-status-dogfood
mode: maintenance
profile: scaffold
adapterKind: process

This package was scaffolded by `scripts/create_orchestration_run.py`.

Initial status:

- currentState: scaffolded
- executionIsolationLevel: protocol-defined
- verificationEvidenceLevel: none
- deliveryStatus: not-certified

Refresh `run-state.json` after runner, judicial, certification, or snapshot
changes:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/top-skill-2-driver-dogfood/2026-05-14-driver-exit-status-dogfood
```

Do not report this run as runner-enforced, hard-check-verified, or delivery
complete until the runner, judicial validation, hard checks, and delivery
certification artifacts provide that evidence.
