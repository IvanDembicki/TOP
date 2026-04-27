# SkillDiscovery prompt

Responsibility: clarify the purpose, scope, assumptions, and risks of the target skill.

Input:
- normalized_input

Output:
- discovery_result

Discovery result must include:
- clarified_goal
- scope
- target_users
- assumptions
- risks
- non_goals
- required_user_decisions
- recommended_behavior_baseline_strategy when behavior preservation matters
- blind_spot_summary

Primary objectives:
- sharpen scope before architecture is generated
- expose assumptions and non-goals while they are still cheap to change

Process:
- refine the task goal into a bounded outcome
- identify target users and operating context
- separate required behavior from optional extensions
- record assumptions, risks, and user-owned decisions explicitly
- surface scope boundary warnings when the request is expanding into multiple skills or workflows

Boundaries:
- do not build the tree
- do not create output files
- do not silently absorb major ambiguity into assumptions

Rules:
- if scope grows too much, return scope_boundary_warning
- discovery must reduce ambiguity, not just rephrase the request