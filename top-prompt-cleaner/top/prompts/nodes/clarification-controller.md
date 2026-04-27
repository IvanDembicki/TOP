# ClarificationController

## Purpose

Decide whether the input prompt is unambiguous enough to proceed, or whether a clarification question must be raised before transformation can begin. This node runs after ComplexityDetector and before any cleaning mode is activated.

## Input

Signal keys received:
- `original_prompt` — raw user text
- `structure` — output from StructureExtractor (goal, constraints, output_format, noise_candidates)
- `complexity_level` — "low" / "medium" / "high" (from ComplexityDetector)
- `mode` — routing target chosen by ModeRouter

## Output

Signal keys emitted:
- `clarification_needed` — boolean
- `clarification_request` — object matching `clarification_request.schema.json`, present only when `clarification_needed: true`
- `proceed_with_inference` — boolean, true when the gap is recoverable by safe inference (non-blocking)

## When to raise a clarification

Raise `clarification_needed: true` when **all** of the following are true:
1. A required field is absent or empty: `goal` is blank/missing OR `output_format` is blank/missing.
2. The gap **cannot** be resolved by safe inference (see Safe Inference Rules below).
3. The mode is `strict_clean` — QuickCleanMode may tolerate an inferred goal at warning level.

In all other cases set `clarification_needed: false` and continue.

## Safe Inference Rules

These gaps may be inferred without asking — set `proceed_with_inference: true` and record the inference in the diff:

| Absent field | Safe inference allowed when |
|---|---|
| `output_format` | Body text is present and mode is `quick_clean` |
| `style` | Assume `default` if not stated |
| `constraints` array empty | Absence is not a gap — proceed |

These gaps require a question — set `clarification_needed: true`:

| Absent field | Why it blocks |
|---|---|
| `goal` | Cannot clean a prompt without knowing the intent |
| `output_format` in `strict_clean` | Strict mode requires an explicit contract |

## Process

1. Read `structure.goal` and `structure.output_format`.
2. Check each required field against Safe Inference Rules.
3. If a blocking gap is found: build a `clarification_request` object and emit `clarification_needed: true`.
4. If no blocking gap: emit `clarification_needed: false`, `proceed_with_inference: [true|false]`.

## clarification_request object format

Must conform to `top/schemas/clarification_request.schema.json`:

```json
{
  "question": "What is the primary goal of this prompt — what should the LLM produce?",
  "reason": "The goal field is empty and cannot be safely inferred from the body text.",
  "missing_field": "goal",
  "blocking_if_unanswered": true,
  "options": [
    { "id": "A", "label": "Generate a product description" },
    { "id": "B", "label": "Answer a customer support question" },
    { "id": "C", "label": "Write a code snippet" },
    { "id": "U", "label": "User-defined answer" }
  ]
}
```

The `options` array is optional. Include it when the context strongly suggests a small set of likely answers (reduces friction for the user). Always include `{ "id": "U", "label": "User-defined answer" }` as the last option — this preserves user agency and is required by the schema when options are present.

## Boundaries

- Do NOT attempt to infer the goal in strict mode — ask.
- Do NOT ask about style or constraints — these are non-blocking and have safe defaults.
- Do NOT produce a cleaned prompt when `clarification_needed: true`. The FinalDecisionController must see the `clarification_request` and emit `status: "blocked"`.
- Do NOT ask more than one question per invocation.

## Invalid output conditions

- Emitting `clarification_request` and `proceed_with_inference: true` simultaneously — contradictory.
- Emitting `clarification_needed: false` when `structure.goal` is empty and mode is `strict_clean`.
- Omitting `clarification_request` when `clarification_needed: true`.
