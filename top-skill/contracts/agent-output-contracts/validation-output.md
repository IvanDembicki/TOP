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
- execution_evidence
- validation_context_independence_check
- validation_evidence
- judicial_handoff_artifact_check
- required_hard_checks
- protocol_only_mode_check
- runner_enforcement_claim_check
- checks_performed
- passed_checks
- failed_checks
- confirmed_violations
- possible_violations
- artifacts_reviewed
- files_inspected
- canon_rules_checked
- detection_patterns_used
- generator_self_validation_claim_check
- rejection_tickets
- generator_learning_ledger_update_required
- incremental_validation_check
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
- concrete_content_privacy_check
- controller_fragment_output_check
- content_owned_setter_bridge_check
- controller_runtime_shape_check
- controller_tree_topology_check
- top_spec_shape_check
- generated_layout_topology_check
- independent_checkpoint_check
- dedicated_migration_branch_check
- separation_of_powers_check
- delivery_report_gate_check
- content_child_import_check
- prompt_code_contract_drift_check
- node_global_store_access_check
- bridge_callback_injection_check
- self_audited_pass_report_check
- semantic_preservation_check
- behavior_preservation_check
- source_platform_leakage_check
- target_adaptation_coherence_check

validation_signals:
- execution_isolation_level
- verification_evidence_level
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
- `execution_evidence` must include `executionIsolationLevel`,
  `verificationEvidenceLevel`, `runnerName`, `separateInvocationIds`,
  `schemaValidationCommand`, `hardCheckCommands`, and `limitations`.
- `executionIsolationLevel` and `verificationEvidenceLevel` are independent
  axes. Schema validation is not role isolation; hard checks are not role
  isolation.
- In protocol-only mode, validation may report
  `executionIsolationLevel: protocol-followed-by-agent`, but must not report
  `runner-enforced`.
- `runner_enforcement_claim_check` must fail when a workflow claims
  `runner-enforced` without external runner name, separate invocation ids,
  separate contexts, and explicit handoff artifact references.
- `required_hard_checks` must list every required executable check with `id`,
  `description`, `requiredForComplete`, `status`, `command`, and `evidence`.
- Required hard-check status `fail` or `not_verified` blocks delivery complete.
- A hard check result without a judicial handoff is evidence, but not a judicial
  verdict.
- A judicial handoff without required hard-check evidence cannot certify
  delivery complete.
- Validation must be independent and adversarial. Previous generator, repair,
  modeling, migration, or implementation reports are claims to inspect, not
  proof. Treating them as proof is `WF-024`; relying on prior chat context or
  memory is `WF-021`.
- `validation_evidence` must list artifacts reviewed, files inspected, checks
  performed, canon rules checked, search/detection patterns used, artifact
  types reviewed, per-check violation/no-violation evidence, ambiguities, and
  unresolved limits. A PASS without this evidence is `WF-025`.
- `generator_self_validation_claim_check` must report whether executor output
  claimed its own validation verdict. Claims such as `TOP-clean`, `CORE-015
  clean`, `canon compliant`, `validation passed`, `no violations`,
  `ready_for_manual_QA`, `ready_for_use`, or `final_status: pass` from the
  executor are `WF-023`.
- If validation fails, the validator must create a structured rejection ticket
  and append a rejection entry to `top/migration/MIGRATION_LOG.md`. Missing
  rejection traceability is `WF-027`.
- A rejection ticket must include `rejection_id`, `validator_agent`, `phase`,
  `attempt_number`, `artifact_under_review`, `files_checked`,
  `canon_rules_checked`, `violation_code`, `violation_summary`, `evidence`,
  `why_invalid`, `required_repair`, `forbidden_repairs`, and
  `return_to_agent`.
- `generator_learning_ledger_update_required` must identify whether
  `top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md` must be updated.
  Missing read/update is `WF-028`; repeated rejected strategy is `WF-029`.
- Retry limits are `max_repair_attempts_per_validation_gate: 3` and
  `max_same_violation_repeats: 2`; exceeding them is `WF-030`.
- `incremental_validation_check` must report whether the smallest meaningful
  artifacts were validated as they appeared, using micro-check, meso-check, and
  macro-check gates from `canon/validation-rejection-protocol.md`.
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
- Validation must report `CORE-033` when concrete locally implemented content
  is imported, instantiated, typed against, downcast to, inspected, stored, or
  called outside its owning controller, or when the owning controller stores it
  as concrete content instead of `IContentAccess`
- Validation must report `CORE-034` when controller APIs return platform/content
  fragments, render/build trees, style/layout fragments, JSX/widget/composable
  fragments, animation objects, content-owned setters, or mutation handles
- Validation must report `CORE-035` when content-owned setter/mutation handles
  cross the content boundary through controller fields, APIs, access contracts,
  adapters, helpers, or callbacks
- Validation must report `CORE-036` when a public TOP node/controller artifact
  is a target-framework wrapper around concrete content, or when
  external/parent/adapter code can name the wrapper to reach concrete content
- Validation must report `CORE-037` when a TOP controller artifact does not
  participate in the runtime controller tree: missing runtime node
  base/interface, missing parent/context or root context, missing lifecycle,
  missing child ownership/registration, missing declared child policy or
  explicit leaf status, declared children not constructed as child controllers,
  or controller-shaped service/helper/module with no spec tree position.
- Validation must report `CONV-007` when a new migration branch spec is stored
  as an ad hoc root-level file in `top/` instead of under `top/specs/` without an
  established project convention
- Validation must report `CONV-008` when implementation prompts or Expected
  Materialization exist but no implementation source root is declared/prepared
- Validation must report `CONV-009` when project TOP specs use ad hoc
  `id`/`name` pseudo-spec node shape instead of canonical `type` or an approved
  equivalent
- Validation must report `CONV-010` when generated implementation layout does
  not mirror the approved TOP tree through source root, effective `props.dir`,
  and prompt layout
- Validation must report `WF-013` when a migration/modeling handoff plans or
  claims future materialization without a canonical materialization plan, source
  root, and honest phase status
- Validation must report `WF-014` when a migration-mode task creates or changes
  TOP artifacts without a current `top/migration/<branch-id>/MIGRATION_PLAN.md`
- Validation must report `WF-015` when a migration-mode handoff or artifact
  change lacks an appended `top/migration/MIGRATION_LOG.md` entry
- Validation must report `WF-016` when a migration-mode task creates or changes
  TOP artifacts without current `top/migration/<branch-id>/MIGRATION_WORKFLOW.json`, or when
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
  active branch workspace without an explicitly allowed thin adapter/integration
  reason recorded in the migration log, overwrite another branch workspace,
  rewrite shared `MIGRATION_LOG.md`, or update shared `MIGRATION_STATUS.md`
  without preserving previous branch history.
- Validation must report `WF-020` when required branch checkpoints are missing
  or stale before handoff.
- Validation must report `WF-021` when validation relies on generator/repair
  memory, prior chat context, or previous reads instead of independent
  current-pass evidence.
- Validation must report `WF-022` when migration writes were performed before
  creating or switching to a dedicated migration branch, when branch safety was
  not logged, when the branch does not match the migration branch id, when
  unrelated work was mixed into migration output, when push occurred without
  explicit user request, or when local commits were not requested or
  phase-documented.
- Validation must report `WF-023` through `WF-030` for generator
  self-validation claims, contaminated validation context, validation without
  artifact evidence, final audit accepting unproven validation, missing
  rejection log entry, missing generator learning ledger update, repeated
  rejected strategy, and exceeded repair circuit breaker.
- `migration_decomposition_check`, `giant_node_review_check`,
  `panel_display_style_check`, `post_generation_source_validation_check`,
  `accepted_deviation_discipline_check`, and
  `migration_workspace_write_check` must explicitly report `pass`, `fail`, or
  `not_applicable`.
- `concrete_content_privacy_check`, `controller_fragment_output_check`,
  `content_owned_setter_bridge_check`, `controller_runtime_shape_check`,
  `controller_tree_topology_check`, `top_spec_shape_check`,
  `generated_layout_topology_check`, and `independent_checkpoint_check` must
  explicitly report `pass`, `fail`, or `not_applicable`.
- `dedicated_migration_branch_check` must explicitly report `pass`, `fail`, or
  `not_applicable`.
- `separation_of_powers_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; it fails when generation/repair and validation/final audit
  are performed by the same pass for the same artifact set.
- `delivery_report_gate_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; it fails when a report says `complete` without
  runner-enforced execution isolation, hard-check-verified validation evidence,
  independent judicial validation evidence, a valid independent judicial
  handoff artifact, required checked files, commands/searches run, violation
  classes checked, failures, and unverified areas.
- `content_child_import_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; it fails when parent locally implemented content imports,
  instantiates, renders, or types against child concrete content classes instead
  of requesting child materialized outputs through controller access.
- `prompt_code_contract_drift_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; it fails when prompts/specs require one controller/content
  contract shape but implementation materializes a different architectural
  contract without an approved prompt/spec update.
- `node_global_store_access_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; it fails when Node/controller files directly import or call
  React hooks, Zustand/global stores, route/navigation hooks, UI framework
  hooks, runtime singleton state, or target hook APIs instead of explicit
  bridge/runtime/data boundaries.
- `bridge_callback_injection_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; raw callbacks entering TOP objects must be wrapped in an
  explicit bridge/runtime/context boundary unless validation proves the callback
  is target-local and non-semantic.
- `self_audited_pass_report_check` must explicitly report `pass`, `fail`, or
  `not_applicable`; delivery fails when the same pass generated/repaired the
  artifacts, wrote validation/final audit, and declared completion without an
  independent judicial pass.
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
- `controller_runtime_shape_check` must include the
  `generated-controller-runtime-shape` micro-check for generated controller
  files.
- `controller_tree_topology_check` must include the `controller-tree-topology`
  meso-check for generated subtrees.
- After repair, validation restarts from the nearest complete validation gate
  affected by the repair.
- If `test_covered_behavior_preserved` is false, `overall_status` must be `fail`
- Commentary cannot substitute for validation
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
