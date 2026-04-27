# Validation Report

- Version: 1.0.0
- Release status: stable
- Validator: pass
- CLI regression suite: pass
- Sensitive-data regression suite: pass
- Stable modes covered by examples: 5/5
- Stable CLI scope: `validate`, `check-output`, `demo`, `create`, `convert`, `update`, `compare`, `rollback`
- Experimental CLI scope: `merge`
- Broken local links: 0
- Schema findings: 0
- Security proof case present: yes

## Stable mode coverage

- CreateNewSkillMode -> `top/examples/create-new-skill-end-to-end/`
- ConvertLegacySkillMode -> `top/examples/convert-legacy-skill-before-after/`
- UpdateExistingSkillMode -> `top/examples/update-existing-skill-partial-case/`
- CompareSkillMode -> `top/examples/compare-skill-end-to-end/`
- RollbackMode -> `top/examples/rollback-skill-end-to-end/`

## Security proof

- `top/examples/convert-sensitive-legacy-skill-blocked/`
- `scripts/test_sensitive_cases.py`

## Release gates executed

1. `python scripts/validate_top_skill_factory.py . --report onboarding/schema-validation-report.md`
2. `python scripts/test_cli_workflows.py`
3. `python scripts/test_sensitive_cases.py`

This report reflects the current repository snapshot only.