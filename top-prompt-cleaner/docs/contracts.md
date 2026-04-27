# Contract Reference — TOP Prompt Cleaner

© 2026 Ivans Dembickis · MIT License

All schemas live in `top/schemas/`. Each is a JSON Schema 2020-12 document with a `$id` matching its filename. The validator compiles all schemas and registers them so `$ref` resolution works across files.

---

## Pipeline node contracts (in execution order)

### 1. `normalized_input.schema.json`

**Produced by:** InputController  
**Purpose:** Raw prompt preserved verbatim, plus any mode/target hints extracted at ingestion.

| Field | Type | Required | Notes |
|---|---|---|---|
| `original_prompt` | string | yes | Exact user input — never modified |
| `normalized` | boolean | yes | True once ingested |
| `mode_hint` | enum | no | Explicit mode override from user |
| `target_style` | enum | no | Explicit target style from user |
| `open_questions` | string[] | no | Ambiguities forwarded to ClarificationController |

---

### 2. `sensitive_data_report.schema.json`

**Produced by:** SensitiveDataDetector  
**Purpose:** Reports any secrets or PII found before transformation begins.

| Field | Type | Required | Notes |
|---|---|---|---|
| `sensitive_findings` | object[] | yes | Empty array when nothing detected |
| `sensitive_blocking` | boolean | yes | True when any finding is `blocking` severity |

Each finding: `type`, `excerpt` (max 40 chars), `severity` (`blocking`/`warning`), `recommendation`.

---

### 3. `complexity_report.schema.json`

**Produced by:** ComplexityDetector  
**Purpose:** Classifies prompt complexity to decide whether to proceed or escalate.

| Field | Type | Required | Notes |
|---|---|---|---|
| `complexity_level` | enum | yes | `low`, `medium`, `high` |
| `signals` | string[] | yes | Named patterns; required non-empty for `high` |
| `recommendation` | enum | yes | `proceed`, `proceed_with_warning`, `escalate` |

`high` always maps to `escalate`. `medium` always maps to `proceed_with_warning`. `low` always maps to `proceed`.

---

### 4. `mode_routing_result.schema.json`

**Produced by:** ModeRouter  
**Purpose:** Records which mode was selected and why. Exactly one mode per run.

| Field | Type | Required | Notes |
|---|---|---|---|
| `selected_mode` | enum | yes | `quick_clean`, `strict_clean`, `target_llm_style` |
| `target_style_source` | enum | when mode is `target_llm_style` | `stated`, `detected`, `default` |
| `routing_reason` | string | yes | References the specific signal or user input |

---

### 5. `extraction_result.schema.json`

**Produced by:** StructureExtractor  
**Purpose:** Intermediate output — raw extraction before conflict detection. Allows empty goal/output_format.

| Field | Type | Required | Notes |
|---|---|---|---|
| `goal` | string | yes | Empty string when `goal_source` is `missing` |
| `goal_source` | enum | yes | `stated`, `inferred`, `missing` |
| `constraints` | string[] | yes | Empty array when none present |
| `output_format` | string | yes | Empty string when `output_format_source` is `missing` |
| `output_format_source` | enum | yes | `stated`, `inferred`, `missing` |
| `noise_candidates` | string[] | no | Passed to OutputBuilder for removal decision |

> Not the same as `structured_prompt`. Final cleaned artifacts use `structured_prompt.json`.

---

### 6. `conflict_report.schema.json`

**Produced by:** ConflictDetector  
**Purpose:** Reports tensions or contradictions in the extracted constraints.

| Field | Type | Required | Notes |
|---|---|---|---|
| `conflicts` | object[] | yes | Empty array when no conflicts found |
| `has_blocking_conflicts` | boolean | yes | True when any conflict is `blocking` severity |

Each conflict: `description`, `severity` (`warning`/`blocking`), `resolution_recommendation`.

---

### 7. `clarification_state.schema.json`

**Produced by:** ClarificationController  
**Purpose:** Records whether clarification is needed and carries the request.

| Field | Type | Required | Notes |
|---|---|---|---|
| `clarification_needed` | boolean | yes | Mutually exclusive with `proceed_with_inference` |
| `proceed_with_inference` | boolean | yes | QuickClean only |
| `clarification_request` | object | when `clarification_needed: true` | See below |

---

### 8. `clarification_request.schema.json`

**Produced by:** ClarificationController (as nested field in `clarification_state`)  
**Purpose:** Carries the clarification question and options to the user.

| Field | Type | Required | Notes |
|---|---|---|---|
| `question` | string | yes | |
| `reason` | string | yes | Why this field is needed |
| `missing_field` | enum | yes | `goal`, `output_format`, `target_style`, `constraints` |
| `blocking_if_unanswered` | boolean | yes | |
| `options` | object[] | no | `[{id, label}]`; last option must be `{id: "U", label: "User-defined answer"}` |
| `user_response` | object | no | Populated when user has responded |

---

### 9. `user_response.schema.json`

**Produced by:** user (in response to clarification)  
**Purpose:** User's answer to a clarification question.

| Field | Type | Required | Notes |
|---|---|---|---|
| `selected_option` | string | yes | id of the chosen option |
| `text` | string | when `selected_option` is `U` | Free-text answer |

---

### 10. `structured_prompt.json`

**Produced by:** OutputBuilder (final cleaned artifact)  
**Purpose:** The clean, structured representation of the prompt. Used in `final_output`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `goal` | string | yes | Non-empty; extracted from original |
| `goal_source` | enum | yes | `stated`, `inferred`, `missing` |
| `constraints` | string[] | yes | |
| `output_format` | string | yes | Non-empty |
| `output_format_source` | enum | yes | `stated`, `inferred`, `missing` |
| `style` | enum | no | `default`, `claude`, `gpt`, `custom` |

> Distinct from `extraction_result`: `structured_prompt` requires non-empty `goal` and `output_format`.

---

### 11. `diff.schema.json`

**Produced by:** OutputBuilder  
**Purpose:** Documents every change made from raw input to cleaned output.

| Field | Type | Required | Notes |
|---|---|---|---|
| `removed_noise` | string[] | yes | |
| `rewritten_phrases` | object[] | yes | Each: `{original, rewritten, reason}` |
| `resolved_conflicts` | object[] | yes | Each: `{conflict, resolution}` |
| `unresolved_conflicts` | object[] | yes | Each: `{conflict, recommendation}` |
| `preserved_constraints` | string[] | yes | |
| `warnings` | string[] | yes | |

All six arrays are required, even if empty.

---

### 12. `validation_result.schema.json`

**Produced by:** ValidationController  
**Purpose:** Records pass/fail for each validation rule.

| Field | Type | Required | Notes |
|---|---|---|---|
| `results` | object[] | yes | One entry per rule: `{rule, pass, detail?}` |
| `all_pass` | boolean | yes | False if any result has `pass: false` |
| `blocking_failures` | string[] | when `all_pass: false` | Rule ids that failed |

---

### 13. `final_decision_signal.schema.json`

**Produced by:** FinalDecisionController (node trace record)  
**Purpose:** Lightweight status signal recorded in the trace. Not the user-facing output.

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | enum | yes | `ready`, `blocked`, `escalated` |
| `diagnosis` | string | when `status: blocked` | Names the violated rule or missing field |

> Distinct from `final_output`: this is a trace record. The full user-facing output conforms to `final_output.schema.json`.

---

### 14. `target_style_output.schema.json`

**Produced by:** TargetLLMStyleMode  
**Purpose:** The adapted prompt in the target model's structural form.

| Field | Type | Required | Notes |
|---|---|---|---|
| `output_type` | enum | yes | `single_prompt`, `message_bundle`, `xml_prompt` |
| `target_style` | enum | yes | `claude`, `gpt`, `default`, `custom` |
| `target_style_source` | enum | yes | `stated`, `detected`, `default` |
| `profile_used` | enum | yes | `claude`, `gpt`, `generic`, `custom` |
| `content` | object | yes (per output_type) | `prompt` or `system_message + user_message` |

---

### 15. `final_output.schema.json`

**Produced by:** OutputBuilder (user-facing result)  
**Purpose:** The complete terminal artifact delivered to the user. Status-gated by `allOf/if/then`.

| Status | Required fields | Forbidden fields |
|---|---|---|
| `ready` | `structured_prompt`, `diff`, exactly one of `cleaned_prompt` / `target_style_output` | `escalation_notice`, `clarification_request` |
| `blocked` | `diagnosis` | `cleaned_prompt`, `target_style_output`, `escalation_notice` |
| `escalated` | `escalation_notice` | `cleaned_prompt`, `target_style_output`, `structured_prompt`, `diff`, `clarification_request` |

---

## Schema dependency graph

```
final_output
├── structured_prompt
├── diff
├── target_style_output
└── clarification_request
      └── user_response (nested)

clarification_state
└── clarification_request
      └── user_response (nested)
```

All other schemas are standalone (no `$ref`).
