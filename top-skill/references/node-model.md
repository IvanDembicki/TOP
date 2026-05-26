# Node Model

The node model describes what a node is in TOP, what properties it has,
how it owns child nodes, and how it relates to runtime/materialization behavior.

---

## 1. Node as the Basic Unit of the Tree

A node is a structural unit within a tree.

At minimum, a node is defined by:
- identity;
- parent relation;
- child policy;
- semantic role;
- ownership boundaries.

A node does not have to coincide with:
- a visual component;
- a runtime instance class;
- a data object.

Every node always has a **controller**.

The controller is the sole architectural carrier of node behavior, manages the node lifecycle and content lifecycle, coordinates orchestration, branching, and the node's external behavior.

The controller is not the node's content and not the node's platform
materialization. It is the external architectural boundary and orchestration
owner only.

The controller may be complex, but only inside the controller responsibility
domain. If it becomes a view, component, widget, renderable artifact,
render/build function, platform UI lifecycle object, or public runtime input
receiver for content composition, the node model is invalid.

The runtime TOP tree is a tree of controller objects. A controller without tree
position is not a TOP controller. A controller-shaped service/helper/module with
no parent/context or root context, no child ownership, no lifecycle, and no
relationship to the spec tree is not a TOP node even if the file or class name
ends with `Controller`.

Canonical formula: A controller without tree position is not a TOP controller.

Every node controller must either extend the project's canonical TOP node base
class or implement the canonical TOP node runtime interface for the
target/project. The concrete names are local, but the roles are required:
parent/context or root/host context, children access, child ownership and
registration, lifecycle, child construction policy, refresh/invalidate/update
lifecycle when applicable, disposal/cleanup, and materialized output access
through its private content boundary when content exists.

Root controllers remain runtime tree roots. Leaf controllers remain runtime
tree nodes. A root has root/host context instead of ordinary parent; a leaf may
declare no children, but it still has or inherits runtime node mechanics.

### 1.0.1. Minimal Runtime Node Shape

Every concrete runtime TOP tree must preserve three canonical node shapes:
- **root controller** - has root/host context and owns its declared children;
  it does not have an ordinary parent;
- **branch controller** - has parent/context, root context, and declared
  child ownership;
- **leaf controller** - has parent/context and root context, declares no
  children, and still has or inherits runtime node mechanics.

Minimum runtime topology contract:
- every non-root node has exactly one parent/context reference;
- every parent-owned child collection contains each direct child exactly once;
- child construction or attachment registers the child with its parent at the
  child's tree position;
- a child cannot be stitched into the topology later through external setters,
  data packets, render composition, or ad hoc list mutation;
- a child resolves the same root/root context as its parent;
- depth, order, and index, when materialized, are derived from current tree
  position or kept consistent with it by the owning topology operation;
- ancestor traversal, debug tree printing, and topology introspection are
  permitted when they expose structure only and do not become behavior-routing
  mechanisms.

Each non-leaf controller must declare its allowed direct child policy. The
policy may be represented by target-language types, schema entries, prompt tree
children, or an equivalent project-local contract, but it must be explicit
enough to reject accidental child kinds. A leaf declaration means the node owns
no children, not that it loses runtime node identity.

If a node has content, the node must consist of two distinct classes:
- `Controller`
- `Content`

If there is no content, a node may consist of the controller alone.

Concrete content is always hidden behind the controller.
The controller is the sole external interface of the node.

Node-level logic must reside in the controller.
Content is permitted in two forms:
- **locally implemented static materialization** — content materializes a
  structurally static content shape and applies already-resolved
  primitive/output values received through its owning controller access
  contract. It contains no conditional selection logic of any kind and must not
  decide, derive, branch, select, toggle, format, concatenate, hardcode, or
  compute which structure, class/style/token, text, icon, visibility, handler,
  child output, platform primitive, representation, output value, or capability
  should be used.
- **black box with an explicit interface** — content encapsulates external,
  native, third-party, or self-contained logic as a black box; the controller
  sees only the explicit interface via `IContentAccess`; the internal
  implementation is inaccessible.

In both cases, content is prohibited from:
- reading architectural state (openedChild, isEditMode, lifecycle phase);
- modifying the tree structure;
- initiating structural transitions;
- becoming a hidden decision engine;
- receiving controller-pushed presentation state or imperative mutation commands.

---

### 1.1. Pull-Based Construction and Locality of Object Birth

A TOP object is constructed at the exact place where it architecturally belongs
in the tree. Objects are not assembled outside the tree and pushed inward.

TOP construction attaches an object to its context; it does not inject the state
it will use. Objects are connected to context, not filled with data. After
attachment, a node, locally implemented content object, connector, or black-box
boundary requests required values through its contextual access contract.

Constructor arguments and post-construction setter-style calls must not be used
as hidden data-flow paths for data packets, flags, callbacks, configuration,
stores, services, child views, presentation values, visibility values, style
values, text values, runtime state, or handlers.

Node construction:
- a static Node constructor receives exactly one semantic argument: its
  parent/context reference;
- a runtime-created branch root may receive parent/context plus one canonical
  Runtime Branch Binding input: entity context reference, stable identity key,
  or typed immutable DTO fallback;
- for a root node, the parent may be `null` or `RootContext`;
- `RootContext` is only a root ownership/bootstrap marker, not a dependency
  injection container;
- the parent Node/Controller owns and constructs its direct children;
- Node/Controller public runtime entrypoints must not receive semantic data,
  parent-derived facts, callbacks, services, stores, child fragments,
  config/options/props-like objects, parameter bags, runtime argument sets, or
  arbitrary props.
- Runtime branch binding must not be scattered data, props/config/callback bags,
  mutable raw model objects, services/stores, presentation values, or arbitrary
  runtime state.
- Shared derived facts are not repaired by choosing between duplicate derivation
  and runtime input tunneling. They require an explicit typed access/update
  boundary, named controller method, or modeled connector contract after the
  child exists at its tree position.

Content construction:
- a Content constructor receives exactly one semantic argument: the owning
  controller instance typed only through the narrow `IControllerAccess` or
  target-equivalent interface, not an
  adapter/facade, method bag, or decomposed prop set;
- the constructor must not be typed as the concrete controller class;
- the runtime object must be the owning controller instance, but Content must store
  and use it only through the narrow access interface;
- if the access interface has no methods, it is an empty zero-contract
  implemented by the owning controller, not a separate dummy access object;
- Content must not import, inspect, or downcast to the concrete controller;
- Content must not receive additional data, callbacks, handlers, flags,
  state, stores, services, child components, slots, prebuilt view fragments,
  platform child views, child view handles, child-output getter bundles,
  view-model objects, config/options/props-like objects, parameter bags,
  runtime argument sets, or arbitrary props;
- public runtime parameters, render/build parameters, composition entrypoints,
  parameter bags, and props-like/config/options objects are not a valid
  substitute for constructor injection.

The legal data-flow direction is:

```text
View -> owning controller -> child controller -> opaque public view handle
```

This keeps ownership local, makes each node understandable in isolation, and
prevents ordinary platform composition from being mistaken for TOP architecture.

---

### 1.2. Controller Role Purity

A TOP controller is a non-renderable orchestration boundary.

It may own lifecycle, child management, state transitions, routing,
validation, async flow, and domain decisions that belong to its node. It must
not itself be the target runtime's rendered content, render/build function,
layout/style/animation/content artifact, platform UI lifecycle object, or
runtime input receiver for content composition.

If the target runtime needs a renderable entrypoint, that entrypoint is
Content or a thin framework adapter. It may host or delegate to the TOP
branch, but it is not the controller identity and must not accumulate
controller logic.

Controller complexity may be a design smell. Controller role leakage is a
structural violation.

---

## 2. Content and `props.contentType`

If a node has content, it must have exactly one concrete content class.

Content is not the architectural owner of node behavior.
It either contains no conditional selection logic of its own at all, or
encapsulates external, native, third-party, or self-contained logic as a black
box accessible to the controller only through an explicit interface.

This content class, when explicit type recording is required, is described via `props.contentType`.

Base canonical values of `props.contentType`:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

Anything materialized as view, component, data, style, animation, transition,
asset/resource, or another content kind belongs to content-side materialization,
not to controller identity.

### 2.1. `view`
Locally implemented content of the given node.
It is subject to the internal rules of the node and is not an independent
external system. It is static implementation material, not a decision-making
layer: it may apply already-resolved primitive/output values, but it must not
contain conditional selection logic, formatting, concatenation, hardcoded
display values, or output derivation.

### 2.2. `component`
Content of the given node, treated as a black box.
It may live by its own internal rules, but for the outside world it is still hidden behind the node's controller.

### 2.3. `data`
Data-content of the given node.
It is not exposed externally as a content-object; access to the data goes only through controller methods.

### 2.4. `style`
Style-content of the given node.

### 2.5. `animation`
Content representing animation behavior or animation state.

### 2.6. `transition`
Content representing the transitional state of a node or subtree.

### 2.7. `asset`
Static resource content: image, icon, svg, sound, template fragment, and similar cases.

### 2.8. `other`
A fallback type for rare cases where a separate canonical type has not yet been defined.

---

## 3. Two Protocol Layers of a Node

A node has two distinct protocol layers. Mixing them is categorically prohibited.

### 3.1. External Node Interaction Protocol

The controller is the sole external interface of the node.
The external node interaction protocol is used for architectural interaction of the node with the outside world:
- with the parent;
- with child nodes;
- with other permitted external participants.

This means:
- direct access to concrete content from outside is prohibited;
- external interaction with a node goes only through the controller;
- orchestration, branching, navigation, lifecycle coordination, and external behavioral coordination belong to the controller;
- content must not become the architectural center of the node.

For visual content, the controller may expose only a general abstract visual interface externally,
if this is required for composing child visual content.

This exposed visual interface is an opaque view handle.
It is permitted only for parent-owned materialization:
- mount;
- unmount;
- insert;
- reorder;
- replace;
- passing the child view into the parent's own content boundary for placement.

The parent/controller must not inspect the handle, attach event listeners to it,
mutate its styles/classes/attributes, query inside it, or use its platform API
as a behavior or communication channel.
Any operation other than placement/composition must go through the child's public node surface
or through an explicit boundary owned by that child.

For non-visual content, no public `getContent()` exists.

### 3.2. Internal Access Boundaries

For a node with a separate content class/object, two internal access boundaries exist:
- `IControllerAccess` — access of content to the controller through a narrow private contract, not through the full public node surface;
- `IContentAccess` — access of the controller to content through a narrow private contract.

These are not the external API of the node and have no relation to the public node surface.

If a node has a separate content class/object, separate explicit access artifacts for these boundaries are mandatory.
Such artifacts may be an interface, a nested interface, an abstract contract, an adapter, a wrapper, a proxy, or a separate access class.
An implicit object without a separate contract artifact does not qualify as a complete materialization of the protocol.
If the language supports explicit typing, these artifacts must be materialized in signatures as well: a constructor/factory/method parameter that accepts an artifact must have an explicit contract type; the field/reference storing the artifact must also be explicitly typed. For Content, the public constructor receives exactly one semantic argument, and that argument must be typed as the narrow access interface. The concrete controller class is not an acceptable Content constructor type even if the controller implements the interface. The owning controller implements even an empty content-to-controller zero-contract and passes itself as `this` typed only as that interface; a separate zero-access runtime object is not a correct substitute. The controller stores content through `IContentAccess`, not through the concrete content class. An anonymous/untyped parameter such as `constructor(facing)` is not a correct implementation of a protocol boundary. Anything else is categorically prohibited.

Through `IControllerAccess`, only the following is permitted:
- obtaining data that the content needs for its own construction and update;
- calling explicitly permitted controller access methods;
- passing to the controller only the content's own events;
- if content is visual, requesting only the explicitly permitted child-view endpoints described by the node contract.

Content interacts with its owning controller only through `IControllerAccess`.
If content is visual, its child-view requests must go only through explicitly declared `IControllerAccess` endpoints.
Visual content must not access child nodes directly, must not read `children` directly, and must not select `openedChild` itself.
The controller applies structural/state rules itself and returns to its view-part only those child views that are permitted by the contract of the given node.

For a regular visual node, only explicitly named child-view endpoints are permitted.
Those access methods must be named by semantic child branch/output, for example
`getAccountIdentityView()`, `getOrganizationsAccessView()`, `getAppPreferencesView()`,
or `getDebugAdminToolsView()`. The name does not have to include `Handle` or
`ViewHandle`; `Section` is used only when the branch is actually modeled as a
section. `slot` terminology and generic `children`/`render`/`builder` names are
forbidden because they describe framework composition mechanics rather than TOP
ownership.
For a `DynamicCollectionViewNode`, a separate explicitly described collection-boundary is permitted, through which the controller can return an ordered collection of direct child views of a homogeneous dynamic collection.

Through `IContentAccess`, only the following is permitted:
- obtaining the root view/content result;
- calling strictly permitted lifecycle/content methods;
- performing other internal actions explicitly permitted by the private boundary.

Through `IContentAccess`, data does not flow from controller to content.
Controller-owned data, view-model values, state flags, action methods, and
child-output handles are requested by content through `IControllerAccess`.
An `IContentAccess` interface containing fields that content reads is a direction
collapse, not a TOP access boundary.

`IContentAccess` must not become a presentation command channel. Controller must
not imperatively command, mutate, update, show, hide, configure, set class/style,
apply state, or render-with into locally implemented content. The controller
updates its own state and marks the node/content/runtime dirty or requests
lifecycle/render refresh through the node/runtime mechanism. During
materialization or refresh, content pulls already-resolved primitive values
through `IControllerAccess` and applies them to its static materialization.

Data content has a separate storage role. A data node controller may expose
typed domain methods such as `setAge(value)`, `updateName(value)`, or
`replaceRecord(record)` when access is architectural, and inside that same node
it may mutate its own private data content through `IContentAccess` or an
equivalent internal storage boundary. This does not permit external direct data
content mutation, presentation content direct data access, constructor data
injection, or presentation mutation channels.

`IContentAccess` must not become a channel through which the controller manually bypasses the content boundary or pushes child nodes/content concrete implementation.
It is also the boundary that hides any larger concrete content/component API from
the controller. Even if the concrete content wraps a native view, framework widget,
or third-party component with many public methods, the controller may see only the
small `IContentAccess` surface.

Through internal access boundaries, the following is prohibited:
- accessing parent/root/sibling interaction;
- accessing the public node surface;
- accessing external implementation objects, host/container references, or integration handles;
- using an access boundary as a surrogate channel to reach the outside world;
- obtaining direct access from view/content to child nodes, `children`, or `openedChild`;
- bypassing the controller when obtaining child visual content;
- tunneling semantic dependencies through public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, prebuilt fragments, child components, platform child views, or arbitrary props.

Anything else is categorically prohibited.

## 4. Content Access Rules

Content does not interact with the outside world other than through `IControllerAccess`. Anything else is categorically prohibited.

The controller does not interact with the internal implementation of content other than through the content object and its explicitly defined external interface. If a node has a separate content object, any direct controller bypass to the concrete implementation is a violation. A public/base-class primitive getter, an inherited primitive member, or any other low-level handle-reference does not legalize such a bypass. Anything else is categorically prohibited.

For the controller of the node's own content, `IContentAccess` is limited to
lifecycle/materialization access, such as obtaining the root content primitive or
participating in controlled lifecycle. It is not a channel for presentation
commands, mutation commands, style/class updates, state application, or
render-with instructions.

The following platform-specific DOM-like forms in controller code are detection examples of a confirmed boundary violation:
- `this.el...`;
- `this.getView().classList...`;
- `this.getView().style...`;
- `this.getView().addEventListener(...)` / `removeEventListener(...)`;
- `this.getView().setAttribute(...)` / `removeAttribute(...)`;
- `this.getView().querySelector(...)`;
- `content.getView()` used to obtain and mutate/read the content primitive directly.

The exception is narrow: `getView()` may expose an opaque view handle for parent-owned placement/composition, not for the owning controller's platform operations.

If content is visual, the controller may expose only an abstract visual interface externally,
sufficient for composing child visual content.
The view-part builds only its own visual shell. If it needs child visual content, it must request it through `IControllerAccess`; the controller itself accesses child nodes according to structural and state rules and returns the obtained child view to its view-part.
The returned child view remains opaque. It is a placement/composition handle, not permission to inspect or mutate the child's concrete implementation.

If content is non-visual:
- the content object is not exposed externally;
- access to data and changes goes only through controller methods or through an explicit black-box interface controlled by the controller.

This is necessary so that the controller can:
- control changes;
- initiate re-render;
- coordinate propagation;
- maintain node consistency.

Propagation ownership follows from the same node boundary. A caller may invoke
the node's declared handler/query, but it must not inspect the node's children,
state, modes, or capabilities to decide how propagation should continue inside
that node. The node itself owns whether to return a result, return no-result,
no-op, stop, delegate to an active or selected child, or delegate through a
connector. External ask-then-handle traversal such as
`if child.canHandle(event) child.handle(event)` breaks the node boundary because
the caller starts making decisions that belong inside the child node.

---


## 4.1. Strict Method Semantics

Runtime/lifecycle methods must maintain strict purpose.

If a method is intended for one semantic role, using it for another role is prohibited. Anything else is categorically prohibited.

In particular, a method such as `buildChildren()` is permitted only as a method for the runtime materialization of child nodes.
It is not a general init method of the controller.
The same rule applies to any materialization/lifecycle method with a narrow semantic role, such as `materializeContent()`, `mountContent()`, or a target-specific equivalent.

Using `buildChildren()` for the following is prohibited:
- creating content of the current node;
- initializing the controller instance;
- initial sync of the current node;
- registering listeners of the current node;
- any actions not directly related to building child nodes.

If a node does not use runtime child construction, `buildChildren()` must not exist in that class. Anything else is categorically prohibited.

## 5. Types of Child Relations

When analyzing a node, several relations must be distinguished.

### 5.1. Structural Child
A child that is part of the tree structure of the node.

### 5.2. Logical Child
A child that conceptually belongs to the node by model,
even if its render/materialization occurs outside the node's own host.

### 5.3. Render-Hosted Descendant
A node or subtree that logically/structurally belongs to one branch,
but is materialized in the render host of another node or ancestor.

### Canonical Rule
Render placement does not override structural or logical ownership.

---

## 6. A Node May Have No View Host of Its Own

A node is not required to have:
- its own visual component;
- its own render container.

This is especially normal for:
- state nodes;
- purely structural nodes;
- helper nodes;
- logical grouping nodes.

### Corollary
The absence of a view host or visual wrapper
does not mean the node "does not exist" in the TOP model.

---

## 7. Node as Child Policy Owner

Every node must have a clear child policy.

It must be clear:
- whether the child set is fixed or mutable;
- whether children are immutable or mutable;
- whether single-child mutable behavior is permitted;
- whether children are switchable or non-switchable;
- if switchable, whether the candidate child set is fixed or dynamic;
- whether `childrenType` is needed;
- whether there is a library/template child pattern;
- who is considered the owner of child instances.

### Canonical Rule
If without `childrenType` or an equivalent child policy description it is unclear
how children are created and replaced, the model is incomplete.

See `references/child-contract.md` — the formal description of the two child contract modes.

### 7.1. Runtime List and Entity Binding Spec Vocabulary

The following spec props are canonical child-policy metadata when a project uses
runtime/library child generation:

- `props.childPolicy` declares how the parent owns and materializes children.
  `runtime-list` means the parent owns a mutable runtime list of homogeneous
  child node instances. It is declarative spec metadata, not runtime props,
  config, or data injection.
- `props.runtimeChildType` names the modeled runtime/library child type created
  under that child policy. It must refer to a declared node type or library node
  type, such as `lib:devices.DeviceItem`; it must not become an arbitrary
  component/class name invented during generation.
- `props.entityBinding` names the narrow entity/model access contract required
  to bind a runtime branch instance to the entity it represents. It is a
  canonical Runtime Branch Binding input, not arbitrary props injection, not a
  raw data packet, and not a config/callback bag.

Generation uses these props only to preserve the modeled child policy:
parent-owned runtime child construction, narrow entity binding for each runtime
child, and explicit controller/content contracts inside the child. Agents must
not introduce new spec props silently; every project-level prop must be defined
in canon, reference material, or a project-local spec vocabulary before it is
used as implementation truth.

---

## 8. Single-Child Mutable Nodes

A `single-child mutable node` is a node in which at a specific child position
only one active child instance is allowed at any given time, but the child itself
can be replaced or recreated over time.

This is not the same as:
- a switchable state holder;
- a fixed immutable single child;
- a list-like mutable container.

### Distinctions
- a switchable node typically has a fixed set of alternative states;
- a single-child mutable node's child instance can be runtime-created/replaced;
- child composition here is mutable, not merely selectable.

---

## 9. Switchable Nodes and State Holders

If a node participates in state switching, the following must be distinguished:
- state holder;
- state node;
- visual reflection of state;
- control element that is not itself a state owner.


### Dynamic switchable

A `dynamic switchable node` is permitted when:
- the candidate child set is created, removed, or replaced at runtime;
- the holder owns exactly one selected/opened child from that candidate set;
- selection changes use the same lifecycle-consistent switching path as any other switchable node;
- the candidate-set source of truth and selected-child source of truth are explicit;
- child type policy is explicit, for example through `childrenType` or an equivalent project-local contract;
- the policy for removing the currently opened child never leaves
  `openedChild` null during active behavior propagation. It must select another
  candidate, open an explicit empty/unavailable state candidate, or leave the
  switchable role through a declared lifecycle transition.

A dynamic switchable node is not a plain mutable collection. The defining feature is not dynamic children by itself, but dynamic candidates plus owner-managed active/opened selection.
### Error
Attributing state ownership to a control element merely because it visually
switches state.

State ownership is determined by the tree model, not by the UI trigger.

---

## 10. Library Nodes (lib:true)

`lib:true` designates a child node whose instances are created not during parent initialization,
but through a library — at runtime or deferred.

Two usage scenarios:
- **dynamic** — instances are created and removed during the application's operation;
- **deferred static** — the instance is effectively static, but is created after parent initialization.

For AI, both scenarios are equivalent: `lib:true` means library node.
The difference in scenario does not affect analysis.

### Library Object External Context Boundary

Recommended pattern: the root of a runtime/library object acts as the external
context boundary for its runtime branch.

The root is the preferred attachment point for branch-external dependencies:
parent context, data tree access, presentation/style tree access, asset tree
access, permissions, runtime services, external connectors, and other external
trees or contextual structures.

Descendants inside the library object should not independently reach outside
the branch. They should request required values or capabilities through the
library object root, or through narrow contracts derived from that root. The
root may obtain external information from its parent, explicitly attached
context contracts, or approved connectors, and then expose only the minimal
resolved access needed by internal descendants.

This is not a hard invariant. It is a strong recommended modeling pattern.
Exceptions are allowed when explicitly described in the spec, prompt, or branch
contract. Do not reduce it to "the root holds the data model": the root is the
external context boundary, not necessarily a data holder.

### Location of the Lib Type

The lib type can be declared:
- inline — as a child node directly in the parent's description (used only in that location);
- in the project `Library` branch under the single root, as a shared project type (used in multiple places).

### External Spec Files

Any subtree, including a library namespace, may be stored in an external spec file.
The parent keeps the node entry in the tree and sets `props.source` to a path relative to the project `top/` directory.
The external file must describe the same node type and is part of the same tree model; it is not an import of a separate tree.

### Canonical Rule

If a node contains `lib:true` children but their type is not documented —
this is an incomplete description. The analyzer must record the violation
and require correction before continuing.

---

## 11. Composite Nodes and Hidden Semantic Parts

If a node appears monolithic but in fact includes several semantic parts,
analysis must attempt to recover the hidden semantic subparts.

This is especially important when:
- one visual block conceals multiple node responsibilities;
- a state holder, content host, and child container effectively live inside the node;
- an implementation mixes different semantic roles in one class/component.

### Canonical Rule
Composite decomposition must be recovered by meaning, not only by files/classes.

---

## 12. Node Ownership vs Render Hosting

The following must be distinguished:
- who is the structural owner of a child;
- who is the logical owner of a child;
- who is the render host;
- who merely provides a container for attachment.

### Permitted Pattern
A child logically belongs to a state node or composite branch,
but is materialized in an ancestor-owned container.

This is not a violation, provided that:
- logical ownership is explicit;
- child lifecycle is controlled by the correct owner;
- render hosting does not obscure tree relations.

### Violation
If a node is considered the parent solely because it contains the visual container,
this is a substitution of structural/logical ownership with visual placement.

---

## 13. Mutable Container Responsibilities

If a node is a mutable container, its responsibilities must be defined:
- create child instances;
- register child instances;
- remove child instances;
- cleanup stale instances;
- maintain ordering;
- coordinate rendered children with structural children;
- coordinate reverse sync with source of truth, if required.

### Canonical Rule
A mutable container must not have diffuse responsibility for child lifecycle.

---

## 14. Node Model and Source of Truth

A node is not required to be a source of truth in itself.
But if a node edits, creates, deletes, or reorders children,
it must be clear:
- whether it is an authoritative owner or a derived runtime layer;
- whether it is required to initiate serialization back;
- which changes are temporary UI-only.

For editor-like systems, this question is mandatory.

---

## 15. Typical Node-Model Violations

Typical violations include:
- absence of the controller as the sole external interface of the node;
- presence of content without separating it from the controller;
- multiple concrete content classes for one node;
- confusion of `view` and `component`;
- direct public access to non-visual content;
- confusion of fixed/dynamic switchable node and single-child mutable node;
- confusion of state owner and visual trigger;
- confusion of logical owner and render host;
- mutable child policy without explicit description;
- absence of `childrenType` when the child policy is unclear without it;
- automatic interpretation of `lib:true` without considering the scenario;
- composite node without an attempt at semantic decomposition.

---

## 16. What a Good Node Analysis Must Deliver

A good node analysis must answer the following questions:
1. What is the semantic role of the node?
2. Who is its structural parent?
3. What are its children and what is their policy?
4. Is there mutable/single-child mutable/fixed switchable/dynamic switchable behavior?
5. Are there hidden semantic subparts?
6. Is there content?
7. What is `props.contentType`, if the content type must be explicitly recorded?
8. Is content separated from the controller?
9. Who owns the children?
10. Where is logical ownership, and where is render hosting?
11. How is the node related to the source of truth?
