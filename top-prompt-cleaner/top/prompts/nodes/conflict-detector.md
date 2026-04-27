# ConflictDetector

Responsibility: find contradictions within the prompt and classify their severity.

Input:
- extraction_result (from StructureExtractor)
- raw_prompt

Output:
- conflict_report containing: conflicts (list), each with: description, severity, resolution_recommendation

Conflict classification:
- blocking: direct contradiction where both sides cannot both be true simultaneously
    example: "keep it under 100 words" + "cover all ten features in detail"
- warning: tension that affects interpretation but does not make the prompt unsatisfiable
    example: "professional tone" + "use emojis freely"

Process:
- compare constraints against each other for mutual exclusivity
- compare constraints against the stated goal for coherence
- compare stated output format against the task type for compatibility
- for each conflict, recommend a resolution or mark as requiring user decision

Boundaries:
- differing style preferences are not conflicts unless they contradict each other
- do not classify ambiguity as a conflict unless the ambiguity makes the prompt contradictory
- do not resolve blocking conflicts silently; surface them

Invalid output conditions:
- blocking conflict found but not reported
- conflict severity downgraded without a rationale
- resolution_recommendation invented without basis in the prompt text

Rules:
- blocking conflicts must be reported in QuickCleanMode and must block output in StrictMode
- warning-level conflicts must appear in diff even when auto-resolved
- conflict_report with zero conflicts is valid and must still be present
