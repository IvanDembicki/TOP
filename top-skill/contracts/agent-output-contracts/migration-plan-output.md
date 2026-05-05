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
- validation_gates
- rollback_points
- migration_log_entry

details:
- scope_selection_rationale
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

- `migration_plan_path` must be `top/migration/MIGRATION_PLAN.md`
- `migration_workflow_path` must be `top/migration/MIGRATION_WORKFLOW.json`
- `agent_work_packages` must list the migration stages and responsible agents.
- `workflow_phase_updates` must list the phase ids, statuses, gates, outputs,
  and next phases written to the workflow JSON.
- `planned_artifacts` must include spec, prompt, status, log, and source-root
  paths when materialization is planned.
- `migration_log_entry` must identify the log entry appended for this planning pass.
- Free text outside the required structure is prohibited.
