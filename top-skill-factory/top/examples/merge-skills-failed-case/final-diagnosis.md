# Final Diagnosis

The merge failed because the source skills are not merely structurally different; they encode incompatible authority models.

- `PolicyAnswerSkill` says the system must escalate before answering on sensitive topics.
- `AutoReplySkill` says the system may answer first and rely on a warning banner plus later escalation.

This is not a missing-information problem, so `blocked` is inaccurate.
This is not a partially useful merged result, so `draft` is inaccurate.

The only truthful state is `failed`:
- the bounded repair budget was exhausted
- the conflict remained incompatible
- any merged artifact would silently choose one policy over the other
