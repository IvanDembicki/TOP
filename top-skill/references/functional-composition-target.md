# Functional Composition Target

Materialization guidance for TOP branches deployed to targets where a branch's
view output is represented as an opaque composable value — an opaque typed view
handle that the parent controller obtains from the child controller, exposes
through a named owner-access method, and allows its own Content to place
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
Content -> asks owning controller for a named child-view endpoint
Owning controller -> asks direct child controller for its public opaque handle
Child controller -> returns its own opaque handle
Owning controller -> returns the opaque handle to its own Content for placement
```

The parent controller:
- constructs the child branch at the child's tree position;
- obtains the child's opaque view handle only from the direct child controller;
- makes that handle available to its own Content through an explicit named
  access method on the narrow access interface;
- never treats the handle as an inspectable platform object.

Content:
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
  renderable artifact owned by Content or by an explicit adapter.
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
function/component/composable belongs to Content or to a thin framework
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
- put render output in Content or a thin adapter;
- keep adapter logic minimal and free of controller responsibilities.

---

## FC-5. Single owning controller input, not decomposed props

Functional composition targets often materialize Content through one public
runtime input object/value. A target-required props/options envelope is a
technical adapter shape only. Semantically, it is valid only when it contains
exactly one value: the owning controller instance typed only as the narrow
content-to-controller owner access contract (`IControllerAccess` or
target-equivalent).

It must not be:
- decomposed `IControllerAccess` members passed as separate props, JSX
  attributes, named function arguments, or a method object literal assembled at
  the render/composition call site;
- a merged `IContentAccess & IControllerAccess` bundle;
- a view-model/data field carrier;
- a callback or handler bag;
- a child-output getter bundle assembled outside the owning controller;
- a generic props/config/options object.

`IContentAccess` is the opposite direction: controller-to-content. It is not a
place to put data that content reads from the controller.

If the target has no stable runtime content object for the controller to store,
and the controller-to-content direction has no permitted calls, the branch must
declare an explicit controller-to-content zero direction in its contracts,
prompt, or materialization notes. A missing runtime content reference is acceptable
only for that zero direction. It is not permission to collapse both directions
into one data/method props object.

Correct direction:
- Content receives one value: the owning controller instance typed as
  `IControllerAccess` or target-equivalent, optionally inside a target-required
  envelope with exactly one semantic field such as `access` or `controller`;
- the runtime value is the owning controller itself typed through the narrow
  interface;
- data, state, actions, and child-output handles are requested through explicit
  controller-owned methods/accessors on that owner access;
- controller-to-content commands, if any, are modeled separately through
  `IContentAccess` or target-equivalent.

Forbidden React-like shape:

```tsx
<AccountScreenView
  getIsLoading={() => isLoading}
  onRetry={handleRetry}
/>
```

Valid React-like shape:

```tsx
<AccountScreenView access={accountScreenAccess} />
```

where `accountScreenAccess` is the owning controller typed as
`IAccountScreenControllerAccess`. The access object is not an adapter/facade and
is not assembled inline from arbitrary closures.

If a target cannot pass controller identity to Content at all, the target
adapter must report a non-final deviation. It must not present a facade, method
bag, or closure bundle as canonical TOP.

Violation code: `CORE-030`.

---

## FC-6. Renderable controller migration waypoint

When migrating a legacy functional composition target, a source artifact may
initially combine controller logic and renderable target materialization. If that
artifact remains in the Node/Controller role, the branch must be marked as a known
migration deviation.

This waypoint does not satisfy TOP controller role purity. Validators must still
report `CORE-026`; the migration status may explain that the violation is
accepted temporarily, but it must not classify the branch as TOP-conformant final
structure and must not produce Validation `PASS` or Final Audit `PASS`.

The target repair direction is:
- extract a non-renderable Controller/Node orchestration boundary;
- keep target-renderable output in Content or an explicit thin adapter;
- keep any required framework-boundary file as a thin adapter only;
- account for `IControllerAccess` and `IContentAccess` without using runtime
  props/config/options as semantic injection.

---

## FC-7. Child Node runtime input is not a TOP access boundary

In functional composition targets, target syntax may make it easy to pass values
into a child component/function at the point where the parent places it. That
syntax is not a TOP access boundary.

A child Node/Controller must not receive parent-derived state, derived facts,
callbacks, handlers, services, stores, config/options/props-like objects,
parameter bags, runtime argument sets, or arbitrary props through its target
runtime entrypoint.

Forbidden:
- a parent deriving a fact and passing it into a child `SomeNode` as runtime
  input;
- repairing derivation duplication by moving the derived value into a child
  Node/Controller prop/config/options object;
- repairing Node/Controller runtime input tunneling by making the child
  independently re-derive the same shared fact from the same source;
- treating a framework component prop as the child controller's owner access
  contract.

Correct direction:
- the child Node/Controller is born at its tree position without semantic runtime
  inputs beyond its parent/owner boundary;
- shared or parent-owned derived facts are exposed through explicit pull access
  methods, named update methods, or modeled connector contracts after the child
  exists at its tree position;
- if no canonical channel exists yet, the repair must report the remaining
  violation instead of introducing target runtime input tunneling or duplicate
  derivation.

If no modeled connector/access/update boundary exists, `CORE-029` remains a
blocking migration issue. It must not be reclassified as an accepted deviation
by project-local documentation. Only TOP-canon-defined waypoint classes can
appear in `accepted_deviations`. Documenting the violation may be useful for
tracking, but it is not repair and does not make the branch eligible for
Validation `PASS`, Final Audit `PASS`, or the next generation stage.

Violation code: `CORE-029`.
