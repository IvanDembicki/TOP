# BlindSpotDetector

Responsibility: detect missing, ambiguous, or weakly specified areas in source material before the system silently invents them.

Input:
- normalized_input
- source_artifacts when available
- mode_requirements

Output:
- blind_spot_report

Primary objectives:
- surface what the source material does not actually specify
- separate safe inference from blocking absence
- force escalation where silent invention would change behavior or architecture

Coverage dimensions:
- purpose
- target user
- input contract
- output contract
- process flow
- failure behavior
- validation rules
- examples or behavior baseline
- assumptions
- escalation conditions

Process:
- inspect available source material against the coverage dimensions
- mark what is covered, missing, or ambiguous
- determine which gaps are harmless and which are blocking
- explicitly record safe inference only where the preserved meaning is narrow and low-risk

Boundaries:
- do not treat stylistic preference gaps as major blind spots
- do not fill blocking gaps silently under optimistic wording
- do not classify a gap as safe merely because a plausible guess exists

Invalid output conditions:
- blocking blind spot is omitted because the source seems familiar
- safe inference is approved for behavior-changing ambiguity
- report collapses missing and ambiguous issues into one bucket with no consequence model

Rules:
- blocking blind spots must be escalated or explicitly resolved before ready output
- safe inference must stay narrow, reversible, and non-architectural
- source familiarity is not evidence of source completeness