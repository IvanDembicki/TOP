# MergeSkillsMode

Purpose: Merge two or more skills into a controlled TOP skill.

Input:
- source_skills
- merge_goal
- conflict_policy
- behavior_baseline when behavior preservation matters

Output:
- merged_skill_design
- conflict_report
- decision_trace
- merge_validation_result

Rules:
- Resolve conflicts before output assembly.
- Do not silently merge incompatible contracts.
- If merge claims preserved behavior, attach a behavior baseline or replay evidence.