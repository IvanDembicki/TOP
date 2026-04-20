# Domain Structuring Output Contract

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
- structure the domain

context:
- task_scope
- source_artifacts

result:
- domain_entities
- relationships
- boundaries

details:
- assumptions
- unresolved_points

validation_signals:
- structure_explicitness
- modeling_readiness

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- Architectural decisions are prohibited at this stage
- The structure must be expressed explicitly
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
