# ValidationController

Responsibility: run validation rules against the assembled output and return a validation_result conforming to validation_result.schema.json.

Input:
- assembled_output (from OutputBuilder)
- structured_prompt
- raw_prompt

Output:
- validation_result containing:
  - results[] — one entry per rule: { rule, pass, detail? }
  - all_pass — true only when every result has pass: true
  - blocking_failures[] — list of rule identifiers that failed

Primary objectives:
- verify every rule has a clear pass or fail outcome
- prevent false-ready states

Process:
- check each rule from validation/rules.md in order
- for each rule: emit { rule: "<rule_id>", pass: true|false, detail: "<reason if false>" }
- set all_pass: false if any result has pass: false
- populate blocking_failures with the rule identifiers of all failed results
- pass validation_result to FinalDecisionController

Rule identifiers (must match validation_result.schema.json enum):
- goal_present
- output_format_defined
- no_unresolved_blocking_contradictions
- constraints_not_removed
- no_high_complexity_in_cleaning_mode
- no_scope_expansion
- diff_present_if_modified
- sensitive_data_cleared

Boundaries:
- ValidationController checks; it does not fix
- do not suppress violations to improve the apparent result
- do not emit a result object without both results[] and all_pass

Invalid output conditions:
- validation_result is absent
- violation found but not recorded in blocking_failures
- rule skipped without a not-applicable reason in detail
- all_pass: true when any result has pass: false

Rules:
- overall all_pass is false when any blocking rule fails
- validation must complete before FinalDecisionController emits ready
- each failing result must include a detail field explaining the failure
