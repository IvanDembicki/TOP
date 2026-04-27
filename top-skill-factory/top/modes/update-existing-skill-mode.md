# UpdateExistingSkillMode

Purpose: apply new requirements to an existing TOP skill without layering contradictions on top of active decisions.

Input:
- existing_top_skill
- new_requirements
- constraints

Output:
- updated_skill
- invalidated_decisions
- rebuild_plan
- validation_result

Primary objectives:
- preserve unaffected valid artifacts
- invalidate only what the new requirements truly impact
- avoid full rebuild when scoped recomputation is enough

Process:
- compare new requirements against the current decision trace and active artifact set
- use InvalidationController to identify conflicting or affected decisions
- build a rebuild plan for only the impacted artifacts
- preserve unaffected artifacts and their traceability
- revalidate the updated bundle before final decision

Boundaries:
- do not layer new requirements on top of contradictory old decisions
- do not rebuild unrelated parts of the skill without dependency evidence
- do not hide behavior-changing updates inside minor wording changes

Invalid output conditions:
- contradictory decisions remain active after the update
- rebuild scope is broader or narrower than dependency evidence supports
- updated skill is marked ready before affected artifacts are revalidated

Rules:
- use InvalidationController before rebuilding affected artifacts
- preserve unaffected artifacts
- if a new requirement changes public behavior or architecture and authority is unclear, escalate rather than guess