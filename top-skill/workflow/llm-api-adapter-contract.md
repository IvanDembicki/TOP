# LLM API Adapter Contract

## Purpose

The LLM API adapter is the first real execution adapter for runner-enforced
role isolation. It lets the protocol runner launch one TOP pass as a separate
model/API invocation rather than asking the current chat context to simulate
another role.

## Adapter Script

```text
scripts/adapters/llm_api_adapter.py
```

The adapter is executed by `scripts/top_protocol_runner.py` as a pass command.
It receives only runner-provided environment variables:

- `TOP_CONTEXT_PACKAGE`
- `TOP_TASK_CAPSULE`
- `TOP_HANDOFF_ARTIFACT`
- `TOP_INVOCATION_EVIDENCE`
- `TOP_WORKFLOW_ID`
- `TOP_RUN_ID`
- `TOP_PASS_ID`
- `TOP_ROLE`

## Required Behavior

The adapter must:

1. read the context package;
2. read the referenced task capsule;
3. build a bounded prompt only from the context package, task capsule, and
   listed input references;
4. include the required handoff output shape in the bounded prompt;
5. call a separate LLM API request;
6. require the model to return one handoff JSON object, or one wrapper object
   with `handoff` and `artifactWrites` when the task capsule explicitly lists
   `artifactWriteRequests`;
7. reject handoffs that self-claim `runner-enforced` isolation or reference
   the wrong task capsule;
8. materialize only exact artifact refs listed in `artifactWriteRequests`;
9. write the handoff artifact;
10. write pass invocation evidence.

The adapter must not pass the current chat transcript, unbounded memory, or
unlisted project context into the model request.

Listed input references may point inside the run package or to
skill-root-relative files named in the task capsule. The adapter may read only
those listed references and must reject any input reference that escapes both
the run root and the skill root.

Listed artifact writes may point only inside the run package. A task capsule
must grant `mayEditFiles: true` and list every writable ref in
`artifactWriteRequests`. The model output must provide complete string file
content for each `artifactWrites` item. The adapter must reject any unlisted
write, missing required write, non-string content, or path escape.

## Invocation Evidence

When a real model/API request succeeds, the adapter writes:

```text
adapterKind: llm-api
freshContext: true
receivedOnlyContextPackage: true
modelInvocationEvidence: true
artifactWrites: [{ ref: string, sha256: string }]
```

If the adapter is run in `--dry-run`, lacks credentials, cannot reach the API,
or receives invalid model output, it must not set
`modelInvocationEvidence: true`.

## Runner-Enforced Eligibility

`llm-api` adapter evidence may contribute to `runner-enforced` only when the
runner also sees:

- distinct required pass invocation ids;
- distinct required pass context ids;
- handoff artifacts matching task capsules;
- hard-check evidence when delivery certification requires it;
- `--accept-external-runner-evidence`.

The adapter alone does not certify delivery. It only creates invocation
evidence for the runner and judicial pass to evaluate.

## Supported Provider

The initial adapter supports an OpenAI Responses-compatible HTTP endpoint with
standard library networking only. Configuration is supplied by arguments or
environment variables:

- `--endpoint` or `TOP_LLM_API_URL`
- `--model` or `TOP_LLM_MODEL`
- `TOP_LLM_API_KEY` or `OPENAI_API_KEY`

No API call is made during package validation unless a runner workflow
explicitly executes the adapter without `--dry-run`.

## Smoke Run

`scripts/create_orchestration_run.py --llm-smoke` creates a minimal two-pass
runner workflow using this adapter:

```text
executive -> judicial
```

The smoke run is designed to test separate LLM/API invocations and bounded
context packages. It does not certify delivery complete by itself.
