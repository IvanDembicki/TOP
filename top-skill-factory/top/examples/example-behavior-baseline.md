# Example behavior baseline

Scenario input:
- Convert a legacy PR review skill into TOP format.

Expected outputs:
- review contains architecture findings first
- unresolved ambiguity yields clarification or blocked state
- no fake ready state when required artifact is missing

Acceptance assertions:
- same blocking decisions as legacy baseline where compatible with TOP invariants
- no silent behavior expansion