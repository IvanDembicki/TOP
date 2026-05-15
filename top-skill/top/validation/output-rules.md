# Output Validation Rules

## Checks

- Required artifacts exist.
- Required artifacts are not empty placeholders.
- JSON artifacts parse.
- Version numbers are synchronized across `skill.json`, `release-metadata.json`,
  `hydration-manifest.json`, `SKILL.md`, `README.md`, `CHANGELOG.md`, and
  `top/spec.json`.
- Hydration manifest references exist.
- Mode manifest does not claim unsupported modes as stable.
- Artifact manifest required paths exist.
- Workflow contract files exist and are hydrated:
  `workflow/enforcement-evidence-model.md`, activation and operating
  procedure, task capsule format, handoff artifact format, role packs, and
  orchestrator protocol.
- Execution evidence, task capsule, handoff artifact, agent workflow, run
  state, validation report, delivery certification, and migration workflow
  schemas parse when present.
- Runner workflow, runner report, context package, and pass invocation evidence
  schemas parse when present.
- Certification snapshot schema parses when present.
- LLM API adapter contract and script exist when `llm-api` adapter evidence is
  claimed.
- Repair pass contract exists when a run contains repair pass evidence.
- Repair artifact writes are listed as task-capsule `artifactWriteRequests`,
  materialized only to exact allowed refs, and recorded as invocation-evidence
  `artifactWrites`.
- Delivery certification procedure and script exist when a run reports
  `deliveryStatus: complete`.
- LLM smoke run packages created by `scripts/create_orchestration_run.py
  --llm-smoke` use concrete context slices, `llm-api` pass commands, and
  portable hard-check command refs.
- Runner workflow hard checks use portable structured command refs when they
  need skill-relative scripts.
- Required judicial and certification pass context packages do not contain
  placeholder context slices or empty input references.
- Orchestration run packages follow `workflow/run-package-layout.md` when they
  are created.
- Orchestration run packages can derive `run-state.json` with
  `scripts/update_orchestration_state.py`; run state is not a substitute for
  delivery certification.
- Runner and certification scripts refresh `run-state.json` automatically after
  writing evidence-changing artifacts unless `--skip-state-update` is used.
- `scripts/validate_orchestration_run.py` checks one run package as a whole and
  reports `RUN_VALID certified`, `RUN_VALID not-certified`, `RUN_STALE`, or
  `RUN_INVALID`.
- `scripts/run_orchestration_workflow.py` runs the ordered create, runner,
  certification, snapshot verification, and final verifier sequence for one
  run package.
- Driver exit code `0` is not a delivery verdict by itself; final reports must
  name the verifier status and `deliveryStatus`.
- Delivery-affecting implementation, validation, repair, and certification
  follow `workflow/activation-and-operating-procedure.md` before work begins.
- `scripts/validate_execution_evidence.py` imports and its smoke fixtures prove
  that protocol-only `not-certified` is allowed while false delivery
  `complete` is rejected.
- `scripts/top_protocol_runner.py` imports and its smoke fixture proves that a
  valid runner workflow can run a required hard check, produce
  `hard-check-verified`, and avoid false `runner-enforced` evidence.
- `scripts/certify_orchestration_run.py` imports and can produce complete
  delivery certification only from runner-enforced evidence, hard-check
  evidence, and independent judicial handoff evidence.
- Certification snapshots can be verified with `--verify-snapshot`; stale
  snapshots block treating an existing complete certification as current.
- `scripts/update_orchestration_state.py` imports and can derive `certified`
  and `stale` states from run-package artifacts.
- `scripts/validate_orchestration_run.py` imports and can accept a valid
  certified smoke run while rejecting stale artifact drift.
- `scripts/validate_orchestration_regressions.py` imports and proves known
  false-complete scenarios stay invalid: missing judicial handoff, required
  hard check `not_verified`, schema-validated false complete, process-only
  false complete, repair without post-repair judicial validation, repair
  self-certification, and stale snapshots.
- `scripts/validate_repair_artifact_fixture.py` imports and rejects invalid
  repair artifact dogfood output while accepting the repaired fixture shape.
- `scripts/run_orchestration_workflow.py` imports and can drive a process-backed
  two-pass smoke run to `RUN_VALID not-certified` without upgrading process
  evidence into runner-enforced delivery.
- Migration-mode project outputs include `MIGRATION_WORKFLOW.json`,
  `MIGRATION_PLAN.md`, `MIGRATION_STATUS.md`, and `MIGRATION_LOG.md` when TOP
  artifacts are created or changed.
- Ready output has no unresolved blocking blind spots.
- Protocol-only output must not claim `runner-enforced` isolation.
- Schema validation and hard checks are not role isolation.
- Delivery `complete` has `executionIsolationLevel: runner-enforced`,
  `verificationEvidenceLevel: hard-check-verified`, a valid independent
  judicial handoff artifact, and no required gate with `fail` or `not_verified`
  status.
- Final audit does not use `complete`, `certified`, `delivery complete`, or
  equivalent wording unless the delivery evidence gate passes.

## Blocking violations

- Missing `top/spec.json`.
- Missing `top/artifact-manifest.json`.
- Missing `top/modes/mode-manifest.json`.
- Missing `workflow/enforcement-evidence-model.md`.
- Missing `workflow/activation-and-operating-procedure.md`.
- Missing reusable `top/schemas/fragments/execution-evidence.schema.json`.
- Missing `scripts/validate_execution_evidence.py`.
- Missing task capsule or handoff artifact schema when workflow evidence is
  claimed.
- Missing `workflow/runner-contract.md`, `top/schemas/runner-workflow.schema.json`,
  `top/schemas/runner-report.schema.json`, or `scripts/top_protocol_runner.py`
  when runner evidence is claimed.
- Missing `workflow/pass-invocation-contract.md`,
  `top/schemas/context-package.schema.json`, or
  `top/schemas/pass-invocation-evidence.schema.json` when runner-enforced
  isolation is claimed.
- Missing `workflow/llm-api-adapter-contract.md` or
  `scripts/adapters/llm_api_adapter.py` when `llm-api` adapter evidence is
  claimed.
- Missing `workflow/repair-pass-contract.md` when repair pass evidence is
  claimed.
- Missing `workflow/delivery-certification-procedure.md` or
  `scripts/certify_orchestration_run.py` when delivery certification is
  claimed.
- Missing `top/schemas/certification-snapshot.schema.json` when certification
  snapshots are claimed.
- Missing `workflow/run-state-machine.md`,
  `top/schemas/run-state.schema.json`, or
  `scripts/update_orchestration_state.py` when run state is claimed.
- Missing `scripts/validate_orchestration_run.py` when run package validity is
  claimed.
- Missing `scripts/validate_orchestration_regressions.py` when regression
  protection against false delivery complete is claimed.
- Missing `scripts/validate_repair_artifact_fixture.py` when repair artifact
  dogfood evidence is claimed.
- Missing `scripts/run_orchestration_workflow.py` when an ordered orchestration
  workflow driver is claimed.
- Missing `workflow/run-package-layout.md` or
  `scripts/create_orchestration_run.py` when a new orchestration run package is
  created.
- Missing validation rules for a ready claim.
- Empty required artifact.
- Invalid JSON in a structured contract artifact.
- Ready claim while validation failed or did not run.
- `runner-enforced` claim without external runner evidence.
- Required delivery pass reported as `pass` without a pass command or
  adapter-provided model invocation evidence.
- Delivery complete after repair without a later independent judicial handoff
  over post-repair artifacts.
- Delivery complete after repair artifact writes when the final judicial
  handoff did not read the repaired refs.
- Repair artifact write to a ref not listed in task-capsule
  `artifactWriteRequests`.
- Repair pass attempts to validate or certify its own output.
- Required judicial/certification pass context contains placeholder context or
  empty input references.
- Delivery complete claim without runner-enforced isolation, hard-check-verified
  evidence, independent judicial handoff artifact, or explicit files/checks/
  violation classes evidence.
- Stale certification snapshot while delivery is treated as current.
- Required hard-check gate is `fail` or `not_verified` while delivery is
  reported as complete.
- Migration output changes TOP artifacts without a current workflow JSON, plan,
  status file, and append-only log.
