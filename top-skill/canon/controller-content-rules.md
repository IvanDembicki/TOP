# Controller / Content Rules

## Rule 1 — External access goes through Controller

If a node exposes behavior, orchestration, or interaction to the outside,
that access should be modeled through `Controller`.

## Rule 2 — Content stays hidden behind the boundary

`Content` is implementation-side structure.
It must not be treated as a second public interface by convenience.

## Rule 3 — Do not flatten the split into naming only

The pair `Controller` / `Content` must not be reduced to decorative labels.
If the split is declared, it must correspond to a real architectural boundary.

## Rule 4 — Generation must preserve the split

When generating code, docs, or node prompts, the system must preserve:

- what belongs to controller responsibility;
- what belongs to content responsibility;
- what is public contract;
- what is hidden implementation.

## Rule 5 — Validation must check boundary leaks

A valid TOP review should explicitly look for:

- controller logic leaking into content assumptions;
- content details exposed as public contract;
- ownership violations caused by bypassing the controller boundary.

## Rule 6 — Content must not initiate interactions outside its controller

Content must not directly call, signal, or otherwise initiate communication
with any node, system, or external boundary other than its own controller.

All outward interaction from a content unit must be routed through
the controller boundary.

Content may subscribe/unsubscribe to low-level events of its own platform
primitive and perform analogous platform commands on its own implementation
material. This is execution, not ownership: content may forward a narrow event
to its controller, but the controller owns interpretation, state transitions,
lifecycle, structure, and orchestration.

## Rule 7 — Controller is the sole derivation boundary for integration data

Integration-layer types — API response shapes, SDK types, database record types,
and any other types that originate outside the node's own domain — must not appear
in content.

The controller is responsible for receiving integration data and deriving a
typed view-model from it. Content requests the derived view-model only through
`IControllerAccess`; the view-model is not pushed into Content as a constructor,
props, parameter, or method-bag input.
Content must have no structural dependency on integration-layer types:
no structural reference, no implicit shape compatibility.

The view-model is the only integration-derived artifact that may be exposed
through the controller/content boundary, and only through the narrow
content-to-controller access interface.

## Rule 8 — Secondary surface belongs entirely within the branch that owns it

A secondary surface — an overlay, modal, popup, or equivalent transient layer
that belongs to a specific branch — must be implemented and owned entirely within
that branch's content.

The controller owns the activation policy: it decides when and whether the
secondary surface is shown, and receives back any semantic result through
`IControllerAccess`. Content executes the show/hide command through `IContentAccess`
and forwards results without interpreting them.

A secondary surface must not be extracted into a sibling or ancestor controller
simply because it visually overlaps other branches at render time.
Visual overlap does not determine ownership. The logical source of the secondary
surface — the branch that holds the data, triggers the action, and processes the
result — is the owner.

## Rule 8a — Node/Controller runtime input is not an access contract

A TOP Node/Controller receives only its parent/owner boundary as semantic input.

Target runtime entrypoints such as functions, callables, components, route
handlers, factories, or equivalent mechanisms must not receive semantic data,
derived facts, callbacks, services, stores, config/options/props-like objects,
parameter bags, runtime argument sets, child fragments, or arbitrary props.

Do not repair ownership or derivation defects by pushing a derived value into a
child Node/Controller through runtime input. That is `CORE-029`.

## Rule 9 — Content construction is pull-based and access-typed

A concrete TOP Content constructor receives exactly one semantic argument:
the owning controller instance typed only through the narrow
`IControllerAccess`/target-equivalent interface.

The Content must not be typed against the concrete controller class. The
runtime object must be the owning controller instance, but the field, constructor
parameter, and all Content references must use the narrow access interface.
Downcasting, importing the concrete controller type for view access, or storing
the concrete controller as such is a boundary violation.

If Content has no permitted calls to the controller, the access interface is
an empty zero-contract implemented by the owning controller. The correct
materialization is still `new Content(this)` with `this` typed only as that
interface from the Content side. A separate dummy `ControllerAccessZero`
object is not a valid substitute for owner access.

The constructor must not receive data, callbacks, handlers, flags, state, stores,
services, child components, slots, prebuilt view fragments, platform child views,
child view handles, child-output getter bundles, view-model objects,
config/options/props-like objects, parameter bags, runtime argument sets, or
arbitrary props. Moving the same information into any public runtime parameter,
render/build parameter, component/native/platform field, composition mechanism,
or other technology-specific entrypoint is still the same violation.

If a technology materializes Content through one public runtime input
object/value, that input must carry exactly one value: the owning controller
instance typed only as the narrow content-to-controller owner access contract
(`IControllerAccess` or target-equivalent). A target-required technical envelope
is allowed only when it contains that single controller-typed value.

Do not decompose the owner access contract into separate runtime props,
parameters, JSX attributes, named function arguments, or an ad hoc object literal
assembled at the render/composition call site. That is `CORE-030`.

The input must not be a merged `IContentAccess & IControllerAccess` bundle, an
access adapter/facade, a method bag, or a general props/config/data/composition
bag.

A semantic bundle with correctly named methods is not valid owner access unless
it is the narrow `IControllerAccess` implemented by the owning controller itself.

Methods exposed through `IControllerAccess` must be controller-boundary methods
owned by the controller. A controller-boundary method may delegate internally to
utilities, services, stores, or platform APIs, but Content must not receive a raw
imported function, externally owned method reference, service method, store
action, or callback as the access method itself.

If Content needs state, actions, data, or child view handles, it requests
them from the owning controller through the narrow access interface. The owning
controller may then ask direct child controllers for opaque public handles and
return those handles to its own Content for placement only.

The reverse direction is symmetrical. When a controller uses its own
Content, it must receive, store, and call the Content instance typed
only as `IContentAccess`/target-equivalent. It must not receive decomposed
content command members, method bags, facade/adapters, closure objects, concrete
Content types, platform primitives, or objects assembled outside the
controller/content construction boundary as substitutes for `IContentAccess`.
That is `CORE-031`.

The reverse direction is equally strict. The controller must store and use its
content through a narrow `IContentAccess` contract, not through the concrete
Content class. This is required even when the concrete content wraps a
large platform component, widget, native view, or third-party object with many
public methods: the controller sees only the small allowed boundary, and every
other concrete method remains invisible.

`IContentAccess` is controller-to-content only. It must not carry view-model
values, state flags, callbacks, child-output handles, or data fields that Content
reads from the controller. Those belong behind `IControllerAccess` methods or
accessors.

## Rule 10 — Controller role purity

Controller is not a content artifact.

The controller owns behavior and orchestration, but it is not the materialized
view/content/renderable object. It must not be registered, mounted, invoked, or
executed by a target runtime as the visual/content entity of the node.

If target syntax requires a framework component, composable, widget, route file,
screen artifact, render function, or any equivalent renderable entrypoint, that
artifact belongs to Content or to a thin framework adapter, not to the
controller itself.

The adapter may delegate to the controller or content boundary, but it must not
accumulate controller logic. The controller remains a non-renderable
orchestration boundary.
