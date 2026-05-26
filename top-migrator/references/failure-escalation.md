# Failure and Escalation Model

The migrator must handle failure as a normal workflow path, not as an exception.

## Hard Questions

### What if behavior tests are missing?

Set `behaviorStatus: behavior_not_verified`. Offer characterization-test generation, runtime traces, snapshots, or manual acceptance scenarios. Ask the developer whether to continue as a structural draft.

### What if tests pass but TOP validation fails?

Route to TOP repair. Preserve behavior evidence, but do not mark the node TOP-valid. After TOP repair, rerun behavior checks because architecture repair may change behavior.

### What if TOP validation passes but tests fail?

Route to behavior repair. Do not weaken TOP rules to satisfy tests. If the expected behavior conflicts with TOP architecture, create a conflict ticket.

### What if the semantic boundary is ambiguous?

Create an ambiguity ticket. Include candidate boundaries, evidence for each, risks, and the ownership question that only the developer can answer.

### What if parallel child agents require incompatible parent contract changes?

Freeze child work, create contract conflict ticket, and route to parent/orchestrator decision. Children must not silently mutate the parent contract.

### What if a child task is based on a stale parent contract?

Mark `integrationStatus: stale_contract`. The child must reload the new contract and either continue, adapt, or return an incompatibility report.

### What if siblings directly depend on each other?

Reject hidden sibling coupling. Move interaction through parent, a data node, connector, shared runtime/lib node, or an explicit declared relationship allowed by TOP canon.

### What if the final residual is meaningless?

Review earlier extraction decisions. If the residual must remain temporarily, classify it as a residual boundary with expiry and target repair direction.

### What if a node is too large?

Trigger decomposition review. The node cannot pass precheck unless the agent proves no hidden state holder, lifecycle branch, async workflow, modal/form/list/card/row responsibility, bridge cluster, data boundary, or reusable pattern remains.

### What if decomposition is too fine-grained?

Reject decorative node creation. A TOP node needs responsibility, lifecycle, state, mutation authority, integration boundary, or stable reusable semantic role.

### What if a framework hook, global store, router, or singleton leaks into a node?

Classify it as connector, bridge boundary, data node, black-box component, or temporary migration residual. Direct access may be accepted only with explicit deviation, expiry, and repair direction.

### What if repair repeats the same violation?

Use a circuit breaker. After repeated failure, set `readinessStatus: blocked` and escalate to developer or canon/model review.

## Failure Classes

`behavior_failure`
: Expected application behavior regressed.

`top_validation_failure`
: TOP architecture or artifact rules were violated.

`contract_conflict`
: Parent/child or sibling contracts are inconsistent.

`stale_contract`
: A child worked from an outdated parent contract.

`ambiguous_ownership`
: AI cannot determine the rightful owner of state, lifecycle, mutation, or integration.

`insufficient_evidence`
: Required files, tests, rules, or runtime traces are missing.

`repair_loop_exhausted`
: Repair repeated or exceeded attempt limits.

`developer_decision_required`
: A business, ownership, or risk decision cannot be inferred from code.

## Developer Escalation Packet

Use this exact shape when AI cannot safely continue:

```text
Problem:
Affected node:
Evidence from code:
What cannot be proven:
Options:
Risk per option:
Migrator recommendation:
Developer decision needed:
```

The packet must ask for the smallest decision that unblocks the workflow.
