# Agents Layer

This directory defines the agent-based workflow layer of the TOP skill.

Each agent represents a specialized role in the pipeline rather than a general-purpose assistant.
Agents must operate within explicit responsibility boundaries and must not replace each other informally.

## Global rule

All agents must follow:

- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `rules/task-modes.md`
- `rules/violation-classification.md`
- relevant `contracts/agent-output-contracts/*`

If any agent behavior conflicts with canon or validation rules, canon and validation rules take priority.


## Agent responsibility rule

Each agent must have:

- a strictly defined role;
- a clearly limited scope;
- explicit inputs;
- explicit outputs;
- explicit handoff rules.

An agent must not silently expand its scope beyond its declared role.

## Pipeline rule

Agents are expected to work as a staged workflow.
A valid handoff must happen explicitly from one agent to the next.

The expected high-level generation pipeline is:

1. Intake Agent
2. Ambiguity Resolver Agent
3. Domain Structuring Agent
4. TOP Modeling Agent
5. Canon Precheck Agent
6. Semantic Interpreter Agent
7. Target Adaptation Agent
8. Generation Agent
9. Spec Sync Agent
10. Validation Agent
11. Repair Agent
12. Final Audit Agent

The Orchestrator Agent manages transitions between these stages.

## Validation rule

No agent may treat compilation success, local functionality, brevity, or convenience as a substitute for architectural validity.

Result is invalid until all required validation checks pass.

## File convention

Each agent file should follow the common template defined in:

- `agents/_agent-template.md`

Recommended file names:

- `agents/intake-agent.md`
- `agents/ambiguity-resolver-agent.md`
- `agents/domain-structuring-agent.md`
- `agents/top-modeling-agent.md`
- `agents/canon-precheck-agent.md`
- `agents/semantic-interpreter-agent.md`
- `agents/target-adaptation-agent.md`
- `agents/generation-agent.md`
- `agents/validation-agent.md`
- `agents/repair-agent.md`
- `agents/final-audit-agent.md`
- `agents/orchestrator-agent.md`

## Contract source of truth

Output fields and output shape are defined exclusively in:
- `contracts/agent-output-contracts/*`

Agent files are not the source of truth for the output schema.
If there is a discrepancy between an agent file and the output contract:
- the output contract takes priority
