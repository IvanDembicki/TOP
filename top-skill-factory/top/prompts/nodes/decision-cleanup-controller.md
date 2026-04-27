# DecisionCleanupController

Responsibility: remove or retire stale, invalidated, or superseded decisions from the active decision state.

Input:
- decision_trace
- invalidation_events

Output:
- cleaned_decision_state

Primary objectives:
- prevent contradictory decision residue
- keep active state small and trustworthy

Process:
- identify decisions marked invalidated or superseded
- ensure downstream references are updated or flagged
- preserve history while removing false-active state

Invalid output conditions:
- invalidated decisions remain active by omission
- cleanup destroys traceability instead of updating status

Rules:
- cleanup must preserve history but shrink active ambiguity
- historical decisions may remain recorded, not active