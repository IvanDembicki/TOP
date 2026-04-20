# Intake Output Contract

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
- task framing

context:
- raw_input
- input_artifacts
- technology_context

result:
- task_type
- task_mode
- proposed_tier
- normalized_task

details:
- known_constraints
- missing_information

validation_signals:
- ambiguity_flag
- confidence_level
- task_mode_justification
- tier_justification

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- Intake Agent proposes `task_mode` and `proposed_tier`, but does not confirm them definitively
- `proposed_tier` and `task_mode` must have explicit justification
- Critical ambiguity must be flagged, not silently resolved
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
