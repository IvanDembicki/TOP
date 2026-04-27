# BatchCleanMode

**Status:** `planned` — not yet active. Spec defined for roadmap alignment.

## Purpose

Clean a list of prompts in a single invocation. Designed for teams maintaining prompt libraries who need to audit and normalize multiple prompts without running them one by one.

## Planned input

```json
{
  "prompts": [
    { "id": "p1", "label": "onboarding email", "content": "..." },
    { "id": "p2", "label": "support reply", "content": "..." }
  ],
  "batch_mode": "quick_clean | strict_clean",
  "target_style": "claude | gpt | default | null"
}
```

## Planned output

```json
{
  "batch_status": "complete | partial | failed",
  "results": [
    {
      "id": "p1",
      "status": "ready | blocked | escalated",
      "cleaned_prompt": "...",
      "diff": {},
      "warnings": []
    }
  ],
  "summary": {
    "total": 2,
    "ready": 1,
    "blocked": 1,
    "escalated": 0
  }
}
```

## Planned behavior

- Each prompt runs through the full single-prompt pipeline independently.
- SensitiveDataDetector runs per prompt — a blocking finding in one prompt does not stop the batch.
- Blocked prompts are reported with their diagnosis; the batch continues.
- Escalated prompts are flagged; the batch continues.
- A summary is produced at the end.

## Difference from running prompts individually

| Single prompt | Batch |
|---|---|
| Full node trace shown | Summary table + per-prompt status |
| Interactive clarification supported | Blocking fields flagged, not asked interactively |
| Sensitive data halts the run | Sensitive data blocks that prompt; batch continues |

## Clarification handling in batch

Batch mode does NOT stop to ask clarification questions. Instead:
- Missing `goal` → flag as `blocked`, include diagnosis, continue to next prompt.
- Missing `output_format` → same.
- Blocked prompts are listed in the summary for manual follow-up.

## Activation (planned)

```
Clean these prompts as a batch: [paste JSON or markdown list]
```

or:

```
Audit my prompt library: [paste list]
```

## Why this is not yet active

Batch mode requires a deterministic per-prompt state machine that does not yet have a runnable implementation. The single-prompt pipeline (1.0.0 stable) must ship first. Targeting a post-1.0 release (1.1.0).
