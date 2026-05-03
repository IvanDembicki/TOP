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
- behavior_preservation_plan

result:
- final_status
- canonicality_statement
- core_violations
- skill_convention_violations
- workflow_gaps

details:
- remaining_risks
- behavior_preservation_gate
- unresolved_limits

validation_signals:
- review_checklist_passed
- validation_passed
- mode_pipeline_completed
- test_covered_behavior_preserved
- no_unresolved_drift

next_step:
- ready_for_use
- recommended_followup

## Rules

- Final audit cannot override failed validation
- Final audit cannot mark the result ready if unresolved drift remains between spec, prompts, project-local TOP artifacts, and materialized implementation artifacts
- Final audit cannot mark a migrated scope ready if test-covered legacy behavior lacks a Behavior Preservation Plan, prompt representation, or TOP-compatible test coverage
- For non-migration tasks, `behavior_preservation_plan`, `behavior_preservation_gate`, and `test_covered_behavior_preserved` must be explicitly `not_applicable`
- Violation types must be separated into three categories
- The final verdict must be explicit
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
