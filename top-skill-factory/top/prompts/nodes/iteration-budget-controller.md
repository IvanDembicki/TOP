# IterationBudgetController

Responsibility: enforce limits on validation-repair loops, clarification loops, and mode retries.

Input:
- iteration_state
- failure_classification
- configured_budgets

Output:
- iteration_budget_decision

Primary objectives:
- prevent endless rework loops
- stop the system from disguising uncertainty as persistence

Process:
- inspect the current loop type and count
- compare usage against configured budgets
- determine whether to continue, escalate, or block
- distinguish productive retry from repeated non-progress

Invalid output conditions:
- budget is exceeded but controller keeps the loop alive without rationale
- non-progress is treated as progress because wording changed slightly

Rules:
- budget exhaustion must not produce ready state
- repeated non-progress should force escalation or stop