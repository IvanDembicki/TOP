# Task Modes

This file defines the official operating modes of the skill.

## Core rule

The skill does not use a single universal pipeline for all tasks.

Five modes are officially supported:

1. analysis-only
2. modeling-refactor
3. generation-pipeline
4. migration
5. spec-change

---

## 1. analysis-only

Used for:
- architectural audit
- architecture explanation
- review
- finding contradictions
- analyzing an existing artifact without materialization

Required stages:
- Intake Agent
- Ambiguity Resolver Agent (if needed)
- Domain Structuring Agent (if needed)
- Validation Agent
- Final Audit Agent

Semantic Interpreter Agent, Target Adaptation Agent, and Generation Agent are not required.
Repair Agent is not required.
Canon Precheck Agent is required only if analysis transitions into an architectural proposal.

---

## 2. modeling-refactor

Used for:
- building a TOP model
- refactor-to-top
- changing the tree
- reworking ownership / boundaries / lifecycle

Required stages:
- Intake Agent
- Ambiguity Resolver Agent (if needed)
- Domain Structuring Agent
- TOP Modeling Agent
- Canon Precheck Agent
- Validation Agent
- Final Audit Agent

Semantic Interpreter Agent, Target Adaptation Agent, and Generation Agent are required only if a materialized implementation is needed.

Execution steps:
1. Determine representation level, content type, statefulness, and materialization mode.
2. Restore or design the tree model.
3. Determine the controller/content split for nodes with content.
4. Record `props.contentType` if the content type must be explicitly defined.
5. Determine the canonical TOP artifact layout: JSON specs under `top/specs/`,
   prompts under `top/prompts/`, migration/status artifacts under
   `top/migration/`, and the implementation source root (`top_src/` by default)
   if materialization is planned.
6. Identify nodes, branches, states, and module boundaries.
7. Perform composite decomposition.
8. Determine the owner state.
9. Determine logical ownership, render attachment rules, and source of truth.
10. Form node specs and the spec tree.
11. If implementation prompts or Expected Materialization are produced, create
    or update the declared source root directory before handoff.
12. Prepare refactoring recommendations if needed.

---

## 3. generation-pipeline

Used for:
- generating a new artifact
- materializing an approved TOP model
- code generation

Required stages:
- Intake Agent
- Ambiguity Resolver Agent (if needed)
- Domain Structuring Agent
- TOP Modeling Agent
- Canon Precheck Agent
- Semantic Interpreter Agent
- Target Adaptation Agent
- Generation Agent
- Spec Sync Agent
- Validation Agent
- Final Audit Agent

Execution steps:
1. Confirm that the tree model is already defined.
2. Verify that nodes have defined: `type`, `doc`, `props.contentType` (if content exists), `prompt`, `props`, `children`.
3. Verify that new JSON branch specs are stored under `top/specs/` unless an
   established project TOP index declares another convention.
4. Verify that node prompt files will be stored inside `top/` in project-local `prompts/` folders alongside the corresponding tree or branch description.
5. Verify that the implementation source root is declared and exists (`top_src/`
   by default, branch root `top_src/<branch-id>/` for new migration branches).
6. Prepare a separate implementation prompt for each code-generated node.
7. Specify `props.sourceRoot` and `props.dir` for generated implementation
   artifacts as needed.
8. Perform code generation.
9. Run node validation rules without fail: detect violations, classify them, choose the canonical correction direction, and perform re-validation after each fix.
10. Run the mandatory drift check: compare JSON topology, prompt behavior/materialization rules, project-local `top/` artifacts, and generated/materialized implementation artifacts.
11. Run the verification loop.
12. On mismatch — fix the prompt/spec and protocol artifacts first, not just the code.
13. After reaching the attempt limit — perform escalation.

Repair Agent is used in a loop on failed validation. If repair changes synchronized artifacts, the loop must pass through Spec Sync Agent before Validation.

---

## 4. migration

Used for:
- moving existing non-TOP code into TOP structure;
- wrapping or replacing legacy branches incrementally;
- preserving behavior while extracting TOP nodes, prompts, and tests.

Required stages:
- Migration Infrastructure Agent
- Migration Planning Agent
- Migration Agent
- Behavior Preservation Agent if the scope has legacy tests or executable behavior evidence
- TOP Modeling Agent
- Canon Precheck Agent
- Validation Agent
- Final Audit Agent

Generation Agent, Semantic Interpreter Agent, Target Adaptation Agent, and Spec Sync Agent are required only if the migration task materializes implementation artifacts.

Execution steps:
1. Confirm a recoverable version-control baseline.
2. Prepare migration infrastructure: `top/specs/`, `top/prompts/`,
   `top/migration/`, `MIGRATION_WORKFLOW.json`, `MIGRATION_PLAN.md`,
   `MIGRATION_STATUS.md`, `MIGRATION_LOG.md`, and planned
   `top_src/<branch-id>/` roots.
3. Create or update the explicit migration plan. If the user named a starting
   scope, use it. If not, choose the starting scope by isolation, risk,
   dependency visibility, and behavior evidence.
4. Create or update the machine-readable migration workflow tree so phases,
   gates, handoffs, responsible agents, and current phase are explicit JSON.
5. Append a migration log entry for every migration-mode stage handoff and every
   persistent artifact change.
6. Define the migration scope and dependency boundary. The user-named scope is
   the analysis root, not proof of one TOP node.
7. Discover legacy tests and executable behavior evidence covering the scope.
8. Produce a Behavior Preservation Plan when test evidence exists.
9. Extract a TOP model that preserves normalized behavior requirements by
   recursively discovering hidden objects, state holders, state alternatives,
   data owners, async workflows, forms, modals, lists/list items, bridge
   boundaries, black boxes, and reusable structures.
10. Persist migration specs under `top/specs/`, prompts under `top/prompts/`,
   and migration status under `top/migration/`.
11. If the migration task creates implementation prompts or materialization
   expectations, declare and prepare the implementation source root before
   generation (`top_src/<branch-id>/` by default, with `.gitkeep` if empty).
12. Update specs, prompts, contracts, and tests together.
13. Validate TOP canon, migration workflow/plan/log integrity, and behavior preservation
    before final audit.

Skipping Behavior Preservation Agent for a tested migration scope is `WF-010`.
Losing, weakening, or failing to represent test-covered behavior is `CORE-028`.
Creating migration specs/prompts outside the canonical layout is a convention
violation. Omitting the materialization source root for a migration that declares
future implementation artifacts is `WF-013`.
Missing `MIGRATION_PLAN.md` is `WF-014`. Missing or stale `MIGRATION_LOG.md` is
`WF-015`. Missing or stale `MIGRATION_WORKFLOW.json` is `WF-016`.
Missing recursive decomposition or giant-node review is `WF-017`.
Undisciplined accepted deviations are `WF-018`. Writes outside the active
migration workspace without explicit adapter/integration allowance are `WF-019`.

---

## 5. spec-change

Used for:
- manual changes to JSON spec without prior code generation;
- any case where the spec has been changed and it is necessary to verify that the code conforms to it.

Required stages:
- Intake Agent
- Spec Change Verification (per protocol `references/spec-change-verification.md`)
- Validation Agent (if there were code changes)
- Final Audit Agent

Semantic Interpreter Agent, Target Adaptation Agent, and Generation Agent are not required.
Spec Sync Agent is not used for the initial spec-change direction. If a later repair changes synchronized artifacts, the repair routing rule still applies and may require Spec Sync Agent before Validation.

Changing spec without completing verification is considered incomplete.

---

## Mode selection

- Intake Agent proposes `task_mode`
- Mode selection must be explicitly recorded
- Incorrect mode selection is considered a workflow violation

If the task:
- only analyzes → analysis-only
- changes the model or structure → modeling-refactor
- creates an implementation artifact → generation-pipeline
- migrates existing non-TOP code → migration
- changes spec and requires code verification → spec-change

---

## Prohibition of false mandatory stages

Semantic interpretation, target adaptation, and generation are not required stages for analysis-only, modeling-refactor, migration, and spec-change tasks unless the task explicitly enters materialization.

It is forbidden to consider an analysis-only task invalid simply because it did not reach the Generation Agent.

## Relationship between Mode and Tier

`Mode` and `Tier` are different classification axes.

- `Mode` defines the type of work:
  - `analysis-only`
  - `modeling-refactor`
  - `generation-pipeline`
  - `migration`
  - `spec-change`

- `Tier` defines the scope of architectural change:
  - Tier 1
  - Tier 2
  - Tier 3

## Priority rule

When forming the pipeline:
- `Mode` determines the required stages
- `Tier` determines the depth of checks and routing within the corresponding mode

## Tier application constraint

`Tier` does not define the pipeline on its own.

`Tier` applies:
- mandatorily within `generation-pipeline`
- optionally within `modeling-refactor`, if the task genuinely changes architectural scope
- optionally within `migration`, after the migration scope and behavior evidence are known
- as an informational depth marker in `analysis-only`, if no generation occurs
- as an informational depth marker in initial `spec-change`; verification direction is controlled by the changed spec and `Spec Change Verification Agent`

If a conflict arises between `Mode` and `Tier`:
- `Mode` takes priority

This means:
- an `analysis-only` task does not become `generation-pipeline` just because a Tier is assigned to it
- `Tier` cannot on its own require `Semantic Interpreter Agent`, `Target Adaptation Agent`, or `Generation Agent` if the active mode does not require materialization
- `Tier` cannot on its own insert `Canon Precheck Agent` into initial `spec-change` or `analysis-only` routing
