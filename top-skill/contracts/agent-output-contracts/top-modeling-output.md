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
- behavior_preservation_plan

result:
- nodes
- relationships
- controller_content_mapping
- protocol_boundaries
- lifecycle_model
- ownership_map
- behavior_requirement_mapping
- decomposition_evidence
- reusable_pattern_candidates
- helper_component_classification
- canonical_artifact_layout
- migration_plan_alignment
- migration_log_entry

details:
- type_definitions
- typing_strength
- structural_assumptions
- single_node_proof
- giant_node_review
- panel_display_style_justification
- bridge_residual_register
- accepted_deviation_register
- prompt_update_requirements_from_behavior
- implementation_source_root
- expected_materialization_roots

validation_signals:
- canonical_compliance
- structural_risks

next_step:
- ready_for_precheck
- allowed_next_stage

## Rules

- Output must follow canon strictly
- For non-migration tasks, `behavior_preservation_plan`, `behavior_requirement_mapping`, and `prompt_update_requirements_from_behavior` must be explicitly `not_applicable`
- Generation artifacts are prohibited at this stage
- If implementation prompts or Expected Materialization are produced, the output
  must name the canonical branch spec path under `top/specs/`, prompt root under
  `top/prompts/`, migration status path when applicable, and implementation
  source root (`top_src/<branch-id>/` by default)
- If no implementation materialization is planned, `implementation_source_root`
  and `expected_materialization_roots` must be explicitly `not_applicable`
- For migration tasks, `decomposition_evidence` must distinguish migration scope
  root from final node boundaries and must classify hidden objects, state
  alternatives, data boundaries, async workflows, forms, modals, lists/list
  items, bridge boundaries, and repeated structures.
- `single_node_proof` is required when the model keeps a user-named scope as one
  node; otherwise it must be `not_applicable`.
- `giant_node_review`, `panel_display_style_justification`,
  `bridge_residual_register`, and `accepted_deviation_register` must be
  explicit for migration tasks, even when empty.
- For migration tasks, `migration_plan_alignment` must state how the model
  follows `top/migration/<branch-id>/MIGRATION_WORKFLOW.json` and
  `top/migration/<branch-id>/MIGRATION_PLAN.md`, and `migration_log_entry` must
  identify the appended log entry. For non-migration tasks both fields must be
  explicitly `not_applicable`.
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
