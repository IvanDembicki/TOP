# Prompts Binding

All prompt files must be executed via agents and follow contracts.

## Rule

Each prompt MUST declare:
- responsible agent
- required input contract
- produced output contract

No standalone executable prompts are allowed, except explicitly designated service/design prompts that are not pipeline execution units.

## Mapping

- analyze-top-project.md -> Intake Agent + Ambiguity Resolver Agent
- generate-top-tree.md -> TOP Modeling Agent
- generate-top-node.md -> Generation Agent
- refactor-to-top.md -> Repair Agent
- explain-top-architecture.md -> Domain Structuring Agent
- derive-state-tree.md -> TOP Modeling Agent
- derive-data-model-tree.md -> TOP Modeling Agent
- derive-top-artifact-layout.md -> Domain Structuring Agent
- generate-node-implementation-prompt.md -> Generation Agent
- verify-node-implementation-prompt.md -> Validation Agent

## Service prompts

These files are allowed outside the main pipeline as design/reference prompts and are not executable pipeline units:

- design-node-prompt-pipeline.md — designing the workflow node → prompt → code → verification

## Enforcement

- Prompt is invalid if agent is not specified
- Prompt is invalid if output contract is missing

## Additional prompt coverage

The following prompts must also be covered by binding rules:

- derive-top-artifact-layout.md
- design-node-prompt-pipeline.md
- generate-node-implementation-prompt.md
- verify-node-implementation-prompt.md

All prompts must follow schema:

- agent
- input_contract
- output_contract
- required_grounding
- execution rules
- handoff
