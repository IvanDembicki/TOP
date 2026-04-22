# Spec Sync Output Contract

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
- resolve drift between relevant TOP artifacts and materialized implementation artifacts

context:
- sync_trigger
- input_artifact_scope
- affected_synchronized_artifacts
- affected_top_artifacts
- affected_materialized_artifacts
- approved_correction_direction

result:
- drift_status
- synchronized_artifacts
- updated_top_artifacts
- updated_materialized_artifacts
- stale_artifacts_detected
- unresolved_sync_issues

details:
- sync_actions
- topology_comparison
- prompt_comparison
- expected_materialization_comparison
- reference_resolution

validation_signals:
- sync_completed
- drift_resolved
- top_consistency_verified
- source_path_verified
- source_references_verified
- asset_references_verified
- presentation_references_verified
- validation_required

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- Spec Sync Agent is applied after Generation Agent, after Repair Agent, or after manual/migration artifact changes when synchronized artifacts changed
- All affected synchronized artifacts must be listed explicitly
- `approved_correction_direction` must state whether the sync updated `top/`, updated materialized artifacts, or escalated because the source-of-truth decision was ambiguous
- `drift_status` must be `resolved`, `unresolved`, or `not_applicable`
- `allowed_next_stage` must be `Validation Agent` only when `drift_status` is `resolved` or `not_applicable`
- If `drift_status` is `unresolved`, `allowed_next_stage` must be `Repair Agent`, `Canon Precheck Agent`, or `Ambiguity Resolver Agent`, depending on the blocker
- `sourcePath` values must be verified as extensionless `.top` artifact stems and resolved through the active target extension rule
- `props.source`, `props.assetPath`, and `props.presentationPath` references must be verified relative to `top/`
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.