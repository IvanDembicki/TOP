# Orchestration Run

workflowId: top-skill-2-repair-loop-dogfood
runId: 2026-05-14-repair-loop-dogfood-2
mode: validation
profile: repair-loop
adapterKind: llm-api

This package was scaffolded by `scripts/create_orchestration_run.py`.

Initial status:

- currentState: scaffolded
- executionIsolationLevel: protocol-defined
- verificationEvidenceLevel: none
- deliveryStatus: not-certified

Refresh `run-state.json` after runner, judicial, certification, or snapshot
changes:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/top-skill-2-repair-loop-dogfood/2026-05-14-repair-loop-dogfood-2
```

Do not report this run as runner-enforced, hard-check-verified, or delivery
complete until the runner, judicial validation, hard checks, and delivery
certification artifacts provide that evidence.

Repair loop profile:

```text
executive -> judicial-initial -> repair-1 -> judicial
```

Delivery complete is forbidden unless the final `judicial` pass validates
post-repair artifacts after `repair-1`.
