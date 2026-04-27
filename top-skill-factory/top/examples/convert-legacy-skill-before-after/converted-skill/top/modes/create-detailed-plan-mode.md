# CreateDetailedPlanMode

Purpose: return a richer strategic plan when the request explicitly warrants it.

Input:
- normalized strategic request
- resolved clarification answers when needed

Output:
- detailed markdown plan with milestones, risks, dependencies, and next steps

Rules:
- this mode must not be activated implicitly from vague importance alone
- assumptions must be labeled explicitly
- missing critical inputs still require clarification before ready output
