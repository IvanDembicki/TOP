# CompareSkillMode

Purpose: compare two skill versions or variants.

Input:
- skill_a
- skill_b
- comparison_criteria

Output:
- structural_diff
- contract_diff
- signal_diff
- validation_diff
- behavior_risk_report

Primary objectives:
- show meaningful differences without altering either skill
- distinguish cosmetic variation from behaviorally significant divergence

Process:
- compare structure, contracts, signals, validation, and evidence separately
- identify whether differences change behavior, readiness, or maintenance risk
- use behavior baseline, dry-run evidence, or replay evidence when behavior equivalence is claimed
- keep comparison results reviewable and category-specific

Boundaries:
- do not merge or modify skills
- do not collapse all differences into one undifferentiated summary

Invalid output conditions:
- behavior equivalence is claimed without baseline or replay evidence
- structurally important difference is described as cosmetic with no rationale
- comparison summary hides which skill owns the risky change

Rules:
- compare artifacts separately
- if behavior equivalence is claimed, use the behavior baseline or replay evidence
- comparison must preserve traceability of what changed and why it matters