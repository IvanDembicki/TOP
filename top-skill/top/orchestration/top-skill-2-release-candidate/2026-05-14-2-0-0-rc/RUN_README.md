# Orchestration Run

workflowId: top-skill-2-release-candidate
runId: 2026-05-14-2-0-0-rc
mode: validation
profile: repair-artifact-dogfood
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
python -B scripts/update_orchestration_state.py --root top/orchestration/top-skill-2-release-candidate/2026-05-14-2-0-0-rc
```

Do not report this run as runner-enforced, hard-check-verified, or delivery
complete until the runner, judicial validation, hard checks, and delivery
certification artifacts provide that evidence.

Repair artifact dogfood profile:

```text
executive -> judicial-initial -> repair-1 -> judicial
```

The repair pass may write only `artifacts/repair-target.json`. Delivery complete
requires the repaired artifact hard check and final post-repair judicial pass.
