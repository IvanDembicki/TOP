# Example: StrictClean — Blocked (Missing Goal)

**Mode:** `strict_clean`
**Final state:** `blocked`
**Blocking reason:** Goal field empty; safe inference not permitted in strict mode.

---

## Input

```
Please make this better:

- Use bullet points
- Keep it short
- Professional tone
```

---

## Node trace

### InputController

```json
{
  "original_prompt": "Please make this better:\n\n- Use bullet points\n- Keep it short\n- Professional tone",
  "normalized": true
}
```

### SensitiveDataDetector

```json
{
  "sensitive_findings": [],
  "sensitive_blocking": false
}
```

### ComplexityDetector

```json
{
  "complexity_level": "low",
  "signals": [],
  "recommendation": "proceed"
}
```

### StructureExtractor

```json
{
  "goal": "",
  "goal_source": "missing",
  "constraints": ["Use bullet points", "Keep it short", "Professional tone"],
  "output_format": "",
  "output_format_source": "missing",
  "noise_candidates": ["Please make this better"]
}
```

### ClarificationController

```json
{
  "clarification_needed": true,
  "proceed_with_inference": false,
  "clarification_request": {
    "question": "What is the primary goal of this prompt — what should the LLM produce or improve?",
    "reason": "The goal field is empty. 'Please make this better' does not specify what 'better' means or what is being rewritten. In strict mode, safe inference is not permitted.",
    "missing_field": "goal",
    "blocking_if_unanswered": true,
    "options": [
      { "id": "A", "label": "Rewrite a text passage to be more concise" },
      { "id": "B", "label": "Improve a job description" },
      { "id": "C", "label": "Clean up a product announcement" },
      { "id": "U", "label": "User-defined answer" }
    ]
  }
}
```

### FinalDecisionController

```json
{
  "status": "blocked",
  "diagnosis": "Goal is missing and cannot be safely inferred in StrictMode. 'Please make this better' does not specify intent.",
  "clarification_request": {
    "question": "What is the primary goal of this prompt — what should the LLM produce or improve?",
    "reason": "The goal field is empty. 'Please make this better' does not specify what 'better' means or what is being rewritten. In strict mode, safe inference is not permitted.",
    "missing_field": "goal",
    "blocking_if_unanswered": true,
    "options": [
      { "id": "A", "label": "Rewrite a text passage to be more concise" },
      { "id": "B", "label": "Improve a job description" },
      { "id": "C", "label": "Clean up a product announcement" },
      { "id": "U", "label": "User-defined answer" }
    ]
  }
}
```

---

## Final output

**Status:** `blocked`

**Clarification question:**

> What is the primary goal of this prompt — what should the LLM produce or improve?
>
> **Why I'm asking:** The goal field is empty. "Please make this better" does not specify what "better" means or what is being rewritten. In strict mode, this cannot be inferred.
>
> **Options:** A — Rewrite a text passage to be more concise / B — Improve a job description / C — Clean up a product announcement / U — User-defined answer

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `strict_clean` |
| 2 | ComplexityDetector runs before any transformation | PASS |
| 3 | High complexity routes to escalation, not a cleaning mode | N/A — complexity is `low` |
| 4 | OutputBuilder cannot invent goal not present in original | PASS — no cleaned_prompt produced |
| 5 | Cleaned prompt must not silently remove user-stated constraints | PASS — no cleaned_prompt produced |
| 6 | Validation must pass before result is marked ready | PASS — result is `blocked`, not `ready` |
| 8 | Diff required when prompt was modified | PASS — no modification occurred |
| 9 | Escalation and cleaned output are mutually exclusive | PASS — `blocked` with clarification, not escalation |
| 10 | SensitiveDataDetector runs before any transformation | PASS — ran before StructureExtractor |
| 11 | ClarificationController blocks in strict mode when goal is absent | PASS |
