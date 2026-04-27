# InvalidationController

Responsibility: coordinate invalidation when new evidence, requirements, or overrides conflict with active decisions.

Input:
- decision_trace
- conflict_set
- new_requirement_or_evidence

Output:
- invalidation_result

Primary objectives:
- retire stale decisions cleanly
- preserve internal consistency during change

Process:
- identify impacted decisions
- determine which decisions must be invalidated, reviewed, or preserved
- trigger cleanup and rebuild planning for affected areas
- keep the trace explicit about why invalidation occurred

Invalid output conditions:
- invalidation changes active state without a recorded reason
- downstream artifacts remain marked valid despite dependency on invalid decisions

Rules:
- invalidation is part of controlled evolution, not an exceptional embarrassment
- every invalidation must leave the system more explicit, not less