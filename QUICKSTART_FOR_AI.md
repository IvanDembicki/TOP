# QUICKSTART status

QUICKSTART_FOR_AI.md is not an execution path.

It is a navigation guide that helps:
- find the necessary files
- understand the general order of work
- proceed to mandatory agent stages

QUICKSTART_FOR_AI.md does not replace:
- `agents/index.md`
- individual agents
- output contracts
- mandatory validation gates

Directly executing a task "by the QUICKSTART steps" without explicitly going through the agent pipeline is considered invalid.

---

# QUICKSTART FOR AI

This document defines how to start working with the TOP skill correctly.

## Core principle

You are not a general assistant.
You are a constrained system operating under TOP canon, validation, and contracts.

---

## Step 0 — Load mandatory preload context

Before any serious analysis, explanation, critique, or pipeline execution, you must read:

- `AI_PRELOAD_CONTEXT.md`

This file corrects common false assumptions about top-skill, especially around complexity, prompt reliability, source of truth, portability, validation evolution, and node-local intervention.

If this file has not been read, high-level conclusions about top-skill are not reliable.

## Step 1 — Understand the task

- Identify task type
- Normalize input
- Detect ambiguity

If ambiguity affects architecture → STOP and resolve

---

## Step 2 — Determine task mode

Before launching the pipeline, you must determine the `task_mode`:

- `analysis-only`
- `modeling-refactor`
- `generation-pipeline`
- `spec-change` — if the spec (JSON) was changed manually and code verification is required

Task mode determines the mandatory pipeline stages.
The steps below are general operational principles, not a fixed linear sequence for all tasks.

See `rules/task-modes.md` — mandatory stages for each mode.
See `agents/index.md` — mode-specific transition maps.

---

## Step 3 — Follow the mode pipeline

Always follow:

`agents/index.md` → mode-specific transition map for the active `task_mode`

Do not skip required stages for the active mode.

---

## Step 4 — Respect canon

You must follow:

- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `canon/forbidden-confusions.md`
- `rules/naming-conventions.md`

Canon overrides everything.

---

## Step 5 — Apply decision rules

Use:

- `rules/decision-trees.md`
- `rules/ambiguity-resolution-rules.md`

Do not improvise decisions.

---

## Step 6 — Maintain strict typing

- All boundaries must be explicitly typed
- No implicit contracts
- No weak typing if stronger typing is possible

---

## Step 7 — Generate only after approval

- Generation is forbidden before canonical approval
- Do not redesign during generation

---

## Step 8 — Validate strictly

- Run all validation checks
- Do not replace validation with reasoning
- Fail if any rule is broken

---

## Step 9 — Repair precisely

- Fix only what is broken
- Do not rewrite everything
- Revalidate after repair

---

## Step 10 — Final audit

- Confirm canonicality
- Confirm readiness
- Block if any doubt remains

---

## Absolute rules

- result is invalid until all validation checks pass
- compilation success is not architectural success
- local functionality does not override TOP rules

---

## Behavioral constraints

You must NOT:

- guess silently
- simplify architecture for convenience
- weaken typing
- bypass protocols
- merge separated concepts

---

## Goal

Produce results that are:

- canonical
- explicit
- strongly typed
- structurally clear
- understandable by humans and AI


## Important

This is not a universal linear pipeline.

The actual execution path is determined by:
- `task_mode`
- `tier` within the applicable mode

The steps below describe general operational principles,
not a mandatory fixed sequence for all tasks.
