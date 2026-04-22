# Agents Index

This file defines the TOP agent pipeline and relationships between agents.

## Pipeline

1. Intake Agent
2. Ambiguity Resolver Agent
3. Domain Structuring Agent
4. TOP Modeling Agent
5. Canon Precheck Agent
6. Semantic Interpreter Agent
7. Target Adaptation Agent
8. Generation Agent
9. Spec Sync Agent
10. Validation Agent
11. Repair Agent (loop if needed)
12. Final Audit Agent

Spec Change Verification Agent — mandatory first step in `spec-change` mode after Intake. See `agents/spec-change-verification-agent.md` and protocol in `references/spec-change-verification.md`.

Orchestrator Agent controls transitions between all stages.

Spec Audit Agent — standalone, launched on demand outside the main pipeline.

Learning Agent — standalone onboarding entrypoint, not part of the pipeline. See `onboarding/top-learning-agent.md`.

Migration Agent — standalone entry point for incremental migration of existing non-TOP projects. See `agents/migration-agent.md`.

## Flow rules

- No stage required by the active task mode may be skipped.
- Stages outside the active mode's required pipeline are not mandatory.
- Canon Precheck is mandatory before semantic interpretation and Generation.
- Semantic Interpreter Agent is mandatory before Target Adaptation Agent in generation-pipeline mode.
- Target Adaptation Agent is mandatory before Generation Agent in generation-pipeline mode.
- Spec Sync is mandatory after Generation in generation-pipeline mode.
- Validation is mandatory after Spec Sync.
- Repair loops back through Spec Sync Agent when it changes synchronized artifacts; otherwise it may return directly to Validation until pass.
- Final Audit is only allowed after successful Validation.

## Transition map

- Intake → Ambiguity Resolver / Domain Structuring
- Ambiguity Resolver → Domain Structuring / stop
- Domain Structuring → TOP Modeling
- TOP Modeling → Canon Precheck
- Canon Precheck → Semantic Interpreter / Repair / Ambiguity Resolver
- Semantic Interpreter → Target Adaptation / Ambiguity Resolver / Repair
- Target Adaptation → Generation / Semantic Interpreter / Ambiguity Resolver
- Generation → Spec Sync
- Spec Sync → Validation
- Validation → Final Audit / Repair
- Repair → Semantic Interpreter / Target Adaptation / Spec Sync / Validation / Canon Precheck
- Final Audit → Delivery


## Repair routing rule

After Repair Agent completes, the orchestrator must inspect the repair output.
If the repair changed semantic inputs or Layer B (`top/semantic/`), the next stage is `Semantic Interpreter Agent` before Target Adaptation, Generation, or Validation. If the repair changed only Layer C (`top/adaptations/<target>/`), the next stage is `Target Adaptation Agent` for the affected target. If the repair changed generated/materialized synchronized artifacts (`src/`, generated/materialized artifacts, JSON specs, implementation prompts, `top/assets/`, or `top/presentation/`), the next stage is `Spec Sync Agent` before `Validation Agent`.
Direct `Repair Agent -> Validation Agent` is permitted only when the repair changed no synchronized artifact or only changed analysis/metadata outside the TOP artifact chain.
If the repair changes the model before generation, return to `Canon Precheck Agent` instead.
## Mode-specific transition maps

### analysis-only

- Intake → Ambiguity Resolver (if needed) / Domain Structuring (if needed) / Validation
- Ambiguity Resolver → Domain Structuring / Validation / stop
- Domain Structuring → Validation
- Validation → Final Audit / stop (validation failure in analysis-only does not route to Repair; findings are reported and the pipeline stops)
- Canon Precheck → Validation / Ambiguity Resolver (only if analysis transitions into an architectural proposal)
- Final Audit → Delivery

Semantic Interpreter Agent, Target Adaptation Agent, Generation Agent, Spec Sync Agent — not part of the pipeline.
Repair Agent — not part of the pipeline; validation findings are reported as output, not corrected.
Canon Precheck Agent — not part of the standard pipeline; used only if analysis transitions into an architectural proposal.

---

### modeling-refactor

- Intake → Ambiguity Resolver (if needed) / Domain Structuring
- Ambiguity Resolver → Domain Structuring / stop
- Domain Structuring → TOP Modeling
- TOP Modeling → Canon Precheck
- Canon Precheck → Validation / Repair / Ambiguity Resolver
- Validation → Final Audit / Repair
- Repair → Spec Sync (if synchronized artifacts changed) / TOP Modeling / Canon Precheck
- Final Audit → Delivery

Semantic Interpreter Agent, Target Adaptation Agent, Generation Agent, Spec Sync Agent — not part of the pipeline unless materialization is required.

---

### generation-pipeline

- Intake → Ambiguity Resolver (if needed) / Domain Structuring
- Ambiguity Resolver → Domain Structuring / stop
- Domain Structuring → TOP Modeling
- TOP Modeling → Canon Precheck
- Canon Precheck → Semantic Interpreter / Repair / Ambiguity Resolver
- Semantic Interpreter → Target Adaptation / Ambiguity Resolver / Repair
- Target Adaptation → Generation / Semantic Interpreter / Ambiguity Resolver
- Generation → Spec Sync
- Spec Sync → Validation
- Validation → Final Audit / Repair
- Repair → Semantic Interpreter / Target Adaptation / Spec Sync / Validation / Canon Precheck
- Final Audit → Delivery

---

### spec-change

- Intake → Spec Change Verification Agent
- Spec Change Verification Agent: pass, no code changes → Final Audit
- Spec Change Verification Agent: pass, code changed → Validation
- Spec Change Verification Agent: fail → Repair / revert spec / Ambiguity Resolver
- Validation → Final Audit / Repair
- Repair → Spec Sync / Validation
- Final Audit → Delivery

Generation Agent, Canon Precheck Agent, TOP Modeling Agent — not part of the initial spec-change pipeline.
Spec Sync Agent is not used for the initial spec-change direction, but the repair routing rule still applies if a later repair changes synchronized artifacts.

Agent: `agents/spec-change-verification-agent.md`
Protocol: `references/spec-change-verification.md`.

---

## Global constraints

- Canon overrides all agents.
- Validation rules are mandatory at all stages.
- Contracts must be followed by each agent.
- No agent may expand its role beyond definition.

## Invalidation rule

Result is invalid unless:
- all required stages completed
- all validation checks passed
- no canonical violations remain

## Resume protocol

When the pipeline stops, the following must be recorded:
- at which stage the stop occurred
- the reason for the stop
- which input data or decisions are missing
- which agent must continue work after the stop condition is resolved

Resume rules:
- Resume is only allowed after the stop reason has been explicitly resolved
- Resume starts from the stage at which the stop occurred, not from an arbitrary point
- Resume authorization is only permitted through:
  - explicit user confirmation
  - the result of `Ambiguity Resolver Agent`
  - the result of a required repair / re-modeling stage

If the stop condition has not been explicitly resolved:
- the pipeline cannot be resumed
- the result remains invalid

See `references/human-confirmation-protocol.md` for interaction options with the human during a stop.

## Tier verification

Tier cannot be accepted solely on the self-report of `Intake Agent`.

Before continuing the pipeline, it is necessary to verify whether the declared Tier matches the actual scope of the task.

### Mandatory Tier verification rules

If the task involves at least one of the following aspects:

- ownership
- protocol boundaries
- lifecycle definition
- controller/content split
- tree structure

then the task cannot be Tier 1.

### Mismatch consequences

If the declared Tier does not match the task scope:
- the pipeline must be stopped
- the current Tier is considered invalid
- the task must be reclassified to a higher Tier
- the next permitted step is determined after reclassification

## Transition map (Tier-aware extension)

Tier-aware routing is subordinate to the active `task_mode`.

- `generation-pipeline` + Tier 1 → `Canon Precheck Agent` (lightweight)
- `analysis-only` + Tier 1 → `Validation Agent` unless analysis transitions into an architectural proposal
- `modeling-refactor` + Tier 1 → follow the modeling-refactor transition map; use lightweight Canon Precheck only when a model/precheck step is actually reached
- `spec-change` + Tier 1 → `Spec Change Verification Agent` after Intake; Tier does not insert Canon Precheck into the initial spec-change pipeline

## Task modes

The pipeline must be selected not only by Tier but also by `task_mode`.

Official modes:

- `analysis-only`
- `modeling-refactor`
- `generation-pipeline`
- `spec-change`

### Mode routing

- `analysis-only` does not require `Generation Agent` if the task does not materialize an implementation
- `modeling-refactor` does not require `Generation Agent` if only an approved model / refactor decision is required
- `generation-pipeline` requires `Semantic Interpreter Agent`, `Target Adaptation Agent`, and `Generation Agent`

An analysis-only task must not be declared invalid solely due to the absence of a generation stage.

## Tier decision ownership

Tier decision is not a single-owner decision of Intake Agent.

Rule:
- `Intake Agent` produces `proposed_tier`
- `Canon Precheck Agent` confirms `effective_tier`

If the task mode does not require Canon Precheck, proposed_tier remains the operational tier only for lightweight routing, but cannot override architectural scope.

## Schema-first output rule

All handoff results must be interpreted according to the schema-first rule:

- output shape is defined by the contract file
- agent file does not duplicate required output fields
- orchestrator and downstream agents must read output through the contract schema, not through prose description

## Mode-aware flow rule

Skipping a stage is only forbidden within the active `task_mode`.

This means:
- stages required by the active mode are mandatory
- stages not part of the active mode's pipeline are not considered skipped
- `analysis-only` does not require `Generation Agent`
- `modeling-refactor` does not require `Generation Agent` if no materialization occurs
