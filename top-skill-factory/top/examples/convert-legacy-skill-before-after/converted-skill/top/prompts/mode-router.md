# ModeRouter

Purpose: select exactly one plan-delivery mode.

Rules:
- route to `CreateCompactPlanMode` when the request is concrete and does not ask for strategic depth
- route to `CreateDetailedPlanMode` only when the request explicitly asks for milestones, risks, dependencies, executive review, or equivalent strategic structure
- if critical information is missing, do not route directly to a delivery mode; require clarification through `InputController` and `UserInteractionController`
- urgency must not be treated as permission to skip mandatory clarification
