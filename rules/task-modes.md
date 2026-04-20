# Task Modes

This file defines the official operating modes of the skill.

## Core rule

The skill does not use a single universal pipeline for all tasks.

Four modes are officially supported:

1. analysis-only
2. modeling-refactor
3. generation-pipeline
4. spec-change

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

Repair Agent is used in a loop on failed validation. If repair changes synchronized artifacts, the loop must pass through Spec Sync Agent before Validation.

---

## 4. spec-change

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
- changes spec and requires code verification → spec-change

---

## Prohibition of false mandatory stages

Semantic interpretation, target adaptation, and generation are not required stages for analysis-only, modeling-refactor, and spec-change tasks unless the task explicitly enters materialization.

It is forbidden to consider an analysis-only task invalid simply because it did not reach the Generation Agent.

## Relationship between Mode and Tier

`Mode` and `Tier` are different classification axes.

- `Mode` defines the type of work:
  - `analysis-only`
  - `modeling-refactor`
  - `generation-pipeline`
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
- as an informational depth marker in `analysis-only`, if no generation occurs
- as an informational depth marker in initial `spec-change`; verification direction is controlled by the changed spec and `Spec Change Verification Agent`

If a conflict arises between `Mode` and `Tier`:
- `Mode` takes priority

This means:
- an `analysis-only` task does not become `generation-pipeline` just because a Tier is assigned to it
- `Tier` cannot on its own require `Semantic Interpreter Agent`, `Target Adaptation Agent`, or `Generation Agent` if the active mode does not require materialization
- `Tier` cannot on its own insert `Canon Precheck Agent` into initial `spec-change` or `analysis-only` routing
