# Final Audit Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
result:
details:
validation_signals:
next_step:

## Required fields

goal:
- final decision

context:
- artifact_scope
- task_mode
- behavior_preservation_plan

result:
- final_status
- canonicality_statement
- core_violations
- accepted_deviations
- skill_convention_violations
- workflow_gaps

details:
- execution_evidence_audit
- validator_audit_check
- incremental_validation_audit
- controller_tree_audit
- separation_of_powers_audit
- delivery_certification_audit
- remaining_risks
- behavior_preservation_gate
- unresolved_limits

validation_signals:
- review_checklist_passed
- validation_passed
- mode_pipeline_completed
- test_covered_behavior_preserved
- no_unresolved_drift

next_step:
- readiness_status
- recommended_followup

## Rules

- Final audit cannot override failed validation
- Final audit audits the validator. It must verify validation ran after
  generation or repair, inspected current artifacts, listed files inspected,
  checked current canon invariants, did not rely on generator self-validation
  claims, closed or routed all rejection tickets, and did not use previous agent
  claims as proof.
- Final audit must verify delivery certification against
  `top/schemas/delivery-certification.schema.json` when a workflow claims
  delivery `complete`. The certification must reference an independent judicial
  validation report and valid independent judicial handoff artifact, must prove
  generation/repair and validation were separate runner-enforced passes, and
  must prove required hard checks passed.
- Final audit must audit `executionEvidence` from
  `workflow/enforcement-evidence-model.md`: `executionIsolationLevel` and
  `verificationEvidenceLevel` are separate evidence axes and cannot be
  upgraded by prose.
- Protocol-only mode may be useful and valid as work output, but it is not
  certified delivery.
- Final audit must not use `complete`, `certified`, `delivery complete`, or
  equivalent wording unless delivery certification satisfies runner-enforced
  execution isolation, hard-check-verified validation evidence, a valid
  independent judicial handoff artifact, and no required gate with `fail` or
  `not_verified` status.
- Schema validation is not role isolation. Hard checks are not role isolation.
- A hard check result without a judicial handoff is evidence, but not a judicial
  verdict. A judicial handoff without required hard-check evidence cannot
  certify delivery complete.
- `separation_of_powers_audit` must fail if the same pass acted as executive,
  judicial validator, final auditor, and delivery certifier for the same
  artifacts.
- `delivery_certification_audit` must fail if any required blocking gate is
  missing, failed, or not verified.
- Accepting validation that lacks artifact evidence or was contaminated by
  executor claims is `WF-026`.
- `incremental_validation_audit` must verify that required micro-check,
  meso-check, and macro-check gates exist for the relevant workflow and that no
  unresolved `REVIEW_REQUIRED` or `FAIL` checkpoint remains.
- `controller_tree_audit` must verify that validation checked
  `generated-controller-runtime-shape`, `controller-tree-topology`, and absence
  of `CORE-037` for generated TOP controller artifacts.
- Final audit cannot mark the result ready if `core_violations` is non-empty
- Final audit cannot mark the result ready if `accepted_deviations` contains a
  core violation or migration waypoint
- Final audit cannot mark the result ready if unresolved drift remains between spec, prompts, project-local TOP artifacts, and materialized implementation artifacts
- Final audit cannot mark a migrated scope ready if test-covered legacy behavior lacks a Behavior Preservation Plan, prompt representation, or TOP-compatible test coverage
- Final audit cannot mark a migrated scope ready unless validation confirmed the
  dedicated migration branch, the first git safety gate log entry, no migration
  writes before branch confirmation, no unrelated file modifications, no
  unauthorized push, and no unauthorized local commit.
- For non-migration tasks, `behavior_preservation_plan`, `behavior_preservation_gate`, and `test_covered_behavior_preserved` must be explicitly `not_applicable`
- Violation types must be separated into three categories
- Reporting `pass`, `ready`, or `ready_for_use` with remaining core violations
  or accepted core deviations is `WF-011`
- `readiness_status` must be one of:
  `not_ready`, `ready_for_generation`, `ready_for_integration`,
  `ready_for_manual_QA`, or `ready_for_production_candidate`.
- Do not use unqualified `ready_for_use`. A spec/prompt model can be
  `ready_for_generation`; generated code can be `ready_for_integration` only
  after post-generation architectural validation; integrated app changes can be
  `ready_for_manual_QA`; production candidate requires runtime/behavior
  validation evidence.
- Labeling a core violation accepted/temporary/deferred/waypoint without a
  TOP-canon-defined migration waypoint is `WF-012`
- The final verdict must be explicit
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.
