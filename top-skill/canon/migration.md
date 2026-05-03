# TOP Migration

Rules for migrating existing code into TOP structure incrementally.

These rules apply specifically to migration phases. They complement — and do not
replace — the universal TOP canon (`canon/architectural-invariants.md`,
`canon/controller-content-rules.md`, `references/architecture-rules.md`).

---

## Intermediate migration states

A migrated branch may exist in a defined intermediate state. These states describe
migration depth, not architecture quality.

### partially-restructured

The controller/content boundary is clean and explicitly typed. The integration
layer beneath it remains wrapped legacy — the controller delegates to existing
services, queries, or subscriptions that have not yet been migrated to a TOP
integration layer.

Content has no dependency on integration-layer types. The TOP boundary holds;
the integration layer migration is deferred.

This is a valid hybrid state, not a structural violation. partially-restructured
is a migration waypoint, not a target state. See `references/hybrid-systems.md`
— the wrapped legacy integration layer is the non-TOP part; the controller/content
split is the TOP part.

---

## Mg-1. Partially-restructured must be explicitly declared

A branch may be declared `partially-restructured` explicitly. This is a precise
description of current migration depth, not a defect.

Validation against this state checks only what the state claims:
- Does the controller/content boundary hold?
- Does content have no structural dependency on integration-layer types?

Validation does not require the integration layer itself to be migrated.

---

## Mg-2. External contract must be preserved

The public interface of the migrated branch must not change as a result of
migration.

Callers, parent connectors, and framework-boundary files must not require changes
to accommodate the migration. If they must change, that change is a separate
explicit decision — not a side effect of the migration.

---

## Mg-3. Residual responsibilities must be explicitly justified

When responsibilities remain in the root controller after child branch
decomposition, each residual responsibility must be explicitly justified.

Accepted justifications:
- the responsibility is genuinely cross-cutting: consumed by two or more child
  branches and cannot be cleanly owned by any single child;
- the responsibility is tied to a framework-level constraint that requires it in
  the root controller (routing context configuration, session-level lifecycle
  setup, etc.);
- the responsibility coordinates a flow that spans multiple child branches and
  requires a single orchestration point.

A responsibility that meets none of these criteria is a candidate for extraction
into a child branch.

Residual justifications must be recorded in the migration spec or implementation
prompt, not left implicit.

---

## Mg-3a. Legacy composition is wrapped legacy, not TOP end state

During migration, existing runtime parameters, parameter bags, config/options/props-like
objects, slots, render/build parameters, callback/handler bundles, service bags,
stores, prebuilt child components, and platform child views
may be retained only as explicitly declared wrapped legacy or adapter mechanics.

They are not TOP-conformant final structure.

The target migration direction is pull-based construction:
- a Node constructor receives only its parent reference;
- a Content/View constructor receives exactly one narrow typed owner access interface;
- Content/View is not typed against the concrete controller;
- Node/Controller artifacts are non-renderable orchestration boundaries, not preserved source framework renderable artifacts;
- parent Nodes/Controllers construct direct children at their tree positions;
- Content asks its owner for data, actions, and permitted output handles;
- the owner asks direct child controllers for opaque public handles.

A migration plan that merely moves legacy constructor injection into public
runtime parameters, parameter bags, config/options/props-like objects,
composition entrypoints, or render/build callbacks has not reached
TOP architecture. It has only changed the platform syntax of the same push-based
composition.

---

## Mg-4. Content boundary isolation check

Before declaring a migration slice implemented, verify:

1. Content has no direct structural dependency on integration-layer types (API
   response shapes, external service types, database record types).
2. All integration-derived data displayed by content has been transformed into
   typed view-model fields at the controller level.
3. `IContentAccess` contains only view-model values and typed command parameters —
   no raw integration types, raw response shapes, or integration handles.

If any of these checks fail, the migration is incomplete regardless of whether the
content is visually correct at runtime.
