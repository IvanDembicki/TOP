# StrictMode

Purpose: thorough validation with explicit clarification when required fields or intent are missing.

Input:
- raw_prompt
- complexity_signal (must be low or medium)

Output:
- cleaned_prompt or clarification_request
- structured_prompt
- validation_result
- diff

Primary objectives:
- require an explicit goal and output format before producing a cleaned result
- surface all contradictions, not only obvious ones
- produce a validation_result that names each rule and its outcome

Process:
- run PromptAnalyzer to extract structure and detect conflicts
- if goal is absent or output format is undefined, emit clarification_request and stop
- resolve all detected conflicts explicitly; record each resolution
- run ValidationController against all rules in validation/rules.md
- emit cleaned_prompt only when validation passes

Boundaries:
- do not emit a cleaned prompt when a required field is absent
- do not auto-resolve ambiguous contradictions without recording them

Invalid output conditions:
- cleaned_prompt produced without a confirmed goal
- validation_result is missing or contains no rule-level detail
- contradiction detected but not addressed

Rules:
- blocked is a valid and honest outcome when required fields are absent
- validation_result must name each checked rule and its pass/fail status
- clarification_request takes precedence over partial output