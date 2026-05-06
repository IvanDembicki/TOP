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
- accepted_deviations
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
- top_layout_check
- implementation_source_root_check
- migration_workflow_check
- migration_plan_check
- migration_log_check
- migration_decomposition_check
- giant_node_review_check
- panel_display_style_check
- post_generation_source_validation_check
- accepted_deviation_discipline_check
- migration_workspace_write_check
- semantic_preservation_check
- behavior_preservation_check
- source_platform_leakage_check
- target_adaptation_coherence_check

validation_signals:
- blocking_failures
- non_blocking_issues
- unresolved_drift
- semantic_intent_preserved
- test_covered_behavior_preserved
- source_platform_leakage_present
- target_adaptation_coherent

next_step:
- required_actions
- allowed_next_stage

## Rules

- Validation must remain a strict pass/fail check
- `core_violations`, `skill_convention_violations`, and `workflow_gaps` must be separated
- `accepted_deviations` may document only TOP-canon-defined migration
  waypoints, and must not remove the corresponding violation from
  `core_violations`
- Labeling a core violation as accepted/temporary/deferred/waypoint without a
  TOP-canon-defined waypoint for that violation is `WF-012`
- If `core_violations` is non-empty, `overall_status` must be `fail` and
  `allowed_next_stage` must not be `Final Audit Agent`
- If `accepted_deviations` contains any core violation, `overall_status` must be
  `fail` and `allowed_next_stage` must not be `Final Audit Agent`
- Reporting `pass` with remaining core violations or accepted core deviations is
  `WF-011`
- Validation must report `CORE-030` when Content receives decomposed
  `IControllerAccess` members as separate props/parameters, method bags,
  facade/adapters, or inline object literals instead of the owning controller
  typed through the narrow interface
- Validation must report `CORE-031` when Controller receives, stores, or uses
  decomposed content lifecycle/materialization members, method bags,
  facade/adapters, concrete Content types, platform primitives, or inline
  objects instead of its own Content instance typed through `IContentAccess`
- Validation must report `CONV-007` when a new migration branch spec is stored
  as an ad hoc root-level file in `top/` instead of under `top/specs/` without an
  established project convention
- Validation must report `CONV-008` when implementation prompts or Expected
  Materialization exist but no implementation source root is declared/prepared
- Validation must report `WF-013` when a migration/modeling handoff plans or
  claims future materialization without a canonical materialization plan, source
  root, and honest phase status
- Validation must report `WF-014` when a migration-mode task creates or changes
  TOP artifacts without a current `top/migration/MIGRATION_PLAN.md`
- Validation must report `WF-015` when a migration-mode handoff or artifact
  change lacks an appended `top/migration/MIGRATION_LOG.md` entry
- Validation must report `WF-016` when a migration-mode task creates or changes
  TOP artifacts without current `top/migration/MIGRATION_WORKFLOW.json`, or when
  the workflow JSON disagrees with plan/status/log
- Validation must report `WF-017` when migration modeling treats a user-named
  scope as a final node boundary, keeps a single-node/giant-node wrapper without
  recursive decomposition proof, omits reusable-pattern/modal/form/list
  classification, or uses display-token clusters as a substitute for
  decomposition.
- Validation must report `WF-018` when an accepted deviation lacks exact
  locations, temporary acceptance rationale, target repair direction, expiry
  condition, and owner phase.
- Validation must report `WF-019` when migration agents modify files outside the
  active migration workspace without an explicitly allowed thin
  adapter/integration reason recorded in the migration log.
- `migration_decomposition_check`, `giant_node_review_check`,
  `panel_display_style_check`, `post_generation_source_validation_check`,
  `accepted_deviation_discipline_check`, and
  `migration_workspace_write_check` must explicitly report `pass`, `fail`, or
  `not_applicable`.
- `spec_sync_check` must explicitly report `pass`, `fail`, or `not_applicable`
- `drift_check` must explicitly report `pass`, `fail`, or `not_applicable`; when applicable it must cover JSON topology, prompts, Expected Materialization, project-local TOP artifacts, and materialized implementation artifacts
- `top_layout_check` must explicitly report `pass`, `fail`, or `not_applicable`
  and verify `top/specs/`, `top/prompts/`, and `top/migration/` placement when
  project-local TOP artifacts exist
- `implementation_source_root_check` must explicitly report `pass`, `fail`, or
  `not_applicable` and verify that materialized/generated TOP artifacts and
  Expected Materialization roots agree
- `migration_workflow_check` must explicitly report `pass`, `fail`, or
  `not_applicable`
- `migration_plan_check` must explicitly report `pass`, `fail`, or
  `not_applicable`
- `migration_log_check` must explicitly report `pass`, `fail`, or
  `not_applicable`
- Topology validation must mention child materialization points, dynamic/library children, prompt paths, and prompt child-interaction rules when applicable
- `source_path_check` must verify extensionless `.top` artifact stems and target-specific artifact resolution
- `source_reference_check`, `asset_reference_check`, and `presentation_reference_check` must verify `props.source`, `props.assetPath`, and `props.presentationPath` references relative to `top/` when applicable
- `behavior_preservation_check` must explicitly report `pass`, `fail`, or `not_applicable`
- If `unresolved_drift` is true, `overall_status` must be `fail` and `allowed_next_stage` must not be `Final Audit Agent`
- If `source_platform_leakage_present` is true in Layer B or in a non-source target, `overall_status` must be `fail`
- In `generation-pipeline`, validation must check semantic preservation, absence of source-platform leakage, target adaptation coherence, and TOP invariants
- In migration scopes with legacy tests, validation must check Behavior Preservation Plan existence, prompt representation, and TOP-compatible test coverage
- After generation, validation must inspect actual generated/materialized source
  files, including controller files, locally implemented content files,
  contracts, bridge components, helper components, modal files, adapters, and
  generated constants/helpers. Type-check success is not TOP validation.
- If `test_covered_behavior_preserved` is false, `overall_status` must be `fail`
- Commentary cannot substitute for validation
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
