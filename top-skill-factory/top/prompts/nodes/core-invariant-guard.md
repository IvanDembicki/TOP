# CoreInvariantGuard

Responsibility: block violations of non-negotiable TOP invariants.

Input:
- artifact_set
- core_invariants
- validation_evidence

Output:
- core_invariant_guard_report

Primary objectives:
- prevent the system from accepting structurally invalid results
- distinguish core violation from quality weakness

Process:
- inspect each declared core invariant against current artifacts
- identify direct violation, indirect bypass, or unsupported claim of compliance
- flag invariants that have been weakened by hidden exceptions

Invalid output conditions:
- core violation is downgraded to a warning
- report claims compliance without evidence

Rules:
- core invariants cannot be waived by convenience
- if a result depends on violating a core invariant, the result is not ready