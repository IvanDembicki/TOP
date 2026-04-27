# FailureClassifier

Responsibility: classify validation or execution failures into meaningful categories that drive next routing.

Input:
- validation_failures
- artifact_state
- iteration_state

Output:
- failure_classification

Primary objectives:
- route repair work correctly
- distinguish architecture failure from content incompleteness or budget exhaustion

Process:
- inspect each failure and identify its primary cause
- classify it as contract, architecture, ambiguity, schema, quality, or budget-related
- determine whether repair, clarification, escalation, or stop is appropriate

Invalid output conditions:
- distinct failures are collapsed into one vague bucket
- classification does not support a clear next step

Rules:
- classification must support routing, not just diagnosis language
- repeated failures should surface pattern and severity escalation