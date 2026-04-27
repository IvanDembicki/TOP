# VersionController

Responsibility: manage version semantics and version-related state transitions for the generated or converted skill.

Input:
- current_version
- change_summary
- compatibility_impact when available

Output:
- version_update_decision

Primary objectives:
- keep version changes consistent with actual change impact
- prevent silent semantic drift across revisions

Process:
- identify whether the change is patch-like, structure-changing, or behavior-affecting
- compare impact against compatibility expectations
- propose or validate an appropriate version update

Invalid output conditions:
- meaningful behavior change leaves version semantics untouched without rationale
- version update is arbitrary and not linked to change impact

Rules:
- versioning must reflect change meaning, not only chronology
- uncertain compatibility impact should be surfaced explicitly