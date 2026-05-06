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
