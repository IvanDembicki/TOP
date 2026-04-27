# RollbackMode

Purpose: return to a previous validated skill version.

Input:
- current_skill
- target_version
- version_history

Output:
- rollback_plan
- restored_skill_reference
- rollback_audit

Primary objectives:
- restore a trustworthy prior state without losing rollback rationale
- ensure rollback scope and evidence are explicit

Process:
- verify that the target version exists and has a clear status
- compare the current state against the rollback target
- identify what will be restored, what will remain external, and what audit evidence must be recorded
- produce a rollback audit that explains why rollback was selected and what risks remain

Boundaries:
- do not treat rollback as an untracked destructive reset
- do not restore a target whose trust status is unknown without explicit warning

Invalid output conditions:
- rollback target is vague or unsupported by version history
- rollback happens without preserving rollback reason and affected scope
- restored state is presented as safe while evidence about target quality is missing

Rules:
- rollback target must be validated or explicitly marked as draft
- preserve rollback reason
- use rollback record compatible with `schemas/rollback-record.schema.json`