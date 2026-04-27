# TOP Prompt Cleaner — Landing Spec

Product landing page specification. Defines the message architecture, sections, and copy direction.

---

## Core value proposition

**Headline:**
> Your AI prompts are probably broken. Here's how to fix them.

**Subheadline:**
> Paste any prompt → get a cleaner version with a full explanation of what changed and why.

**CTA:**
> Try it now (paste your prompt below)

---

## Problem statement

Most people who use AI tools write prompts that are:
- Noisy — full of filler, repetition, and politeness phrases the model ignores
- Contradictory — "keep it short but cover everything"
- Vague — "make it better" without saying what better means
- Unstructured — no clear goal, no output format, no constraints

The result: inconsistent outputs, repeated back-and-forth, wasted time.

---

## The fix

TOP Prompt Cleaner takes your raw prompt and returns:

| What you get | What it means |
|---|---|
| **Cleaned prompt** | Noise removed, contradictions surfaced, structure clarified |
| **Structured breakdown** | Your goal, constraints, and output format — explicit |
| **Diff** | Exactly what changed and why |
| **Escalation notice** | If your prompt is actually a workflow, we tell you |

---

## How it works (3 steps)

**Step 1 — Paste**
Give it your prompt. Any length, any topic, any model target.

**Step 2 — Analyze**
It checks for sensitive data, complexity, conflicts, and missing fields before touching anything.

**Step 3 — Get results**
One of three outcomes:
- `ready` — cleaned prompt + diff
- `blocked` — specific conflict, missing field, or sensitive data detected; includes resolution options or a clarification question when a required field is missing
- `escalated` — this is a workflow, not a prompt; here's where to go instead

---

## Differentiators

### It shows its work
Every change comes with a reason. Nothing is silently rewritten.

### It knows when to stop
Sensitive data in your prompt? It halts immediately and tells you what to remove.
High-complexity workflow? It escalates instead of producing a cleaned fragment of the wrong thing.

### It adapts to your model
Claude and GPT have different prompt conventions. Declare your target model → get a prompt formatted for it.

### It protects your intent
Constraints are never silently removed. Conflicts are surfaced, not decided for you.

---

## Use cases

| Who | What they use it for |
|---|---|
| Product managers | Cleaning prompts before adding to team prompt libraries |
| Developers | Structuring system prompts for production use |
| AI consultants | Auditing client prompts before deploying to an agent |
| Marketers | Adapting a working ChatGPT prompt to Claude (or vice versa) |
| Anyone | "My prompt keeps giving inconsistent results — what's wrong with it?" |

---

## Entry into the TOP ecosystem

TOP Prompt Cleaner is the entry point for users who are not ready for full skill design.

```
User has one prompt to fix
        │
        ▼
TOP Prompt Cleaner
        │
        ├─ Single prompt → clean and return
        │
        └─ Multi-step workflow detected → escalate to TOP Skill Factory
```

It answers the question: **"Is this a prompt problem or a system design problem?"**
If it's a prompt problem, it solves it here.
If it's a system problem, it hands the user off to the right tool.

---

## Tone

- Direct, not salesy
- Specific, not vague ("here's exactly what it does" over "AI-powered prompt magic")
- Honest about scope ("it does not write prompts from scratch")
- Technical enough for developers; simple enough for non-technical users

---

## Sections order (landing page)

1. Headline + subheadline + CTA
2. Problem (3 bullet points max)
3. "What you get" table
4. "How it works" (3 steps)
5. Differentiators (4 items)
6. Use cases table
7. Ecosystem context (where it fits)
8. Second CTA
