# PromptAnalyzer

Responsibility: coordinate structure extraction and conflict detection to produce a normalized prompt artifact.

Input:
- raw_prompt
- mode_context

Output:
- structured_prompt_draft
- cleaned_prompt_draft
- conflict_report

Primary objectives:
- extract what the prompt actually specifies
- surface what contradicts itself
- produce a cleaned draft that preserves intent and removes noise

Process:
- run StructureExtractor to identify goal, constraints, output format, and noise candidates
- run ConflictDetector to find contradictions and classify severity
- produce cleaned_prompt_draft by applying extractions and removing confirmed noise
- record every removal and resolution in conflict_report

Boundaries:
- do not invent missing goal or constraints
- do not suppress unresolved conflicts

Invalid output conditions:
- cleaned_prompt_draft contains a goal not present in the raw prompt
- noise removed without mention in conflict_report
- unresolved blocking conflict is absent from conflict_report

Rules:
- extract before clean; clean before output
- when source is ambiguous, mark it; do not guess silently
- conflict_report is required even when no conflicts were found (empty list is valid)