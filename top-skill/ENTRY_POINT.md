---
# TOP Skill — Entry Point
---

## Step 1 — One-time preload (required before first task)

Read `AI_PRELOAD_CONTEXT.md` before any analysis, critique, or pipeline execution.

If already read in this session — skip.

---

## Step 2 — What are you doing?

Choose one:

| I want to… | Task mode |
|---|---|
| Audit, review, or explain existing architecture | `analysis-only` |
| Build or refactor a TOP model, change tree structure | `modeling-refactor` |
| Generate code from an approved spec | `generation-pipeline` |
| I changed the JSON spec manually and need to verify code | `spec-change` |
| I don't know yet | Read `rules/task-modes.md` for detailed descriptions |

---

## Step 3 — Go to Intake Agent

File: `agents/intake-agent.md`

The Intake Agent classifies your task, confirms the task mode, and routes you to the correct pipeline.

Expected output: `contracts/agent-output-contracts/intake-output.md`

---

## Pipeline reference

Full mode-specific pipelines: `agents/index.md`

Canon rules: `canon/core-axioms.md`, `canon/validation-rules.md`
