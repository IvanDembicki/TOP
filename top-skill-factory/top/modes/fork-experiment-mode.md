# ForkExperimentMode

Purpose: Create an isolated experimental branch of a skill.

Input:
- source_skill
- experiment_goal
- constraints

Output:
- forked_skill
- experiment_trace
- comparison_plan

Rules:
- Never overwrite the source skill.
- Maintain baseline reference.
- Mark experimental artifacts clearly.