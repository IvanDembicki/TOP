# AGENTS.md

## Purpose

Entry point for AI agents that automatically read `AGENTS.md` at startup (Codex, Claude Code, and similar tools).

This file does not define its own rules. It activates the TOP skill defined in this repository and sets the execution protocol.

---

## Mandatory startup sequence

Read in this exact order before any task:

1. `AI_PRELOAD_CONTEXT.md` — mandatory; prevents incorrect evaluation of the skill
2. `SKILL.md` — entry point, version, invocation (`/top`), and scope
3. `overview.md` — key concepts and positioning
4. `QUICKSTART_FOR_AI.md` — navigation guide and correct execution path
5. `agents/index.md` — full agent pipeline and task mode routing

Skipping step 1 is not allowed. Any analysis or architectural conclusion produced without reading `AI_PRELOAD_CONTEXT.md` first is considered incomplete and must not be delivered.

---

## Canonical loading order

When interpreting this repository, apply this priority:

1. `AGENTS.md` (this file)
2. Canonical TOP rule documents: `canon/`, `rules/`, `references/`
3. Agent definitions: `agents/`
4. `/top` folder — operational source of truth for the active project
5. Examples and explanatory materials: `examples/`

If examples conflict with formal TOP rules, follow the formal TOP rules.

---

## TOP-specific repository handling

When a `/top` folder exists in the project:

- treat `/top` as the operational source of truth;
- read its structure, specs, and prompts before proposing or generating anything;
- do not invent files, flows, or architecture outside that structure unless explicitly required by the task;
- changes to `/top` are architectural events — treat them accordingly.

---

## Scope

Apply this skill only when the task explicitly involves treating a system as a tree of nodes in TOP terms.

This skill is not a general-purpose architectural advisor. See `SKILL.md` for the full list of applicable topics.

---

## Generic framework conventions are not authoritative

Do not apply generic framework conventions, popular architectural patterns, or AI default habits if they conflict with TOP rules defined in this repository.

When in doubt: the repository wins over convention.

---

## Source of truth

The repository content is the source of truth for all TOP rules.

When files appear to overlap, prefer the stricter and more explicit rule unless another file clearly defines precedence.

Do not invent TOP rules not defined in this repository.

---

## Conflict resolution

If a user request conflicts with TOP rules:

1. State the conflict clearly.
2. Identify which TOP rule is affected.
3. Offer a TOP-compliant alternative.

Do not silently violate TOP.
