# Migration Plan Output Contract

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
- create explicit migration plan

context:
- project_path
- task_mode
- user_requested_scope
- infrastructure_source

result:
- migration_plan_path
- migration_workflow_path
- selected_scope
- branch_id
- planned_artifacts
- workflow_phase_updates
- agent_work_packages
- decomposition_work_packages
- validation_gates
- incremental_validation_gates
- rollback_points
- migration_log_entry

details:
- scope_selection_rationale
- scope_root_vs_node_boundary_policy
- dependency_scan_plan
- behavior_evidence_scan_plan
- materialization_plan
- unresolved_questions

validation_signals:
- plan_ready
- behavior_preservation_required
- materialization_ready
- blocking_risks

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- `migration_plan_path` must be `top/migration/<branch-id>/MIGRATION_PLAN.md`
- `migration_workflow_path` must be `top/migration/<branch-id>/MIGRATION_WORKFLOW.json`
- Shared `top/migration/MIGRATION_LOG.md` is append-only, and shared
  `top/migration/MIGRATION_STATUS.md` updates must preserve previous branch
  history.
- `agent_work_packages` must list the migration stages and responsible agents.
- `incremental_validation_gates` must list planned micro-check, meso-check, and
  macro-check gates for the smallest meaningful artifacts and phase groups.
- `workflow_phase_updates` must list the phase ids, statuses, gates, outputs,
  and next phases written to the workflow JSON.
- `planned_artifacts` must include spec, prompt, status, log, and source-root
  paths when materialization is planned.
- `decomposition_work_packages` must include hidden architecture discovery,
  recursive decomposition, giant-node review, reusable pattern extraction,
  modal/form/list candidate analysis, hook bridge residual classification,
  accepted deviation discipline, and post-generation source validation gates.
- `scope_root_vs_node_boundary_policy` must state that a user-named screen,
  route, tab, section, component, or file is the migration scope root, not proof
  of a single TOP node.
- `migration_log_entry` must identify the log entry appended for this planning pass.
- Free text outside the required structure is prohibited.
