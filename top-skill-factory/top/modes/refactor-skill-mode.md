# RefactorSkillMode

Purpose: Improve internal structure without changing external behavior.

Input:
- source_skill
- refactor_goal
- behavior_baseline

Output:
- refactored_skill
- behavior_preservation_report
- validation_result

Rules:
- External input/output contract must remain stable unless user approves change.
- All structural changes must be traceable.
- Behavior preservation claims require baseline comparison.