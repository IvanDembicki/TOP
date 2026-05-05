# Minimum Viable Read Paths

This file defines the minimum set of reads for common task modes.

## 1. analysis-only

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `rules/violation-classification.md`
- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `agents/index.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/final-audit-output.md`

## 2. modeling-refactor

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `agents/index.md`
- `contracts/agent-output-contracts/intake-output.md`
- `contracts/agent-output-contracts/canon-precheck-output.md`
- `contracts/agent-output-contracts/validation-output.md`

## 3. generation-pipeline

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `agents/index.md`
- `contracts/agent-output-contracts/intake-output.md`
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

## 4. migration

Minimum:
- `SKILL.md`
- `rules/task-modes.md`
- `canon/migration.md`
- `canon/validation-rules.md`
- `rules/violation-catalog.md`
- `agents/index.md`
- `agents/migration-infrastructure-agent.md`
- `agents/migration-planning-agent.md`
- `agents/migration-agent.md`
- `agents/behavior-preservation-agent.md`
- `agents/top-modeling-agent.md`
- `contracts/agent-output-contracts/migration-infrastructure-output.md`
- `contracts/agent-output-contracts/migration-plan-output.md`
- `contracts/agent-output-contracts/behavior-preservation-output.md`
- `contracts/agent-output-contracts/top-modeling-output.md`
- `contracts/agent-output-contracts/validation-output.md`
- `contracts/agent-output-contracts/final-audit-output.md`
- `top/schemas/migration-workflow.schema.json`

If the migrated scope has no legacy tests or executable behavior evidence,
Migration Agent records that absence and Behavior Preservation Agent is not
required.

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
