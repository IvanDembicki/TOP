# CompatibilityCheckMode

Purpose: Check whether a skill remains compatible with a target environment, host policy, or previous contract expectations.

Input:
- target_skill
- compatibility_target
- compatibility_constraints

Output:
- compatibility_report
- breaking_changes
- required_adapters

Rules:
- Compatibility must be checked against explicit criteria, not intuition.
- Breaking changes must be named individually.
- Compatibility pass cannot override a core invariant violation.