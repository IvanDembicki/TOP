# SplitSkillMode

Purpose: Split an oversized skill into smaller TOP skills.

Input:
- source_skill
- split_reason
- complexity_report
- behavior_baseline when external behavior must stay stable

Output:
- skill_parts
- boundary_contracts
- migration_plan

Rules:
- Preserve external behavior unless explicitly changed.
- Define contracts between resulting skills.
- If external behavior is claimed stable, provide behavior preservation evidence.