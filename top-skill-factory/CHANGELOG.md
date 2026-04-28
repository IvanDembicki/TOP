# Changelog

## [1.1.0] — 2026-04-28

### Added

- **ExistingSolutionCheck gate** — mandatory check in `CreateNewSkillMode` that runs between `SkillDiscovery` and `SkillDesignController`.
  - Three modes: Skip, Quick Check (default), Deep Check.
  - Internal-first search protocol: internal inventory is always scanned before external candidates.
  - External search is gated on explicit user confirmation; declined search is recorded as `user_declined_external`.
  - Candidate evaluation matrix with coverage, gaps, TOP compatibility, adaptation effort, composability, and recommended action columns.
  - Six decision outcomes: Reuse, Adapt, Compose, Build, Reject, Skipped.
  - Build decisions require an explicit `build_justification` naming every reviewed candidate and the specific gap that disqualified it.
  - Composability assessment required whenever any candidate is a partial match.
  - Time-box rules: Quick Check 10 min, Deep Check 30 min.
  - New node: `top/prompts/nodes/existing-solution-check.md`.

- **ResearchForInsight** — optional standalone step, offered to the user after ExistingSolutionCheck in `CreateNewSkillMode` and at the start of `ConvertLegacySkillMode`.
  - Runs only on explicit user confirmation; never triggered automatically.
  - Produces a landscape report: known approaches, identified gaps, relevant patterns, open questions, sources reviewed.
  - Decision to run is the user's alone and does not depend on any prior pipeline result.
  - User-facing question is defined canonically in the node and must be adapted to the user's language.
  - Time-boxed to 60 minutes; partial findings delivered if limit is reached.
  - New node: `top/prompts/nodes/research-for-insight.md`.

### Changed

- `top/modes/create-new-skill-mode.md` — ExistingSolutionCheck inserted into the process flow; ResearchForInsight offered after ExistingSolutionCheck; routing rules added for each decision outcome; `SkillDesignController` is blocked when decision is Reuse or Reject; new invalid output conditions added.
- `top/modes/convert-legacy-skill-mode.md` — ResearchForInsight offered as the first step before conversion work begins.
- `top/spec.json` — `ExistingSolutionCheck` and `ResearchForInsight` added to the CoreControllers tree; `skill_version` bumped to 1.1.0.
- `release-metadata.json` — `current_version` bumped to 1.1.0; release notes updated.

### Validation

- `top/validation/output-rules.md` — two new blocking violations:
  - `CreateNewSkillMode` result presented without an `ExistingSolutionCheck` result.
  - Decision is `build` without a populated `build_justification`.

## [1.0.0] — initial stable release

First stable bounded release. Covers CreateNewSkillMode, ConvertLegacySkillMode, UpdateExistingSkillMode, CompareSkillMode, RollbackMode. Includes CLI workflows, validator coverage, regression tests, and security proof cases.
