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
- node constructors receive only the parent reference as semantic input
- Node/Controller public runtime entrypoints do not receive semantic data,
  parent-derived facts, callbacks, services, stores, config/options/props-like
  objects, parameter bags, runtime argument sets, or arbitrary props
- root `RootContext`, if present, is not a dependency injection container
- Content/View constructors receive exactly one narrow typed owner access interface
- Content/View is not typed against or downcast to the concrete controller
- content-to-controller zero-contracts are empty owner access interfaces implemented by the owning controller, not separate dummy runtime objects
- controller access to content is typed through `IContentAccess`, not through the concrete Content/View class
- `IContentAccess` is not used as a data/view-model/state/callback/child-output bag for content
- public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, and prebuilt fragments are not used as semantic injection channels
- any single public runtime input object/value used to materialize Content is exactly the narrow content-to-controller owner access contract, not a merged `IContentAccess & IControllerAccess` bundle or general props/config/data/composition bag
- no externally assembled access bundle replaces the narrow owner access interface implemented by the owning controller
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

---

## 7. Generation discipline

- no architecture changes during generation
- implementation matches model

---

## 8. Migration Behavior Preservation

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

## 9. Repair correctness

- only targeted fixes applied
- no unnecessary rewrite
- no new violations introduced
- no confirmed core violation is reclassified as accepted/temporary/deferred/waypoint unless TOP canon defines that exact migration waypoint
- documenting a violation is not treated as repair

---

## 10. Ambiguity handling

- all critical ambiguity resolved or blocked
- assumptions explicitly stated
- no silent decisions

---

## 11. Readability

- naming is clear and descriptive
- no unnecessary abbreviations
- code is understandable to humans

---

## 12. Final status

- not just working, but canonical
- no remaining critical risks
- ready for use justified

---

## Final rule

If any item fails, result must not be finalized.
