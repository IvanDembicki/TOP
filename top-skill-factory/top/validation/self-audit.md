# Self-audit protocol

SelfAudit is a judge, not a fixer.

Input:
- generated_or_converted_skill
- decision_trace
- validation_rules
- quality_control_results

Output:
- pass
- violations
- warnings
- required_fixes

Rules:
- SelfAudit must not rewrite artifacts.
- SelfAudit must not silently accept partial compliance.
- If pass is false, FinalDecisionController cannot mark the skill ready.