# ComplexityBudgetController

Responsibility: enforce bounded complexity for the generated or converted skill.

Input:
- skill_tree_design
- signal_definitions
- validation_rule_set
- complexity_thresholds

Output:
- complexity_budget_report

Primary objectives:
- keep the skill reviewable
- prevent unnecessary node growth, signal sprawl, and validation inflation

Process:
- count nodes, tree depth, signal variants, validation files, and payload complexity
- compare actual shape against declared thresholds
- distinguish justified complexity from drift
- require explicit rationale when thresholds are exceeded

Invalid output conditions:
- budget report records counts but gives no judgment
- excessive complexity is accepted without rationale or approval

Rules:
- budgets exist to control maintainability and context size
- exceeding a hard budget without approval is blocking
- exceeding a soft budget requires explanation, not silence