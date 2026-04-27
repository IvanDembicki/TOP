# OutputAssembler

Responsibility: assemble the final artifact package from validated component artifacts.

Input:
- generated_artifacts
- output_contract
- validation_state

Output:
- assembled_output

Primary objectives:
- gather a coherent deliverable artifact set
- refuse to hide missing components

Process:
- collect artifacts required by the current mode and output contract
- verify that required pieces exist before assembly
- preserve references, statuses, and supporting reports
- emit missing-artifact signals instead of fabricating absent files

Invalid output conditions:
- assembler invents a missing artifact to make the package look complete
- assembled output omits a required report while claiming readiness

Rules:
- OutputAssembler cannot invent missing artifacts
- missing artifacts must remain visible to downstream validation and final decision logic