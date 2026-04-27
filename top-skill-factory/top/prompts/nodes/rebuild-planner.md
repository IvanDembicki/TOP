# RebuildPlanner

Responsibility: plan the smallest necessary rebuild after invalidation, repair, or structural change.

Input:
- affected_decision_set
- current_artifact_state
- dependency_map when available

Output:
- rebuild_plan

Primary objectives:
- avoid unnecessary full regeneration
- ensure all impacted artifacts are revisited

Process:
- identify which artifacts directly depend on affected decisions
- determine the smallest safe rebuild scope
- order rebuild steps so prerequisites are restored before dependents

Invalid output conditions:
- plan rebuilds too little and leaves stale dependent artifacts untouched
- plan rebuilds too much without dependency rationale

Rules:
- rebuild scope must be evidence-based
- partial recomputation is preferred when it preserves correctness