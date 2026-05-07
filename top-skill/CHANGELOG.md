# Changelog

All significant changes to top-skill are recorded in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.1.23] — 2026-05-06

- Added mandatory dedicated migration git branch safety: every migration must
  create or switch to `top-migration/<branch-id>` or a documented deterministic
  equivalent before any migration write.
- Added the git safety gate to migration infrastructure, logs, contracts, and
  validation: initial branch, migration branch, checkout result, working tree
  status, remote status, unrelated changes, write permission, commit policy, and
  no-push policy must be recorded.
- Added `WF-022` for migration writes outside a dedicated branch, missing branch
  safety logging, branch/id mismatch, unrelated work mixing, unauthorized push,
  or unauthorized local commit.
- Updated migration, generation, repair, validation, final audit, orchestration,
  contracts, pattern recognition, README/SKILL, and quick validation checks for
  the dedicated-branch rule.

## [1.1.22] — 2026-05-06

- Strengthened strict migration modeling: migration must discover hidden
  architecture rather than wrap a legacy screen behind one hub node, with
  persistent short checkpoints and independent adversarial validation.
- Added hard validation coverage for concrete content privacy, controller
  platform/content fragment outputs, and content-owned setter bridges
  (`CORE-033` through `CORE-035`).
- Added convention checks for canonical TOP spec shape and generated
  layout/topology correspondence (`CONV-009`, `CONV-010`).
- Added workflow gaps for missing migration checkpoints and non-independent
  validation (`WF-020`, `WF-021`).
- Extended generation, repair, validation, code-generation references, pattern
  recognition, and quick validation prefilters for the stricter content,
  layout, and validation-flow rules.

## [1.1.21] — 2026-05-06

- Fixed hydration consistency for migration and generation-pipeline modes:
  Canon Precheck, Final Audit, TOP Modeling, generation, spec-sync, validation,
  repair agents, prompts, and output contracts now hydrate with the modes that
  require them.
- Clarified constructor rules around Runtime Branch Binding: static nodes remain
  parent/context-only, while runtime-created branch roots may receive one
  canonical entity context, stable identity key, or typed immutable DTO binding.
- Refined migration workspace ownership to branch-scoped control artifacts under
  `top/migration/<branch-id>/`, with shared append-only logs and history-preserving
  status files.
- Added quick validation consistency checks for hydration-vs-mode-manifest drift,
  constructor-only-parent wording that omits runtime branch binding, and
  branch-scoped migration control wording.

## [1.1.20] — 2026-05-06

- Added migration canon that migration means discovering and externalizing
  hidden structure, not wrapping legacy screens/files/components in TOP-shaped
  controller/content facades.
- Added scope-vs-node-boundary, recursive decomposition, giant-node review,
  `PanelDisplayStyle` discipline, reusable structure/library extraction,
  modal/form/list candidate analysis, hook bridge residual isolation, and
  global-store residual rules.
- Added Runtime Branch Binding Pattern and active migration workspace ownership
  rules, including stricter forensic `MIGRATION_LOG.md` entry requirements.
- Added `WF-017`, `WF-018`, and `WF-019` for missing decomposition review,
  undisciplined accepted deviations, and migration workspace scope violations.
- Replaced ambiguous final-audit readiness with explicit statuses:
  `ready_for_generation`, `ready_for_integration`, `ready_for_manual_QA`, and
  `ready_for_production_candidate`.
- Strengthened post-generation validation requirements so type-check clean does
  not replace architectural review of generated source files, bridge files,
  helpers, modals, contracts, and adapters.
- Tightened migration and modeling-refactor hydration so generation, spec-sync,
  repair, branch-scoped migration control artifacts, and generation prompts are
  loaded with the agents that depend on them.

## [1.1.19] — 2026-05-05

- Tightened locally implemented content static materialization so content must
  not derive output values by formatting, concatenating, hardcoding, or
  computing text, labels, style/class/token names, icons, visibility,
  handlers, representation values, or other output primitives.
- Corrected the tree-editor canonical example: BuildInfo and toolbar action
  labels now pull controller-resolved output values, and TreeEditor no longer
  receives source data through a TOP runtime entrypoint.
- Clarified that presentation content executes only target-local materialization,
  refresh, disposal, and event mechanics, not controller-requested presentation
  commands through `IContentAccess`.
- Extended quick validation example scanning with platform-neutral candidates
  for source-data runtime injection and content-side output derivation wording.

## [1.1.18] — 2026-05-05

- Reconciled the event/request model with context attachment: semantic
  events/requests may move through allowed contracts, but data/config/
  presentation packets and imperative mutation commands must not be pushed into
  child nodes or locally implemented presentation content.
- Clarified the distinction between locally implemented presentation content and
  data content: presentation content reports intent and pulls resolved values;
  data controllers may mutate their own private data content through internal
  storage boundaries.
- Updated tree-editor from a previously noncanonical example to the current
  canonical flow: child nodes attach to parent/context, item records are pulled
  through owner contracts, and presentation nodes pull resolved label/icon/
  indentation/drop/drag values.

## [1.1.17] — 2026-05-05

- Added `CORE-032` for context data injection: TOP objects are attached to
  context and must not be filled with constructor data, config, callbacks,
  state, services, stores, child views, or presentation values.
- Extended canon, node model, validation, generation, repair, and verification
  rules so nodes receive parent/context only, locally implemented content
  receives owning controller access only, and connectors/black-box boundaries
  receive only their explicit boundary interface.
- Added platform-neutral quick validation candidates for constructor data
  injection and setter-style post-construction pushing, while keeping semantic
  verdicts in Validation Agent.
- Marked earlier tree-editor examples that used reset/data/setter-style
  materialization as invalid under the context-attachment invariant. Those
  examples are canonical again as of 1.1.18.

## [1.1.16] — 2026-05-05

- Fixed the locally implemented content motivation placement in architectural
  invariants and gave static materialization its own cacheability,
  pre-rendering, portability, and verifiability rationale.
- Strengthened controller/content flow: controller must not push presentation
  commands, state, or mutations into locally implemented content; presentation
  changes flow through controller state, dirty/render refresh, and content pull
  of already-resolved values.
- Updated hydration tiers so generation, validation, and repair agents are
  loaded in workflows that depend on their rule changes.
- Changed quick validation conditional-content detection into a separate
  agent-review candidate channel rather than a final architectural verdict.
- Clarified that platform-specific pattern examples are semantic review
  examples only and must not be copied into platform-neutral quick validation.

## [1.1.15] — 2026-05-05

- Added a cross-cutting canonical rule that locally implemented content must
  contain no conditional selection logic of any kind.
- Tightened `CORE-015` so conditional selection inside locally implemented
  content is a hard validation error, including structure, class/style/token,
  text, icon, visibility, handler, child output, platform primitive,
  representation, and capability selection.
- Updated canon, node model, validation, generation, repair, verifier, and
  pattern-recognition guidance with the canonical repairs: move primitive
  derivation to the owning controller, split structural alternatives into child
  state nodes, or wrap external/self-contained logic as black-box component
  content.
- Added a platform-neutral quick validation prefilter for conditional constructs
  inside locally implemented content boundaries, reporting candidates for
  Validation Agent review without making the final architectural verdict.

## [1.1.14] — 2026-05-04

- Applied TOP Skill Factory governance rules to `top-skill` itself by adding `top/spec.json`, `top/artifact-manifest.json`, `top/modes/mode-manifest.json`, `top/validation/output-rules.md`, `top/shared-rules/skill-governance.md`, and `top/provenance.json`.
- Added `top/schemas/migration-workflow.schema.json` and made project migrations maintain `top/migration/MIGRATION_WORKFLOW.json` as the machine-readable process tree alongside `MIGRATION_PLAN.md`, `MIGRATION_STATUS.md`, and `MIGRATION_LOG.md`.
- Added `WF-016` for missing or stale migration workflow trees.
- Updated migration infrastructure, planning, validation, repair, modeling, generation, spec-sync, review, and output contracts so agents cannot treat Markdown-only planning as sufficient for migration control.
- Added self-governance artifacts to hydration and quick validation so they are loaded and checked as part of the skill package.
- Synchronized self-governance metadata with runtime skill metadata: `top/spec.json` now lists all skill agents, `skill.json` includes `canon/migration.md`, migration quickstart reads include infrastructure/planning agents and workflow schema, and behavior-preservation status routing is explicit.

## [1.1.13] — 2026-05-04

- Added a mandatory migration control plane: `top/migration/MIGRATION_PLAN.md`, `MIGRATION_STATUS.md`, and append-only `MIGRATION_LOG.md`.
- Added Migration Infrastructure Agent and Migration Planning Agent so migration starts with baseline/layout setup and an explicit plan before scope analysis, modeling, generation, or validation.
- Added output contracts for migration infrastructure and migration planning.
- Added `WF-014` for missing migration plans and `WF-015` for missing or stale migration logs.
- Updated migration, validation, repair, generation, modeling, spec-sync, review, and hydration rules so each migration-mode agent follows the plan and appends log entries on handoff or persistent artifact changes.

## [1.1.12] — 2026-05-03

- Added canonical migration artifact layout requirements: branch specs under `top/specs/`, prompts under `top/prompts/`, status under `top/migration/`, and materialized TOP implementation artifacts under `top_src/<branch-id>/` by default.
- Added `CONV-007` for noncanonical TOP spec placement, `CONV-008` for missing TOP implementation source root, and `WF-013` for migration/modeling handoffs that declare future materialization without source-root setup and honest phase status.
- Updated migration, modeling, generation, validation, spec-sync, prompt, and output-contract rules so analysis/modeling that creates Expected Materialization must also declare and prepare the implementation source root.
- Added `contracts/top-folder-contract.md` and `rules/spec-sync-rules.md` to hydration tiers so migration and validation agents load the artifact-layout rules before judging project files.

## [1.1.11] — 2026-05-03

- Added `CORE-030` for decomposed owner access input and `CORE-031` for decomposed content access input.
- Made both canonical internal directions explicit: Content receives only the owning controller instance typed through `IControllerAccess`/target-equivalent, and Controller receives/stores/uses only its own Content instance typed through `IContentAccess`/target-equivalent.
- Forbid method bags, access adapters/facades, inline closure objects, decomposed JSX props, and decomposed content lifecycle/materialization bags as substitutes for real controller/content instances.

## [1.1.10] — 2026-05-03

- Added `WF-012` for ad hoc accepted-deviation labels on core violations that have no TOP-canon-defined migration waypoint.
- Clarified that documenting a violation is tracking, not repair, and cannot make `CORE-029` an accepted deviation.
- Tightened validation, repair, final-audit, migration, and functional-composition rules so only canon-defined waypoint classes may appear in `accepted_deviations`.

## [1.1.9] — 2026-05-03

- Added `CORE-029` for semantic runtime input into Nodes/Controllers, closing the repair loophole where derivation duplication was replaced by prop/config/parameter tunneling into a child node.
- Added `WF-011` for validation/final-audit results that report pass/readiness while confirmed core violations or accepted core deviations remain.
- Added shared derived fact repair rules: agents must not repair `CORE-029` by restoring duplicate derivation, and must not repair Invariant 14 by runtime input tunneling.
- Tightened migration, validation, final-audit, repair, functional-composition, typing, and review rules so documented migration waypoints remain core violations until structurally fixed.
- Clarified that FC-6 renderable-controller waypoints may be tracked as known migration deviations, but cannot produce Validation `PASS` or Final Audit `PASS`.

## [1.1.8] — 2026-05-03

- Added Behavior Preservation Agent and output contract for migration flows where legacy tests cover the migrated scope.
- Added canonical migration rule: legacy tests are requirements evidence, and migration is incomplete until test-covered behavior is extracted, normalized, mapped to TOP nodes/contracts, reflected in prompts, and re-covered by TOP-compatible tests.
- Added `CORE-028` for test-covered behavior loss and `WF-010` for missing behavior preservation pass.
- Updated migration, modeling, generation, validation, repair, review, and prompt guidance so behavior preservation is a mandatory migration sub-flow rather than a checklist.

## [1.1.7] — 2026-05-03

- Clarified that `IContentAccess` is a controller-to-content lifecycle/materialization boundary and must not be used as a data bag for view-model values, state flags, callbacks, or child-output handles.
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
- Clarified that target-required renderable entrypoints belong to Content or thin framework adapters, not to controller identity.

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
- Strengthened Content constructor rules: one narrow owner access interface, no semantic injection through constructors, runtime props, slots, builders, callbacks, stores, services, child handles, or prebuilt fragments.
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
