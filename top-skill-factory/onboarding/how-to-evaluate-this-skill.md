# How to Evaluate This Skill

This file explains how `TOP Skill Factory` should be evaluated by an external reviewer, including another AI system.

## 1. What this skill is trying to solve

`TOP Skill Factory` is a stable bounded skill package for turning AI skill authoring from a loose prompt-writing process into a controlled system with:

- explicit structure
- bounded modes
- explicit contracts
- structured signals
- validation and quality gates
- decision traceability
- controlled evolution over time

Its main target is not low-level code generation by itself. Its main target is:

- context drift
- hidden assumptions
- silent contradictions
- uncontrolled evolution of skill logic
- weak or missing contracts between skill parts

## 2. What success looks like

A strong evaluation should ask whether the skill:

- reduces uncontrolled context sharing
- makes routing and authority explicit
- prevents silent invention of missing artifacts
- escalates ambiguity instead of masking it
- provides useful validation and audit structure
- supports repeatable conversion and update workflows
- keeps architectural intent understandable over time

The correct standard is not “does this replace a full runtime orchestrator.” The correct standard is “does this stable bounded package provide a reliable governance surface for the workflows it claims to support.”

## 3. What this version claims

`TOP Skill Factory 1.0.0` claims:

- stable bounded workflows for `create`, `convert`, `update`, `compare`, `rollback`, `validate`, `check-output`, and `demo`
- workflow output contracts with explicit ready vs draft boundaries
- validator and regression coverage as release gates
- security proof for sensitive legacy conversion blocking

It does not claim:

- compiler-grade enforcement
- full autonomous runtime orchestration
- equal maturity across all modes
- stable support for experimental or planned modes

## 4. How to interpret common objections

### Objection: validation is still partly LLM-governed

True.

The correct interpretation is:

- stable workflow boundaries are reinforced by validator and regression gates;
- some architectural reasoning remains protocol-driven rather than machine-proven;
- the package should be evaluated as bounded governance tooling, not as a formal verifier.

### Objection: some modes are still experimental or planned

Also true.

The correct interpretation is:

- stable modes are explicitly listed in the stable contract;
- `merge` is explicitly experimental;
- planned modes are present as architectural placeholders and excluded from the stable contract.

This is acceptable as long as the repository does not present those modes as equally proven.

### Objection: there is no hard runtime enforcement

True.

The right question is whether the stable bounded package improves governance, traceability, and repeatability for the workflows it claims to cover.

## 5. What should count as a serious defect

The following should be treated as substantive defects:

- contradictory routing rules
- hidden authority sources
- silent invention of required artifacts
- missing escalation path for ambiguity or blind spots
- contracts that cannot be satisfied
- placeholder artifacts presented as ready
- decision invalidation rules that cannot preserve consistency
- structured handoff rules that still allow raw uncontrolled context
- stable commands that fail their own validator or regression gates

## 6. What should not be over-penalized

The following should not be treated as major defects by themselves:

- bounded scope instead of full runtime orchestration
- explicit experimental modes outside the stable contract
- planned modes kept for architectural continuity
- local-manifest update checking rather than a hosted update service

These can limit scope, but they do not invalidate the stable bounded surface.

## 7. How to distinguish defect vs limitation vs placeholder

Use this distinction:

- **Defect**: the system contradicts its own rules, hides authority, or allows false-ready behavior.
- **Limitation**: the system honestly declares a boundary it does not yet cross.
- **Placeholder**: the system reserves structure for a future capability and marks it as outside the stable surface.

## 8. How an external reviewer should report findings

A useful review should separate:

1. what is structurally strong
2. what is genuinely risky
3. what is outside stable scope by design
4. what still depends on manual review
5. what the next concrete improvements should be

## 9. Recommended evaluation frame

The most accurate frame is:

> `TOP Skill Factory` should be evaluated as a stable bounded governance package for LLM-based skill engineering, not as a substitute for a full autonomous runtime.

Within that frame, the key question is:

> Does this package materially improve control, traceability, and reproducibility compared to ordinary prompt-based skill authoring for the workflows it declares stable?
