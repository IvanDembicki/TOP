# Pass Invocation Contract

## Purpose

This contract defines what a real runner invocation must prove before
top-skill may treat role separation as more than protocol-only structure.

It sits between task capsules, context packages, handoff artifacts, and the
runner report.

## Context Package

Before a pass runs, the runner materializes one context package:

```text
contexts/<pass-id>.context-package.json
```

The context package records:

- task capsule reference
- expected handoff reference
- input references
- context slices
- forbidden inputs
- context hash
- runner name and materialization time

The pass may receive the context package. It must not receive the full prior
chat, unbounded agent memory, or broad project context unless those inputs are
explicitly listed.

Required judicial and certification passes must not run with placeholder context slices such as `fill with minimal required context before launch`.
Their context package must include concrete input references unless the task
capsule explicitly defines a zero-input pass.

## Invocation Evidence

After a pass runs, the runner or adapter records one invocation evidence
artifact:

```text
invocations/<pass-id>.invocation-evidence.json
```

The evidence records:

- adapter kind
- invocation id
- context id
- task capsule reference
- context package reference
- handoff reference
- context hash
- handoff hash
- whether the pass had a fresh context
- whether the pass received only the context package
- whether the adapter proves an actual model/agent invocation

## Adapter Kinds

Allowed adapter kinds:

- `process`
  The runner launched an OS process. This is useful execution evidence but not
  proof of LLM context isolation by itself.

- `llm-api`
  The runner launched a direct model/API call with a fresh context window.

- `external-agent-runtime`
  The runner launched another agent runtime that creates a fresh context
  window and writes invocation evidence.

- `manual`
  A human or unmanaged process produced artifacts. This cannot certify
  runner-enforced isolation.

## Runner-Enforced Isolation Gate

`executionIsolationLevel: runner-enforced` requires all delivery-required
passes to provide invocation evidence where:

- `adapterKind` is `llm-api` or `external-agent-runtime`;
- `freshContext` is `true`;
- `receivedOnlyContextPackage` is `true`;
- `modelInvocationEvidence` is `true`;
- invocation ids are distinct;
- context ids are distinct;
- the runner explicitly accepts external runner evidence.

Different strings in `invocationId` or `contextId` are not enough.
A process adapter without model invocation evidence cannot certify runner-enforced role isolation.

## Report Status

The runner report may still show `hard-check-verified` when hard checks really
ran and passed. That does not imply `runner-enforced`.

If any required pass handoff is `not-verified`, `not-certified`, `partial`,
`not-started`, or `in-progress`, the runner report status must be
`not_verified` unless a blocking failure occurred.
