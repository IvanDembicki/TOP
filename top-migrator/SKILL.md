---
name: top-migrator
description: Migrate existing non-TOP projects into Tree-Oriented Programming using descending recursive semantic analysis, child-agent delegation, checkpoints, logs, readiness aggregation, behavior tests vs TOP validation separation, repair/rollback loops, component retention policy, and final migration reporting. Use when planning, executing, auditing, or troubleshooting legacy-to-TOP migrations.
---

# TOP Migrator

**Version:** 0.1.0
**Last updated:** 2026-05-25 21:31 -07:00
**Status:** draft
**Depends on:** `top-skill` 2.0.7 or compatible

> When modifying `top-migrator`, update the version or last-updated field when the change is user-visible.

Use this skill to migrate an existing non-TOP project into Tree-Oriented Programming (TOP) without mixing migration orchestration with TOP canon.

`top-migrator` owns the migration process. It does not define TOP. TOP architecture, node semantics, validation rules, controller/content law, agent power separation, and rejection rules must come from the installed `top-skill`.

## Required Dependency

Before making TOP architectural claims, locate and hydrate `top-skill`.

Preferred sibling layout:

```text
../top-skill/
```

If `top-skill` is not found next to this skill, search the active skills list or known skill roots. Read `top-skill/SKILL.md`, then follow its hydration instructions. For migration work, load the `migration` task tier when needed.

If `top-skill` cannot be hydrated, continue only as a process draft and do not claim `top_valid`, `TOP-clean`, `canon compliant`, or delivery complete.

## Operating Boundary

Do:

- run legacy-to-TOP migration planning and orchestration;
- apply the Method of Descending Recursive Semantic Analysis;
- manage child-agent task boundaries, logs, checkpoints, readiness aggregation, repair loops, rollback decisions, component inventories, and final reports;
- call into `top-skill` for TOP canon, validation rules, node classification, and architecture verdicts.

Do not:

- redefine TOP canon;
- copy TOP validation rules into this skill as a fork;
- let a migration/generation/repair agent validate its own TOP correctness;
- treat passing tests as TOP validation;
- treat TOP validation as behavior preservation;
- hide unresolved legacy residuals behind successful wording.

## Mode Selection

Choose one mode per request unless the user explicitly asks for a full run.

`PlanMigration`
: Build migration scope, profile, gates, artifacts, agent roles, and risk map.

`RunSemanticAnalysis`
: Decompose one scope or node using descending recursive semantic analysis.

`CheckpointReview`
: Review one migration checkpoint, including logs, tests, TOP validation state, and rollback safety.

`RepairOrRollback`
: Classify a failed checkpoint and route to behavior repair, TOP repair, contract repair, or rollback.

`FinalMigrationReport`
: Produce the final migration report, including completed tree status, unresolved residuals, preserved components, TOP candidates, tests, validation, and developer decisions.

## Core Workflow

1. Establish scope and profile.
   Define root scope, migration profile, required behavior evidence, required TOP validation gates, allowed residual policy, rollback strategy, and developer escalation thresholds.

2. Create the temporary root node.
   Treat the whole target scope as a temporary root legacy container. This is an analysis root, not proof that the final result is one node.

3. Apply descending recursive semantic analysis.
   For the current node, identify one semantically independent child candidate at a time. Extract the candidate, define responsibility and parent contract, log the decision, and immediately delegate the child node to a separate agent/task when possible.

4. Continue parent analysis.
   The parent agent keeps analyzing the remaining code. The last residual fragment must become a meaningful child node, a black-box boundary, a connector, a local implementation detail, or an explicitly temporary residual. Do not create meaningless "remaining" nodes.

5. Validate checkpoints according to profile.
   Each completed extraction creates a checkpoint. Depending on profile, run behavior tests, TOP validation, structural checks, or defer them with explicit `not_verified` status.

6. Aggregate readiness bottom-up.
   Leaves report whether they are irreducible and why. Parents become ready only when all child statuses and local integration requirements satisfy the active migration profile.

7. Route failures.
   Use separate repair paths for behavior failures, TOP validation failures, contract conflicts, stale child work, ambiguous ownership, repeated repair failure, and human decision requirements.

8. Produce the final report.
   Do not claim complete migration unless structural readiness, behavior evidence, TOP validation evidence, component inventory, residual policy, and unresolved decision logs support that claim.

## Status Model

Track these statuses independently for every node or checkpoint:

```text
decompositionStatus: pending | decomposing | leaf_irreducible | children_ready | blocked
behaviorStatus: not_required | not_tested | tests_passed | tests_failed | behavior_not_verified
topValidationStatus: not_required | not_verified | top_valid | top_invalid | contaminated
integrationStatus: not_started | pending | integrated | integration_failed | stale_contract
readinessStatus: draft | partial | blocked | ready_structural | ready_verified
```

Never collapse these into one vague `done` state.

## Independence Rules

Behavior tests and TOP validation are independent checks.

- Passing tests means expected behavior appears preserved.
- Passing TOP validation means architecture satisfies TOP rules.
- One can pass while the other fails.

Route repairs accordingly:

- behavior failure -> behavior repair agent;
- TOP validation failure -> TOP repair agent and independent validator;
- contract/version conflict -> parent/orchestrator contract decision;
- repeated failure -> circuit breaker and developer escalation.

TOP validation should be performed by an independent external validator whenever possible. If an external validator is not available, mark `topValidationStatus: not_verified` or `contaminated`; do not upgrade it to `top_valid`.

## Resource Map

Read only the reference files needed for the current task:

- `references/descending-recursive-semantic-analysis.md` for the core method.
- `references/migration-profiles-and-checkpoints.md` for strict, draft, and hybrid profiles.
- `references/failure-escalation.md` for hard "what if" scenarios and escalation packets.
- `references/component-retention-policy.md` for deciding whether legacy/framework components stay as components or become TOP candidates.
- `references/final-report-contract.md` for required final report sections.

Optional structural artifacts:

- `release-metadata.json`
- `schemas/migration-log.schema.json`
- `schemas/node-readiness.schema.json`
- `schemas/component-inventory.schema.json`
- `scripts/validate_migration_artifacts.py`

## Output Discipline

For every migration decision, preserve:

- node path;
- source artifact(s);
- extracted responsibility;
- parent contract version;
- child agent/task id when delegated;
- behavior evidence status;
- TOP validation status;
- unresolved assumptions;
- rollback anchor or checkpoint id.

When blocked, provide a developer escalation packet:

```text
Problem:
Affected node:
Evidence from code:
What cannot be proven:
Options:
Risk per option:
Migrator recommendation:
Developer decision needed:
```
