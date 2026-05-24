# Architectural Invariants

These invariants hold without exception.
Any deviation is a structural violation, not a local accommodation.

---

## 1. Spec + Prompt Invariant

**Spec + Node Implementation Prompt MUST be the single source of truth for node behavior.**

Everything else — code, comments, runtime observation — is derivative.

`spec + prompt` is the minimal sufficient unit for:

- regeneration after change;
- verification against architectural intent;
- portability across stacks;
- controlled evolution.

Invariant:
- If there is no spec, there is no regeneration — there is only rewriting.
- If there is no prompt, there is no executable unit — there is only a description.
- Code without spec + prompt is not a TOP artifact.

Forbidden:
- treating code as the primary source of truth;
- regenerating from code alone when spec exists;
- skipping the prompt layer because "the spec is clear enough."

---

## 2. Locality Invariant

A node must be understandable, generatable, and verifiable using:

- its own spec;
- its own implementation prompt;
- explicit contracts with direct neighbors.

If understanding or verifying a node requires implicit knowledge of the full system graph,
the TOP structure is either missing or broken.

Invariant:
- Local context is sufficient for correct generation.
- Global knowledge may not be assumed as a substitute for explicit contracts.
- **Node MUST NOT depend on implicit knowledge of other nodes.**

Forbidden:
- generating a node that implicitly depends on undeclared global state;
- verifying a node by tracing through unspecified cross-system paths;
- justifying cross-boundary coupling with "everyone knows this."

---

## 2a. Pull-Based Construction / Locality of Object Birth Invariant

A TOP object must be constructed at the exact place where it architecturally belongs in the tree.

Objects are not assembled outside the tree and pushed inward.
Objects are born at their position in the tree.

This invariant is foundational. It is not tied to any particular language, platform, UI framework, component model, or render/build mechanism, and it is not merely a constructor style preference. Push-based composition breaks TOP ownership semantics by making the tree decorative instead of real.

### Construction rule

- A static Node constructor receives exactly one semantic argument: its
  Parent/context reference.
- A runtime-created branch root may receive parent/context plus one canonical
  Runtime Branch Binding input: entity context reference, stable identity key,
  or typed immutable DTO fallback. That binding is not arbitrary data injection.
- A Node/Controller public runtime entrypoint must not receive semantic data,
  derived facts, callbacks, handlers, services, stores, child fragments,
  config/options/props-like objects, parameter bags, runtime argument sets, or
  arbitrary props. In targets where a Node/Controller is materialized through a
  function, callable, component, route, adapter, factory, or equivalent runtime
  entrypoint, that entrypoint is not a semantic input channel.
- For a root node, the parent may be `null` or a special `RootContext`.
- `RootContext` is only a root ownership/bootstrap marker. It must not become a generic dependency injection container and must not pass application data, callbacks, services, stores, child instances, view fragments, or arbitrary props into the tree.
- A parent Node/Controller owns its direct children and is responsible for constructing them.
- A Content constructor receives exactly one semantic argument: the owning
  controller instance typed only as the narrow `IControllerAccess` access
  interface. Content must not receive any semantic value other than its
  owning controller through that interface.
- The Content constructor must not receive the concrete Node/Controller as its concrete class type. The runtime object must be the owning controller instance, but the Content must be typed only against the narrow access interface.
- If Content has no permitted calls to the controller, the content-to-controller zero-contract is an empty narrow access interface implemented by the owning controller. A separate dummy `ControllerAccessZero` object is not a valid owner access object.
- The Content constructor must not receive additional data, callbacks, handlers, flags, state, stores, services, child components, slots, prebuilt view fragments, platform child views, child view handles, child-output getter bundles, view-model objects, config/options/props-like objects, parameter bags, runtime argument sets, or arbitrary props.
- This restriction is technology-independent. Moving injection from constructor parameters into any public runtime parameter, render/build parameter, component/native/platform field, composition mechanism, or other technology-specific entrypoint is still the same violation.
- If a technology materializes Content through one public runtime input object/value, that input must carry exactly one value: the owning controller instance typed only as the narrow content-to-controller owner access contract (`IControllerAccess` or target-equivalent). A target-required technical envelope is allowed only when it contains that single controller-typed value.
- Content must not receive the members of `IControllerAccess` decomposed as separate runtime props/parameters, JSX attributes, named function arguments, or an ad hoc object literal assembled at the render/composition call site. This is `CORE-030`.
- The owner access runtime value must be the owning controller itself typed through the narrow interface. It must not be an access adapter, facade object, externally assembled method bag, or inline closure bundle unless the target cannot pass controller identity at all; that exception must be documented as a non-final target adapter constraint and validated as a deviation, not as canonical TOP.
- The input must not be a merged `IContentAccess & IControllerAccess` bundle, a view-model/data field carrier, or a general props/config/data/composition bag.
- A semantic bundle with correctly named methods is not valid owner access unless it is the narrow `IControllerAccess` implemented by the owning controller itself.
- Methods exposed through `IControllerAccess` must be controller-boundary methods owned by the controller. They may delegate internally, but a raw imported function, externally owned method reference, service method, store action, or callback must not be exposed directly to Content as the access method itself.
- For any node with separate content, controller-to-content access must also go through a narrow `IContentAccess` or equivalent interface. The controller must store and use content through this interface, not through the concrete content class. `IContentAccess` is not a data channel into content.
- The controller-side runtime value for that direction must be the node's own
  Content instance typed only as `IContentAccess`/target-equivalent. The
  controller must not receive decomposed content lifecycle/materialization
  members, method bags, facade/adapters, closure objects, concrete Content types, platform
  primitives, or objects assembled outside the controller/content construction
  boundary as substitutes for `IContentAccess`. This is `CORE-031`.

### Context attachment, not data injection

TOP construction attaches an object to its context; it does not inject the state
it will use.

Objects are connected to context, not filled with data. TOP object constructors
must receive only the narrow contextual reference required to place the object
inside its ownership boundary:
- a static node receives its parent/context reference;
- a runtime-created branch root receives parent/context plus one canonical
  Runtime Branch Binding input when it needs entity attachment;
- locally implemented content receives its owning controller access contract;
- a connector or black-box boundary receives its explicit boundary interface.

After attachment, the object requests required information through that
contextual access contract. The surrounding object is responsible for exposing
the required values through the contract, but it must not push those values into
the object during construction or later through imperative setters.

A constructor must not receive data packets, flags, callbacks, config objects,
stores, services, child views, presentation values, visibility values, style
values, text values, or runtime state as additional arguments. Runtime branch
binding must be one canonical entity context, identity key, or typed immutable
DTO input, not scattered data.

Conceptual violations:

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

Correct attachment:

```text
new ChildNode(parent)
new LocalContent(controllerAccess)
```

Then:

```text
child asks parent/controller/context through its public contract
content asks controllerAccess for already-resolved values
```

This keeps TOP objects context-bound instead of parameter-bound. If data,
flags, callbacks, configuration, presentation values, or runtime state are
pushed into objects, object behavior depends on construction-time packets and
imperative updates. This weakens tree locality, creates hidden data-flow paths,
makes regeneration less predictable, and makes caching/pre-rendering harder.

This does not forbid domain methods on a data node controller, such as
`setAge(value)` or `replaceRecord(record)`, when access to that data controller
is architecturally valid. Such methods belong to the data node controller API;
they are not constructor injection and not a controller-to-presentation-content
push. The data controller may mutate its own private data content internally.
External objects still must not mutate data content directly or inject data into
data content from outside.

Canonical repair:
- remove additional constructor arguments;
- add the missing value/request to the appropriate access contract;
- let the object pull the value through that contract;
- if pushed values represent different states or structural alternatives, model
  them as explicit child state nodes;
- if the pushed object is external component configuration, wrap it behind a
  black-box boundary with a narrow explicit interface;
- if the pushed value is a service/store/global dependency, route access through
  the owning context, parent, or controller contract instead of direct injection.

### Pull direction

Correct direction:

```text
View -> asks owning Node/Controller for data/actions/child view handles
Owning Node/Controller -> asks child Node/Controller for public view handles
Child Node/Controller -> returns opaque public view handle
```

Incorrect direction:

```text
Parent/root/external code creates data/actions/children/fragments outside the tree
-> pushes them into Content through constructor parameters, runtime parameters, parameter bags, callbacks, handlers, config/options/props-like objects, child-output getter bundles, or prebuilt handles
```

Also incorrect:

```text
Parent/root/external code derives a fact or obtains state/action references
-> pushes them into a child Node/Controller through target runtime input
```

When a parent View needs to render a child, the parent View asks its owning Node/Controller through its narrow access interface. The owning Node/Controller then asks the direct child Node/Controller for its public opaque view handle. The child Node/Controller returns its own view handle through its public API. The View may place returned opaque handles, but must not construct, import, inspect, downcast, or directly own child nodes.

### Spec props clarification

TOP spec props are declarative metadata in the TOP specification. `props.source`, `props.contentType`, `props.dir`, and analogous fields are not runtime parameters, component fields, platform fields, render/build parameters, or any other technology-specific input channel. They are not a runtime injection channel and must not be used to justify props-based composition or external assembly in any target.

### Platform mechanics clarification

The phrase "exactly one semantic argument" applies to the public constructor of the concrete TOP Content. Inside the Content implementation, it may create internal platform objects or pass internal objects to protected/base constructors when required by the platform abstraction. External code must not pass platform primitives, flags, tokens, children, slots, callbacks, handlers, stores, services, parameter bags, config/options/props-like objects, child-output getter bundles, or prebuilt fragments into the TOP Content constructor.

### Internal access symmetry clarification

The controller/content boundary is bidirectional. Content depends on the owning controller only through `IControllerAccess`; the controller depends on content only through `IContentAccess`.

`IControllerAccess` is the only direction through which content requests controller-owned data, state, actions, and permitted child/output handles. `IContentAccess` is controller-to-content lifecycle/materialization access only. It must not contain view-model values, state flags, callbacks, child handles, presentation commands, mutation commands, or data fields for content to read.

Data content has a narrow exception: if content is the private storage of a data
node, the owning data controller may use `IContentAccess` or an equivalent
internal storage boundary to mutate that private data content. Business rules and
validation stay in the data controller. The exception does not allow
presentation content mutation, external direct data-content mutation, or
data/config injection into data content from outside.

This symmetry is mandatory even when one direction currently has no methods. An empty zero-contract is still a named access interface at the boundary. For content-to-controller, that empty interface is implemented by the owning controller and passed as `this` typed only as the interface. It is not materialized as a separate runtime dependency object. For controller-to-content, if the target has no stable runtime content object for the controller to store, the zero direction must still be declared explicitly in the prompt/materialization contract; absence of a runtime reference is acceptable only when there are no permitted controller-to-content calls and the target cannot express such a reference cleanly.

This is especially important when content wraps a large platform component, widget, native view, or third-party object. The concrete content object may expose many public methods, but the controller may be allowed to use only one or two of them. `IContentAccess` cuts off the rest of the concrete surface and keeps the content implementation replaceable, portable, and verifiable.

### Runtime controller tree

TOP runtime is a tree of controller objects.

A controller without tree position is not a TOP controller. A TOP controller is
the public runtime object of a TOP node; it is not a standalone service/helper
module and not merely a file named `*Controller`.

Every generated TOP node controller must participate in the runtime controller
tree by extending the project's canonical TOP node base class or implementing
the canonical TOP node runtime interface for the active target/project.

The exact API names are target/project-specific. The required roles are
canonical:
- parent/context reference, or root/host context for a root node;
- child ownership and child registration;
- children access;
- lifecycle;
- child construction policy;
- refresh/invalidate/update lifecycle entry when applicable;
- disposal/cleanup lifecycle;
- materialized output access through the node's own content boundary when it
  has content;
- sibling access only through parent/declarative child collection mechanisms
  when the base runtime supports them;
- ancestor navigation only through allowed typed mechanisms.

Static node constructors attach the node to the runtime tree. They receive only
parent/context as semantic input. Runtime-created branch roots may receive
parent/context plus one canonical Runtime Branch Binding input when the branch
needs entity attachment.

Root nodes are not exempt. A root controller may have no ordinary parent, but
it must still be a runtime tree root with root/host context, child ownership,
lifecycle, branch identity, integration boundary, and materialized output access
through its own content boundary when it has content.

Leaf nodes are not exempt. A leaf controller may have no children, but it must
still attach to parent/context, have or inherit lifecycle, be represented in the
spec/prompt, and own its private content boundary when it has content.

Child construction must create child controllers/node objects, not child content
objects, render fragments, public wrapper components, or target artifacts
pretending to be child nodes.

```text
parent controller -> child controller
child controller -> private content boundary
```

Forbidden:
- creating child content directly as a child node;
- creating public wrapper components as child nodes;
- creating child render fragments as children;
- composing child content inside parent content;
- treating framework components as TOP child nodes unless they are explicitly
  classified as black-box content or external target artifacts.

TOP generation must produce a controller tree, not a set of controller-shaped
service files. A controller-shaped service/helper/module with no runtime tree
position is `CORE-037`.

### Absolute content privacy

Concrete locally implemented content is private to its owning controller. It is
not a public class dependency, a parent dependency, a sibling dependency, or an
adapter dependency.

Only the owning controller may create its concrete content, and it must store
and use that content only as `IContentAccess`/target-equivalent. No other
artifact may import, instantiate, type against, downcast to, inspect, store, or
call the concrete content class. A public controller API may expose only
controller-level values or opaque placement handles where canon permits; it must
not leak concrete content or content-owned platform primitives.

This is a hard boundary. Moving concrete content access into a helper, adapter,
factory, hook, closure, or generated method bag is still concrete content
exposure.

If external code can name a concrete content class, privacy is broken. A public
target-framework wrapper around concrete content is also concrete content
exposure (`CORE-036`). Runtime TOP trees are controller trees, not content
trees. Parent, adapter, sibling, and external code must interact with child
controller public APIs, not with child content or wrappers around child content.

### One controller, zero-or-one content

A TOP node has exactly one controller. It may have no content, or it may have
one locally implemented content object owned by that controller.

If a legacy artifact contains several presentation fragments, modal helpers,
form helpers, cards, rows, bridge components, or platform widgets, those pieces
must be classified before generation as child nodes, state nodes, black-box
components, bridge boundaries, reusable library nodes, or target-local
implementation detail inside the one private content object. They must not
become an unmodeled helper-component forest inside one giant node.

### Controller output is not content implementation

A controller must not return platform view fragments, render/build trees,
content fragments, style/layout fragments, JSX/widget/composable fragments,
animation objects, content-owned setter handles, or platform mutation handles as
part of its controller API.

When parent-owned placement is required, the public child output must be opaque
and placement-only. The caller must not receive concrete content, platform
internals, callback registration handles, setter handles, or a mutation surface.

### Content-owned setters do not cross the boundary

Content-owned setter/mutation functions are private content mechanics. They must
not be captured by controllers, stored in controller fields, returned through
controller APIs, passed through `IControllerAccess`/`IContentAccess`, or handed
to parents/adapters/helpers.

The canonical replacement is controller-owned state plus dirty/render/lifecycle
refresh and content pull of already-resolved values during materialization.

### Locally implemented content static materialization clarification

Locally implemented content must contain no conditional selection logic of any
kind. It must not decide, derive, branch, select, toggle, or compute which
structure, class/style/token, text, icon, visibility, handler, child output,
platform primitive, representation, or capability should be used.

Locally implemented content may only materialize a structurally static content
shape and apply already-resolved primitive values received through its owning
controller access contract.

Conditional selection constructs inside locally implemented content are hard
`CORE-015` violations when they participate in selection or derivation. This
includes `if`/`else`, `switch`/`case`, ternary selection, conditional rendering,
conditional return, multiple return branches, `&&`/`||` conditional selection,
`match`/`when`/guard branches, or target-equivalent constructs.

Primitive derivation belongs to the owning controller. Structural, visibility,
handler, representation, or capability alternatives belong in explicit child
state nodes. External, native, third-party, or self-contained logic must be
wrapped as black-box component content behind a narrow explicit interface.

### Motivation for locally implemented content static materialization

This rule preserves deterministic materialization, cacheability,
pre-rendering, portability, and verifiability. If locally implemented content
contains selection logic, the system cannot reliably know in advance which
objects, classes, platform primitives, handlers, or structural shape may exist
inside that content.

Content with selection logic becomes a hidden decision engine and breaks the
TOP boundary between controller/tree decision ownership and content
materialization.

### Motivation for Pull-Based Construction / Locality of Object Birth

This rule keeps the tree real, not decorative. If objects are assembled outside the tree and pushed inward, the visible tree no longer explains who owns what. Ownership direction becomes hidden in external assembly code.

It preserves locality. A node should be locally understandable from its own spec, prompt, parent contract, children, and explicit access interfaces. Push-based composition creates hidden external dependencies that are invisible when reviewing the node itself.

It prevents input/composition tunneling. Passing data, callbacks, handlers, services, stores, child components, child-output getter bundles, or prebuilt view fragments through constructors, public runtime parameters, parameter bags, config/options/props-like objects, or composition entrypoints creates a side-channel that bypasses the tree.

It makes the architecture verifiable. AI agents and validators can check local construction, ownership, and access interfaces when objects are born at their tree positions. They cannot reliably verify hidden external assembly dependencies that are pushed into Content from arbitrary code.

It keeps TOP cross-platform. The rule is about ownership semantics, not the syntax of any particular language, UI framework, component model, or render/build mechanism. Technology-specific input and composition syntax may be local materialization syntax, but it does not define TOP ownership.

---

## 2b. Controller Role Purity Invariant

A TOP controller must remain only a controller.

A controller may contain orchestration, coordination, lifecycle,
state-transition, validation, routing, async-flow, child-management, and domain
decision logic when that logic belongs to the node responsibility.

However, a controller must not become, extend, implement, replace, or be
materialized as any content-side or platform-renderable artifact.

A controller must not be the artifact that the target runtime treats as the
node's rendered content, visual component, render/build function,
layout/style/animation/content artifact, platform UI lifecycle object, or public
runtime input receiver for content composition.

A controller may own and coordinate content through `IContentAccess`.
A controller may expose opaque output handles where canon allows parent-owned
placement. But the controller itself must not participate in the platform
rendering lifecycle.

If a target runtime requires a renderable entrypoint, route file, component,
widget, composable, screen artifact, render function, or equivalent executable
render surface, that artifact belongs to Content or to a thin framework
adapter. It is not the TOP controller. The adapter must not accumulate
controller logic.

Controller complexity may be a design smell. Controller role leakage is a
structural violation.

This invariant prevents ordinary framework component composition from being
mistaken for TOP architecture. A renderable artifact may host or delegate to a
TOP branch, but the controller identity remains a non-renderable orchestration
boundary.

---

## 3. AI Executor Invariant

AI operates as executor within the model — not as architect of the model.

Permitted:
- deriving structure from explicit inputs;
- generating artifacts from defined structure;
- verifying artifacts against canonical rules;
- regenerating artifacts after spec or prompt changes.

Forbidden:
- silently choosing architecture where the model is absent;
- substituting convenience decisions for explicit structural definitions;
- treating model ambiguity as permission to invent structure;
- proceeding past unresolved architectural ambiguity without escalation;
- **inferring or extending system structure beyond the provided spec.**

---

## 4. Non-Tree Relationship Rule

All relationships between nodes must be expressed through defined connectors
or explicit structural contracts.

Forbidden:
- implicit cross-links between non-adjacent nodes;
- shared mutable state accessed outside ownership boundaries;
- hidden graph dependencies that bypass the tree structure.

If a non-tree relationship is architecturally necessary, it must be modeled
explicitly as a connector — not handled silently in implementation.

---

## 5. Static Chain / Typed Ancestor Guarantee Invariant

A node may access a non-adjacent ancestor directly **only if** the entire chain
from that node to the ancestor is architecturally guaranteed.

In an architecturally guaranteed chain, the ancestor's type and existence are guaranteed at all times.
Direct access is permitted and is **guaranteed (non-nullable)** — no null check is required.

A lib subtree does not automatically break this guarantee.
If the parent chain above the lib node is explicitly typed and the target ancestor's
type and existence are guaranteed by the model, upward access remains guaranteed
and non-nullable.

The guarantee breaks only at the point where the parent type, target ancestor type,
or ancestor existence ceases to be guaranteed. This can happen at an untyped host,
external attachment point, abstract integration boundary, connector boundary, or
runtime-dependent placement point.

See `references/interaction-contracts.md` — guaranteed vs. search access.

When the guarantee breaks, direct upward lookup must stop.
The required dependency must be expressed through a typed contract, connector,
interface, or equivalent boundary artifact.

Invariant:
- Fully typed guaranteed chain, including through a lib subtree → direct ancestor access is permitted.
- Untyped or external boundary in the chain → connector/contract is mandatory.
- A lib node must not assume ancestors above its attachment point unless that attachment point is part of an explicitly typed deployment context.

Forbidden:
- direct ancestor access above the point where parent typing becomes unknown;
- relying on a specific ancestor type from within a lib subtree when the lib attachment context is not typed;
- passing events or data above an untyped or external boundary without an explicit connector or contract.

---

## 6. View Access Invariant

A node exposes its view through `getView()`. The only node entitled to call `getView()` on a given node is its direct parent.

Any other node — whether an ancestor at any level above or a sibling — does not have the right to call `getView()` directly. If a node's view is required at a higher level, each intermediate parent must obtain `getView()` from its own direct child and include the result in its own view composition. View access is resolved strictly one level at a time.

A node does not "give" its view to anyone — it exposes `getView()` and the caller is bound by tree position.

Permitted:
- an owning parent controller calling `getView()` on its direct children only as part of pull-based, parent-owned materialization, then handing the opaque handles to its own Content through an explicit local boundary for placement.

Forbidden:
- calling `getView()` on a node from any position other than its direct parent;
- accessing a descendant's view by bypassing intermediate nodes;
- calling `getView()` on a sibling node directly;
- skipping levels in view composition;
- receiving child view handles from external assembly code through constructor parameters, public runtime parameters, parameter bags, callbacks, handlers, config/options/props-like objects, child-output getter bundles, composition entrypoints, or prebuilt fragments.

---

## 7. Content Encapsulation Invariant

Internal implementation fields (content) are never public.
They are internal to the owning node, and no external code may access them directly.

External access is allowed only through explicit controller getters.
Such getters may return only values that do not expose internal implementation objects (content), do not reveal the node's internal structure, and do not provide back-channel access into the node's internal model.

The caller receives a value, not a handle to the node's internals.
A returned value must not allow the caller to navigate into the node's model or mutate it indirectly.

**Violation:**
- any direct external access to another node's internal implementation field;
- any public or externally reachable exposure of an internal implementation field.

**Repair:**
- remove external access;
- remove public exposure;
- move the logic into the owning node and expose only a controller-level contract.

---

The same encapsulation principle applies in the reverse direction.

The platform primitive owned by the content — the native element, DOM node, or platform-equivalent object — is the content's internal implementation. It is internal to the content and must not be accessed by the controller for behavior, mutation, inspection, event wiring, styling, querying, or any other platform operation. The only exception is an opaque view handle exposed through `getView()` for parent-owned placement/composition.

The controller must not imperatively command, mutate, update, show, hide,
configure, or push presentation state into locally implemented content through
`IContentAccess` or any other channel.

Correct flow:
1. The controller changes its own state.
2. The controller marks the node/content/runtime as dirty or requests lifecycle
   or render refresh through the node/runtime mechanism.
3. The materialization or refresh lifecycle runs.
4. Locally implemented content pulls already-resolved primitive values from the
   controller through `IControllerAccess`.
5. Content applies those values to its static materialization.

Controller-to-content access through `IContentAccess` is lifecycle and
materialization access only, such as obtaining the root content primitive or
participating in controlled lifecycle. It is not a presentation command channel.

The only permitted low-level handle exposure is the node's opaque `getView()` result for parent-owned placement/composition. This handle is not part of the controller's permission to operate on its own content primitive.

The controller must not depend on the type, structure, or API of the platform primitive.

The prohibition applies not only to usage but also to definition. A base class in the controller hierarchy that defines a public property or getter exposing the platform primitive is itself a violation — even if no direct usage of that property appears in application code. The existence of such a mechanism constitutes a structural bypass of the invariant: it makes the violation available to every subclass automatically, without any explicit act of access.

**Violation:**
- controller accessing the platform primitive owned by the content, including through a public or base-class property or any exposed reference;
- controller code using the node's own render/view/native primitive, its platform API, or any equivalent exposed primitive handle for its own content;
- any class in the controller hierarchy defining a public property or getter that exposes the platform primitive, including in a base class;
- content exposing its platform primitive through `IContentAccess` for anything other than the narrow opaque `getView()` placement/composition handle.
- controller pushing presentation state or imperative mutation into locally
  implemented content, including show/hide, update, configure, class/style,
  render-with, or apply-state commands.

**Detection examples (DOM-like targets):** `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()`. On other platforms, the equivalent is any direct handle to the native/render primitive owned by the content.

**Repair:**
- move the presentation decision or primitive derivation into controller state;
- mark the node/content/runtime dirty or request lifecycle/render refresh
  through the node/runtime mechanism;
- let locally implemented content pull the already-resolved primitive value
  through `IControllerAccess` during materialization or refresh.

---

## 8. Declaration Order Invariant

Generated node implementation declarations must follow architectural depth from outside to inside.

The controller/node is the external surface of the node and must be the first declaration for that node's implementation unit.

Internal access boundary artifacts stand between the controller and the hidden Content implementation. Therefore they must be declared after the controller/node and before the Content implementation. Both internal directions are part of this ordering rule: controller-to-content (`IContentAccess` or equivalent) and content-to-controller (`IControllerAccess` or equivalent). If one direction has no permitted calls, an explicit zero-contract must be declared according to the target technology or project convention.

The hidden Content implementation is the deepest implementation part and must be declared after the boundary artifact that mediates access to it.

For a one-file node implementation, the canonical order is:

```text
Controller/Node
IContentAccess or technology-specific controller-to-content boundary
IControllerAccess or technology-specific content-to-controller boundary
Content
```

If a direction is intentionally empty, the zero-contract declaration belongs in the same boundary layer.

If a target technology requires separate files or a project convention uses split materialization, the same public-to-private organization must be preserved in file structure and exports: external controller/node artifact first, internal boundary artifacts next, hidden Content implementation artifacts last.

**Violation:**
- Content declared before the access boundary that stands between controller and content;
- `IControllerAccess` omitted silently when content can report or request semantic actions from controller;
- raw callbacks, handlers, anonymous objects, externally assembled access bundles, parameter bags, or full controller/content references used instead of named internal contract artifacts where the technology can express them;
- generated file organized from implementation detail outward when the technology does not require it;
- controller/node declaration buried after hidden implementation classes in a one-file node implementation.

**Repair:**
- reorder declarations so the implementation reads from external node surface toward internal content implementation;
- preserve runtime behavior while moving only declaration order;
- keep technology-specific syntax secondary to the architectural ordering.

---

## 9. Child Node Encapsulation Invariant

Child nodes are the internal implementation of the parent. The parent owns them,
initializes them, and orchestrates their lifecycle. External code has no claim to
direct access to a parent's children.

A node must not expose its child nodes through public getters or any other public
interface. A child node reference gives the caller unrestricted access to the
child's full API — bypassing the parent entirely. This is a structural bypass of
the tree hierarchy, equivalent in severity to exposing a content object directly.

If external code requires a piece of information or behavior that a child provides,
the parent must define an explicit getter or method that extracts and returns only
the required value — not the child node itself.

**Permitted:**
- a parent exposing derived values obtained from its children (not the children themselves).

**Forbidden:**
- a node defining a public getter or method that returns a child node reference;
- external code holding a direct reference to a non-direct child;
- bypassing the parent's public interface by going directly to the child.

**Violation:**
- any public getter on a node that returns a child node instance;
- any external code that accesses another node's child directly.

**Repair:**
- remove the public getter that exposes the child;
- if the caller needed specific data from the child, add a dedicated getter on
  the parent that returns only that data value, not the child node itself.

---

## 10. Phase Separation Invariant

A node's constructor must not serve as a bucket for initialization phases that belong to separate semantic lifecycle methods.

The constructor may be used by a target runtime as the materialization entrypoint.
When it is used this way, it must still keep semantic responsibilities explicit:
- parent registration / parent linkage;
- guaranteed reference capture;
- content materialization;
- child materialization;
- initial child assignment, if applicable;
- local content subscriptions, if they belong to content materialization.

The following must not appear in the constructor:
- attaching or mounting this node's view into an external container;
- parent-owned child placement performed by a child;
- lifecycle activation/deactivation behavior that belongs to `onOpen()` / `onClose()` or equivalent;
- refresh/data-sync behavior;
- unrelated initialization logic mixed into the materialization path without a named semantic role.

If the technology provides explicit semantic lifecycle methods (`materializeContent`, `materializeChildren`, `onOpen`, `onClose`, `refresh`, etc.), their roles cannot be collapsed into an undifferentiated initialization bucket. If the target runtime materializes one or more phases inside the constructor, the implementation must still keep content materialization, child materialization, activation, and refresh responsibilities explicit and ordered.

**Forbidden:**
- using the constructor as an undifferentiated substitute for content materialization, child materialization, or activation;
- performing content lifecycle and child materialization in a single undifferentiated constructor body;
- treating the constructor as a general initialization bucket for all phases.

**Repair:**
- move content creation into the content materialization phase or method;
- move child materialization into the child materialization phase or method;
- move mount/attach logic into the parent's composition method or switchable
  commit path.

---

## 11. Parent-Owned Materialization Invariant

A child node must not attach or mount its own view into the parent's integration surface.

The decision of where and when to insert a child's visual result belongs exclusively to the parent controller.

A child may:
- prepare and expose its own view through `getView()`;
- perform internal initialization and wiring.

A child must not:
- call `parent.content.mount(this.getView())` or any equivalent from within itself;
- call any parent platform integration method directly from within itself (e.g., `parent.el.appendChild(this.el)` for DOM);
- attach itself to any external container from `onOpen()`, `onClose()`, or any other lifecycle hook;
- assume responsibility for its own placement in the parent's layout.

The parent is the sole authority over where and when each child's view enters the parent's visual composition.

**Forbidden:**
- child self-mounting in `onOpen()`, constructor, content materialization, or child materialization;
- any form of "child integrates itself into parent integration surface";
- relying on parent structure knowledge from inside the child to perform self-insertion.

**Repair:**
- move mount/insert calls to the parent's switchable commit path,
  `buildChildren()`, or a dedicated parent-side composition method;
- child exposes only `getView()`; parent decides placement.

---

## 12. Content Materialization Invariant

A node with content must materialize its content as a separate explicit class — not as inline platform-primitive construction within the controller. This invariant applies when content is declared by `props.contentType`, required by the node prompt, inferred from the implementation model, or otherwise architecturally prescribed.

The content class must own all platform primitive construction, layout, and platform-specific behavior for its node.

The controller must not:
- construct platform primitives (DOM elements, native views, etc.) inline as a substitute for the content layer;
- perform any platform-specific layout or view initialization that belongs to the content class.

A thin content shell that exists only as a formal stub, while the actual platform logic remains in the controller, is a violation equivalent to the absence of a content class.

`props.contentType` is the spec field for explicitly recording content type when that classification must be stored in the model. Its absence does not permit inline platform-primitive construction when the node still has architecturally prescribed content. When `props.contentType` is present, it is a binding contract: a real, non-trivial content class must exist in the implementation, even if content behavior is simple.

**Forbidden:**
- inline `el = document.createElement(...)` or equivalent in the controller constructor when a content class is architecturally prescribed;
- substituting content with a wrapper/area object without a separate class while placing platform construction in the controller;
- treating content class creation as optional when `props.contentType` is declared;
- treating absent `props.contentType` as permission to inline content when the prompt, model, or implementation role still prescribes content.

**Repair:**
- move all platform primitive construction into a dedicated content class;
- controller interacts with content through `IContentAccess`;
- content is created in the content materialization phase.

---

## 13. Shared State Ancestor Invariant

State that is consumed by two or more sibling branches must be owned and
coordinated at the closest common ancestor controller.

Mutation authority determines ownership, not read volume. The controller that
owns the action that changes the state is the owner, regardless of how many
branches read it. Reading a value in multiple branches does not split ownership.

When cross-cutting state is needed by multiple children, the common ancestor
derives it once and exposes it through explicit access methods or named update
methods owned by the relevant controller boundary. It must not push the derived
value into child constructors, Content constructors, public runtime parameters,
parameter bags, config/options/props-like objects, callbacks, handlers, or prebuilt fragments. Children consume the derived value
through explicit local access/update methods after they have been constructed at
their tree positions; they do not independently derive the same fact from
cross-cutting sources.

See also: `references/architecture-rules.md` R4c — the related but distinct
case where the state holder must be the owner of the managed entity, not the
control element that triggers the state change.

Forbidden:
- duplicating state derivation in multiple controllers when a common ancestor could own it;
- passing raw integration sources to multiple sibling controllers so each derives
  the same fact independently;
- treating the controller that reads state most often as the owner.

---

## 14. Derivation Uniqueness Invariant

A typed fact derived from a cross-cutting source must be computed at exactly one
controller per subtree, then distributed as an explicit typed value.

If the same fact appears in multiple controllers — each independently deriving it
from the same underlying source — this is a derivation duplication defect.
The correct form: one controller derives the fact once; other controllers obtain
the derived value through explicit access methods or named update methods after
they have been constructed at their tree positions. The derived value must not be
pushed through child constructors, Content constructors, public runtime parameters,
parameter bags, config/options/props-like objects, callbacks, handlers, or prebuilt fragments.

This invariant applies regardless of whether the derivation is cheap or expensive.
The concern is ownership clarity: one derivation point makes the source-of-truth
unambiguous and refactoring safe.

Forbidden:
- two controllers independently computing the same typed fact from the same raw source;
- distributing raw integration data to multiple controllers so each independently
  performs the same derivation.

### Shared derived fact repair rule

Repair must not trade one ownership violation for the other.

If a shared or parent-owned derived fact is duplicated in multiple controllers,
repair must not pass the derived value into a child Node/Controller through
constructors, public runtime parameters, config/options/props-like objects,
parameter bags, callbacks, handlers, or prebuilt fragments. That repair only
replaces Invariant 14 with `CORE-029`.

If a child Node/Controller receives a parent-derived fact through a public
runtime input, repair must not make the child independently derive the same fact
from the same cross-cutting source. That repair only replaces `CORE-029` with
Invariant 14.

The valid direction is to introduce or use an explicit typed access/update
boundary, named controller method, or modeled connector contract after the child
exists at its tree position. If that boundary is not yet modeled, the repair is
blocked and must report the remaining violation instead of inventing a local
workaround.
