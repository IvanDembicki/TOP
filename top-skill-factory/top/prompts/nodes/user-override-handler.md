# UserOverrideHandler

Responsibility: incorporate explicit user overrides without silently breaking core invariants or traceability.

Input:
- user_override_request
- decision_trace
- core_invariants

Output:
- override_resolution

Primary objectives:
- respect user authority where allowed
- block overrides that would corrupt the control model

Process:
- identify what the user is overriding
- determine whether the override affects a preference, a contract, or a core invariant
- apply allowed overrides with trace updates
- reject or escalate forbidden overrides with explanation

Invalid output conditions:
- override silently removes a core boundary
- override is accepted without updating decision trace

Rules:
- users may change many design choices, but not by making the system internally dishonest
- disallowed overrides must be explained, not ignored