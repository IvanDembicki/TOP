# Changelog

All significant changes to top-skill are recorded in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.1.0] — 2026-05-01

- Added migration canon refinements for residual responsibility, legacy composition, and target adaptation.
- Added Pull-Based Construction / Locality of Object Birth as a foundational ownership invariant.
- Strengthened Content/View constructor rules: one narrow owner access interface, no semantic injection through constructors, runtime props, slots, builders, callbacks, stores, services, child handles, or prebuilt fragments.
- Clarified that `RootContext` is only a root ownership/bootstrap marker and that TOP spec `props` are declarative metadata, not runtime props.
- Added validation catalog entries and checklists for pull-based construction, concrete controller exposure, pushed child composition, View child ownership, RootContext misuse, and spec/runtime props confusion.
- Clarified semantic child-output access method naming: names identify the child branch/output and do not require artificial `Handle`, `ViewHandle`, `Section`, or `slot` terminology.
- Strengthened internal controller/content access symmetry: controllers use content only through `IContentAccess`, content uses controllers only through `IControllerAccess`, and zero-contracts are empty owner-implemented interfaces rather than dummy runtime objects.
- Updated migration, generation, target adaptation, node-model, functional-composition, validation, onboarding, and examples to align with the new ownership rules.

## [1.0.1] — 2026-04-24

- Switched license from CC BY-NC 4.0 to MIT
- Removed license gate from SKILL.md and onboarding
- Restructured repository: skill moved to `top-skill/` subfolder
- Added ENTRY_POINT.md for task mode selection
- Added root AGENTS.md and README as repository routers
- Moved Workflow A/B into task-modes.md as mode execution steps
- Converted all agent files to XML-tag structure
- Added `<investigate_before_answering>`, `<use_parallel_tool_calls>`, `<avoid_over_engineering>` constraints
- Fixed email consistency across skill.json and LICENSE.md
- Fixed broken reference in contracts/agent-output-contracts/README.md

## [1.0.0] — 2026-04-20

First stable release.
