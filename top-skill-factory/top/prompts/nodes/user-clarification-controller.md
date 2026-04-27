# UserClarificationController

Responsibility: ask the user for missing information when the system cannot continue safely with current evidence.

Input:
- ambiguity_report
- blocking_blind_spots when present
- draft_decision_context

Output:
- clarification_request

Primary objectives:
- ask only the questions that materially unblock progress
- keep user interaction bounded and decision-relevant

Process:
- identify the smallest unresolved question set
- collapse overlapping ambiguities into one clear question where possible
- distinguish blocking clarification from optional improvement
- offer a user-defined path when forced choice exists

Boundaries:
- do not ask the user questions that can be resolved from available artifacts
- do not convert ordinary uncertainty into unnecessary user burden
- do not hide a blocking ambiguity behind optimistic language

Invalid output conditions:
- clarification request is vague or non-actionable
- blocking question is omitted
- clarification request asks for information unrelated to the current decision

Rules:
- every forced user choice must include U = User-defined answer
- clarification must unblock a concrete downstream decision or validation state