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

If a node has content, the node must consist of two distinct classes:
- `Controller`
- `Content`

If there is no content, a node may consist of the controller alone.

Concrete content is always hidden behind the controller.
The controller is the sole external interface of the node.

Node-level logic must reside in the controller.
Content is permitted in two forms:
- **logic-free implementation material** — content only creates structure and applies styling; it contains no behavioral logic of its own; all behavior is delegated to the controller via `IControllerAccess`;
- **black box with an explicit interface** — content encapsulates internal presentation logic (animations, scroll state, focus management, etc.) as a black box; the controller sees only the explicit interface via `IContentAccess`; the internal implementation is inaccessible.

In both cases, content is prohibited from:
- reading architectural state (openedChild, isEditMode, lifecycle phase);
- modifying the tree structure;
- initiating structural transitions.

---

## 2. Content and `props.contentType`

If a node has content, it must have exactly one concrete content class.

Content is not the architectural owner of node behavior.
It either contains no logic of its own at all, or encapsulates internal logic as a black box accessible to the controller only through an explicit interface.

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

### 2.1. `view`
Locally implemented content of the given node.
It is subject to the internal rules of the node and is not an independent external system.

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
- `IControllerAccess` — access of content/view to the controller through a narrow private contract, not through the full public node surface;
- `IContentAccess` — access of the controller to content through a narrow private contract.

These are not the external API of the node and have no relation to the public node surface.

If a node has a separate content class/object, separate explicit access artifacts for these boundaries are mandatory.
Such artifacts may be an interface, a nested interface, an abstract contract, an adapter, a wrapper, a proxy, or a separate access class.
An implicit object without a separate contract artifact does not qualify as a complete materialization of the protocol.
If the language supports explicit typing, these artifacts must be materialized in signatures as well: a constructor/factory/method parameter that accepts an artifact must have an explicit contract type; the field/reference storing the artifact must also be explicitly typed. An anonymous/untyped parameter such as `constructor(facing)` is not a correct implementation of a protocol boundary. Anything else is categorically prohibited.

Through `IControllerAccess`, only the following is permitted:
- obtaining data that the content needs for its own construction and update;
- calling explicitly permitted controller access methods;
- passing to the controller only the content's own events;
- if content is a `view`, requesting only the explicitly permitted child-view endpoints described by the node contract.

If content is a `view`, its child-view requests must go only through `IControllerAccess`.
A `view` must not access child nodes directly, must not read `children` directly, and must not select `openedChild` itself.
The controller applies structural/state rules itself and returns to its view-part only those child views that are permitted by the contract of the given node.

For a regular visual node, only explicitly named child-view endpoints are permitted.
For a `DynamicCollectionViewNode`, a separate explicitly described collection-boundary is permitted, through which the controller can return an ordered collection of direct child views of a homogeneous dynamic collection.

Through `IContentAccess`, only the following is permitted:
- obtaining the root view/content result;
- calling strictly permitted lifecycle/content methods;
- performing other internal actions explicitly permitted by the private boundary.

`IContentAccess` must not become a channel through which the controller manually bypasses the content boundary or pushes child nodes/content concrete implementation.

Through internal access boundaries, the following is prohibited:
- accessing parent/root/sibling interaction;
- accessing the public node surface;
- accessing external implementation objects, host/container references, or integration handles;
- using an access boundary as a surrogate channel to reach the outside world;
- obtaining direct access from view/content to child nodes, `children`, or `openedChild`;
- bypassing the controller when obtaining child visual content.

Anything else is categorically prohibited.

## 4. Content Access Rules

Content does not interact with the outside world other than through `IControllerAccess`. Anything else is categorically prohibited.

The controller does not interact with the internal implementation of content other than through the content object and its explicitly defined external interface. If a node has a separate content object, any direct controller bypass to the concrete implementation is a violation. A public/base-class primitive getter, an inherited primitive member, or any other low-level handle-reference does not legalize such a bypass. Anything else is categorically prohibited.

For the controller of the node's own content, the required form is an explicitly named command on `IContentAccess`,
for example `this.content.setDragging(value)` or `this.content.setDropPosition(position)`.
The content executes the platform operation internally.

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
- the policy for removing the currently opened child is explicit: fallback selection, null/empty state, or another declared behavior.

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
