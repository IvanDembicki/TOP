# Migration Profiles and Checkpoints

Migration profiles define how much evidence is required during recursive migration.

## Strict Incremental Profile

Use when the project must remain working after each extraction.

After every node extraction:

- update migration log;
- verify the parent still composes with extracted children;
- run relevant behavior tests or smoke checks;
- request independent TOP validation when possible;
- block on failed required gates;
- create repair or rollback obligations.

The project should remain runnable at each checkpoint, even while part of the scope is still legacy residual.

## Draft Full-Pass Profile

Use when the user wants a fast exploratory conversion.

Allowed:

- full recursive structural analysis without per-node behavior tests;
- deferred TOP validation;
- deferred behavior confirmation;
- larger temporary residuals.

Required:

- every deferred check must be logged as `not_verified`;
- final output must not claim complete migration;
- final validation must localize failures by node or subtree;
- repair/rollback must be available after final checks.

## Hybrid Profile

Use when some areas require strict evidence and others may be drafted.

Typical policy:

- strict for high-risk flows, payments, auth, data mutation, routing, state holders, integrations;
- draft for low-risk visual components, static content, simple layouts, and isolated library wrappers.

## Checkpoint Types

`extraction_checkpoint`
: One child node was extracted and logged.

`contract_checkpoint`
: Parent/child interface was created or changed.

`behavior_checkpoint`
: Tests, smoke checks, characterization checks, or manual scenarios were run.

`top_validation_checkpoint`
: Independent TOP validation was run or explicitly marked unavailable.

`integration_checkpoint`
: Parent re-composed children and residual code.

`rollback_checkpoint`
: A stable rollback anchor exists for this node or subtree.

## Checkpoint Rule

Each checkpoint must say exactly what is proven and what is not proven.

Bad:

```text
status: done
```

Good:

```text
decompositionStatus: children_ready
behaviorStatus: tests_passed
topValidationStatus: not_verified
integrationStatus: integrated
readinessStatus: ready_structural
```

## Required Evidence Split

Behavior evidence:

- legacy tests;
- characterization tests;
- smoke tests;
- snapshots;
- manual acceptance scenarios;
- trace comparison.

TOP evidence:

- independent validation report;
- files inspected;
- rules checked;
- violations checked;
- ambiguity and limitation list;
- rejection tickets if failed.

These evidence classes are independent. Do not substitute one for the other.
