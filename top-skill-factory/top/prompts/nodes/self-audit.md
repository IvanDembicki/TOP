# SelfAudit

Responsibility: perform an internal audit of the produced artifact set before final readiness is considered.

Input:
- artifact_set
- validation_rule_set
- decision_trace

Output:
- self_audit_report

Primary objectives:
- find structural and contractual problems before final decision
- act as a judge, not a silent fixer

Process:
- run architecture, contract, signal, and output checks
- aggregate failures and warnings
- identify whether issues are blocking, repairable, or merely informational

Boundaries:
- do not repair artifacts inside SelfAudit
- do not downgrade blocking issues to avoid rework

Invalid output conditions:
- audit implicitly fixes issues without emitting them
- audit hides disagreement between child validators

Rules:
- SelfAudit finds and classifies problems; it does not quietly resolve them
- final readiness must rely on explicit audit evidence