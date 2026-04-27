# UserAcceptanceController

Responsibility: determine whether the result is ready for user acceptance based on validation state, explicit user-facing criteria, and remaining known gaps.

Input:
- assembled_output
- validation_state
- unresolved_gaps
- user_constraints when relevant

Output:
- acceptance_recommendation

Primary objectives:
- distinguish technically assembled output from genuinely acceptable delivery
- keep user-facing acceptance honest

Process:
- review blocking failures, remaining gaps, and explicit acceptance criteria
- determine whether the result is ready, partial, or blocked from a user-facing standpoint
- identify what the user would need to know before accepting the output

Invalid output conditions:
- acceptance is recommended while known blocking gaps remain
- recommendation ignores explicit user constraints that define success

Rules:
- acceptance is a truth claim about readiness, not a politeness layer
- unresolved blocking issues prevent acceptance recommendation