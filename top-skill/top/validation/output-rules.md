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
- Migration-mode project outputs include `MIGRATION_WORKFLOW.json`,
  `MIGRATION_PLAN.md`, `MIGRATION_STATUS.md`, and `MIGRATION_LOG.md` when TOP
  artifacts are created or changed.
- Ready output has no unresolved blocking blind spots.

## Blocking violations

- Missing `top/spec.json`.
- Missing `top/artifact-manifest.json`.
- Missing `top/modes/mode-manifest.json`.
- Missing validation rules for a ready claim.
- Empty required artifact.
- Invalid JSON in a structured contract artifact.
- Ready claim while validation failed or did not run.
- Migration output changes TOP artifacts without a current workflow JSON, plan,
  status file, and append-only log.

