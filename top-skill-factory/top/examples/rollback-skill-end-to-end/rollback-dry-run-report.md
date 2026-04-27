# Rollback dry run report

Scenario:
- request: "Plan a team demo"

Expected after rollback:
- concise mode selected by default
- no implicit escalation into detailed mode

Observed:
- restored router preserves concise default behavior
- detailed mode requires explicit request

Conclusion:
- rollback restores the validated default-behavior boundary