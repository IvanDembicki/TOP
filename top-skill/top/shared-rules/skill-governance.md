# Skill Governance Rules

These rules adapt TOP Skill Factory governance to `top-skill` itself.

## Core rules

1. A skill is a controlled TOP tree, not a free-form prompt.
2. Context is controlled input for a mode or agent, not a global text stream.
3. Mode routing is explicit and must match the active task.
4. Output shape is defined by contracts.
5. Required artifacts cannot be empty placeholders in a ready result.
6. If validation fails, the skill or generated artifact is not ready.
7. Core TOP invariants cannot be disabled by user override.
8. New requirements must invalidate conflicting old decisions.
9. Every important decision must be traceable to input, rule, artifact, or
   validation evidence.
10. A valid rule must have a known verification method.
11. Delivery honesty is governed by `workflow/enforcement-evidence-model.md`.
12. Orchestration activation and the operating loop are governed by
    `workflow/activation-and-operating-procedure.md`.
13. Protocol-only execution must not be reported as runner-enforced execution.
14. A result cannot be called delivery complete unless the execution evidence
    and verification evidence gates both satisfy the delivery law.
15. Runner evidence must be produced by `workflow/runner-contract.md` artifacts
    and executable runner checks, not by prose claims.
16. Runner-enforced isolation additionally requires context packages and pass
    invocation evidence governed by `workflow/pass-invocation-contract.md`.
17. LLM API pass execution is governed by
    `workflow/llm-api-adapter-contract.md`.
18. Repair pass authority and post-repair validation are governed by
    `workflow/repair-pass-contract.md`; repair is not a verdict and cannot
    certify delivery.
19. Repair artifact writes must be bounded by task-capsule
    `artifactWriteRequests`, materialized only to exact listed refs, and
    recorded as invocation-evidence `artifactWrites`.
20. New orchestration runs must use `workflow/run-package-layout.md` so context,
    handoffs, runner evidence, validation, certification, and logs are stored
    in predictable locations.
21. Run package process state is governed by
    `workflow/run-state-machine.md` and `scripts/update_orchestration_state.py`;
    it must not be used as a replacement for delivery certification.
22. Runner and certification scripts must refresh `run-state.json`
    automatically after evidence-changing operations unless explicitly skipped
    for diagnostics.
23. Run package validity claims must be checked by
    `scripts/validate_orchestration_run.py`, which reports valid, stale, or
    invalid state without changing run artifacts.
24. Orchestration false-complete protection is governed by
    `scripts/validate_orchestration_regressions.py`; these fixtures must keep
    known invalid delivery paths invalid.
25. Ordered orchestration workflow claims may use
    `scripts/run_orchestration_workflow.py`, but the driver must use the final
    read-only verifier result as the workflow readiness status.

## Update rule

When updating `top-skill`, preserve unaffected valid artifacts, invalidate only
conflicting decisions, update affected contracts and hydration references, then
run package validation.

Do not hide behavior-changing updates as minor wording changes.

## Structured artifact rule

When a workflow artifact controls routing, gates, or handoff, prefer JSON with a
schema over prose-only state. Prose may explain; JSON controls.

For migration projects, the structured process artifact is:

```text
top/migration/<branch-id>/MIGRATION_WORKFLOW.json
```

## Readiness rule

A result is not ready while required artifacts are missing, stale, empty,
contradictory, or unvalidated.

A result is not delivery complete while it lacks runner-enforced execution
isolation, hard-check-verified validation evidence, a valid independent judicial
handoff artifact, or a required gate remains `fail` or `not_verified`.

A result is not delivery complete after repair unless a later independent
judicial pass validates the post-repair artifacts.

A result is not delivery complete after repair artifact writes unless the final
judicial pass read the repaired refs named by the repair handoff or invocation
evidence.

Runner reports are evidence, not judicial verdicts. Final delivery still
requires judicial validation and delivery certification.
