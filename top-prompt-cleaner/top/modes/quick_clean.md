# QuickCleanMode

Purpose: fast single-pass cleanup of a prompt without user interaction.

Input:
- raw_prompt
- complexity_signal (must be low or medium)

Output:
- cleaned_prompt
- structured_prompt
- diff

Primary objectives:
- remove noise without destroying user intent
- make goal, constraints, and output format explicit
- auto-resolve warning-level conflicts only; surface blocking conflicts in diff as unresolved warnings

Process:
- run PromptAnalyzer to extract structure and detect conflicts
- for warning-level conflicts: apply resolution, record in diff under resolved_conflicts
- for blocking conflicts: do NOT auto-resolve; record in diff under unresolved_conflicts with a recommended resolution
- produce cleaned_prompt that preserves all user-stated constraints
- produce structured_prompt and diff as required artifacts

Boundaries:
- do not ask for user clarification
- do not invent goals or constraints not present in the original
- do not run if complexity_signal is high — route to FactoryEscalationController instead

Invalid output conditions:
- cleaned_prompt removes a user-stated constraint without noting it in diff
- goal in structured_prompt is invented rather than extracted
- diff is absent when the prompt was changed

Rules:
- preserve all user intent; remove only noise
- ambiguous contradictions that cannot be auto-resolved appear in diff as warnings, not silent choices
- mode result is ready only when diff and structured_prompt are both present AND no blocking conflicts remain unresolved
- if a blocking conflict is found, status is blocked — not ready; diff must list it under unresolved_conflicts