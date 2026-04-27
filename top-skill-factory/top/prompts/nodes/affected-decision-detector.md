# AffectedDecisionDetector

Responsibility: detect which existing decisions are impacted by a new requirement, new evidence, or invalidation event.

Input:
- decision_trace
- new_requirement_or_evidence

Output:
- affected_decision_set

Primary objectives:
- prevent stale decisions from remaining active after conditions changed
- scope rebuild work precisely

Process:
- compare the new requirement or evidence against active decisions
- find direct conflicts, implicit assumptions, and dependent downstream decisions
- classify impact as direct, indirect, or informational only
- identify which decisions must be invalidated, reviewed, or preserved

Invalid output conditions:
- clearly conflicting decision remains outside the affected set
- detector marks broad unrelated areas without justification

Rules:
- prefer precise dependency tracking over broad suspicion
- if a decision can no longer be justified, it must enter the affected set