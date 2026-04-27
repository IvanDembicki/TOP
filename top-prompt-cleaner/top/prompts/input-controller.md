# InputController

Responsibility: normalize raw user input and run early-stage checks before routing.

Input:
- raw_prompt (the prompt to be cleaned)
- optional mode_hint (quick / strict / style)
- optional target_style (claude / gpt / custom)

Output:
- normalized_input containing: raw_prompt, mode_hint, target_style, open_questions
- sensitive_report (from SensitiveDataDetector)
- complexity_report (from ComplexityDetector)

Process:
1. Preserve raw_prompt unchanged.
2. Run SensitiveDataDetector on raw_prompt → produce sensitive_report.
3. If sensitive_blocking is true → halt immediately; emit blocked final output with diagnosis. ComplexityDetector and all downstream nodes do NOT run.
4. Run ComplexityDetector on raw_prompt → produce complexity_report.
5. Extract mode_hint and target_style when present in the user request.
6. Identify open_questions only when the request itself (not the prompt content) is unclear.

Boundaries:
- do not analyze or clean the prompt here
- do not invent mode_hint or target_style
- SensitiveDataDetector always runs before ComplexityDetector — no exceptions

Invalid output conditions:
- raw_prompt is modified during normalization
- ComplexityDetector runs when sensitive_blocking is true
- target_style is assumed without being explicitly stated or auto-detected

Rules:
- normalization is about the user's request, not the prompt content
- pass raw_prompt forward intact
- complexity_report is the sole authority for escalation routing
- sensitive_report is the sole authority for sensitive data blocking
