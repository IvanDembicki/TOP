# TOP Modeling Output Contract

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
- define canonical structure

context:
- domain_scope
- task_mode

result:
- nodes
- relationships
- controller_content_mapping
- protocol_boundaries
- lifecycle_model
- ownership_map

details:
- type_definitions
- typing_strength
- structural_assumptions

validation_signals:
- canonical_compliance
- structural_risks

next_step:
- ready_for_precheck
- allowed_next_stage

## Rules

- Output must follow canon strictly
- Generation artifacts are prohibited at this stage
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
