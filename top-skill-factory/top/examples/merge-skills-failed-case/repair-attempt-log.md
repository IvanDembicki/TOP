# Repair Attempt Log

## Attempt 1

Proposal:
- default to direct answer
- escalate only after answer confidence falls below threshold

Result:
- rejected
- weakens PolicyAnswerSkill escalation-first guarantee

## Attempt 2

Proposal:
- default to escalation-first on all policy-adjacent topics
- keep direct answers only for fully safe FAQ cases

Result:
- rejected
- materially narrows AutoReplySkill public behavior and no longer preserves its direct-answer contract

## Attempt 3

Proposal:
- expose a mode switch that lets the merged system choose permissive or strict policy at runtime

Result:
- rejected
- changes authority ownership and pushes an unresolved product decision into runtime instead of resolving it structurally
