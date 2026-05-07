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
- initial_branch
- migration_branch
- branch_created
- branch_checked_out
- created_directories
- created_files
- modified_files
- migration_plan_path
- migration_workflow_path
- migration_status_path
- migration_log_path
- source_root_status

details:
- git_safety_gate
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

- `migration_plan_path` must be `top/migration/<branch-id>/MIGRATION_PLAN.md`
- `migration_workflow_path` must be `top/migration/<branch-id>/MIGRATION_WORKFLOW.json`
- `migration_status_path` must be `top/migration/MIGRATION_STATUS.md`
- `migration_log_path` must be `top/migration/MIGRATION_LOG.md`
- `migration_branch` must normally be `top-migration/<branch-id>` unless a
  deterministic project equivalent is documented.
- `branch_checked_out` must be `true` before any migration write is valid.
- `git_safety_gate` must include current branch check, working tree status,
  uncommitted changes check, remote status when available, unrelated work
  decision, migration write permission, local commit policy, and no-push policy.
- `migration_workflow_check` must confirm valid JSON and the initial phase tree.
- If implementation materialization is planned, `source_root_status` must name
  the declared source root and whether it exists.
- `active_migration_workspace` must name the branch-owned paths where agents may
  write without per-file confirmation, including
  `top/migration/<branch-id>/MIGRATION_PLAN.md`,
  `top/migration/<branch-id>/MIGRATION_WORKFLOW.json`,
  `top/migration/<branch-id>/reports/**`, `top/specs/<branch-id>.json`,
  `top/prompts/<branch-id>/**`, and `top_src/<branch-id>/**`.
- Shared `top/migration/MIGRATION_LOG.md` is append-only, and shared
  `top/migration/MIGRATION_STATUS.md` updates must preserve previous branch
  history.
- The contract must state that legacy app files remain user-owned except
  explicitly logged thin adapter/integration changes.
- `log_entry_written` must be `true` for a valid handoff.
- The first log entry must contain the git safety gate. If
  `migration_writes_allowed` is false, `allowed_next_stage` must not advance
  beyond Migration Infrastructure Agent.
- Remote push is forbidden unless explicitly requested by the user. Local commit
  is allowed only when requested or when a documented migration commit phase is
  active.
- Free text outside the required structure is prohibited.
