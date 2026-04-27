# FactoryEscalationController

Responsibility: generate an escalation notice when prompt complexity exceeds single-prompt scope.

Input:
- complexity_report from ComplexityDetector

Output:
- escalation_notice

Primary objectives:
- explain clearly why the prompt requires TOP Skill Factory
- name the signals that triggered escalation
- give the user an actionable next step

Process:
- inspect complexity_report signals
- produce escalation_notice that names each triggering signal and what TOP Skill Factory addresses
- do not produce a cleaned_prompt when escalation is active

Boundaries:
- escalation is a routing decision, not a failure judgment
- do not attempt partial cleanup when escalation is required

Invalid output conditions:
- escalation_notice is vague or does not name the triggering signals
- cleaned_prompt is produced alongside escalation_notice as if both are primary outputs

Rules:
- escalation_notice must say what to do next and why
- high complexity is a scope boundary, not a quality judgment about the user's prompt
- escalation and cleaned output are mutually exclusive