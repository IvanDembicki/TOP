# OutputBuilder

Responsibility: assemble the final deliverable from validated analysis artifacts.

Input:
- cleaned_prompt_draft (from PromptAnalyzer)
- structured_prompt (validated)
- conflict_report
- style_adapted_prompt (when TargetLLMStyleMode is active)
- escalation_notice (when escalation was triggered)

Output:
- final_output:
    ready case    → cleaned_prompt + structured_prompt + diff
    escalated case → escalation_notice
    blocked case  → diagnosis

Primary objectives:
- present the result in a form the user can immediately use
- make every change visible through diff
- refuse to hide unresolved issues or missing artifacts

Process:
- if escalation_notice is present, return it as the primary output; do not emit cleaned_prompt
- otherwise assemble: cleaned_prompt (or style_adapted_prompt), structured_prompt, and diff
- diff must list every removed phrase, resolved contradiction, and structural change
- pass assembled output to ValidationController before emitting

Boundaries:
- OutputBuilder cannot invent goal, constraints, or output format
- OutputBuilder cannot emit ready without a ValidationController pass

Invalid output conditions:
- diff is absent when the prompt was modified
- cleaned_prompt emitted alongside escalation_notice
- missing structured fields filled with placeholder content

Rules:
- diff is a required artifact whenever the prompt was changed
- escalation and cleaned output are mutually exclusive primary outputs
- blocked result must include a diagnosis, not silence
