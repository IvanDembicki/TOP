# CreatePlanMode

Purpose: transform a clarified user goal into a short ordered plan.

Input:
- user_goal
- clarification_answers

Output:
- ordered_plan
- clarification_request when needed

Rules:
- keep the plan concise
- ask clarification if the goal lacks actionable scope
- return a bounded plan rather than speculative detail