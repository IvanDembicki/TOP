---
name: top-prompt-cleaner
version: 1.0.0
description: Clean, structure, validate, and adapt any single prompt. Escalates complex multi-step workflows to TopSkillFactory.
trigger: when a user shares a prompt they want improved, cleaned, structured, or adapted for a specific model
---

# TOP Prompt Cleaner

## Startup sequence

On every invocation, before processing the user's prompt:

1. Read `release-metadata.json`.
2. If a trusted comparison manifest is available, compare versions and surface the result.
3. If the user references a different version, or update state is uncertain, re-read `SKILL.md` and `top/spec.json` before proceeding.
4. Proceed to `InputController`.

See `top/shared-rules/startup-update-check.md` for full behavior.

---

Use this skill when:
- User gives one prompt and wants it improved, shortened, or restructured
- User asks why their prompt produces inconsistent results
- User wants a prompt adapted for Claude or GPT conventions
- User wants to see what changed and why (diff)

Do not use this skill when:
- Task describes a multi-agent or multi-step AI workflow
- Task requires designing a skill, agent, or system
- Request involves routing between multiple AI behaviors based on runtime conditions
-> For those cases: use TopSkillFactory in CreateNewSkillMode

## What the user receives

| Output | Description |
|---|---|
| `cleaned_prompt` | Noise-free, contradiction-resolved version |
| `structured_prompt` | Explicit goal / constraints / output_format |
| `diff` | What changed and why |
| `escalation_notice` | When the prompt is actually a workflow |

## Modes

- **QuickCleanMode** - fast single-pass, no questions asked
- **StrictMode** - validates required fields, blocks when goal or output format are missing
- **TargetLLMStyleMode** - adapts style for Claude or GPT conventions

## Key behavior

- High complexity -> escalation to TopSkillFactory, no partial cleanup
- Sensitive content (API keys, passwords) -> blocked immediately
- PII / internal URLs -> warning in QuickClean, blocked in StrictClean
- Blocking conflicts -> surfaced in diff, not silently resolved
- Missing goal or output_format in StrictMode -> clarification request

## Reading order for reviewers

1. `release-metadata.json` - current release metadata and startup update check policy
2. `top/spec.json` - tree structure, invariants, output contract
3. `top/shared-rules/core-invariants.md` - 16 rules that govern every output
4. `top/shared-rules/startup-update-check.md` - startup update behavior
5. `top/prompts/mode-router.md` - routing logic
6. `top/modes/` - relevant mode
7. `top/schemas/` - all machine-checkable contracts
8. `top/examples/` - worked examples covering all terminal states
9. `RELEASE_NOTES.md` - release history
