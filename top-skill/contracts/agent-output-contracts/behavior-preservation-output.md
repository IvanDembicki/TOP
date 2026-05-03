# Behavior Preservation Output Contract

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
- preserve test-covered behavior during TOP migration

context:
- migration_scope
- legacy_code_scope
- legacy_test_scope
- source_of_test_evidence

result:
- behavior_preservation_plan
- legacy_test_inventory
- extracted_behavior_expectations
- normalized_requirements
- node_responsibility_mapping
- method_state_event_contract_mapping
- prompt_update_requirements
- test_preservation_classification
- top_test_coverage_mapping
- blocking_gaps
- acceptance_criteria

details:
- implementation_specific_assertions_discarded
- discard_justifications
- uncovered_requirements
- unresolved_ambiguities
- test_generation_or_adaptation_notes

validation_signals:
- all_legacy_behavior_tests_accounted_for
- all_behavior_expectations_normalized
- all_normalized_requirements_mapped_to_nodes
- all_mapped_requirements_reflected_in_prompts
- all_prompt_requirements_covered_by_tests
- blocking_gaps_present

next_step:
- ready_for_top_modeling
- allowed_next_stage

## Required Behavior Preservation Plan sections

The `behavior_preservation_plan` must contain:

1. Migration Scope
2. Legacy Test Inventory
3. Extracted Behavior Expectations
4. Normalized Requirements
5. Node Responsibility Mapping
6. Method / State / Event Contract Mapping
7. Prompt Update Requirements
8. Test Preservation Classification
9. TOP Test Coverage Mapping
10. Blocking Gaps
11. Acceptance Criteria

## Rules

- Legacy tests are requirements evidence.
- Test files are not the migration target; test-proven behavior is.
- A legacy test may be discarded only with a reason and with its behavioral
  meaning either declared obsolete by explicit decision or re-covered through a
  normalized TOP requirement.
- Missing coverage must be reported as a blocking gap or as a new test creation
  requirement.
- A missing behavior preservation pass for a tested migration scope is `WF-010`.
- Lost, weakened, unmapped, unprompted, or uncovered test-covered behavior is
  `CORE-028`.
- Free text outside the required structure is prohibited.

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
