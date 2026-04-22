# Validation Output Contract

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
- validate artifact

context:
- artifact_scope
- evaluated_mode

result:
- overall_status
- core_violations
- skill_convention_violations
- workflow_gaps

details:
- checks_performed
- passed_checks
- failed_checks
- confirmed_violations
- possible_violations
- spec_sync_check
- drift_check
- source_path_check
- expected_materialization_check
- source_reference_check
- asset_reference_check
- presentation_reference_check
- semantic_preservation_check
- source_platform_leakage_check
- target_adaptation_coherence_check

validation_signals:
- blocking_failures
- non_blocking_issues
- unresolved_drift
- semantic_intent_preserved
- source_platform_leakage_present
- target_adaptation_coherent

next_step:
- required_actions
- allowed_next_stage

## Rules

- Validation must remain a strict pass/fail check
- `core_violations`, `skill_convention_violations`, and `workflow_gaps` must be separated
- `spec_sync_check` must explicitly report `pass`, `fail`, or `not_applicable`
- `drift_check` must explicitly report `pass`, `fail`, or `not_applicable`; when applicable it must cover JSON topology, prompts, Expected Materialization, project-local TOP artifacts, and materialized implementation artifacts
- Topology validation must mention child materialization points, dynamic/library children, prompt paths, and prompt child-interaction rules when applicable
- `source_path_check` must verify extensionless `.top` artifact stems and target-specific artifact resolution
- `source_reference_check`, `asset_reference_check`, and `presentation_reference_check` must verify `props.source`, `props.assetPath`, and `props.presentationPath` references relative to `top/` when applicable
- If `unresolved_drift` is true, `overall_status` must be `fail` and `allowed_next_stage` must not be `Final Audit Agent`
- If `source_platform_leakage_present` is true in Layer B or in a non-source target, `overall_status` must be `fail`
- In `generation-pipeline`, validation must check semantic preservation, absence of source-platform leakage, target adaptation coherence, and TOP invariants
- Commentary cannot substitute for validation
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
