# Runner Contract

## Purpose

The runner is the executable harness layer for the top-skill 2.0 protocol. It
turns task capsules, handoff artifacts, and hard checks into a blocking process
gate.

## Runner Scope

The minimal runner has two supported jobs:

- launch or verify one process per task capsule;
- run required hard checks and block on non-zero exit codes.

The normal runner additionally materializes context packages and records pass
invocation evidence as defined by
`workflow/pass-invocation-contract.md`.
LLM-backed pass execution is defined by
`workflow/llm-api-adapter-contract.md`.

It does not replace the orchestrator, validator, or final audit. It does not
invent verdicts. It produces a runner report that downstream judicial and final
audit passes may inspect.

## Input Artifact

Runner input is a `runner-workflow` artifact. It must list:

- workflow id
- run id
- runner name
- mode
- runner capabilities
- pass definitions
- task capsule references
- handoff artifact references
- context package references
- invocation evidence references
- adapter kind
- hard-check commands
- optional delivery certification reference

Runner workflow artifacts normally live in the run package defined by
`workflow/run-package-layout.md`.

## Portable Commands

Runner workflows should avoid OS-specific relative paths such as
`..\\..\\scripts\\check.py`.

For Python hard checks or pass commands, prefer structured command fields:

```json
{
  "commandType": "python-script",
  "scriptRef": "scripts/quick_validate.py",
  "scriptBaseRef": "skill-root",
  "args": ["."],
  "cwdRef": "skill-root"
}
```

The runner resolves these references with `pathlib` for the current operating
system. Raw `command` arrays are still allowed for adapter-specific processes,
but portable workflow artifacts should use `scriptRef` where possible.

## Pass Execution

When pass execution is enabled, the runner launches each pass command as a
separate OS process. The runner provides only the assigned task capsule and
expected handoff path through environment variables. It also provides:

- `TOP_CONTEXT_PACKAGE`
- `TOP_INVOCATION_EVIDENCE`

Each pass must stop after writing its handoff artifact. The runner validates the
handoff against the capsule before allowing the workflow to advance.

An OS process is not automatically an isolated LLM invocation. A process adapter
may execute useful work, but `runner-enforced` isolation requires invocation
evidence from a `llm-api` or `external-agent-runtime` adapter.

The built-in `llm-api` adapter is `scripts/adapters/llm_api_adapter.py`.
It reads the runner context package, performs one separate model/API request,
writes the handoff, and writes pass invocation evidence.

## Hard Checks

Required hard checks are executable commands. A required hard check with a
non-zero exit code is a blocking failure. A required hard check that is not run
is `not_verified`.

A required pass without a pass command and without adapter-provided model invocation evidence is also `not_verified`; a pre-existing handoff cannot make that pass look executed.

## Evidence Honesty

`scripts/top_protocol_runner.py` may prove hard-check execution and artifact
consistency. It may report `hard-check-verified` only after required hard
checks actually pass.

Runner-enforced role isolation requires external invocation evidence: separate
invocation ids, separate context ids, separate task capsules, context packages,
handoff artifacts, and adapter evidence proving fresh model/agent contexts.
The runner must not report `runner-enforced` unless it accepts external runner
evidence explicitly.

## Output Artifact

The runner writes a `runner-report` artifact. It records:

- runner status
- pass results
- hard-check results
- execution evidence
- delivery certification validation result
- limitations

The report is evidence. It is not a judicial verdict by itself.

After the runner report changes, `scripts/top_protocol_runner.py` refreshes
`run-state.json` unless `--skip-state-update` is used. Runner success can move
the run to `runner-verified` or later if judicial/certification evidence
already exists, but it still does not certify delivery complete by itself.
