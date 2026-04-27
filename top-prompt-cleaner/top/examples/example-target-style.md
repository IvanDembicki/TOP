# Example: TargetLLMStyle — Claude Profile Applied

**Mode:** `target_llm_style`
**Target style:** `claude`
**Final state:** `ready`

---

## Input

```
Hi ChatGPT! You are a helpful assistant. Please kindly help me with the following task if you don't mind.

I need you to act as a senior backend engineer. You are a senior backend engineer with 10 years of experience. You are an expert in Python. You know a lot about APIs.

Task: Review the following Python function and tell me if it has any problems. Also please tell me if there are any improvements. Additionally, please let me know if the code is good or bad. Here is the function:

{{function_code}}

Please respond in a structured way. Please use headers. Please be thorough. Thank you!
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
  "goal": "Review a Python function for problems and improvements",
  "goal_source": "stated",
  "constraints": ["10 years of experience as role detail"],
  "output_format": "Structured response with headers",
  "output_format_source": "stated",
  "noise_candidates": [
    "Hi ChatGPT!",
    "You are a helpful assistant.",
    "Please kindly help me with the following task if you don't mind.",
    "You are an expert in Python. You know a lot about APIs.",
    "Also please tell me if there are any improvements.",
    "Additionally, please let me know if the code is good or bad.",
    "Please respond in a structured way.",
    "Please use headers.",
    "Please be thorough.",
    "Thank you!"
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

### TargetLLMStyleMode (profile: claude)

Anti-patterns found and fixed:

| Anti-pattern | Fix applied |
|---|---|
| "Hi ChatGPT!" — wrong model greeting | Removed |
| "You are a helpful assistant." — zero-value preamble | Removed |
| "Please kindly … if you don't mind" | Removed |
| Role description repeated 3 times across 3 sentences | Merged into 1 sentence; **"10 years" preserved** as role detail |
| Task repeated 3 times ("tell me if it has any problems", "tell me if there are any improvements", "let me know if the code is good or bad") | Unified into single task statement |
| Output format repeated 3 times ("structured", "use headers", "be thorough") | Kept "structured with headers", removed "be thorough" (implied by structured) |
| "Thank you!" | Removed |

Profile-specific additions applied:
- Added `<context>` / `<task>` XML wrappers (Claude profile recommendation for prompts mixing role with task)

Note on "10 years of experience": this is a role detail, not noise. The profile rule is "compress, don't remove." The merged sentence retains it as "with 10 years of Python and API experience."

---

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
  "goal": "Review a Python function for problems and improvements",
  "goal_source": "stated",
  "constraints": ["10 years of experience as role detail"],
  "output_format": "Structured response with headers",
  "output_format_source": "stated"
}
```

**Cleaned prompt:**

```
<context>
You are a senior backend engineer with 10 years of Python and API experience.
</context>

<task>
Review the Python function below. Identify any problems and suggest improvements. Respond in a structured format with headers.

{{function_code}}
</task>
```

**Diff:**

```json
{
  "removed_noise": [
    "Hi ChatGPT!",
    "You are a helpful assistant.",
    "Please kindly help me with the following task if you don't mind.",
    "Also please tell me if there are any improvements.",
    "Additionally, please let me know if the code is good or bad.",
    "Please respond in a structured way.",
    "Please use headers.",
    "Please be thorough.",
    "Thank you!"
  ],
  "rewritten_phrases": [
    {
      "original": "I need you to act as a senior backend engineer. You are a senior backend engineer with 10 years of experience. You are an expert in Python. You know a lot about APIs.",
      "rewritten": "You are a senior backend engineer with 10 years of Python and API experience.",
      "reason": "Role stated three times across four sentences; merged into one. '10 years' preserved as a role detail — not filler. Domain specifics (Python, APIs) compressed into one phrase."
    },
    {
      "original": "tell me if it has any problems ... tell me if there are any improvements ... let me know if the code is good or bad",
      "rewritten": "Identify any problems and suggest improvements.",
      "reason": "Three restatements of the same task unified."
    }
  ],
  "resolved_conflicts": [],
  "unresolved_conflicts": [],
  "preserved_constraints": ["10 years of experience as role detail", "Structured response with headers"],
  "warnings": []
}
```

**Full final output (machine-verifiable contract):**

```json
{
  "status": "ready",
  "cleaned_prompt": "<context>\nYou are a senior backend engineer with 10 years of Python and API experience.\n</context>\n\n<task>\nReview the Python function below. Identify any problems and suggest improvements. Respond in a structured format with headers.\n\n{{function_code}}\n</task>",
  "structured_prompt": {
    "goal": "Review a Python function for problems and improvements",
    "goal_source": "stated",
    "constraints": ["10 years of experience as role detail"],
    "output_format": "Structured response with headers",
    "output_format_source": "stated"
  },
  "diff": {
    "removed_noise": [
      "Hi ChatGPT!",
      "You are a helpful assistant.",
      "Please kindly help me with the following task if you don't mind.",
      "Also please tell me if there are any improvements.",
      "Additionally, please let me know if the code is good or bad.",
      "Please respond in a structured way.",
      "Please use headers.",
      "Please be thorough.",
      "Thank you!"
    ],
    "rewritten_phrases": [
      {
        "original": "I need you to act as a senior backend engineer. You are a senior backend engineer with 10 years of experience. You are an expert in Python. You know a lot about APIs.",
        "rewritten": "You are a senior backend engineer with 10 years of Python and API experience.",
        "reason": "Role stated three times across four sentences; merged into one. '10 years' preserved as a role detail — not filler. Domain specifics (Python, APIs) compressed into one phrase."
      },
      {
        "original": "tell me if it has any problems ... tell me if there are any improvements ... let me know if the code is good or bad",
        "rewritten": "Identify any problems and suggest improvements.",
        "reason": "Three restatements of the same task unified."
      }
    ],
    "resolved_conflicts": [],
    "unresolved_conflicts": [],
    "preserved_constraints": ["10 years of experience as role detail", "Structured response with headers"],
    "warnings": []
  }
}
```

---

## Invariants verified

| # | Invariant | Status |
|---|---|---|
| 1 | ModeRouter activates exactly one mode | PASS — `target_llm_style` |
| 2 | ComplexityDetector runs before any transformation | PASS |
| 4 | OutputBuilder cannot invent goal not present in original | PASS — goal preserved |
| 5 | Cleaned prompt must not silently remove user-stated constraints | PASS — "10 years" preserved in output |
| 6 | Validation must pass before result is marked ready | PASS — all 6 rules pass |
| 7 | TargetLLMStyleMode changes style only, not semantics | PASS |
| 8 | Diff required when prompt was modified | PASS — diff present |
| 9 | Escalation and cleaned output are mutually exclusive | PASS — status is `ready`, no escalation |
| 10 | SensitiveDataDetector runs before any transformation | PASS — ran before StructureExtractor |
