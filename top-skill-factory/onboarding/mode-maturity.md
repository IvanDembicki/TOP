# TopSkillFactory Mode Maturity

This file explains how to interpret mode readiness in TopSkillFactory 1.0.0.

## Stable

These modes are part of the stable 1.0 contract and have the strongest evidence base.

- CreateNewSkillMode
- ConvertLegacySkillMode
- UpdateExistingSkillMode
- CompareSkillMode
- RollbackMode

Expected use:
- real authoring and conversion flows
- contract-driven updates
- bounded compare and rollback workflows

## Experimental

These modes are implemented and partly evidenced, but they are not part of the stable 1.0 contract.

- ForkExperimentMode
- MergeSkillsMode
- DocumentationMode
- RefactorSkillMode
- SplitSkillMode

Expected use:
- targeted restructuring work
- bounded experimentation
- guided author-side iteration with review

## Planned

These modes exist to reserve architecture, contracts, or future operational surfaces.

- RuntimeMonitorMode
- MarketplaceValidationMode
- CompatibilityCheckMode
- DeprecationMode
- ReplayDebuggerMode

Expected use:
- roadmap planning
- future infrastructure alignment
- early contract discussion

They should not be described as equally mature execution paths.

## Stable contract note

The stable 1.0 contract includes Create, Convert, Update, Compare, and Rollback only. `MergeSkillsMode` remains experimental.