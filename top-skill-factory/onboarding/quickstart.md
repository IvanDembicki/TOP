# TopSkillFactory Quick Start

## 1. What it is

TopSkillFactory is a TOP-based system for turning loose prompt-skills into structured, validated skill artifacts.

## 2. Stable release scope

This stable release treats the following commands as stable bounded workflows:

- `validate`
- `check-output`
- `demo`
- `create`
- `convert`
- `update`
- `compare`
- `rollback`

`merge` remains experimental. Planned and skeletal modes are excluded from the stable contract.

## 3. Startup update check

Use:

```powershell
pwsh ./top-skill-factory.ps1 check-updates
```

If you have a newer release metadata file to compare against:

```powershell
pwsh ./top-skill-factory.ps1 check-updates --manifest .\release-metadata.json
```

## 4. Release gates

Read:

1. `RELEASE_CRITERIA.md`
2. `VALIDATION_REPORT.md`
3. `top/artifact-manifest.json`
4. `top/modes/mode-manifest.json`

## 5. Run validation

```powershell
pwsh ./top-skill-factory.ps1 validate
py -3 scripts/test_cli_workflows.py
py -3 scripts/test_sensitive_cases.py
```

## 6. Build the demo

```powershell
pwsh ./top-skill-factory.ps1 demo --out .\tmp\demo-output
```

## 7. Security proof

See `top/examples/convert-sensitive-legacy-skill-blocked/` for the blocked sensitive-import case.

## Release check

Run `python scripts/release_check.py` for the full release gate pass.
