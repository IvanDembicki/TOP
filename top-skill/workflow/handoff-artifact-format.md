# Handoff Artifact Format

## Purpose

A handoff artifact is the required output of one pass. It records what the pass
did, what evidence it produced, and what powers it did not exercise.

## Handoff Artifact Contract

A handoff must identify:

- workflow id
- pass id
- task id
- role
- agent name
- task capsule reference
- input references
- output references
- files read
- files changed
- commands run
- status
- execution evidence
- limitations
- handoff target

## Pass Authority Flags

Each handoff must state whether the pass was allowed to edit files, validate,
repair, report, or certify delivery. Executive handoffs must not claim
validation authority or delivery certification authority.

## Required executionEvidence

Any handoff that can affect delivery must include `executionEvidence` as defined
in `workflow/enforcement-evidence-model.md`.

## What This Pass Did Not Do

The handoff must explicitly list powers not exercised by the pass. For example,
an executive pass must state that it did not independently validate its work and
did not declare delivery complete.

## Invalid Handoff Conditions

A handoff is invalid when it combines incompatible powers, omits execution
evidence, claims runner enforcement without runner evidence, or declares
delivery completion outside the delivery certification gate.
