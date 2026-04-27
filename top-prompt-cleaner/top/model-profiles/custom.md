# Model Profile: Custom

## Identity

`target_style: "custom"`

Applies when the target LLM is a fine-tuned, self-hosted, or enterprise model that does not match the Claude or GPT conventions. Also applies when the team has defined their own prompting standard that overrides generic defaults.

## When to use this profile

- Internal LLM deployments (e.g., Llama fine-tune, Mistral, Falcon, custom Azure OpenAI endpoint)
- Teams with a documented internal prompt style guide
- Models with non-standard input formats (e.g., instruction tags like `[INST]`, `<<SYS>>`, Alpaca format)

## What TargetLLMStyleMode does in custom mode

Without a custom spec, `custom` falls back to `generic` behavior:
- Remove universal anti-patterns (filler, greetings, repeated constraints)
- Do not apply Claude or GPT structural conventions
- Surface a warning that no custom spec was found

With a custom spec (`top/model-profiles/custom-spec.md`):
- Apply the conventions defined in the spec
- Document which rules were applied in the diff

## Custom spec format

Create `top/model-profiles/custom-spec.md` in your project to define your own rules:

```markdown
# Custom Model Profile: [Your Model Name]

## Instruction format
[INST] {{task}} [/INST]

## Role framing
Not used — this model ignores role declarations.

## Output directive
Always end with: "Respond in JSON."

## Anti-patterns to fix
| Anti-pattern | Fix |
|---|---|
| XML tags | Remove — not supported |
| System/user split | Merge into single [INST] block |
```

When `custom-spec.md` is present, TargetLLMStyleMode reads it and applies its rules instead of generic defaults.

## Output

`output_type` for custom profile:
- `single_prompt` by default (unless custom-spec specifies otherwise)
- `profile_used: "custom"` or `profile_used: "generic"` (if no spec found)

## Warning emitted when no custom spec exists

```json
{
  "warnings": [
    "target_style 'custom' was requested but no custom-spec.md was found. Generic profile applied. To define your own conventions, create top/model-profiles/custom-spec.md."
  ]
}
```

## Anti-patterns to fix regardless of custom spec

These are universally harmful:

| Anti-pattern | Fix |
|---|---|
| "As an AI language model…" response artifact | Remove |
| Prompt greeting ("Hi!", "Hello!") | Remove |
| Duplicate constraints | Keep once |
| Empty brackets `()` `[]` | Remove |
| Trailing "Thank you!" | Remove |
