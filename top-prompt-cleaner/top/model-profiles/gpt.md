# Model Profile: GPT (OpenAI)

## Identity

`target_style: "gpt"`

Applies when the cleaned prompt will be sent to OpenAI models: GPT-4o, GPT-4-turbo, GPT-4, o1, o3, or ChatGPT via API.

## Formatting preferences

| Dimension | GPT preference |
|---|---|
| Instruction structure | Explicit numbered steps work well, especially for multi-part tasks |
| Role framing | Effective. "You are a senior software engineer…" style system prompts improve output quality reliably. |
| System / human split | GPT uses a system message + user message model. Put persona, rules, and output format in system; the actual task in user. |
| Tone directive | Include when needed. GPT follows tone instructions literally. |
| Output length hint | Token-count hints are understood but sentence/word counts are clearer. |
| JSON mode | When JSON output is needed, use `response_format: { type: "json_object" }` AND instruct the model to produce JSON in the system message — both together. |
| Chain-of-thought | Use "Let's think step by step" or "Reason through this step by step before answering." |

## What to preserve from the original prompt

- All explicit constraints stated by the user.
- The goal and output format as specified.
- Any domain-specific vocabulary.

## What TargetLLMStyleMode changes

- Moves role description into a system message block if not already there.
- Structures multi-step instructions as a numbered list.
- Separates background context from the task instruction.
- Makes the output format explicit when it was already stated or safely inferred — restates it in a clear directive form ("Respond only with…", "Return a JSON object with…"). Does NOT introduce a new output format that was not present or inferable from the original.

## What it never changes

- The semantic goal.
- Any constraint — even if it seems redundant.
- Output format specification.

## Anti-patterns to fix for GPT

| Anti-pattern | Fix |
|---|---|
| Role description buried in user message | Move to system message |
| Output format stated but buried or implicit | Make it explicit as a directive; do not invent if truly absent |
| Task and context interleaved | Separate: context first, task second |
| "Think step by step" missing on reasoning tasks | Add it |
| Constraints listed after the task | Move constraints before the task |

## Notes on o1/o3 (reasoning models)

- o1 and o3 do not support a system message in the same way — use a single user message.
- Do not add "Think step by step" — these models reason internally and the directive is redundant.
- Keep prompts shorter and more direct; verbose prompts do not improve output quality.
- TargetLLMStyleMode should detect `target_model: "o1"` or `"o3"` and apply the reasoning-model sub-profile.
