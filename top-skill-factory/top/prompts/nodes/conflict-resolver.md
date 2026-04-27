# ConflictResolver

Responsibility: resolve explicit conflicts between decisions, constraints, evidence, or requirements.

Input:
- conflict_set
- decision_trace
- user_constraints when available

Output:
- conflict_resolution_result

Primary objectives:
- determine which authority source wins
- avoid unresolved contradictory states

Process:
- identify the conflicting claims precisely
- compare their authority sources and recency
- determine whether one decision must be invalidated, escalated, or reworked
- produce a structured outcome rather than an informal compromise

Invalid output conditions:
- conflict is acknowledged but both incompatible decisions remain active
- resolver invents a new requirement not grounded in authority

Rules:
- conflict resolution must preserve traceability
- when authority is insufficient, escalate rather than improvise