# CreateLaunchPlanMode

Purpose: turn clarified launch inputs into a bounded launch plan.

Input:
- user_goal
- clarification_answers

Output:
- ordered_plan
- clarification_request when needed

Rules:
- require explicit domain clarification when launch meaning changes plan structure
- do not generalize one domain's launch logic to another without authority