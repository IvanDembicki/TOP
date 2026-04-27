# Usage Guide — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

---

## 1. Installation

TOP Prompt Cleaner is a Claude skill — no server, no binary.

**As a Claude skill:**

Paste the contents of `SKILL.md` at the start of a Claude conversation, or reference it as a system prompt. The skill activates automatically when you give Claude a prompt to clean.

**To run the validator:**

```bash
npm install
npm run validate
```

Requires Node.js ≥ 18.

---

## 2. Using the skill

**Basic usage:**

```
Clean this prompt: [paste your prompt here]
```

**Specifying a target model:**

```
Clean this prompt for Claude: [prompt]
Clean this prompt for GPT: [prompt]
```

**Specifying a mode:**

```
mode: strict
Clean this prompt: [prompt]
```

**Batch (roadmap):**

```
Clean these prompts: [list]
```

> BatchCleanMode is planned for a future post-1.0 release (target: 1.1.0). Use one prompt per request for now.

---

## 3. Modes

| Mode | When to use | What happens |
|---|---|---|
| **QuickClean** | Default — fast iteration | Remove noise, resolve warning conflicts, structure output |
| **StrictClean** | When you need guarantees | Validate goal + output format; block and ask if either is missing |
| **TargetLLMStyle** | Specify `target_style: claude` or `gpt` | Adapt formatting to the target model's conventions |

The mode is selected automatically based on your input. Use `mode: strict` to override.

---

## 4. Using the meta-prompt

`meta-prompt.md` is a standalone copy-paste prompt that activates the full 9-step pipeline in any Claude conversation without loading `SKILL.md` first.

Open `meta-prompt.md` and follow the instructions at the top.

---

## 5. Output states

Every run ends in one of three terminal states:

| State | Meaning | What you receive |
|---|---|---|
| `ready` | Prompt cleaned successfully | `cleaned_prompt` + `structured_prompt` + `diff` |
| `blocked` | Cannot proceed without your input | `diagnosis` explaining what is missing or conflicting |
| `escalated` | Prompt is a multi-step workflow, not a single prompt | `escalation_notice` with recommended next step |

---

## 6. Reading the diff

The `diff` block explains every change:

- `removed_noise` — filler phrases that were stripped
- `rewritten_phrases` — each rewrite with the reason
- `resolved_conflicts` — warning-level tensions that were auto-resolved
- `unresolved_conflicts` — blocking conflicts surfaced for you to decide
- `preserved_constraints` — user-stated constraints kept unchanged
- `warnings` — non-blocking notices (inferred fields, medium complexity)

---

## 7. Answering clarification questions

When the skill is blocked and asks a clarification question:

- Options are labeled `A`, `B`, `C`, etc.
- Pick an option by letter, or type `U` followed by your own answer.

Example:

```
U: I want to write a product description for a SaaS tool, output as a short paragraph.
```

The skill re-runs with your answer incorporated.

---

## 8. Handling blocked output

If you receive `status: blocked`:

1. Read the `diagnosis` — it names the specific problem.
2. If it's a **clarification question**, answer it (see above).
3. If it's a **conflict**, choose which constraint to keep and resubmit.
4. If it's **sensitive data**, remove the secret and replace with a placeholder.

---

## 9. Handling escalated output

If you receive `status: escalated`, your prompt describes a multi-step AI workflow.

The skill cannot clean it — it is not a single prompt. Use **TOP Skill Factory** instead.

The `escalation_notice` will list the specific signals that triggered escalation.

---

## 10. Running the validator

```bash
npm run validate          # summary output
npm run validate:verbose  # block-by-block detail
```

The validator checks:

- All schemas listed in `top/spec.json` exist on disk
- All JSON blocks in `top/examples/` conform to the correct schema
- Version consistency across `package.json`, `release-metadata.json`, `top/spec.json`
- Markdown links in repo docs resolve to existing files

Exit code 0 = all checks passed. Exit code 1 = failures found.
