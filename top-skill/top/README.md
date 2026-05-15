# top/

This folder is the self-governance layer for `top-skill`.

It exists so `top-skill` is governed by the same rules it applies to other
systems: explicit structure, artifact contracts, mode maturity, validation
rules, schemas, and traceability.

## Contents

- `spec.json` — skill execution model, root tree, invariants, and validation model
- `artifact-manifest.json` — readiness contracts for the skill package and
  migration project outputs
- `modes/mode-manifest.json` — supported mode maturity and routing boundaries
- `schemas/` — machine-readable schemas for structured project artifacts
- `../workflow/` — protocol-layer contracts for execution evidence, task
  capsules, handoff artifacts, role packs, activation, orchestrator control,
  and runner control
- `shared-rules/` — cross-cutting rules for skill maintenance and evolution
- `validation/` — output and readiness validation rules
- `provenance.json` — evidence for where this governance layer came from

## Source-of-truth rules

- Required artifacts must not be empty placeholders.
- Structured workflow artifacts use JSON when a schema exists.
- Examples and previous outputs are evidence, not authority.
- When a schema and prose disagree, schema and validation rules win.
- A ready claim is invalid while required validation has not run.
- A delivery-complete claim is invalid without the evidence required by
  `workflow/enforcement-evidence-model.md`.
- Delivery-affecting work follows `workflow/activation-and-operating-procedure.md`
  before implementation, validation, repair, or certification begins.
- A runner report is evidence for validation, not a replacement for judicial
  verdict or delivery certification.
- Runner-enforced isolation requires context packages and pass invocation
  evidence from a supported LLM/API or external agent runtime adapter.
- LLM API pass execution is governed by
  `workflow/llm-api-adapter-contract.md`.
- Repair pass authority and post-repair validation are governed by
  `workflow/repair-pass-contract.md`.
- A new orchestration run package lives under
  `top/orchestration/<workflow-id>/<run-id>/` and starts as
  `protocol-defined` / `not-certified`.
- Run package process state is derived into `run-state.json` by
  `scripts/update_orchestration_state.py`; it indexes evidence state but does
  not replace delivery certification.
- Run package validity is checked read-only by
  `scripts/validate_orchestration_run.py`; it does not rewrite run artifacts.
- False delivery-complete scenarios are guarded by
  `scripts/validate_orchestration_regressions.py`.
- Ordered run execution may be driven by
  `scripts/run_orchestration_workflow.py`; the driver still reports the final
  read-only verifier status as the readiness claim.
