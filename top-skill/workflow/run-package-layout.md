# Orchestration Run Package Layout

## Purpose

An orchestration run package is the canonical filesystem container for one
top-skill 2.0 workflow run. It makes task capsules, handoffs, runner reports,
validation reports, delivery certification, logs, and scratch evidence
discoverable without relying on chat memory.

When to create or use a run package is defined in
`workflow/activation-and-operating-procedure.md`.

## Canonical Path

```text
top/orchestration/<workflow-id>/<run-id>/
```

## Required Layout

```text
top/orchestration/<workflow-id>/<run-id>/
  RUN_README.md
  run-state.json
  capsules/
    <pass-id>.task-capsule.json
  contexts/
    <pass-id>.context-package.json
  handoffs/
    <pass-id>.handoff.json
  invocations/
    <pass-id>.invocation-evidence.json
  runner/
    runner-workflow.json
    runner-report.json
  reports/
    validation-report.json
    delivery-certification.json
    certification-snapshot.json
    final-audit.md
  logs/
    RUN_LOG.md
  scratch/
```

## Ownership

- Orchestrator owns `RUN_README.md`, `runner/runner-workflow.json`, and task
  capsules.
- Run state is derived from run artifacts and written to `run-state.json` by
  `scripts/update_orchestration_state.py`.
- Runner owns context packages under `contexts/` and invocation evidence under
  `invocations/`, unless an external adapter writes invocation evidence before
  the runner records its report.
- Each pass owns exactly one handoff artifact under `handoffs/`.
- Runner owns `runner/runner-report.json`.
- Judicial validation owns `reports/validation-report.json`.
- Certification/final audit owns `reports/delivery-certification.json` and
  `reports/certification-snapshot.json` and `reports/final-audit.md`.
- `logs/RUN_LOG.md` is append-only.
- `scratch/` is temporary evidence storage and must not be required for final
  certification unless referenced from a report.

## Status Semantics

A scaffolded run package starts as `protocol-defined` and `not-certified`.
It must not be reported as `runner-enforced`, `hard-check-verified`, or
delivery `complete` until the required runner, judicial, hard-check, and
delivery evidence exists.

The process state is explicit in `run-state.json`. Valid states are defined in
`workflow/run-state-machine.md`:

```text
scaffolded -> passes-executed -> runner-verified -> judicial-validated -> certified
```

`not-certified`, `stale`, and `failed` record blocked or invalid delivery
states. The state artifact is evidence indexing, not a delivery verdict.

## LLM Smoke Profile

`scripts/create_orchestration_run.py --llm-smoke` creates a bounded two-pass
run package for testing real `llm-api` invocation evidence:

- `executive` writes one handoff and does not edit project files.
- `judicial` reads the executive handoff and invocation evidence, then writes
  an independent judicial handoff.
- The runner workflow uses portable `python-script` refs to
  `scripts/adapters/llm_api_adapter.py`.
- `top-skill-quick-validate` is configured as a required hard check.

The LLM smoke profile is not a delivery-complete claim. It exists to prove or
reject runner-enforced isolation evidence under a real API-backed run. Without
`TOP_LLM_API_KEY` or `OPENAI_API_KEY` and `TOP_LLM_MODEL`, it remains
not-certified.

## Handoff Rule

One pass returns one handoff. A pass must not write another pass's handoff,
advance the workflow, validate its own output, repair its own validation result,
or certify delivery unless its task capsule explicitly grants that authority.

## Runner Rule

The runner workflow lists pass capsules, expected handoff paths, hard checks,
and delivery certification references. The runner report is evidence for
judicial validation, not a judicial verdict by itself.

## Certification Rule

After runner evidence and judicial handoff exist, run:

```text
python -B scripts/certify_orchestration_run.py --root top/orchestration/<workflow-id>/<run-id>
```

This writes the validation report, delivery certification, and final audit for
the run package. It may report `deliveryStatus: complete` only under the
delivery law in `workflow/enforcement-evidence-model.md` and the procedure in
`workflow/delivery-certification-procedure.md`.

To check whether the certification still matches current artifacts, run:

```text
python -B scripts/certify_orchestration_run.py --root top/orchestration/<workflow-id>/<run-id> --verify-snapshot
```

`SNAPSHOT_STALE` means at least one checked artifact changed after
certification, so the delivery certification must be treated as stale until
the run is re-certified.

After runner, judicial, certification, or snapshot evidence changes, update the
state artifact. Runner and certifier scripts do this automatically unless
`--skip-state-update` is used:

```text
python -B scripts/update_orchestration_state.py --root top/orchestration/<workflow-id>/<run-id>
```

To validate the current run package as one evidence object, run:

```text
python -B scripts/validate_orchestration_run.py --root top/orchestration/<workflow-id>/<run-id>
```

The verifier is read-only. It reports `RUN_VALID certified`,
`RUN_VALID not-certified`, `RUN_STALE`, or `RUN_INVALID`.

To run the standard ordered workflow driver for an existing package, run:

```text
python -B scripts/run_orchestration_workflow.py --run-root top/orchestration/<workflow-id>/<run-id> --execute-passes --execute-hard-checks
```

The driver coordinates runner, certification, snapshot verification, and final
verification. It must not invent a readiness status; its final status is the
read-only verifier result.

Driver exit semantics:

- exit `0` means the final verifier returned `RUN_VALID certified` or
  `RUN_VALID not-certified` and the driver saw no internal step error;
- exit `1` means the final verifier returned `RUN_STALE`;
- exit `2` means the final verifier returned `RUN_INVALID` or the driver could
  not complete the ordered sequence.

The exit code is operational evidence only. Human-facing readiness wording must
still name the verifier status and `deliveryStatus`.
