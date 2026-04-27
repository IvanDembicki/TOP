# ValidationFailureHandler

Responsibility: convert validation failure reports into the correct next action.

Input:
- validation_failure_set
- failure_classification
- iteration_budget_decision

Output:
- validation_failure_resolution

Primary objectives:
- prevent false-ready continuation after failed validation
- route failures to repair, clarification, escalation, or stop

Process:
- inspect blocking versus non-blocking failures
- combine failure class with iteration state
- choose the next allowed transition
- preserve evidence for why the current state is not ready

Invalid output conditions:
- handler acknowledges blocking failure but still allows ready state
- next action is unclear or unsupported by the failure set

Rules:
- validation failure must change state meaningfully
- non-progressing validation loops must respect iteration budgets