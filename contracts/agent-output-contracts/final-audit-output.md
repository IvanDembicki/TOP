# Final Audit Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
result:
details:
validation_signals:
next_step:

## Required fields

goal:
- final decision

context:
- artifact_scope
- task_mode

result:
- final_status
- canonicality_statement
- core_violations
- skill_convention_violations
- workflow_gaps

details:
- remaining_risks
- unresolved_limits

validation_signals:
- review_checklist_passed
- validation_passed
- mode_pipeline_completed
- no_unresolved_drift

next_step:
- ready_for_use
- recommended_followup

## Rules

- Final audit cannot override failed validation
- Final audit cannot mark the result ready if unresolved drift remains between spec, prompts, project-local TOP artifacts, and materialized implementation artifacts
- Violation types must be separated into three categories
- The final verdict must be explicit
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
