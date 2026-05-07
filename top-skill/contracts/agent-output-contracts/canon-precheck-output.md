# Canon Precheck Output Contract

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
- evaluate canonical readiness before generation or approved modeling transition

context:
- model_scope
- source_artifacts
- relevant_canon_sections
- proposed_tier

result:
- canonical_elements
- violations
- ambiguities
- precheck_status
- effective_tier

details:
- precheck_context_independence_check
- artifacts_inspected
- required_repairs
- block_reason
- tier_mismatch_reason

validation_signals:
- generation_allowed
- blocking_violations_present
- unresolved_ambiguity_present
- tier_verified

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- `precheck_status` must be one of: passed | failed | blocked
- `block_reason` is required when `failed` or `blocked`
- `effective_tier` is required
- Intake proposes `proposed_tier`, Canon Precheck confirms `effective_tier`
- Canon Precheck is judicial. It must inspect current model artifacts against
  canon and must not accept modeler self-validation claims as evidence.
- `artifacts_inspected` must list the actual specs/prompts/models reviewed.
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
