# OutputCheck

Responsibility: verify that the final output artifact set is complete, non-placeholder, and consistent with declared readiness.

Input:
- output_artifacts
- output_contract
- validation_evidence

Output:
- output_check_report

Primary objectives:
- prevent false-ready outputs
- ensure artifact completeness and declared readiness align

Process:
- compare produced artifacts against the required output set
- identify placeholders, missing files, or unsupported ready claims
- verify that output examples and reports support the claimed mode behavior when required

Invalid output conditions:
- ready state is claimed without required artifacts
- output is structurally present but semantically empty
- examples promise behavior the output cannot support

Rules:
- readiness is an evidence-backed state, not a mood
- placeholder output cannot be presented as complete delivery