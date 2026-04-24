# Agent Output Contracts

This directory is the single source of truth for the output shape of agents.

## Core rule

Agent files must not redefine required output fields on their own.

An agent file may:
- reference a contract
- explain the meaning of the output
- specify validation focus

An agent file must not:
- duplicate the required schema shape separately from the contract
- diverge from the contract on required fields
- introduce an alternative output form

If there is a discrepancy between an agent file and a contract:
- the contract takes priority

## Analysis contract note

Analysis-only output schema is defined in:
- `contracts/agent-output-contracts/analysis-output.md`

Authoritative source of agent output schema remains:
- `contracts/agent-output-contracts/*`
## Generation-pipeline semantic contracts

In `generation-pipeline` mode:

- `semantic-interpretation-output.md` is the authoritative Layer B output contract.
- `target-adaptation-output.md` is the authoritative Layer C output contract.
- `generation-output.md` must reference both outputs and must not regenerate semantics directly from source-platform notes.
