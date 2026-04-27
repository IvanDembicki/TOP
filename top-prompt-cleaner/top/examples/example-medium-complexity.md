# Example: QuickClean — Ready with Medium Complexity Warning

**Mode:** `quick_clean`
**Final state:** `ready`
**Note:** Medium complexity — cleaned successfully, but upgrade recommendation issued.

---

## Input

```
I need a prompt that first asks the AI to analyze a customer support ticket, then
categorizes it as billing, technical, or account issue, then drafts a reply based on
the category, and finally checks the reply for tone. Make sure it handles edge cases
where the category is unclear.

Keep it professional. Max 3 paragraphs in the reply.
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
  "complexity_level": "medium",
  "signals": [
    "sequential multi-step logic: analyze → categorize → draft → check",
    "conditional routing based on category",
    "edge case handling for unclear category"
  ],
  "recommendation": "proceed_with_warning"
}
```

Medium (not high) because: all steps are instructions to ONE model in a single context window. No separate agents, no persistent state across turns, no external system handoff. The "conditional routing based on category" happens inside the same model invocation — it is conditional logic in a prompt, not agent routing.

If the prompt said "a second AI reviews it" or "store the category in a database" → high complexity.

### StructureExtractor

```json
{
  "goal": "Process a customer support ticket: analyze, categorize, draft reply, and check tone",
  "goal_source": "stated",
  "constraints": [
    "professional tone",
    "reply max 3 paragraphs",
    "handle unclear category as edge case"
  ],
  "output_format": "categorized reply with tone check",
  "output_format_source": "stated",
  "noise_candidates": ["Make sure", "finally"]
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
  "conflicts": [],
  "has_blocking_conflicts": false
}
```

### ValidationController

```json
{
  "results": [
    { "rule": "goal_present", "pass": true },
    { "rule": "output_format_defined", "pass": true },
    { "rule": "no_unresolved_blocking_contradictions", "pass": true },
    { "rule": "constraints_not_removed", "pass": true },
    { "rule": "no_scope_expansion", "pass": true },
    { "rule": "diff_present_if_modified", "pass": true }
  ],
  "all_pass": true
}
```

### FinalDecisionController

```json
{
  "status": "ready"
}
```

---

## Final output

**Status:** `ready`

**Structured prompt:**

```json
{
  "goal": "Process a customer support ticket: analyze, categorize, draft reply, and check tone",
  "goal_source": "stated",
  "constraints": ["professional tone", "reply max 3 paragraphs", "handle unclear category as edge case"],
  "output_format": "categorized reply with tone check",
  "output_format_source": "stated"
}
```

**Cleaned prompt:**

```
You will process a customer support ticket in four steps:

1. Analyze the ticket to understand the core issue.
2. Categorize it as: billing, technical, or account issue.
   If the category is unclear, flag it as "needs_review" and explain why.
3. Draft a reply based on the category. Keep it professional. Max 3 paragraphs.
4. Check the reply tone before finalizing.
```

**Diff:**

```json
{
  "removed_noise": ["Make sure", "finally"],
  "rewritten_phrases": [
    {
      "original": "first asks the AI to analyze ... then categorizes ... then drafts ... and finally checks",
      "rewritten": "numbered 4-step list: Analyze → Categorize → Draft → Check",
      "reason": "Sequential 'then...then' chain converted to numbered steps for clarity."
    },
    {
      "original": "handles edge cases where the category is unclear",
      "rewritten": "flag it as 'needs_review' and explain why",
      "reason": "Edge case made explicit with a concrete action and output label."
    }
  ],
  "resolved_conflicts": [],
  "unresolved_conflicts": [],
  "preserved_constraints": [
    "professional tone",
    "reply max 3 paragraphs",
    "handle unclear category as edge case"
  ],
  "warnings": [
    "Medium complexity detected: this prompt includes sequential routing logic and conditional branching. It works as a single prompt now, but if it grows (more steps, more agents, dynamic routing), consider moving it to TOP Skill Factory as a skill."
  ]
}
```

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `quick_clean` |
| 2 | ComplexityDetector runs before any transformation | PASS |
| 3 | High complexity routes to escalation | N/A — complexity is `medium`, not `high` |
| 4 | OutputBuilder cannot invent goal or constraints | PASS |
| 6 | Validation must pass before ready | PASS — all rules pass |
| 8 | Diff required when prompt was modified | PASS — diff present |
