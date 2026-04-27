# Example: TargetLLMStyle — Generic Profile (Auto-detected)

**Mode:** `target_llm_style`
**Target style:** `default` (generic)
**Target style source:** `detected`
**Output type:** `single_prompt`
**Final state:** `ready`

---

## Input

```
As an AI language model, I cannot provide financial advice, but I will try my best
to help you understand investment basics.

Hi! Please kindly explain to me what a P/E ratio is () and why investors care about it [].

Please be helpful. Thank you thank you!!
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

### ModeRouter

No `target_style` declared. However, the prompt contains "As an AI language model, I cannot…" — a response artifact mistakenly included as an instruction. This is a universally-fixable anti-pattern (listed in `generic.md`). Mode selected: `target_llm_style` with `target_style_source: "detected"`, profile: `generic`.

```json
{
  "selected_mode": "target_llm_style",
  "target_style_source": "detected",
  "routing_reason": "Prompt contains 'As an AI language model' response artifact — generic profile anti-pattern detected."
}
```

### StructureExtractor

```json
{
  "goal": "Explain what a P/E ratio is and why investors care about it",
  "goal_source": "stated",
  "constraints": [],
  "output_format": "explanation",
  "output_format_source": "inferred",
  "noise_candidates": [
    "As an AI language model, I cannot provide financial advice, but I will try my best to help you understand investment basics.",
    "Hi!",
    "Please kindly",
    "()",
    "[]",
    "Please be helpful.",
    "Thank you thank you!!"
  ]
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

### TargetLLMStyleMode (profile: generic)

Generic anti-patterns fixed:

| Anti-pattern | Fix applied |
|---|---|
| "As an AI language model, I cannot…" response artifact in the prompt | Removed — this is not an instruction |
| "Hi!" greeting | Removed |
| "Please kindly" | Removed |
| Empty `()` and `[]` | Removed |
| "Please be helpful." | Removed (implied) |
| "Thank you thank you!!" | Removed |

Generic profile: no structural changes (no role framing added, no XML wrappers, no system/user split). Only universal noise removed.

Recommendation issued in warnings: target model not specified.

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

---

## Final output

**Status:** `ready`

**Structured prompt:**

```json
{
  "goal": "Explain what a P/E ratio is and why investors care about it",
  "goal_source": "stated",
  "constraints": [],
  "output_format": "explanation",
  "output_format_source": "inferred"
}
```

**Cleaned prompt:**

```
Explain what a P/E ratio is and why investors care about it.
```

**Diff:**

```json
{
  "removed_noise": [
    "As an AI language model, I cannot provide financial advice, but I will try my best to help you understand investment basics.",
    "Hi!",
    "Please kindly",
    "()",
    "[]",
    "Please be helpful.",
    "Thank you thank you!!"
  ],
  "rewritten_phrases": [],
  "resolved_conflicts": [],
  "unresolved_conflicts": [],
  "preserved_constraints": [],
  "warnings": [
    "Target model not specified. Generic profile applied — minimal, conservative cleaning only. For model-optimized results, specify target_style: claude | gpt.",
    "output_format inferred as 'explanation' from context (no explicit format stated)."
  ]
}
```

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `target_llm_style` |
| 4 | OutputBuilder cannot invent goal not present in original | PASS — goal extracted verbatim |
| 7 | TargetLLMStyleMode changes style only, not semantics | PASS — only noise removed |
| 8 | Diff required when prompt was modified | PASS — diff present |
| 10 | SensitiveDataDetector runs before any transformation | PASS |
