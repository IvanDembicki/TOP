# Spec Change Verification

This document describes the mandatory verification protocol that is triggered by any change to the spec (JSON).

---

## Principle

The spec is the source of truth. Any change to the spec creates an obligation to verify that the existing code conforms to it.

Changing the spec without verifying the code is considered incomplete.

---

## When it is triggered

Verification is mandatory when:
- adding a new node to the JSON;
- changing the type, role, or doc of an existing node;
- changing props (contentType, lib, dir);
- adding, removing, or reordering children;
- changing the description of lifecycle, ownership, or content.

Verification is not required when:
- fixing typos in doc without semantic changes;
- updating references to prompt files without changing the architecture.

---

## Protocol steps

### Step 1. Identify affected nodes

For each changed entry in the JSON, record:
- type of change: added / modified / removed;
- affected fields;
- whether the node has an implementation prompt.

### Step 2. For each affected node — verification

#### Variant A: node with an implementation prompt

1. Regenerate the node implementation from the current prompt and the updated spec.
2. Compare the regenerated code with the existing code.
3. Record discrepancies.
4. Use `prompts/verify-node-implementation-prompt.md` as the execution prompt.

#### Variant B: hand-coded node (no active prompt)

1. Read the existing node code.
2. Compare with the updated spec on the following criteria:
   - semantic role matches;
   - children correspond to the spec;
   - contentType in spec corresponds to the presence/absence of content in the code;
   - lifecycle methods correspond to the described behavior;
   - props (lib, dir, contentType) are correctly reflected in the code;
   - if the node is fixed switchable — children are state nodes; if it is dynamic switchable — candidate child type, candidate-set source of truth, selected-child source of truth, and active-child removal policy are explicitly described;
   - if the node has content — controller/content split is present.
3. Record discrepancies.

### Step 3. For each discrepancy — a decision

For each discrepancy found, make one of two decisions:

- **Update the code** — the spec change is correct, the code is behind;
- **Revert the spec** — the code is correct, the spec change was erroneous.

The decision must be explicit. Silently leaving a discrepancy unresolved is not permitted.

### Step 4. Result verification

After applying decisions:
- re-check the affected nodes;
- confirm that the spec and code are in agreement;
- record the status: `pass` or `escalate`.

---

## Output format

```
spec_change_verification:
  changed_nodes:
    - type: <NodeType>
      change: added | modified | removed
      fields_changed: [...]
      verification_variant: A | B
      discrepancies:
        - field: <field>
          spec_says: <what the spec says>
          code_has: <what the code has>
          decision: update_code | revert_spec
      status: pass | fail | escalate
  overall_status: pass | fail | escalate
```

---

## Escalation

Escalation is required if:
- a discrepancy cannot be resolved without changing the architecture;
- the spec and code contradict each other non-trivially;
- the affected node has downstream dependencies that also need to be updated.

When escalating, record:
- which node failed;
- the specific contradiction;
- what is needed from a human to proceed.

---

## Relationship with other agents

- Triggered instead of or after `Spec Sync Agent` depending on the direction of changes.
- If verification detects code changes → pass to `Validation Agent`.
- If verification detects spec revert → update the spec and finish.

See `agents/index.md` → `spec-change` pipeline.
