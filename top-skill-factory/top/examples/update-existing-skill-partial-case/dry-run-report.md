# Dry run report

Scenario 1:
- request: "Plan a team demo"

Expected:
- default concise mode selected
- prior concise behavior preserved

Observed:
- concise mode remained the default path
- no accidental routing into the detailed mode

Scenario 2:
- request: "Give me a detailed execution checklist for the team demo"

Expected:
- detailed mode selected only because the user explicitly asked for it

Observed:
- detailed mode selection matched the explicit request
- artifact support exists, but example coverage is still incomplete

Result:
- update is structurally coherent
- final state should remain draft until example coverage is updated