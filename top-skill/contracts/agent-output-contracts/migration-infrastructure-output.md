# Migration Infrastructure Output Contract

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
- prepare migration infrastructure

context:
- project_path
- task_mode
- version_control_state
- existing_top_layout

result:
- baseline_status
- created_directories
- created_files
- modified_files
- migration_plan_path
- migration_workflow_path
- migration_status_path
- migration_log_path
- source_root_status

details:
- top_layout_check
- source_root_check
- migration_control_plane_check
- migration_workflow_check
- active_migration_workspace
- log_entry_written

validation_signals:
- infrastructure_ready
- blocking_risks
- user_decision_required

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- `migration_plan_path` must be `top/migration/MIGRATION_PLAN.md`
- `migration_workflow_path` must be `top/migration/MIGRATION_WORKFLOW.json`
- `migration_status_path` must be `top/migration/MIGRATION_STATUS.md`
- `migration_log_path` must be `top/migration/MIGRATION_LOG.md`
- `migration_workflow_check` must confirm valid JSON and the initial phase tree.
- If implementation materialization is planned, `source_root_status` must name
  the declared source root and whether it exists.
- `active_migration_workspace` must name the branch-owned paths where agents may
  write without per-file confirmation, and must state that legacy app files
  remain user-owned except explicitly logged thin adapter/integration changes.
- `log_entry_written` must be `true` for a valid handoff.
- Free text outside the required structure is prohibited.
