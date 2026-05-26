# Final Migration Report Contract

The final report is an evidence index and decision record. It must not inflate partial or unverified work into complete migration.

## Required Sections

`Scope`
: Migrated project/scope, excluded areas, profile, dates/checkpoint range, root node.

`Tree Summary`
: Root, child branches, leaf count, blocked nodes, residual nodes, black-box nodes, connector nodes, candidate library nodes.

`Readiness Summary`
: Counts by `decompositionStatus`, `behaviorStatus`, `topValidationStatus`, `integrationStatus`, and `readinessStatus`.

`Behavior Evidence`
: Tests/checks run, passing/failing/not-run areas, characterization evidence, manual scenarios, limits.

`TOP Validation Evidence`
: Independent validator identity, files checked, rules checked, pass/fail/not-verified status, contaminated validations, rejection tickets.

`Component Inventory`
: Preserved local components, external components, black-box components, TOP candidates, residual components.

`Residuals and Deviations`
: Accepted temporary deviations, exact locations, reason, target repair direction, expiry condition.

`Repair and Rollback History`
: Failed gates, repairs attempted, repeated failures, rollback anchors used or available.

`Developer Decisions`
: Questions asked, answers received, unresolved decisions.

`Final Decision`
: One of:

- `complete_verified`
- `complete_structural_only`
- `partial_ready`
- `blocked`
- `draft_unverified`

## Forbidden Claims

Do not claim:

- complete migration when TOP validation is missing but required;
- behavior preserved when tests/traces/manual scenarios are missing;
- TOP-valid when validation was done by the same agent that generated/repaired the artifact;
- external component internals are TOP-compliant;
- residual legacy code is canonical TOP.

## Decision Meanings

`complete_verified`
: Required structural, behavior, integration, and independent TOP validation evidence exists.

`complete_structural_only`
: Tree structure was produced, but behavior and/or TOP validation evidence is incomplete by profile.

`partial_ready`
: Some branches are verified; others are blocked, draft, residual, or not verified.

`blocked`
: Migration cannot continue without developer decision, missing evidence, failed validation, or repeated repair failure.

`draft_unverified`
: Exploratory output only. Useful for review, not acceptance.
