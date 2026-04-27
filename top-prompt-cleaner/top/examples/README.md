# Examples Index — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

10 worked examples covering all terminal states, all active modes, and key edge cases.

---

## Index

| Example | Mode | Terminal state | Key scenario |
|---|---|---|---|
| [example-quick-clean](example-quick-clean.md) | QuickClean | `ready` | Warning-level conflict auto-resolved |
| [example-medium-complexity](example-medium-complexity.md) | QuickClean | `ready` | Medium complexity — cleaned with upgrade warning |
| [example-strict-blocked](example-strict-blocked.md) | StrictClean | `blocked` | Goal missing — clarification issued |
| [example-clarification-with-u](example-clarification-with-u.md) | StrictClean | `ready` | Full clarification round-trip, user answers with option U |
| [example-blocking-conflict](example-blocking-conflict.md) | QuickClean | `blocked` | Blocking conflict — mutually exclusive constraints |
| [example-target-style](example-target-style.md) | TargetLLMStyle | `ready` | Claude profile — XML wrappers, role compression |
| [example-gpt-style](example-gpt-style.md) | TargetLLMStyle | `ready` | GPT profile — role to system message, task to user message |
| [example-generic-style](example-generic-style.md) | TargetLLMStyle | `ready` | Generic profile — auto-detected from AI artifact idiom |
| [example-sensitive-blocked](example-sensitive-blocked.md) | (any) | `blocked` | API key detected — pipeline halted before transformation |
| [example-escalation](example-escalation.md) | (none) | `escalated` | Multi-agent workflow — routed to TopSkillFactory |

---

## Terminal state coverage

| Terminal state | Examples |
|---|---|
| `ready` | quick-clean, medium-complexity, clarification-with-u, target-style, gpt-style, generic-style |
| `blocked` | strict-blocked, blocking-conflict, sensitive-blocked |
| `escalated` | escalation |

---

## Schema coverage

Every example validates with `npm run validate`. Each JSON block in every example is matched to a schema and validated.

Run `npm run validate:verbose` to see block-by-block results.

---

## Reading an example

Each example follows this structure:

1. **Metadata** — mode, terminal state, key scenario
2. **Input** — the raw prompt submitted by the user
3. **Node trace** — output of each node in the pipeline (InputController → SensitiveDataDetector → ComplexityDetector → StructureExtractor → ConflictDetector → ValidationController → FinalDecisionController)
4. **Final output** — the user-facing result (human-readable + machine-verifiable JSON)
5. **Invariants verified** — which of the 16 core invariants apply and pass

The **Full final output** JSON block at the end of each worked example conforms to `final_output.schema.json` and is validated by the validator. All 78 JSON blocks across all example files pass schema validation.
