# FinalDecisionController

Responsibility: emit the final state of the cleaning run.

Input:
- validation_result (from ValidationController)
- escalation_signal (when FactoryEscalationController was triggered)

Output states:
- ready: validation passed; output is complete and honest
- blocked: required field missing or blocking validation failure; diagnosis included
- escalated: high complexity detected; escalation_notice is the primary result

Primary objectives:
- make readiness an evidence-backed decision
- prevent optimistic or ambiguous state labeling

Process:
- if escalation_signal is present, emit escalated regardless of other results
- if validation_result.all_pass is false, emit blocked with diagnosis listing the blocking_failures
- if validation_result.all_pass is true, emit ready

Rules:
- ready requires validation_result.all_pass: true and no escalation_signal
- blocked requires explicit diagnosis naming which rule(s) in blocking_failures failed
- escalated takes precedence when escalation_signal is present
- do not emit ready when a blocking violation exists
- draft is not used in this skill; partial results route to blocked with a partial diagnosis
