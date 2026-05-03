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
- root `RootContext`, if present, is not a dependency injection container
- Content/View constructors receive exactly one narrow typed owner access interface
- Content/View is not typed against or downcast to the concrete controller
- content-to-controller zero-contracts are empty owner access interfaces implemented by the owning controller, not separate dummy runtime objects
- controller access to content is typed through `IContentAccess`, not through the concrete Content/View class
- public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, and prebuilt fragments are not used as semantic injection channels
- any single public runtime input object/value used to materialize Content is exactly the narrow owner access contract, not a general props/config/data/composition bag
- no externally assembled access bundle replaces the narrow owner access interface implemented by the owning controller
- access methods exposed to Content are controller-boundary methods owned by the controller, even when they delegate internally
- raw imported functions, externally owned method references, service methods, store actions, and callbacks are not exposed directly to Content as access methods
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
- content remains passive
- no architectural logic in content

---

## 7. Generation discipline

- no architecture changes during generation
- implementation matches model

---

## 8. Repair correctness

- only targeted fixes applied
- no unnecessary rewrite
- no new violations introduced

---

## 9. Ambiguity handling

- all critical ambiguity resolved or blocked
- assumptions explicitly stated
- no silent decisions

---

## 10. Readability

- naming is clear and descriptive
- no unnecessary abbreviations
- code is understandable to humans

---

## 11. Final status

- not just working, but canonical
- no remaining critical risks
- ready for use justified

---

## Final rule

If any item fails, result must not be finalized.
