# Changelog

All significant changes to top-skill are recorded in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.1.7] — 2026-05-03

- Clarified that `IContentAccess` is only the controller-to-content command/request boundary and must not be used as a data bag for view-model values, state flags, callbacks, or child-output handles.
- Clarified functional composition target materialization: a single public runtime input object/value must be the narrow content-to-controller owner access contract, not a merged `IContentAccess & IControllerAccess` props/data bundle.
- Clarified migration status for renderable controllers: they may be explicitly tracked as a known migration deviation, but are not TOP-conformant final structure and still report `CORE-026`.
- Added `CORE-027` for `IContentAccess` data bag misuse and extended validation, generation, migration, and checklist wording to detect the direction-confusion loophole.

## [1.1.6] — 2026-05-03

- Added runtime hydration protocol: `SKILL.md` is now the bootstrap and fallback entrypoint; the agent must hydrate from the installed skill filesystem directory on every invocation before applying any canon, validation rules, references, or prompts.
- Added `hydration-manifest.json` with tiered read paths (`always`, `task`, `full`); the agent reads only what each task requires while guaranteeing freshness of core files.
- Added `validation` and `migration` as explicit task tiers in the hydration manifest, covering the files previously declared absent in the first validation pass.
- Extended `rules/startup-update-check.md` with the runtime freshness and hydration policy, version check sequence, and explicit hydration failure reporting rule.
- Updated `release-metadata.json` with `runtime_freshness_strategy`, `hydration_manifest`, and `hydration_policy` fields.
- Extended `scripts/quick_validate.py` to require and validate the hydration manifest, its version, metadata linkage, tier structure, and file references.
- Added post-update reinstall notice to `README.md`; clarifies that restarting a session is insufficient and packages older than 1.1.6 must be reinstalled to enable hydration.

## [1.1.5] — 2026-05-02

- Added Controller Role Purity as a foundational invariant: controllers must remain non-renderable orchestration boundaries and must not become content-side or platform-renderable artifacts.
- Added `CORE-026` for controller role leakage and extended validation, review, generation, target adaptation, migration, and repair guidance to detect and correct renderable controllers.
- Clarified that target-required renderable entrypoints belong to Content/View or thin framework adapters, not to controller identity.

## [1.1.4] — 2026-05-02

- Added fresh validation/review requirements: agents must load current skill rules and re-read target artifacts in the current pass instead of relying on previous session reads.
- Clarified that a technology runtime input object/value is valid only when it is exactly the narrow owner access contract, not a general props/config/data/composition bag.
- Clarified that `IControllerAccess` methods must be controller-boundary methods owned by the controller; they may delegate internally, but raw external function/service/store references must not be exposed directly as access methods.

## [1.1.3] — 2026-05-02

- Corrected the Tree Editor `ChildrenList` prompt to construct content with the owning controller instance typed through the narrow owner access interface, not a separately named access object.
- Tightened skill maintenance wording so general constructor, ownership, lifecycle, protocol-boundary, and access-interface rules are written for `Content` unless the rule is specifically visual.
- Added `scripts/quick_validate.py` as a package sanity validator for required files, JSON parsing, manifest references, version consistency, markdown links, canonical phrases, and risky maintenance patterns.

## [1.1.2] — 2026-05-02

- Strengthened pull-based construction rules to forbid technology-independent semantic input bundles, including parameter bags, props-like/config/options objects, callbacks/handlers bundles, child-output getter bundles, view-model objects, runtime argument sets, and externally assembled access bundles.
- Clarified that correctly named methods do not make an external bundle a valid `IControllerAccess`; the runtime object must be the owning controller typed through the narrow owner access interface.
- Added `rules/skill-maintenance-rules.md` and linked it from `SKILL.md` as mandatory guidance for maintaining top-skill itself.
- Reworked migration, validation, generation, target adaptation, and checklist wording to avoid platform-specific rule framing.

## [1.1.1] — 2026-05-02

- Clarified that `View` is a visual specialization of `Content`, not a separate access model.
- Expanded the glossary definition of `Content` to cover view, component, data, style, animation, transition, asset/resource, and other modeled content kinds.
- Updated controller/content access wording so content access consistently flows through `IControllerAccess`, with visual child-output access described as the visual-content case.

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
