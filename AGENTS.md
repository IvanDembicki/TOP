# AGENTS.md

## Purpose

This file is the entry point for AI agents that automatically read `AGENTS.md` at startup (Codex, Claude Code, and similar tools).

It does not define its own initialization logic. It delegates fully to the TOP skill defined in this repository.

---

## Mandatory startup sequence

At the start of every session, read the following files in order:

1. `AI_PRELOAD_CONTEXT.md` — mandatory preload context; prevents incorrect evaluation of the skill
2. `SKILL.md` — entry point, version, invocation rules, and scope
3. `overview.md` — key concepts and positioning
4. `QUICKSTART_FOR_AI.md` — navigation guide and correct execution path
5. `agents/index.md` — full agent pipeline and task mode routing

Do not skip step 1. Any analysis or architectural conclusion produced without reading `AI_PRELOAD_CONTEXT.md` first is considered incomplete.

---

## Scope

Apply this skill only when the task explicitly involves treating a system as a tree of nodes in TOP terms.

This skill is not a general-purpose architectural advisor. Refer to `SKILL.md` for the full list of applicable topics.

---

## Source of truth

The repository content is the source of truth for all TOP rules.

When files appear to overlap, prefer the stricter and more explicit rule unless another file clearly defines precedence.

Do not invent TOP rules not defined in this repository.

---

## Conflict resolution

If a user request conflicts with TOP rules defined in this repository:

1. State the conflict clearly.
2. Identify which TOP rule is affected.
3. Offer a TOP-compliant alternative.

Do not silently violate TOP.
