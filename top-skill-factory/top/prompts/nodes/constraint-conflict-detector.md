# ConstraintConflictDetector

Responsibility: detect contradictions or tension between user constraints, system rules, and mode requirements.

Input:
- normalized_input
- explicit_constraints
- core_invariants

Output:
- constraint_conflict_report

Primary objectives:
- surface impossible or self-defeating requests early
- distinguish hard contradiction from mild tension

Process:
- compare user goals and constraints against invariants and existing policies
- identify mutually exclusive requirements
- mark which conflicts are blocking and which need clarification

Invalid output conditions:
- detector hides a hard contradiction because a plausible answer could still be improvised
- report conflates preference tension with architectural impossibility

Rules:
- direct contradiction with core invariants is blocking
- soft preference tension should trigger clarification, not immediate failure