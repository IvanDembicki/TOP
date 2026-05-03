# Functional Composition Target

Materialization guidance for TOP branches deployed to targets where a branch's
view output is represented as an opaque composable value — an opaque typed view
handle that the parent controller obtains from the child controller, exposes
through a named owner-access method, and allows its own Content/View to place
without inspection.

This file describes how existing TOP semantics materialize in functional
composition targets. It does not introduce new architectural rules. All canonical
TOP rules apply unchanged; this file provides target-specific materialization form.

See `references/target-adaptation-layer.md` for the general target adaptation
workflow. See Rule 23 in the core skill file for the canonical opaque view handle
placement rule that FC-1 materializes.

---

## FC-1. Opaque typed view handle placement

In a functional composition target, a child branch's view output may be represented
as a first-class composable value. That value is still only an opaque view handle.
It is not a slot payload, runtime prop, child component injection, or ownership
transfer.

The pull direction remains canonical:

```text
Content/View -> asks owning controller for a named child-view endpoint
Owning controller -> asks direct child controller for its public opaque handle
Child controller -> returns its own opaque handle
Owning controller -> returns the opaque handle to its own Content/View for placement
```

The parent controller:
- constructs the child branch at the child's tree position;
- obtains the child's opaque view handle only from the direct child controller;
- makes that handle available to its own Content/View through an explicit named
  access method on the narrow access interface;
- never treats the handle as an inspectable platform object.

Content/View:
- requests the handle from the owning controller through the narrow access interface;
- places the returned handle into the layout at the position designated by its own
  node contract;
- must not construct, import, inspect, read from, attach listeners to, mutate, or
  pass the handle outside the branch boundary.

### FC-1a. Child-output access method naming

Child output must be requested through named methods on the narrow owner access
interface. The name identifies the semantic child branch/output, not the transport
mechanism.

Acceptable examples:
- `getAccountIdentityView()`
- `getOrganizationsAccessView()`
- `getAppPreferencesView()`
- `getDebugAdminToolsView()`

Do not require artificial suffixes such as `Handle` or `ViewHandle` when they
reduce readability. Do not require `Section` unless the branch is actually modeled
as a section. Do not use `slot` terminology.

Forbidden generic names include names based on `slot`, `children`, `render`,
`builder`, or framework composition mechanics instead of the semantic branch name.

This is the functional-composition-target materialization of the canonical opaque
view handle placement rule. Platform syntax may look like composition, but the
ownership semantics remain pull-based. A target API that uses props, children,
slots, builders, or composable values internally does not make those mechanisms a
TOP injection channel.

---

## FC-2. Thin framework-boundary file

Certain deployment frameworks require specific files to exist at fixed structural
paths — routing entries, module entry points, or platform application roots — that
cannot be relocated to align with the TOP branch root.

When this constraint applies, the canonical form is:

- The framework-boundary file contains only a thin adapter or re-export to a
  renderable artifact owned by Content/View or by an explicit adapter.
- The framework-boundary file is not a TOP node. It has no controller logic, no
  contracts, and no state.
- The TOP branch root controller remains a non-renderable controller; the
  framework-boundary file is a framework integration adapter only.

The thin delegation must not accumulate logic. If additional logic appears in the
framework-boundary file over time, that logic must be moved into the root controller
or a child branch according to ownership, preserving the framework-boundary file
as an adapter only. The controller must not be exported as the runtime-rendered
component/function/entity.

---

## FC-3. Forced residual responsibility

Some deployment frameworks require state, configuration, or lifecycle setup that
can only be expressed from within the execution context of the framework-boundary
file. When the framework mandates placement at that structural position, the
responsibility may be owned by the root controller of the branch whose
framework-boundary file provides the delegation entry point.

This is called forced residual responsibility.

### Requirements for declaring forced residual

A responsibility may be declared forced residual only when all of the following are
satisfied:

1. **Framework origin is documented.** The responsibility must trace directly to a
   framework constraint, not to a design preference. The constraint and its source
   must be recorded in the migration spec or implementation prompt.

2. **Mg-3 justification is satisfied.** The responsibility must also satisfy at
   least one justification in `canon/migration.md` Mg-3: it must be genuinely
   cross-cutting, framework-mandated, or a multi-branch orchestration point. Forced
   residual does not exempt a responsibility from the Mg-3 evaluation — it adds the
   framework-constraint condition on top of it.

3. **The responsibility is not a decomposition candidate.** If the responsibility
   could be moved to a child branch without losing the framework constraint, it must
   be moved.

### What forced residual is not

Forced residual is not a category of convenience. Any responsibility attributed to
this pattern without a documented framework constraint is a decomposition defect
that must be corrected.

The forced residual declaration must appear in the implementation prompt. An
undocumented responsibility remaining in the root controller does not qualify as
forced residual — it is an unjustified residual (see `canon/migration.md` Mg-3).

---

## FC-4. Controller is not the functional component

In functional composition targets, a function or callable artifact invoked by the
target runtime as a component, composable, renderable entity, route/screen
artifact, or render/build function is not a TOP controller.

A TOP controller may provide access methods, own child construction, coordinate
lifecycle, and expose opaque handles where canon allows it. The renderable
function/component/composable belongs to Content/View or to a thin framework
adapter.

Forbidden:
- a `SomeNode` controller function that receives framework props/config/options
  and returns render output;
- target lifecycle hooks or UI lifecycle callbacks used as the controller's own
  lifecycle;
- arbitrary props passed into a Node/Controller function and treated as
  controller input.

Non-exhaustive example of the forbidden shape:

```text
function SomeNode(props) {
  return SomeView(...)
}
```

Correct direction:
- keep the TOP controller as a non-renderable orchestration boundary;
- put render output in Content/View or a thin adapter;
- keep adapter logic minimal and free of controller responsibilities.
