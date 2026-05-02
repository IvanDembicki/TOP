# Release Notes

## 1.1.1 - 2026-05-02

- Normalized TOP Prompt Cleaner display naming in factory onboarding and conversion demo artifacts.
- Synchronized release metadata, TOP spec, changelog, release notes, and validation report version metadata to 1.1.1.

## 1.0.0

This stable release freezes the bounded workflow surface and promotes the validator and regression suites to release gates.

### Stable bounded workflows

- `validate`
- `check-output`
- `demo`
- `create`
- `convert`
- `update`
- `compare`
- `rollback`

### Experimental

- `merge`

### Added or tightened

- `RELEASE_CRITERIA.md`
- `VALIDATION_REPORT.md`
- `stable_workflow_contract`
- `workflow_draft_contract`
- generated output provenance via `top/provenance.json`
- security-sensitive conversion proof case
- release-grade validator checks for links, prompt references, stable mode coverage, version consistency, and workflow outputs
- richer workflow bundle surface for stable and draft CLI outputs

### Still out of scope

- autonomous runtime orchestration
- marketplace validation as a stable feature
- roadmap modes as part of the stable release contract
