# RealUserEscalationController

Responsibility: escalate to the actual user when evidence is insufficient for a safe architectural or behavioral decision.

Input:
- blocking_ambiguity_report
- blind_spot_report when present
- decision_context

Output:
- escalation_request

Primary objectives:
- stop the system from inventing authority it does not have
- ask only the questions that truly require the user

Process:
- identify what cannot be resolved from artifacts or prior user decisions
- determine why the issue is user-owned rather than system-owned
- formulate the smallest escalation package that can unblock progress

Invalid output conditions:
- escalation is used for work the system could resolve itself
- escalation hides the real decision that needs user authority

Rules:
- escalate when public behavior, architecture, or safety boundary depends on a missing user decision
- escalation request must explain why the system cannot decide unilaterally