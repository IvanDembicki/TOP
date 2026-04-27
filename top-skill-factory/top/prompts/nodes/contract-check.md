# ContractCheck

Responsibility: verify that node and mode contracts are explicit, non-overlapping, and satisfiable.

Input:
- node_contracts
- mode_contracts when present
- schema_artifacts

Output:
- contract_check_report

Primary objectives:
- catch vague contracts before they become runtime confusion
- ensure each contract can be satisfied by available artifacts

Process:
- inspect inputs, outputs, and ownership boundaries per node
- identify generic fields, missing fields, and circular dependencies
- verify that downstream requirements are actually produced upstream

Invalid output conditions:
- contract accepted despite generic catch-all outputs
- contract says a node consumes data that no node or artifact supplies

Rules:
- undefined or unsatisfiable contracts are blocking
- overlap between node contracts requires explicit parent coordination