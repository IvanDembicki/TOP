# DeprecationMode

Purpose: Mark a skill, mode, node, or artifact as deprecated without silently breaking dependents.

Input:
- target_artifact
- deprecation_reason
- replacement_plan

Output:
- deprecation_record
- affected_dependents
- migration_notice

Rules:
- Deprecation must be traceable.
- Deprecation must identify affected artifacts and a migration or removal policy.
- Deprecation must not silently remove active dependencies.