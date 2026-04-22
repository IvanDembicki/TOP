# Spec Change Verification Output Contract

## Schema-first rule

This file is the authoritative source for the output shape of `Spec Change Verification Agent`.
Agent files do not define output schema. This contract does.

## Required output fields

```yaml
spec_change_verification:
  changed_nodes:
    - type: <NodeType>
      change: added | modified | removed
      fields_changed: [<field>, ...]
      verification_variant: A | B
      discrepancies:
        - field: <field>
          spec_says: <what the spec says>
          code_has: <what the code has>
          decision: update_code | revert_spec
      status: pass | fail | escalate
  overall_status: pass | fail | escalate
  code_changed: true | false
  next_stage: Final Audit Agent | Validation Agent | Repair Agent | Ambiguity Resolver Agent
  block_reason: <required if overall_status is fail or escalate>
```

## Field rules

- `changed_nodes` — must list every node whose spec entry was changed; omitting an affected node is a violation
- `discrepancies` — may be empty if spec and code are in agreement for this node
- `decision` — must be explicit for every discrepancy; omitting a decision is a violation
- `code_changed` — true if any `update_code` decision was applied
- `block_reason` — required when `overall_status` is not `pass`; must name the specific contradiction and what is needed to proceed
- `next_stage` — must follow the handoff rules in `agents/spec-change-verification-agent.md`
