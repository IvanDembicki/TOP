# Minimum Viable Read Paths

This file defines the minimum set of reads for common task modes.

## 1. analysis-only

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `rules/violation-classification.md`
- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `canon/agent-power-separation.md`
- `agents/index.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/final-audit-output.md`

## 2. modeling-refactor

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/core-axioms.md`
- `canon/migration.md`
- `canon/validation-rules.md`
- `canon/agent-power-separation.md`
- `canon/validation-rejection-protocol.md`
- `agents/index.md`
- `agents/canon-precheck-agent.md`
- `agents/top-modeling-agent.md`
- `agents/validation-agent.md`
- `agents/repair-agent.md`
- `contracts/agent-output-contracts/intake-output.md`
- `contracts/agent-output-contracts/migration-infrastructure-output.md`
- `contracts/agent-output-contracts/migration-plan-output.md`
- `contracts/agent-output-contracts/top-modeling-output.md`
- `contracts/agent-output-contracts/canon-precheck-output.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/repair-output.md`
- `contracts/top-folder-contract.md`
- `top/schemas/migration-workflow.schema.json`

## 3. generation-pipeline

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `canon/agent-power-separation.md`
- `canon/validation-rejection-protocol.md`
- `agents/index.md`
- `agents/top-modeling-agent.md`
- `agents/canon-precheck-agent.md`
- `agents/generation-agent.md`
- `agents/validation-agent.md`
- `agents/repair-agent.md`
- `contracts/agent-output-contracts/intake-output.md`
- `contracts/agent-output-contracts/top-modeling-output.md`
- `contracts/agent-output-contracts/canon-precheck-output.md`
- `references/semantic-ui-layer.md`
- `references/target-adaptation-layer.md`
- `references/multi-target-generation.md`
- `agents/semantic-interpreter-agent.md`
- `agents/target-adaptation-agent.md`
- `contracts/agent-output-contracts/semantic-interpretation-output.md`
- `contracts/agent-output-contracts/target-adaptation-output.md`
- `contracts/agent-output-contracts/generation-output.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/repair-output.md`
- `prompts/generate-top-node.md`
- `prompts/verify-node-implementation-prompt.md`

## 4. migration

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/migration.md`
- `canon/validation-rules.md`
- `canon/agent-power-separation.md`
- `canon/validation-rejection-protocol.md`
- `rules/violation-catalog.md`
- `agents/index.md`
- `agents/migration-infrastructure-agent.md`
- `agents/migration-planning-agent.md`
- `agents/migration-agent.md`
- `agents/behavior-preservation-agent.md`
- `agents/top-modeling-agent.md`
- `agents/canon-precheck-agent.md`
- `agents/generation-agent.md`
- `agents/spec-sync-agent.md`
- `agents/validation-agent.md`
- `agents/repair-agent.md`
- `agents/final-audit-agent.md`
- `contracts/agent-output-contracts/migration-infrastructure-output.md`
- `contracts/agent-output-contracts/migration-plan-output.md`
- `contracts/agent-output-contracts/behavior-preservation-output.md`
- `contracts/agent-output-contracts/top-modeling-output.md`
- `contracts/agent-output-contracts/canon-precheck-output.md`
- `contracts/agent-output-contracts/generation-output.md`
- `contracts/agent-output-contracts/spec-sync-output.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/repair-output.md`
- `contracts/agent-output-contracts/final-audit-output.md`
- `prompts/generate-top-node.md`
- `prompts/verify-node-implementation-prompt.md`
- `top/schemas/migration-workflow.schema.json`

If the migrated scope has no legacy tests or executable behavior evidence,
Migration Agent records that absence and Behavior Preservation Agent is not
required.

If migration includes materialization, generation repair, or spec sync, the
generation, spec-sync, validation, and repair output contracts above are
mandatory reads. A migration task must not rely on `Generation Agent` hydration
without also loading `generation-output.md` and the generation prompt.

## 5. spec-change

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `agents/index.md`
- `agents/spec-change-verification-agent.md`
- `references/spec-change-verification.md`
- `contracts/agent-output-contracts/spec-change-verification-output.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/final-audit-output.md`

## Core rule

A full pre-read of all documents is not required for every minor task.

Load only:
- the mode-specific minimum path
- plus task-specific files as needed
