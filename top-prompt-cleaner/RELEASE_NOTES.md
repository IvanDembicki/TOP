# Release Notes

## 1.0.0 - 2026-04-26

- **Stable release.** All single-prompt cleaning contracts finalized and machine-verified.
- Added `$id` to all 15 schemas; `$ref` resolution now works across schemas in ajv.
- Strengthened `final_output.schema.json`: `oneOf` for `cleaned_prompt`/`target_style_output`; property-level `false` schemas forbid cross-contamination between terminal states.
- Created 5 new schemas: `conflict_report`, `mode_routing_result`, `normalized_input`, `final_decision_signal`, `clarification_state`.
- Created `user_response.schema.json`; clarification round-trip now fully machine-verifiable.
- Added full `final_output` JSON block for every terminal state in examples (ready, blocked, escalated).
- Validator upgraded: Ajv2020 for draft 2020-12 support; unknown JSON blocks treated as failures; markdown link checking added.
- Added `docs/usage.md`, `docs/troubleshooting.md`, `docs/contracts.md`, `docs/security.md`.
- Added `top/examples/README.md` with index table.
- Added `.github/workflows/validate.yml` CI workflow.
- Added `.gitignore` excluding `node_modules/`.
- Moved deprecated `FrontendStyle` artifacts to `docs/migration/`; `batch_clean.md` to `top/roadmap/`.
- All 77 JSON blocks in examples pass validation; 30 repo checks pass.

## 0.3.1-alpha - 2026-04-26

- Added `extraction_result.schema.json` to separate intermediate extractor output from final `structured_prompt`.
- Synchronized invariants across `spec.json` and `core-invariants.md` (16 invariants after startup update check alignment).
- Fixed execution order: `SensitiveDataDetector` strictly before `ComplexityDetector`.
- Resolved `final_output.schema.json` to support `target_style_output` alongside `cleaned_prompt`.
- Fixed `complexity_report` recommendation enum in all examples.
- Added medium vs high complexity boundary definition.
- Replaced legacy startup version banner with standardized startup update check metadata and rule.

## 0.3.0-alpha - 2026-04-26

- Renamed `FrontendStyleMode` to `TargetLLMStyleMode`.
- Added `SensitiveDataDetector` and `ClarificationController` nodes.
- Added model profiles: `claude`, `gpt`, `generic`, `custom`.
- Added 4 new schemas: `final_output`, `validation_result`, `target_style_output`, `sensitive_data_report`.
- Expanded examples to 10 covering all terminal states.
- Added product layer: landing, user-flow, output-layout.

## 0.2.0-alpha - 2026-04-25

- Rewrote `spec.json` with proper tree structure and 9 invariants.
- Expanded all mode and prompt files from stubs to full specifications.
- Added `SKILL.md` entrypoint.
- Added `diff.schema.json`, `complexity_report.schema.json`, `clarification_request.schema.json`.
- Added 2 worked examples: quick-clean and escalation.
