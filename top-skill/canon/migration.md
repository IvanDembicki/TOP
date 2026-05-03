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

### renderable-controller waypoint

During migration from renderable-artifact-centered code, a branch may temporarily
retain a source renderable artifact in the Node/Controller position only when it
is explicitly declared as a known migration deviation.

This is not TOP-conformant structure. It remains a `CORE-026` controller role
purity violation until the branch is split into:
- a non-renderable Controller/Node orchestration boundary;
- Content/View or an explicit thin adapter for renderable target materialization;
- explicit `IControllerAccess` and `IContentAccess` accounting.

This waypoint is useful for tracking staged repair work. It must not be reported
as validated TOP architecture, must not produce Validation `PASS` or Final Audit
`PASS`, and must not be used as a generation target. The deviation remains listed
under `core_violations` until the renderable/controller split is actually
performed.

### no ad hoc accepted deviations

Only migration waypoints explicitly defined by TOP canon may appear in
`accepted_deviations`. A project prompt, migration status file, validation report,
or repair report must not convert an arbitrary core violation into an accepted
deviation by documenting it as "known", "temporary", "accepted", "deferred", or
"planned".

Documentation may track an unresolved violation, but tracking is not repair and
does not make the violation an accepted deviation. In particular, `CORE-029`
semantic runtime input has no standalone accepted-deviation waypoint. It remains
blocking until structurally repaired or returned to modeling as a blocked
migration issue.

---

## Mg-1. Partially-restructured must be explicitly declared

A branch may be declared `partially-restructured` explicitly. This is a precise
description of current migration depth, not a defect.

Validation against this state checks only what the state claims:
- Does the controller/content boundary hold?
- Does content have no structural dependency on integration-layer types?

Validation does not require the integration layer itself to be migrated.
It does not waive universal canon violations such as controller role purity,
push-based construction, semantic runtime injection, or access-direction collapse.

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

Derived facts, owner state, and cross-cutting values must not be tunneled into
child Nodes/Controllers through target runtime input. A repair that removes
duplicate derivation by passing the derived value into a child Node/Controller
through props/config/options/parameters has only replaced the original violation
with `CORE-029`.

The opposite repair is also invalid. A repair that removes `CORE-029` by making
the child independently re-derive the same parent-owned or shared fact from the
same cross-cutting source has only restored the Invariant 14 violation. Migration
repair must introduce or use an explicit typed access/update boundary, named
controller method, or modeled connector contract. If no such boundary exists in
the current model, the migration remains blocked or in a declared waypoint; the
agent must not invent a props-based or duplicate-derivation workaround.

Declaring the resulting `CORE-029` as an accepted deviation is not a repair
unless TOP canon defines a specific waypoint for that violation. For shared
derived facts, no such waypoint exists. The correct next stage is structural
repair or re-modeling of the missing access/update boundary.

---

## Mg-4. Content boundary isolation check

Before declaring a migration slice implemented, verify:

1. Content has no direct structural dependency on integration-layer types (API
   response shapes, external service types, database record types).
2. All integration-derived data displayed by content has been transformed into
   typed view-model fields at the controller level.
3. Content obtains view-model values only through the content-to-controller owner
   access contract (`IControllerAccess` or target-equivalent), using explicit
   methods or accessors owned by the controller.
4. `IContentAccess` is not used as a view-model/data carrier. It contains only
   controller-to-content commands/requests, or it is explicitly declared as a
   zero-contract when that direction has no permitted calls.

If any of these checks fail, the migration is incomplete regardless of whether the
content is visually correct at runtime.

---

## Mg-5. Legacy tests are requirements evidence

Legacy tests covering the migrated scope must be treated as executable evidence
of expected behavior, not merely as verification files.

Do not migrate tests as files. Migrate the behavioral requirements proven by
those tests.

Implementation-specific assertions may be discarded only after their behavioral
meaning is:
- extracted from the legacy test;
- normalized into a platform-neutral requirement;
- mapped to TOP nodes, contracts, state, events, or lifecycle responsibilities;
- reflected in the relevant spec and implementation prompts;
- re-covered by preserved, adapted, replaced, or newly generated TOP-compatible
  tests.

Migration is incomplete until behavior preserved by legacy tests is represented
in TOP prompts and covered by TOP-compatible tests.

Validation must fail if:
- a migration scope has tests but no Behavior Preservation Plan was produced;
- a legacy behavior expectation has no mapped TOP requirement;
- a mapped requirement has no prompt representation;
- a prompt requirement has no TOP-compatible test coverage;
- a legacy test was discarded without justification;
- behavior gaps remain unresolved.
