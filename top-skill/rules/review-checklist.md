# Review Checklist

This checklist must be applied before any result is considered final.

## Core rule

A result is not valid until all checklist items pass.

---

## 1. Canon compliance

- structure follows TOP canon
- no forbidden confusions present
- ownership boundaries are explicit

---

## 2. Validation completeness

- all required validations executed
- no skipped checks
- no softened violations
- current skill rules required by the active task were loaded for this pass
- target artifacts listed as checked were re-read in this pass
- previous session reads, old skill memory, or earlier generation context were not used as validation evidence

---

## 3. Typing strength

- all boundaries explicitly typed
- no implicit contracts
- no weak shape-based typing where avoidable

---

## 4. Protocol integrity

- all interactions go through protocols
- no direct implementation access
- no bypass paths

---


## 4a. Pull-Based Construction

- TOP objects are born at their architectural position in the tree
- TOP construction attaches objects to context; it does not inject the state
  they will use
- constructors receive only the narrow contextual reference for their boundary:
  node parent/context, locally implemented content owning controller access, or
  connector/black-box boundary interface
- no constructor data packets, flags, callbacks, config/options/props-like
  objects, stores, services, child views, presentation values, visibility
  values, style values, text values, runtime state, handlers, or arbitrary extra
  arguments (`CORE-032`)
- no post-construction setter-style data/config/state/presentation pushes into
  child nodes, locally implemented content, connectors, or black-box boundaries
  (`CORE-032`)
- node constructors receive only the parent reference as semantic input
- Node/Controller public runtime entrypoints do not receive semantic data,
  parent-derived facts, callbacks, services, stores, config/options/props-like
  objects, parameter bags, runtime argument sets, or arbitrary props
- root `RootContext`, if present, is not a dependency injection container
- Content constructors receive exactly one semantic value: the owning controller instance typed only as the narrow `IControllerAccess`/target-equivalent interface
- Content is not typed against or downcast to the concrete controller
- content-to-controller zero-contracts are empty owner access interfaces implemented by the owning controller, not separate dummy runtime objects
- controller access to content is typed through `IContentAccess`, not through the concrete Content class
- controller receives/stores/uses its own Content instance typed through `IContentAccess`, not decomposed content lifecycle/materialization bags, facade/adapters, platform primitives, or inline closure objects (`CORE-031`)
- `IContentAccess` is not used as a data/view-model/state/callback/child-output bag for content
- public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, and prebuilt fragments are not used as semantic injection channels
- any single public runtime input object/value used to materialize Content carries exactly one controller-typed value, not a merged `IContentAccess & IControllerAccess` bundle or general props/config/data/composition bag
- no decomposed `IControllerAccess` members are passed as separate props/parameters/JSX attributes or assembled into inline method bags (`CORE-030`)
- no externally assembled access bundle, adapter/facade, or closure object replaces the owning controller typed as the narrow owner access interface
- access methods exposed to Content are controller-boundary methods owned by the controller, even when they delegate internally
- raw imported functions, externally owned method references, service methods, store actions, and callbacks are not exposed directly to Content as access methods
- shared derived fact repairs do not replace Invariant 14 with `CORE-029`, or `CORE-029` with duplicate derivation from the same cross-cutting source
- shared derived facts move through explicit typed access/update boundaries, named controller methods, or modeled connector contracts; otherwise repair is blocked
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles
- child-output access methods are named by semantic branch/output, not by generic slot/children/render/builder terminology
- artificial `Handle`/`ViewHandle` suffixes are not required; `Section` is used only when the branch is actually modeled as a section
- TOP spec props are not confused with runtime inputs

## 5. Lifecycle correctness

- lifecycle ownership is explicit
- no hidden retention
- no uncontrolled creation/destruction

---

## 6. Controller vs Content

- controller owns behavior
- controller is not a renderable platform/framework entity
- controller does not return render output
- controller does not receive framework/runtime props, config, or options as component input
- framework UI lifecycle APIs, hooks, callbacks, or equivalent target lifecycle mechanisms are not used as controller lifecycle
- renderable-controller migration waypoints are marked as known deviations and still report `CORE-026`
- accepted core deviations and migration waypoints do not produce validation pass or final-audit pass
- content remains passive
- no architectural logic in content
- locally implemented content contains no conditional selection logic
- locally implemented content does not select or derive structure,
  class/style/token, text, icon, visibility, handler, child output, platform
  primitive, representation, output value, or capability
- locally implemented content does not format, concatenate, hardcode, or derive
  displayed/output values from constants, runtime data, props, config,
  environment values, platform values, assets, or other local sources
- locally implemented content applies only already-resolved primitive/output
  values received through its owning controller access contract

---

## 7. Generation discipline

- no architecture changes during generation
- implementation matches model
- generated TOP implementation artifacts are under the declared implementation
  source root (`top_src/` by default), except explicitly declared thin adapters
- Expected Materialization, `props.sourceRoot`, and `props.dir` resolve to the
  same source root

---

## 8. TOP artifact layout

- new branch specs live under `top/specs/`, not ad hoc root-level JSON files
- implementation prompts live under `top/prompts/`
- migration status/tracking lives under `top/migration/`
- `top/migration/MIGRATION_PLAN.md` exists and names the current scope, phases,
  responsible agents, planned artifacts, gates, and rollback/stop points
- `top/migration/MIGRATION_WORKFLOW.json` exists, parses as JSON, and names the
  same scope, branch id, phase order, current phase, responsible agents, gates,
  and handoffs as the plan/status
- `top/migration/MIGRATION_LOG.md` exists and has append-only entries for
  migration-mode handoffs and artifact changes
- migration/modeling handoffs that create Expected Materialization also prepare
  `top_src/<branch-id>/` or the approved equivalent, with `.gitkeep` if empty
- analysis/modeling outputs use honest phase status and do not call themselves
  complete/validated before implementation and validation exist
- migration scope root is not treated as final node boundary; recursive
  decomposition evidence exists for hidden states, data owners, async
  workflows, forms, modals, lists/list items, bridge boundaries, black boxes,
  and reusable structures
- giant-node review exists for large controller access surfaces, many
  display-style methods, many bridge hooks, many pending actions/mutations, or
  many unrelated modal/form/list/workflow responsibilities
- `PanelDisplayStyle` or equivalent display-token methods do not hide state
  alternatives, workflows, modal/form/list ownership, async process states,
  permission-gated capabilities, or data boundaries
- accepted migration deviations include exact locations, temporary rationale,
  target repair direction, expiry condition, and owner phase
- generated migration source files have been architecturally validated after
  generation; type-check clean is not treated as TOP-clean
- report `CONV-007`, `CONV-008`, `WF-013`, `WF-014`, `WF-015`, `WF-016`,
  `WF-017`, `WF-018`, or `WF-019` when these
  checks fail

---

## 9. Migration Behavior Preservation

- migration scopes with legacy tests have a Behavior Preservation Plan
- legacy tests are treated as requirements evidence, not only as files to rerun
- test-covered behavior expectations are extracted and normalized
- normalized requirements are mapped to TOP nodes, contracts, state, events, lifecycle, and prompts
- prompt requirements derived from legacy tests are covered by preserved, adapted, replaced, or newly generated TOP-compatible tests
- discarded legacy tests have explicit behavior-level justifications
- unresolved behavior gaps block validation and final audit
- `WF-010` is reported when the behavior preservation pass is missing
- `CORE-028` is reported when test-covered behavior is lost, weakened, or not represented in TOP sources of truth

---

## 10. Repair correctness

- only targeted fixes applied
- no unnecessary rewrite
- no new violations introduced
- no confirmed core violation is reclassified as accepted/temporary/deferred/waypoint unless TOP canon defines that exact migration waypoint
- documenting a violation is not treated as repair

---

## 11. Ambiguity handling

- all critical ambiguity resolved or blocked
- assumptions explicitly stated
- no silent decisions

---

## 12. Readability

- naming is clear and descriptive
- no unnecessary abbreviations
- code is understandable to humans

---

## 13. Final status

- not just working, but canonical
- no remaining critical risks
- readiness status is precise and justified: `ready_for_generation`,
  `ready_for_integration`, `ready_for_manual_QA`, or
  `ready_for_production_candidate`; do not use unqualified ready-for-use wording

---

## Final rule

If any item fails, result must not be finalized.
