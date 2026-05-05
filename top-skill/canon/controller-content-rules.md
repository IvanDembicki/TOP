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

Controller must not imperatively command, mutate, update, show, hide,
configure, or push presentation state into locally implemented content.

Correct flow:
1. Controller changes its own state.
2. Controller marks the node/content/runtime as dirty or requests lifecycle or
   render refresh through the node/runtime mechanism.
3. Render/materialization lifecycle runs.
4. Locally implemented content pulls already-resolved primitive values from the
   controller through `IControllerAccess`.
5. Content applies those values to its static materialization.

Allowed controller-to-content access through `IContentAccess` is lifecycle and
materialization access only, such as obtaining the root content primitive or
participating in controlled lifecycle. It must not become a channel for
presentation decisions or imperative mutations.

For data content, the rule is narrower: external objects still interact only
with the data node controller, but the data controller may mutate its own private
data content through `IContentAccess` or an equivalent internal storage boundary
when that content is the node's own data storage. Validation and business rules
belong in the data controller. Presentation content must not directly access or
mutate data content.

## Rule 6a — Locally implemented content is decisionally static

The controller owns all decision logic.

Locally implemented content only materializes a structurally static content
shape and applies already-resolved primitive/output values received through its
owning controller access contract.

Locally implemented content must not decide, derive, branch, select, toggle,
format, concatenate, hardcode, or compute which structure, class/style/token,
text, icon, visibility, handler, child output, platform primitive,
representation, output value, or capability should be used.

Output values include text, labels, counts, formatted strings, icon names,
style/class/token names, visibility tokens, handler choices, and any
representation value. They are resolved by the owning controller before content
asks for them.

Any conditional selection construct inside locally implemented content is a hard
boundary violation when it participates in selection or derivation, including
`if`/`else`, `switch`/`case`, ternary selection, conditional return, multiple
return branches, `&&`/`||` conditional selection, `match`/`when`/guard branches,
or target-equivalent constructs.

Canonical repair:
- primitive value selection moves to the owning controller and is exposed as an
  already-resolved value through controller access;
- structural, visibility, handler, representation, or capability alternatives
  become explicit child state nodes;
- external, native, third-party, or self-contained logic is wrapped as
  black-box component content with a narrow explicit interface.

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

The controller owns the activation policy and resolved presentation state. It
decides when and whether the secondary surface is shown, marks the
node/content/runtime dirty or requests lifecycle/render refresh through the
node/runtime mechanism, and receives back any semantic result through
`IControllerAccess`. Content pulls the already-resolved values through
`IControllerAccess` during materialization or refresh and forwards results
without interpreting them.

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

## Rule 8b — Context attachment, not data injection

TOP construction attaches an object to its context; it does not inject the state
it will use.

Objects are connected to context, not filled with data. A constructor must
receive only the narrow contextual reference required to place the object inside
its ownership boundary:
- a child node receives its parent/context reference;
- locally implemented content receives its owning controller access contract;
- a connector or black-box boundary receives its explicit boundary interface.

The object then requests required information through that contextual contract.
The surrounding object exposes required values through the contract, but it must
not push those values into the object during construction or later through
imperative setters.

Forbidden conceptual forms:

```text
new ChildNode(parent, data, flags, callbacks, config)
new Content(controllerAccess, title, isVisible, onClick)
new Content(controllerAccess, styleToken, labelText)
child.applyConfig(...)
child.setData(...)
content.setVisible(...)
content.updateText(...)
content.setCallbacks(...)
```

Correct conceptual forms:

```text
new ChildNode(parent)
new LocalContent(controllerAccess)
```

If the pushed values represent different states or structural alternatives,
model those alternatives as explicit child state nodes. If the pushed value is
external component configuration, wrap it behind a black-box boundary with a
narrow explicit interface. If the pushed value is a service, store, or global
dependency, route access through the owning context, parent, or controller
contract instead of direct injection.

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
content lifecycle/materialization members, method bags, facade/adapters, closure
objects, concrete Content types, platform primitives, or objects assembled
outside the controller/content construction boundary as substitutes for
`IContentAccess`.
That is `CORE-031`.

The reverse direction is equally strict. The controller must store and use its
content through a narrow `IContentAccess` contract, not through the concrete
Content class. This is required even when the concrete content wraps a
large platform component, widget, native view, or third-party object with many
public methods: the controller sees only the small allowed boundary, and every
other concrete method remains invisible.

`IContentAccess` is controller-to-content lifecycle/materialization access only.
It must not carry view-model values, state flags, callbacks, child-output
handles, presentation commands, mutation commands, or data fields that Content
reads from the controller. Those belong behind `IControllerAccess` methods or
accessors as already-resolved values, or in the node/runtime lifecycle when the
controller needs to mark materialization dirty.

For data content owned by a data node, `IContentAccess` may expose private
storage mutation methods to that same data node controller only. This exception
does not apply to locally implemented presentation content and does not permit
external direct mutation of data content or presentation content access to data
content.

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
