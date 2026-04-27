# Example: QuickCleanMode — ready case

## Input prompt (raw)

```
write me a marketing email for my startup that is short but also covers all the features
and has a professional tone but also feels friendly and personal and make sure it's not too salesy
```

## ComplexityDetector result

```json
{
  "complexity_level": "low",
  "signals": [],
  "recommendation": "proceed"
}
```

## StructureExtractor result

```json
{
  "goal": "write a marketing email for a startup",
  "goal_source": "stated",
  "constraints": ["short", "covers key features", "professional tone", "friendly and personal", "not salesy"],
  "output_format": "email",
  "output_format_source": "stated",
  "noise_candidates": ["also", "and make sure", "but also"]
}
```

## ConflictDetector result

```json
{
  "conflicts": [
    {
      "description": "'short' and 'covers all the features' are in tension: a short email cannot exhaustively cover all features.",
      "severity": "warning",
      "resolution_recommendation": "Narrow to most impactful features to satisfy both constraints."
    }
  ],
  "has_blocking_conflicts": false
}
```

Note: This conflict is `warning` severity, not `blocking`. Both constraints are user-stated preferences, not contradictory requirements — the tension is resolvable by narrowing scope without violating either intent. QuickCleanMode auto-resolves warning-level conflicts.

## Final output

**Status:** `ready`

**Structured prompt:**

```json
{
  "goal": "write a marketing email for a startup",
  "goal_source": "stated",
  "constraints": ["short", "most impactful features only", "professional and friendly tone", "not salesy"],
  "output_format": "email",
  "output_format_source": "stated"
}
```

**Cleaned prompt:**

Write a short marketing email for my startup. Highlight the most impactful features rather than all of them. Tone: professional and friendly. Avoid a pushy or salesy feel.

**Diff:**

```json
{
  "removed_noise": ["also", "but also", "and make sure"],
  "rewritten_phrases": [
    {
      "original": "covers all the features",
      "rewritten": "most impactful features",
      "reason": "Warning-level tension with 'short'; narrowed to satisfy both constraints."
    }
  ],
  "resolved_conflicts": [
    {
      "conflict": "'short' vs 'covers all the features'",
      "resolution": "Narrowed to 'most impactful features'"
    }
  ],
  "unresolved_conflicts": [],
  "preserved_constraints": ["short", "professional tone", "friendly and personal", "not salesy"],
  "warnings": []
}
```

**Full final output (machine-verifiable contract):**

```json
{
  "status": "ready",
  "cleaned_prompt": "Write a short marketing email for my startup. Highlight the most impactful features rather than all of them. Tone: professional and friendly. Avoid a pushy or salesy feel.",
  "structured_prompt": {
    "goal": "write a marketing email for a startup",
    "goal_source": "stated",
    "constraints": ["short", "most impactful features only", "professional and friendly tone", "not salesy"],
    "output_format": "email",
    "output_format_source": "stated"
  },
  "diff": {
    "removed_noise": ["also", "but also", "and make sure"],
    "rewritten_phrases": [
      {
        "original": "covers all the features",
        "rewritten": "most impactful features",
        "reason": "Warning-level tension with 'short'; narrowed to satisfy both constraints."
      }
    ],
    "resolved_conflicts": [
      {
        "conflict": "'short' vs 'covers all the features'",
        "resolution": "Narrowed to 'most impactful features'"
      }
    ],
    "unresolved_conflicts": [],
    "preserved_constraints": ["short", "professional tone", "friendly and personal", "not salesy"],
    "warnings": []
  }
}
```

