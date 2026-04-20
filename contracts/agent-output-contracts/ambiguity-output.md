# Ambiguity Resolver Output Contract

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
- clarify ambiguities

context:
- input_scope
- relevant_artifacts

result:
- identified_ambiguities
- resolved_ambiguities
- unresolved_ambiguities

details:
- safe_assumptions
- unsafe_assumptions

validation_signals:
- blocking_ambiguity
- impact_on_pipeline

next_step:
- allowed_next_agents
- allowed_next_stage

## Rules

- Critical ambiguity must not be silently resolved
- Resolved and unresolved items must be explicitly separated
- Unsafe assumptions must be marked as unsafe
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
