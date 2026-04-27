# Model Profile: Claude (Anthropic)

## Identity

`target_style: "claude"`

Applies when the cleaned prompt will be sent to Claude (any version: Claude 3 Haiku, Sonnet, Opus, or Claude 4+).

## Formatting preferences

| Dimension | Claude preference |
|---|---|
| Instruction structure | Prose paragraphs or light markdown; avoid rigid numbered lists for conversational tasks |
| Role framing | Optional. Claude responds well to role framing but does not require it. Keep it short (1 sentence). |
| System / human split | Claude uses a system prompt + human turn model. Output the goal and context in the system prompt; the specific task in the human turn. |
| Tone directive | Not required. Claude defaults to helpful and direct. Add only when a non-default tone is explicitly needed. |
| Output length hint | Effective. Use "respond in 2-3 sentences" or "produce a complete implementation" rather than token counts. |
| XML tags | Supported and useful for multi-section inputs: `<context>`, `<task>`, `<constraints>`, `<format>`. |
| Chain-of-thought | Use "Think step by step" or "Think through this carefully" — works well with extended thinking models. |

## What to preserve from the original prompt

- All explicit constraints stated by the user.
- The goal and output format as specified.
- Any domain-specific vocabulary.

## What TargetLLMStyleMode changes

- Replaces `"As a language model, ..."` preamble with a direct instruction.
- Removes redundant politeness phrases ("Please kindly", "If you don't mind").
- Normalizes list formatting to prose or simple bullet list depending on task type.
- Adds `<context>` / `<task>` XML wrappers when the prompt mixes background info with instructions.

## What it never changes

- The semantic goal.
- Any constraint — even if it seems redundant.
- Output format specification.

## Anti-patterns to fix for Claude

| Anti-pattern | Fix |
|---|---|
| Overly long role description (3+ sentences) | Trim to 1 sentence |
| "respond ONLY with JSON and nothing else" + no schema | Add a schema or example |
| Duplicate constraint stated 3 times | Keep once, in `<constraints>` block |
| "You are a helpful assistant" with no other context | Remove — adds nothing |
