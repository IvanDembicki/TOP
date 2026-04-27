# Troubleshooting — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

---

## Validator issues

### `npm run validate` fails with `Cannot find package 'ajv'`

Run `npm install` first:

```bash
npm install
npm run validate
```

### `npm run validate` exits with failures

Run with `--verbose` to see which block failed and why:

```bash
npm run validate:verbose
```

Each failure shows the example file, block number, schema name, and the specific validation error.

### Validator reports broken markdown links

A file referenced by a relative link in docs or examples doesn't exist on disk. Check the path listed in the failure message and either fix the link or create the missing file.

### Validator reports unknown JSON block

A JSON block in an example was not matched to any schema. This means either:
- The block needs a schema that doesn't exist yet
- The `detectSchema()` heuristic in `scripts/validate.js` needs an entry for it

Add the schema or update the detection heuristic. Unknown blocks are treated as failures — not silently skipped.

---

## Skill behavior issues

### Prompt returns `blocked` — sensitive data detected

The skill detected a secret (API key, password, private key) in your prompt before processing.

**Fix:** Remove the secret and replace it with a placeholder:

```
Before: My API key is sk-proj-abc123...
After:  My API key is {{OPENAI_API_KEY}}
```

Resubmit after removing the secret. The skill will not process the prompt until it is clear.

### Prompt returns `blocked` — goal missing

The skill cannot identify what the prompt is asking for.

**Fix:** Answer the clarification question. The skill will ask:
- What should the LLM produce?
- What format should the output be?

Pick an option (`A`, `B`, `C`) or use `U` to type your own answer.

### Prompt returns `blocked` — output format missing

In StrictClean mode, the output format must be explicit.

**Fix:** Add an output format to your prompt:

```
Before: Explain what a P/E ratio is.
After:  Explain what a P/E ratio is. Output: 2-paragraph explanation.
```

### Prompt returns `blocked` — blocking conflict

Two or more constraints are mutually exclusive and cannot be auto-resolved without silently violating your intent.

**Fix:** Read the `unresolved_conflicts` list and choose which constraint to keep. Remove or relax the one you don't need, then resubmit.

Example:
```
Conflict: "under 100 words" vs "include all edge cases and full API contract"
Fix: either remove the word limit, or narrow scope to one section only.
```

### Prompt returns `escalated`

Your prompt describes a multi-step AI workflow — not a single prompt.

**Signals that trigger escalation:**
- Multiple AI agents with distinct roles
- Conditional routing between agents based on runtime results
- Stateful loops (loop-back, retry, shared memory)
- Persistent state or external system handoffs

**Fix:** Use TOP Skill Factory to design the multi-agent system. The `escalation_notice.signals` list explains exactly what was detected.

### Target style not applied

You asked for `target_style: claude` or `target_style: gpt` but the output doesn't look adapted.

Check:
1. Did you include `target_style: claude` (or `gpt`) at the top of your prompt?
2. Is the target style spelled correctly? Valid values: `claude`, `gpt`, `custom`.

If target_style is not declared, the skill auto-detects from idioms. If no idioms are found, it defaults to the generic profile (minimal cleaning only).

### Medium complexity warning in diff

Your prompt includes sequential logic, conditional branching, or edge-case handling that could grow into a workflow.

This is not an error. The prompt was cleaned successfully. The warning in `diff.warnings` suggests considering TOP Skill Factory if the prompt grows more complex.

---

## Version issues

### Version mismatch in validator

```
Version mismatch: release-metadata.json (X) vs package.json (Y)
```

All three files must have the same version:
- `package.json`
- `release-metadata.json`
- `top/spec.json`

Update all three to match before running `npm run validate`.

---

## Common mistakes

| Symptom | Likely cause | Fix |
|---|---|---|
| Goal is extracted incorrectly | Prompt has no explicit goal sentence | Add "Goal: ..." or "Task: ..." to the prompt |
| Constraints removed in output | Constraint was flagged as noise | Check `diff.removed_noise` — if wrong, report the issue |
| Wrong mode activated | No mode hint in prompt | Add `mode: strict` or `target_style: claude` to override |
| Clarification loop repeats | Response not incorporated | Make sure your answer addresses the specific `missing_field` |
