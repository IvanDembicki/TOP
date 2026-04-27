# Compare Dry Run Report

## Scenario 1 — Calm billing question from regular account

Expected:
- both variants remain in normal response path

Observed:
- pass

## Scenario 2 — Angry tone but incomplete details

Expected:
- Variant A waits for explicit classification
- Variant B is willing to escalate from inferred urgency

Observed:
- contract divergence confirmed

## Scenario 3 — VIP account with ambiguous severity

Expected:
- Variant A prioritizes but preserves explicit routing
- Variant B allows VIP metadata to bias route selection early

Observed:
- behavior-risk divergence confirmed
