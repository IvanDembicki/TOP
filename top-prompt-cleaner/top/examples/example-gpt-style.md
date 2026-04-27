# Example: TargetLLMStyle — GPT Profile (message_bundle)

**Mode:** `target_llm_style`
**Target style:** `gpt`
**Target style source:** `stated`
**Output type:** `message_bundle`
**Final state:** `ready`

---

## Input

```
target_style: gpt

You are an experienced copywriter. Write a product description for a B2B SaaS tool
that helps HR teams automate onboarding. It should be persuasive, under 150 words,
and highlight time savings and compliance benefits. Avoid jargon.
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
  "goal": "Write a product description for a B2B SaaS HR onboarding tool",
  "goal_source": "stated",
  "constraints": [
    "persuasive",
    "under 150 words",
    "highlight time savings and compliance benefits",
    "avoid jargon"
  ],
  "output_format": "product description",
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
  "conflicts": [],
  "has_blocking_conflicts": false
}
```

### TargetLLMStyleMode (profile: gpt)

GPT profile applied:
- Role description moved to system message
- Task moved to user message
- Constraints listed explicitly before output requirements in user message
- `output_type` set to `message_bundle` (standard GPT API format)
- No output directive added — output format was already clearly stated ("product description")

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
  "goal": "Write a product description for a B2B SaaS HR onboarding tool",
  "goal_source": "stated",
  "constraints": ["persuasive", "under 150 words", "highlight time savings and compliance benefits", "avoid jargon"],
  "output_format": "product description",
  "output_format_source": "stated"
}
```

**Target style output:**

```json
{
  "output_type": "message_bundle",
  "target_style": "gpt",
  "target_style_source": "stated",
  "profile_used": "gpt",
  "content": {
    "system_message": "You are an experienced copywriter specializing in B2B SaaS.",
    "user_message": "Write a product description for an HR onboarding automation tool.\n\nConstraints:\n- Persuasive tone\n- Under 150 words\n- Highlight: time savings and compliance benefits\n- No jargon\n\nOutput: product description (plain paragraph form)"
  }
}
```

**Diff:**

```json
{
  "removed_noise": ["target_style: gpt"],
  "rewritten_phrases": [
    {
      "original": "You are an experienced copywriter. Write a product description...",
      "rewritten": "system_message: 'You are an experienced copywriter...'; user_message: task + constraints",
      "reason": "GPT profile: role moved to system message, task and constraints to user message."
    }
  ],
  "resolved_conflicts": [],
  "unresolved_conflicts": [],
  "preserved_constraints": [
    "persuasive",
    "under 150 words",
    "highlight time savings and compliance benefits",
    "avoid jargon"
  ],
  "warnings": []
}
```

---

**Full final output (machine-verifiable contract):**

```json
{
  "status": "ready",
  "target_style_output": {
    "output_type": "message_bundle",
    "target_style": "gpt",
    "target_style_source": "stated",
    "profile_used": "gpt",
    "content": {
      "system_message": "You are an experienced copywriter specializing in B2B SaaS.",
      "user_message": "Write a product description for an HR onboarding automation tool.\n\nConstraints:\n- Persuasive tone\n- Under 150 words\n- Highlight: time savings and compliance benefits\n- No jargon\n\nOutput: product description (plain paragraph form)"
    }
  },
  "structured_prompt": {
    "goal": "Write a product description for a B2B SaaS HR onboarding tool",
    "goal_source": "stated",
    "constraints": ["persuasive", "under 150 words", "highlight time savings and compliance benefits", "avoid jargon"],
    "output_format": "product description",
    "output_format_source": "stated"
  },
  "diff": {
    "removed_noise": ["target_style: gpt"],
    "rewritten_phrases": [
      {
        "original": "You are an experienced copywriter. Write a product description...",
        "rewritten": "system_message: 'You are an experienced copywriter...'; user_message: task + constraints",
        "reason": "GPT profile: role moved to system message, task and constraints to user message."
      }
    ],
    "resolved_conflicts": [],
    "unresolved_conflicts": [],
    "preserved_constraints": [
      "persuasive",
      "under 150 words",
      "highlight time savings and compliance benefits",
      "avoid jargon"
    ],
    "warnings": []
  }
}
```

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `target_llm_style` |
| 7 | TargetLLMStyleMode changes style only, not semantics | PASS — goal and all constraints preserved |
| 8 | Diff required when prompt was modified | PASS — diff present |
| 10 | SensitiveDataDetector runs before any transformation | PASS |
