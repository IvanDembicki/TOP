# Generation Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
result:
details:
validation_signals:
next_step:
spec_sync_handoff:

## Required fields

goal:
- generate implementation from approved canonical model

context:
- approved_model_scope
- semantic_layer_source
- target_adaptation_source
- target_technology
- source_contracts
- behavior_preservation_source

result:
- generated_artifact
- explicit_contracts
- typing_decisions
- boundary_mapping
- semantic_mapping_used
- behavior_preservation_mapping_used
- top_test_coverage_mapping
- target_adaptation_decisions_applied
- implementation_source_root_used
- migration_plan_alignment
- migration_log_entry

details:
- architectural_deviations
- behavior_preservation_notes
- self_check_notes

validation_signals:
- model_fidelity_preserved
- non_canonical_deviation_present
- validation_required
- synchronized_artifacts_changed
- changed_synchronized_artifacts
- semantic_intent_preserved
- test_covered_behavior_preserved
- source_platform_leakage_present
- target_adaptation_followed

next_step:
- recommended_agent
- allowed_next_stage

spec_sync_handoff:
- created_files
- modified_files
- deleted_files
- created_synchronized_artifacts
- modified_synchronized_artifacts
- deleted_synchronized_artifacts
- affected_top_artifacts
- affected_materialized_artifacts
- discovered_materialization_details
- requires_drift_check

## Rules

- `architectural_deviations` must be empty for a valid result
- `non_canonical_deviation_present` must be `false` for a valid result
- `allowed_next_stage` must be `Spec Sync Agent` for a valid result in `generation-pipeline`
- `spec_sync_handoff` is required if any synchronized artifact was created, modified, or deleted
- Synchronized artifacts are `src/`, generated/materialized implementation artifacts, JSON specs, implementation prompts, `top/assets/`, `top/presentation/`, `top/semantic/`, and persisted `top/adaptations/` artifacts
- `requires_drift_check` must be `true` whenever synchronized artifacts changed
- `discovered_materialization_details` must list target-specific facts that need to be reflected in prompts or Expected Materialization without turning platform-specific implementation details into platform-neutral behavior
- `implementation_source_root_used` must match the approved model and Expected
  Materialization. Generated TOP implementation artifacts must be under that root
  unless they are explicitly declared thin framework adapters.
- For migration tasks, `migration_plan_alignment` must state how generated
  artifacts follow `top/migration/MIGRATION_WORKFLOW.json` and
  `top/migration/MIGRATION_PLAN.md`, and `migration_log_entry`
  must identify the appended log entry. For non-migration tasks both fields must
  be explicitly `not_applicable`.
- Generation is not permitted to override the approved architecture
- Generation is not permitted to bypass Semantic Interpreter or Target Adaptation outputs in generation-pipeline mode
- For non-migration tasks, `behavior_preservation_source`, `behavior_preservation_mapping_used`, `top_test_coverage_mapping`, and `behavior_preservation_notes` must be explicitly `not_applicable`
- `source_platform_leakage_present` must be `false` for a valid result
- `semantic_intent_preserved` and `target_adaptation_followed` must be `true` for a valid result
- `test_covered_behavior_preserved` must be `true` for a valid migration result when legacy tests covered the migrated scope
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
