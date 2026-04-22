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
- a parent calling `getView()` on its direct children and composing the results into its own view.

Forbidden:
- calling `getView()` on a node from any position other than its direct parent;
- accessing a descendant's view by bypassing intermediate nodes;
- calling `getView()` on a sibling node directly;
- skipping levels in view composition.

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

The controller communicates with content exclusively through explicitly named command methods of `IContentAccess`. Such methods accept commands, parameters, and handlers. They do not expose the platform primitive and do not return a handle to it for controller-side manipulation.

The only permitted low-level handle exposure is the node's opaque `getView()` result for parent-owned placement/composition. This handle is not part of the controller's permission to operate on its own content primitive.

The controller must not depend on the type, structure, or API of the platform primitive.

The prohibition applies not only to usage but also to definition. A base class in the controller hierarchy that defines a public property or getter exposing the platform primitive is itself a violation — even if no direct usage of that property appears in application code. The existence of such a mechanism constitutes a structural bypass of the invariant: it makes the violation available to every subclass automatically, without any explicit act of access.

**Violation:**
- controller accessing the platform primitive owned by the content, including through a public or base-class property or any exposed reference;
- controller code using the node's own render/view/native primitive, its platform API, or any equivalent exposed primitive handle for its own content;
- any class in the controller hierarchy defining a public property or getter that exposes the platform primitive, including in a base class;
- content exposing its platform primitive through `IContentAccess` for anything other than the narrow opaque `getView()` placement/composition handle.

**Detection examples (DOM-like targets):** `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()`. On other platforms, the equivalent is any direct handle to the native/render primitive owned by the content.

**Repair:**
- add a named command method to `IContentAccess`;
- the controller calls the method, passing the necessary parameter or handler;
- the content executes the command on its platform primitive internally.

---

## 8. Declaration Order Invariant

Generated node implementation declarations must follow architectural depth from outside to inside.

The controller/node is the external surface of the node and must be the first declaration for that node's implementation unit.

Internal access boundary artifacts stand between the controller and the hidden content/view implementation. Therefore they must be declared after the controller/node and before the content/view implementation. Both internal directions are part of this ordering rule: controller-to-content (`IContentAccess` or equivalent) and content-to-controller (`IControllerAccess` or equivalent). If one direction has no permitted calls, an explicit zero-contract must be declared according to the target technology or project convention.

The hidden content/view implementation is the deepest implementation part and must be declared after the boundary artifact that mediates access to it.

For a one-file node implementation, the canonical order is:

```text
Controller/Node
IContentAccess or technology-specific controller-to-content boundary
IControllerAccess or technology-specific content-to-controller boundary
Content/View
```

If a direction is intentionally empty, the zero-contract declaration belongs in the same boundary layer.

If a target technology requires separate files or a project convention uses split materialization, the same public-to-private organization must be preserved in file structure and exports: external controller/node artifact first, internal boundary artifacts next, hidden content/view implementation artifacts last.

**Violation:**
- content/view declared before the access boundary that stands between controller and content;
- `IControllerAccess` omitted silently when content can report or request semantic actions from controller;
- raw callbacks, anonymous objects, or full controller/content references used instead of named internal contract artifacts where the technology can express them;
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
- move mount/attach logic into the parent's composition method or `openChild()`.

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
- move mount/insert calls to the parent's `openChild()`, `buildChildren()`, or a dedicated parent-side composition method;
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
