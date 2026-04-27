# DecisionTraceController

Responsibility: maintain traceability between inputs, constraints, user decisions, validation evidence, and generated outputs.

Input:
- active_decisions
- new_decision_candidates
- validation_evidence

Output:
- decision_trace

Primary objectives:
- preserve why a decision exists
- make invalidation and supersession reviewable
- prevent hidden architectural authority

Process:
- attach each important decision to a concrete source
- record whether the source is user input, explicit constraint, evidence, or validation finding
- update statuses when decisions are superseded or invalidated
- surface orphaned decisions that no longer have a valid authority source

Invalid output conditions:
- active decision cannot be traced to an authority source
- invalidated decision remains effectively active
- decision history is collapsed into prose instead of structured records

Rules:
- no important decision may exist without traceable justification
- decision trace must support audit, invalidation, and repair routing