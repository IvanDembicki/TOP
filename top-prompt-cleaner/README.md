# TOP Prompt Cleaner

© 2026 Ivans Dembickis · [ivan.dembicki@gmail.com](mailto:ivan.dembicki@gmail.com) · MIT License

Paste any prompt -> get a better one, with a full explanation of what changed and why.

This product is the prompt-cleaning layer in the TOP product line. If the prompt turns out to be a multi-step workflow or an actual skill, escalate to `top-skill-factory` instead of stretching this tool past its scope.

---

## Quickstart

**Step 1.** Give the skill your prompt:
```
Clean this prompt: [paste your prompt here]
```

**Step 2.** Optionally, tell it your target LLM:
```
Clean this prompt for Claude: [prompt]
Clean this prompt for GPT: [prompt]
```

**Step 3.** Get back:
- `cleaned_prompt` — noise-free, contradiction-resolved version
- `structured_prompt` — explicit goal / constraints / output format
- `diff` — what changed and why

**Step 4.** If you get a clarification question, answer it (pick A / B / C or type your own with U).

**Step 5.** If you get an escalation notice, your prompt is actually a multi-step AI workflow — use TopSkillFactory instead.

---

## Modes

| Mode | When it activates | What it does |
|---|---|---|
| **QuickClean** | Default | Fast single-pass: remove noise, resolve warning conflicts, structure output |
| **StrictClean** | When you need guarantees | Validates goal + output format; blocks and asks if either is missing |
| **TargetLLMStyle** | When you specify `target_style: claude` or `gpt` | Adapts formatting to the target model's conventions |

---

## What it handles

| Input | Output |
|---|---|
| Noisy, repetitive prompt | Cleaned, deduplicated version |
| Prompt with contradictory constraints | Conflict surfaced; auto-resolved if warning, blocked if blocking |
| Prompt missing a goal | Clarification question (StrictClean) or inference with warning (QuickClean) |
| Prompt with an API key, password, or private key | Blocked immediately — blocking severity; no processing until removed |
| Prompt with PII (email, phone, name+ID) or internal URLs | Warning surfaced in diff; blocks in StrictClean, proceeds with warning in QuickClean |
| Prompt that's actually a workflow | Escalated to TopSkillFactory |

---

## What it does NOT do

- Does not build AI agents or multi-step workflows — use TopSkillFactory
- Does not rewrite prompt goals — only extracts and makes them explicit
- Does not invent constraints you did not write

---

## Examples

10 worked examples covering all terminal states and modes. See `top/examples/README.md` for the full index.

| Example | Mode | Terminal state |
|---|---|---|
| `example-quick-clean` | QuickClean | `ready` |
| `example-medium-complexity` | QuickClean | `ready` with upgrade warning |
| `example-strict-blocked` | StrictClean | `blocked` — goal missing |
| `example-clarification-with-u` | StrictClean | `ready` after clarification round-trip |
| `example-blocking-conflict` | QuickClean | `blocked` — mutually exclusive constraints |
| `example-target-style` | TargetLLMStyle | `ready` — Claude profile |
| `example-gpt-style` | TargetLLMStyle | `ready` — GPT profile |
| `example-generic-style` | TargetLLMStyle | `ready` — Generic profile |
| `example-sensitive-blocked` | (any) | `blocked` — API key detected |
| `example-escalation` | (none) | `escalated` |

All examples are validated by `npm run validate`. 77 JSON blocks pass, 0 fail, 0 skipped.

---

## Validator

```bash
npm install
npm run validate          # summary
npm run validate:verbose  # block-by-block detail
npm run validate:release  # same as validate, explicit release gate
```

---

## Reading order (for reviewers)

1. `top/spec.json` — tree structure, invariants, output contract
2. `top/shared-rules/core-invariants.md` — 16 rules that govern every output
3. `top/prompts/mode-router.md` — routing logic
4. `top/modes/` — one file per mode
5. `top/schemas/` — 15 machine-checkable contracts for every output type
6. `top/examples/` — 10 worked examples covering all terminal states
7. `docs/contracts.md` — contract reference table for all 15 schemas
8. `docs/security.md` — sensitive data policy
9. `docs/usage.md` — user guide
10. `VALIDATION_REPORT.md` — last validator run results
