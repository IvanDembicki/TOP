# Demo Script

## 30-second version

1. Show a loose legacy prompt skill in one file.
2. Say: `This is still usable, but it already has hidden logic and unsafe assumptions.`
3. Run:

```powershell
pwsh ./top-skill-factory.ps1 demo --out .\tmp\demo-output
```

4. Open:
   - `before.md`
   - `demo-output/normalized-conversion-input.json`
   - `demo-output/blind-spot-report.json`
   - `demo-output/conversion-report.json`
   - `demo-output/final-decision.json`
   - `demo-output/converted-skill/top/`

5. Say:
   - `The point is not blind code generation.`
   - `The point is governed conversion into explicit artifacts.`
   - `Unsafe assumptions become visible.`
   - `The result stays draft until readiness is actually justified.`

## 2-minute version

### Setup

Run:

```powershell
pwsh ./top-skill-factory.ps1 validate
pwsh ./top-skill-factory.ps1 demo --out .\tmp\demo-output
```

### Talking points

1. `TopSkillFactory is for when a skill stopped being just a prompt.`
2. `It converts loose workflow text into explicit contracts, validation surfaces, and mode structure.`
3. `It does not hide uncertainty behind fake ready states.`
4. `It can validate both the repository and generated workflow outputs.`
5. `It now has bounded executable workflows, not just design docs.`

### Files to highlight

- `SKILL.md`
- `README.md`
- `top/artifact-manifest.json`
- `scripts/top_skill_factory_cli.py`
- `scripts/test_cli_workflows.py`
- `.\tmp\demo-output\demo-output\validation-report.md`

## Short screen-recording outline

1. Show repo root
2. Show `README.md`
3. Show `before.md`
4. Run `demo`
5. Open `conversion-report.json`
6. Open `final-decision.json`
7. Open generated `top/spec.json`
8. Open `validation-report.md`
9. End on the generated bundle tree
