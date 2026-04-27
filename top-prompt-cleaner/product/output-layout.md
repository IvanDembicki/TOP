# Output Layout

How the final output should be presented to the user in each terminal state.

---

## State: ready

```
─────────────────────────────────────────
✓ Prompt cleaned
─────────────────────────────────────────

CLEANED PROMPT
──────────────
[cleaned_prompt text]

WHAT CHANGED
────────────
Removed noise:
  • [item 1]
  • [item 2]

Rewritten:
  • "[original]"
    → "[rewritten]"
    Why: [reason]

Conflicts resolved (auto):
  • [conflict] → [resolution]

Preserved constraints:
  • [constraint 1]
  • [constraint 2]

Warnings:
  ⚠ [warning text, if any]

STRUCTURED BREAKDOWN
────────────────────
Goal:          [goal]
Output format: [output_format]
Constraints:   [list]
Goal source:   stated | inferred
```

---

## State: blocked (conflict)

```
─────────────────────────────────────────
✗ Cannot clean — unresolved conflict
─────────────────────────────────────────

CONFLICT FOUND
──────────────
[conflict description]

This is a blocking conflict. Auto-resolution would silently
violate your intent.

OPTIONS TO RESOLVE
──────────────────
A — [option A]
B — [option B]

Please clarify and resubmit.
```

---

## State: blocked (missing field)

```
─────────────────────────────────────────
✗ Cannot clean — missing required field
─────────────────────────────────────────

QUESTION
────────
[question text]

Why I'm asking: [reason]

OPTIONS
───────
A — [label]
B — [label]
C — [label]
U — User-defined answer

Reply with A / B / C, or type your own answer.
```

---

## State: blocked (sensitive data)

```
─────────────────────────────────────────
✗ Stopped — sensitive content detected
─────────────────────────────────────────

FINDING
───────
Type:     [api_key | password | pii_email | ...]
Location: [truncated excerpt — max 40 chars]
Severity: blocking

What to do:
[recommendation]

Processing will not continue until the sensitive content
is removed. Fix it and resubmit.
```

---

## State: escalated

```
─────────────────────────────────────────
↑ This is a workflow, not a prompt
─────────────────────────────────────────

WHY IT ESCALATED
─────────────────
[reason text]

Signals detected:
  • [signal 1]
  • [signal 2]

This prompt describes a multi-step AI workflow.
TOP Prompt Cleaner handles single prompts only.

NEXT STEP
─────────
Use TOP Skill Factory → CreateNewSkillMode
to design the full workflow as a proper skill.
```

---

## Layout rules

- Never show internal node names to the user (no "StructureExtractor", no "ComplexityDetector")
- Never show raw JSON to the user — render as human-readable layout
- Diff section is always present in `ready` state; always absent in `escalated` state
- Warnings are shown in `ready` state only — they do not block; they inform
- Structured breakdown is shown in `ready` state only; collapsed by default in UI implementations
