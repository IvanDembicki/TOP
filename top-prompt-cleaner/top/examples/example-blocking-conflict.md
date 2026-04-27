# Example: QuickClean — Blocked (Blocking Conflict)

**Mode:** `quick_clean`
**Final state:** `blocked`
**Blocking reason:** Mutually exclusive output requirements; auto-resolution would silently violate user intent.

---

## Input

```
Write a detailed technical specification for the new authentication module.
It must be under 100 words. Include all edge cases, error codes, security considerations,
failure modes, and the full API contract.
```

---

## Node trace

### InputController

```json
{
  "original_prompt": "...",
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
  "goal": "Write a technical specification for an authentication module",
  "goal_source": "stated",
  "constraints": [
    "under 100 words",
    "include all edge cases",
    "include all error codes",
    "include security considerations",
    "include failure modes",
    "include the full API contract"
  ],
  "output_format": "technical specification",
  "output_format_source": "stated",
  "noise_candidates": []
}
```

### ClarificationController

```json
{
  "clarification_needed": false,
  "proceed_with_inference": false
}
```

### ConflictDetector

```json
{
  "conflicts": [
    {
      "description": "'under 100 words' and 'include all edge cases, error codes, security considerations, failure modes, and full API contract' are mutually exclusive. A complete technical specification of this scope cannot fit in 100 words.",
      "severity": "blocking",
      "resolution_recommendation": "Choose one: (A) remove the word limit and allow a full specification, or (B) narrow the scope to one section only (e.g. API contract only, no edge cases)."
    }
  ],
  "has_blocking_conflicts": true
}
```

### FinalDecisionController

```json
{
  "status": "blocked",
  "diagnosis": "Blocking conflict: 'under 100 words' vs 'include all edge cases, error codes, security considerations, failure modes, and full API contract'. Constraints are mutually exclusive and cannot be auto-resolved."
}
```

---

## Final output

**Status:** `blocked`

**Diagnosis:**

> The prompt contains a blocking conflict that cannot be auto-resolved without silently violating your intent.
>
> **Conflict:** "under 100 words" vs "include all edge cases, error codes, security considerations, failure modes, and full API contract"
>
> These constraints are mutually exclusive. A complete technical specification of this scope cannot fit in 100 words.
>
> **Options to resolve:**
> - A — Remove the word limit; allow a full specification document
> - B — Keep the word limit; narrow scope to one section only (e.g., API contract only)
>
> Please clarify your intent and resubmit.

**Diff:**

```json
{
  "removed_noise": [],
  "rewritten_phrases": [],
  "resolved_conflicts": [],
  "unresolved_conflicts": [
    {
      "conflict": "'under 100 words' vs 'include all edge cases, error codes, security considerations, failure modes, and full API contract'",
      "recommendation": "Choose one: (A) remove the word limit, or (B) narrow scope to a single section."
    }
  ],
  "preserved_constraints": [],
  "warnings": []
}
```

---

**Full final output (machine-verifiable contract):**

```json
{
  "status": "blocked",
  "diagnosis": "Blocking conflict: 'under 100 words' vs 'include all edge cases, error codes, security considerations, failure modes, and full API contract'. Constraints are mutually exclusive and cannot be auto-resolved without silently violating user intent."
}
```

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `quick_clean` |
| 5 | Cleaned prompt must not silently remove user-stated constraints | PASS — no cleaned_prompt produced |
| 6 | Validation must pass before result is marked ready | PASS — status is `blocked` |
| 12 | Conflict resolution must be explicit; silent choices are not allowed | PASS — blocking conflict surfaced, not resolved |
| QuickClean rule | Blocking conflicts result in status: blocked, not ready | PASS |
