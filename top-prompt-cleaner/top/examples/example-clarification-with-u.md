# Example: StrictClean — Clarification Round-Trip (User Responds with U)

**Mode:** `strict_clean`
**Final state:** `ready` (after clarification)
**Scenario:** Goal was missing → clarification issued → user responded with custom free-text answer (option U).

---

## Round 1: Initial submission

### Input

```
Please help me write something better.

Constraints:
- Use bullet points
- Keep it under 200 words
- Formal tone
```

---

### Node trace (Round 1)

#### SensitiveDataDetector → `sensitive_blocking: false`

#### ComplexityDetector

```json
{ "complexity_level": "low", "signals": [], "recommendation": "proceed" }
```

#### StructureExtractor

```json
{
  "goal": "",
  "goal_source": "missing",
  "constraints": ["bullet points", "under 200 words", "formal tone"],
  "output_format": "",
  "output_format_source": "missing"
}
```

#### ClarificationController

```json
{
  "clarification_needed": true,
  "proceed_with_inference": false,
  "clarification_request": {
    "question": "What exactly should the LLM write or rewrite? And what format should the result take?",
    "reason": "Goal and output format are both missing. 'Something better' cannot be processed without knowing what the content is and what form the output should take.",
    "missing_field": "goal",
    "blocking_if_unanswered": true,
    "options": [
      { "id": "A", "label": "Rewrite a job description" },
      { "id": "B", "label": "Improve a LinkedIn bio" },
      { "id": "C", "label": "Clean up a report section" },
      { "id": "U", "label": "User-defined answer" }
    ]
  }
}
```

#### FinalDecisionController → `status: blocked`

---

### Output (Round 1)

**Status:** `blocked`

> What exactly should the LLM write or rewrite? And what format should the result take?
>
> **Why I'm asking:** Goal and output format are both missing. "Something better" cannot be processed without knowing what the content is.
>
> **Options:** A — Rewrite a job description / B — Improve a LinkedIn bio / C — Clean up a report section / U — User-defined answer

---

## Round 2: User responds with option U

### User response

```json
{
  "selected_option": "U",
  "text": "I want to rewrite the company mission statement on our About page. Output should be a short paragraph, not bullets."
}
```

### clarification_request (updated with user_response)

```json
{
  "question": "What exactly should the LLM write or rewrite?",
  "reason": "Goal and output format were missing.",
  "missing_field": "goal",
  "blocking_if_unanswered": true,
  "options": [
    { "id": "A", "label": "Rewrite a job description" },
    { "id": "B", "label": "Improve a LinkedIn bio" },
    { "id": "C", "label": "Clean up a report section" },
    { "id": "U", "label": "User-defined answer" }
  ],
  "user_response": {
    "selected_option": "U",
    "text": "I want to rewrite the company mission statement on our About page. Output should be a short paragraph, not bullets."
  }
}
```

---

### Node trace (Round 2)

Pipeline re-runs with resolved goal and output_format from `user_response.text`.

#### StructureExtractor (Round 2)

```json
{
  "goal": "Rewrite the company mission statement on the About page",
  "goal_source": "inferred",
  "constraints": ["bullet points", "under 200 words", "formal tone"],
  "output_format": "short paragraph (not bullet list)",
  "output_format_source": "stated",
  "noise_candidates": ["Please help me write something better."]
}
```

Note: `goal_source: "inferred"` because the goal came from the user's clarification response, not the original prompt body. The output_format directive "not bullets" overrides the "Use bullet points" constraint — ConflictDetector will evaluate.

#### ConflictDetector

```json
{
  "conflicts": [
    {
      "description": "Original constraint 'Use bullet points' conflicts with user's clarification: 'not bullets, use a short paragraph'.",
      "severity": "warning",
      "resolution_recommendation": "User's clarification supersedes the original constraint. Output format: short paragraph."
    }
  ],
  "has_blocking_conflicts": false
}
```

Severity is `warning`, not `blocking`, because the user explicitly resolved the contradiction in their clarification response. Auto-resolution permitted.

#### ValidationController → `all_pass: true`

#### FinalDecisionController → `status: ready`

---

## Final output (Round 2)

**Status:** `ready`

**Cleaned prompt:**

```
Rewrite the following company mission statement for the About page.
Requirements: formal tone, under 200 words, output as a single short paragraph.

{{mission_statement}}
```

**Structured prompt:**

```json
{
  "goal": "Rewrite the company mission statement on the About page",
  "goal_source": "inferred",
  "constraints": ["formal tone", "under 200 words"],
  "output_format": "short paragraph",
  "output_format_source": "stated"
}
```

**Diff:**

```json
{
  "removed_noise": ["Please help me write something better."],
  "rewritten_phrases": [],
  "resolved_conflicts": [
    {
      "conflict": "'Use bullet points' vs user clarification 'not bullets, short paragraph'",
      "resolution": "User clarification supersedes original constraint. Output format: short paragraph."
    }
  ],
  "unresolved_conflicts": [],
  "preserved_constraints": ["formal tone", "under 200 words"],
  "warnings": [
    "goal_source is 'inferred': goal was provided by user in clarification, not present in original prompt body."
  ]
}
```

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 4 | OutputBuilder cannot invent goal not present in original | PASS — goal came from explicit user clarification |
| 5 | Cleaned prompt must not silently remove user-stated constraints | PASS — conflict resolved explicitly |
| 6 | Validation must pass before result is marked ready | PASS |
| 10 | SensitiveDataDetector runs before any transformation | PASS |
| 11 | ClarificationController blocks in strict mode when goal absent | PASS — blocked in Round 1, proceeded after Round 2 |
