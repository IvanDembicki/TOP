# InputCompletenessCheck

Responsibility: verify whether current input is sufficient to begin the requested mode safely.

Input:
- normalized_input
- mode_requirements

Output:
- input_completeness_report

Primary objectives:
- prevent premature execution on underspecified input
- separate missing essentials from optional refinements

Process:
- compare normalized input against mode requirements
- identify missing mandatory fields, weak assumptions, and usable present evidence
- classify missing information as blocking or non-blocking

Invalid output conditions:
- report marks input complete when required fields are absent
- report treats optional polish as blocking

Rules:
- completeness means enough to proceed honestly, not enough to guess confidently
- blocking incompleteness must trigger clarification or escalation