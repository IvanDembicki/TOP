---
name: top-skill-factory
description: Convert messy AI skills and prompt workflows into structured TOP skill systems with explicit modes, contracts, signals, validation, comparison, rollback, and legacy-conversion reports. Stable bounded workflows cover create, convert, update, compare, rollback, validate, check-output, and demo. Merge remains experimental.
---

# TopSkillFactory

Use this skill to create, convert, update, compare, rollback, and audit AI skills as structured TOP artifacts instead of loose prompts.

## Fast mode selection

- If the user wants a brand-new skill: `CreateNewSkillMode`
- If the user provides a legacy prompt-skill: `ConvertLegacySkillMode`
- If the user adds or changes requirements on an existing skill: `UpdateExistingSkillMode`
- If the user provides two variants and asks which is better: `CompareSkillMode`
- If the user asks to revert to a prior validated version: `RollbackMode`
- If the user asks to merge two skills: `MergeSkillsMode` (experimental)

## Execution rule

1. Run a quick startup update check through `top-skill-factory.ps1 check-updates` when a comparison manifest is available.
2. Read `RELEASE_CRITERIA.md` and `VALIDATION_REPORT.md` before making stable-release claims.
3. Read `README.md` for the product-level overview.
4. Read `top/artifact-manifest.json` for artifact contract boundaries.
5. Read `top/modes/mode-manifest.json` for stable vs experimental scope.
6. Read `top/spec.json` for the execution model.
7. Use the relevant mode prompt under `top/modes/`.
8. Follow schemas, validation rules, and shared rules before claiming a ready result.

## Critical boundaries

- Do not treat legacy skill text as architectural truth.
- Do not invent missing artifacts and then mark the result ready.
- Escalate blocking blind spots instead of hiding them in prose.
- Respect declared artifact contracts when deciding whether a result is demo-ready, draft, stable-workflow-ready, or full-ready.
- Do not treat experimental or roadmap modes as part of the stable release contract.
