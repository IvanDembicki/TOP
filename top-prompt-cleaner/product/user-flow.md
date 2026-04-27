# User Flow

## Entry points

| Where user starts | What they bring |
|---|---|
| Direct use via Claude/ChatGPT | A prompt they already have and want improved |
| Referred from TOP Skill Factory | A single-prompt question, not a skill design task |
| Team prompt library review | A batch of prompts to audit and clean |

---

## Happy path (QuickClean)

```
User pastes a prompt
        │
        ▼
TOP Prompt Cleaner receives it
        │
        ├─ SensitiveDataDetector → clean? ──NO──▶ Blocked: sensitive data notice
        │
        ├─ ComplexityDetector → high? ──YES──▶ Escalated: refer to TOP Skill Factory
        │
        ├─ StructureExtractor → goal found? ──YES──▶ continue
        │
        ├─ ConflictDetector → blocking conflict? ──YES──▶ Blocked: show conflict + options
        │
        ├─ QuickCleanMode: remove noise, resolve warning conflicts, rebuild structure
        │
        ├─ ValidationController: all rules pass?
        │
        └─ ready output: cleaned_prompt + structured_prompt + diff
```

---

## Strict path (StrictClean)

Same as above, but:
- goal or output_format missing → ClarificationController blocks and asks
- user answers (or selects option U) → pipeline resumes with resolved fields
- blocking conflicts are never auto-resolved — always blocked

---

## Style adaptation path (TargetLLMStyle)

```
User pastes a prompt + declares target_style: claude | gpt
        │
        ▼
Sensitive check → complexity check → structure extraction
        │
        ▼
TargetLLMStyleMode:
  - load model profile (claude / gpt / generic)
  - apply anti-pattern fixes
  - restructure for target model conventions
        │
        ▼
ready output:
  - single_prompt  (Claude, generic)
  - message_bundle (GPT system + user)
  - xml_prompt     (Claude with context/task blocks)
```

---

## Escalation path

```
Complexity: high → no cleaning happens
        │
        ▼
Escalation notice:
  - signals that triggered escalation
  - recommended next step: TOP Skill Factory → CreateNewSkillMode
```

---

## Clarification round-trip

```
Round 1: submit prompt
        │
        ▼
ClarificationController detects missing goal or output_format
        │
        ▼
Blocked: clarification question + options (A / B / C / U)
        │
        ▼
User selects option or types free text (U)
        │
        ▼
Round 2: pipeline resumes with resolved fields
        │
        ▼
Normal QuickClean or StrictClean path continues
```

---

## What the user sees at each terminal state

| Status | User sees |
|---|---|
| `ready` | Cleaned prompt + structured breakdown + diff of changes |
| `blocked` (conflict) | The specific conflict, its severity, and resolution options |
| `blocked` (missing field) | A clarification question with suggested answers including free text |
| `blocked` (sensitive data) | What was found, why it blocks, and what to do before resubmitting |
| `escalated` | Why it escalated and a direct referral to TOP Skill Factory |

---

## What the user does NOT need to know

- Which internal node ran
- What the schema looks like
- What "structured_prompt" means internally

The output should feel like: **paste prompt → get better prompt + explanation of what changed.**
