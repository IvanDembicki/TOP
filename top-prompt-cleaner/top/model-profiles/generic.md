# Model Profile: Generic

## Identity

`target_style: "default"` (also used as fallback when `target_style` is absent)

Applies when the target LLM is unknown, unspecified, or is a model not covered by a named profile (e.g., Gemini, Mistral, Llama, Cohere, custom fine-tunes).

## Design principle

This profile applies the smallest safe set of cleaning actions that improve clarity without making model-specific assumptions. It prioritizes correctness over optimization.

## Formatting preferences

| Dimension | Generic preference |
|---|---|
| Instruction structure | Clear paragraph or simple bulleted list. Avoid deep nesting. |
| Role framing | Keep if present; do not add if absent. |
| Tone directive | Keep if present; do not add if absent. |
| Output length hint | Keep if present; normalize phrasing only. |
| Output format | Keep exactly as stated. Do not assume JSON, markdown, or plain text. |
| Chain-of-thought | Keep if present; do not add. |

## What TargetLLMStyleMode changes in generic mode

- Removes obvious noise (filler phrases, redundant politeness, duplicate statements).
- Normalizes whitespace and removes blank lines within a single-topic block.
- Surfaces unresolved contradictions as warnings — does not auto-resolve.
- Does not restructure, reorder, or reframe the prompt.

## What it never changes

- The semantic goal.
- Any constraint — even if it seems redundant.
- Output format specification.
- Role framing (present or absent).

## When to upgrade to a named profile

Suggest switching to a named profile when:
- The user states the target model explicitly.
- The prompt contains model-specific idioms (e.g., "You are ChatGPT", Claude XML tags).
- The output format requirement is highly model-specific (e.g., function-calling JSON for OpenAI).

Emit this recommendation in the diff `warnings` array:
```json
{
  "warnings": [
    "Target model not specified. Cleaned using generic profile. For better results, specify target_style: claude | gpt | gemini."
  ]
}
```

## Anti-patterns to fix regardless of model

These are universally harmful and are always cleaned:

| Anti-pattern | Fix |
|---|---|
| "As an AI language model, I cannot…" in the prompt | Remove — this is a response artifact, not an instruction |
| Prompt that starts with "Hi Claude/GPT" | Remove greeting |
| Triple-repeated constraint | Keep once |
| Empty parentheses or brackets `()` `[]` | Remove |
| Trailing "Thank you!" | Remove |
