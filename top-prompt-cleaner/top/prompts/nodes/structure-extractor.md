# StructureExtractor

Responsibility: extract goal, constraints, output format, and noise candidates from the raw prompt.

Input:
- raw_prompt

Output:
- extraction_result containing: goal, constraints, output_format, noise_candidates

Process:
- identify the primary task or objective the prompt is requesting
- list all explicitly declared constraints and limitations
- identify the expected output format when stated or clearly implied
- mark phrases as noise_candidates when they are filler, redundant connectors, or repetition

Boundaries:
- extract only what is stated or unambiguously implied; do not infer missing fields
- noise_candidates are candidates, not confirmed noise; ConflictDetector confirms before removal

Invalid output conditions:
- goal field contains content not derivable from the raw prompt
- a stated constraint is absent from the extraction
- output_format is marked as stated when it was inferred

Rules:
- when goal is absent, leave field empty and flag as missing; do not invent
- when output_format is implicit but clearly inferable, mark it as inferred in the extraction_result
- noise_candidates must reference the original phrase, not a paraphrase
