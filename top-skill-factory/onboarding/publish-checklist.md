# Publish Checklist

## Repository hygiene

- [ ] Run `pwsh ./top-skill-factory.ps1 check-updates`
- [ ] Run `python scripts/validate_top_skill_factory.py . --report onboarding/schema-validation-report.md`
- [ ] Run `python scripts/test_cli_workflows.py`
- [ ] Run `python scripts/test_sensitive_cases.py`
- [ ] Confirm `onboarding/schema-validation-report.md` shows `Status: pass`
- [ ] Confirm there are no local absolute links in release-facing docs
- [ ] Confirm there are no temporary output folders in the release snapshot

## Public entrypoints

- [ ] `README.md` explains the product in the first screen
- [ ] `SKILL.md` is concise and accurate
- [ ] `VALIDATION_REPORT.md` reflects the current snapshot
- [ ] Root launchers exist:
  - [ ] `top-skill-factory.ps1`
  - [ ] `top-skill-factory.cmd`

## Stable release messaging

- [ ] Present this as `TOP Skill Factory 1.0.0 stable bounded skill package`
- [ ] Keep `merge` explicitly experimental
- [ ] Do not claim full runtime orchestration
- [ ] Do not claim compiler-grade enforcement
- [ ] Lead with the problem:
  - messy skills
  - hidden logic
  - uncontrolled drift
  - untraceable updates

## Demo readiness

- [ ] Run `pwsh ./top-skill-factory.ps1 demo --out .\tmp\demo-output`
- [ ] Run `pwsh ./top-skill-factory.ps1 check-output .\tmp\demo-output\demo-output`
- [ ] Confirm the demo folder contains:
  - [ ] `before.md`
  - [ ] `demo-output/normalized-conversion-input.json`
  - [ ] `demo-output/blind-spot-report.json`
  - [ ] `demo-output/conversion-report.json`
  - [ ] `demo-output/final-decision.json`
  - [ ] `demo-output/converted-skill/top/...`

## Launch assets

- [ ] Quick start is current
- [ ] Release notes are current
- [ ] Demo script is current
- [ ] Historical alpha-era reports are archived, not presented as current release evidence

## Reuse outside this repo

- [ ] If this pattern should be copied into another product, start from `templates/startup-update-check/integration-checklist.md`
