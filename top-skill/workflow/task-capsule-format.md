# Task Capsule Format

## Purpose

A task capsule is the only input contract for one microprocess pass. It defines
one role, one task, the allowed context, and the required output contract.

## Task Capsule Contract

A capsule must identify:

- workflow id
- task id
- role
- objective
- allowed actions
- forbidden actions
- input references
- context slices
- output contract
- required checks, when applicable
- stop condition
- authority flags

## Allowed / Forbidden Actions

Allowed actions are role-specific. Forbidden actions must explicitly block role
expansion, including validation by an executive pass and repair by a judicial
pass.

## Context Minimization

The capsule must include only the context needed for the assigned role. It must
not include full-skill or full-project context when a smaller slice is enough.

## Stop Condition

After producing the required handoff artifact, the pass must stop. It must not
select the next task, self-validate, repair, report final status, or certify
delivery unless its capsule explicitly authorizes that role.

## Relation to Enforcement Evidence Model

Capsules participate in the enforcement evidence model defined in
`workflow/enforcement-evidence-model.md`. In protocol-only mode, a capsule can
document intended isolation, but it cannot prove runner-enforced isolation.
