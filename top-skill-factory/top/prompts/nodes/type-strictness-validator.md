# TypeStrictnessValidator

Responsibility: reject weakly typed contracts, schemas, and payload definitions.

Input:
- node_contracts
- schema_artifacts
- signal_definitions

Output:
- type_strictness_report

Primary objectives:
- remove generic data shapes that hide ambiguity
- force concrete field-level meaning where possible

Process:
- inspect contracts and schemas for overly generic fields
- identify placeholders such as `data`, `context`, `content`, or `result`
- determine whether each generic field can be replaced by explicit structure

Invalid output conditions:
- generic fields are accepted even though explicit fields are feasible
- report flags a generic field but does not explain why it is risky

Rules:
- strictness is about reducing ambiguity, not about syntactic perfection alone
- explicit structure should be preferred wherever downstream behavior depends on it