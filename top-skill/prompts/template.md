# Generation Prompt Template

## Required grounding

Follow:
- canon/core-axioms.md
- canon/validation-rules.md
- rules/task-modes.md
- rules/violation-classification.md
- relevant contracts/agent-output-contracts/*

## Validation before finalizing

Result is invalid until all validation checks pass.  
Compilation success is not architectural success.  
Local functionality does not override TOP rules.

Do not finalize output if any rule is violated.


## Mode and contract discipline

Prompt must be executed within the active task mode.

Required:
- active `task_mode` must be known
- active agent must be known
- relevant output contract must be known

Legacy general contracts are not authoritative for output schema.
