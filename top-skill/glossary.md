# Glossary

## 1. Tree

**Tree** — a hierarchical structure of nodes with strict parent-child relationships.

---

## 2. Node

**Node** — the basic unit of a tree. A node always has a controller.
If a node has content, the content is separated from the controller and hidden behind it.

---

## 3. Controller

**Controller** — the mandatory part of a node, the sole external interface of a node and the sole architectural carrier of node behavior.

Controller:
- stores and organizes node logic;
- receives events from content;
- manages state, propagation, and re-render;
- manages node lifecycle and content lifecycle;
- coordinates orchestration, branching, and external node behavior;
- exposes only the permitted abstract interface of the node to the outside;
- does not use the internal implementation of content as an interaction channel.

---

## 4. Content

**Content** — the hidden internal implementation of a node.
If a node has content, it must be extracted into a separate concrete content-class.

Exactly one concrete content-class is permitted per node.
Ordinary content has no architectural will and does not interact with the outside world other than through `IControllerAccess`. Any other approach is strictly forbidden.

---

## 4.1. `IControllerAccess`

**`IControllerAccess`** — the private protocol for content/view access to the controller. Through it, content/view does not receive the full public node surface, but only a narrow, permitted internal access contract.
Through it, content receives only a narrow, explicitly permitted, and strictly limited access to the data and actions of the controller
that are genuinely needed for building, updating, and handling content's own events.

`IControllerAccess`:
- is not an external API of the node;
- is not the full controller;
- does not grant access to parent/root/sibling interaction;
- does not grant access to the public node surface;
- does not contain host/container references or integration handles unless they are part of the strictly permitted private contract;
- must be explicitly and as strictly as possible typed where the language allows;
- must be hidden from the outside world to the extent the technology permits.

If a node has a separate content-class/object, an explicit `IControllerAccess` is mandatory. Any other approach is strictly forbidden.

## 4.2. `IContentAccess`

**`IContentAccess`** — the private protocol for controller access to content. Through it, the controller does not gain access to arbitrary internals of content, but only to the narrow permitted internal access surface.
Through it, the controller receives only explicitly permitted access to content,
necessary for obtaining the root view/content result, lifecycle operations, and other strictly permitted internal actions.

`IContentAccess`:
- is not an external API of the node;
- is not a surrogate channel for bypassing the content boundary;
- does not legalize direct access to the concrete implementation outside the permitted content surface;
- must be explicitly and as strictly as possible typed where the language allows;
- must be hidden from the outside world to the extent the technology permits.

If a node has a separate content-class/object, an explicit `IContentAccess` is mandatory. Any other approach is strictly forbidden.

## 4.2.1. Access artifact materialization

**Access artifact materialization** — the concrete form of implementing `IControllerAccess` and/or `IContentAccess`.
It is a specially designated and explicitly defined interface/class/reference/adapter/proxy/wrapper artifact
through which the corresponding internal boundary is materialized.

If a node has a separate content-class/object, materialization of internal access boundaries is mandatory.
It may be implemented as a separate interface, nested interface, abstract contract, adapter,
wrapper, proxy, or other explicitly designated typed artifact, if the technology permits.
An implicit object without a separate typed boundary does not qualify as a full materialization protocol.

It:
- is not an external API of the node;
- is not the full controller or the full concrete content-object;
- cannot be used as a surrogate-channel for accessing the outside world;
- must exist as a named contract artifact or other explicitly designated typed boundary;
- must be present as an explicitly typed boundary reference in the places in code
  where it is passed, stored, or received, if the language permits.

Any other approach is strictly forbidden.

## 4.3. Public node surface

**Public node surface** — the protocol through which a node interacts with the outside world
as an architectural unit: with parent, child nodes, and other permitted external participants.

This protocol:
- belongs to the node/controller, not to content;
- is not exposed to content;
- is not mixed with `IContentAccess` and `IControllerAccess`.

Any other approach is strictly forbidden.

## 4.4. Closed black box

**Closed black box** — content whose internal logic is completely closed and inaccessible to the controller,
except through the explicitly defined external interface.

## 4.5. Explicit protocol typing

**Explicit protocol typing** — the requirement to explicitly and as strictly as possible define types at protocol boundaries
wherever the language allows. An implicit or loosely defined protocol object is not permitted
if the language allows the contract to be defined explicitly. This includes:
- a separate named contract artifact;
- explicitly typed constructor/factory/method parameters accepting the protocol artifact;
- explicitly typed fields/references where the protocol artifact is stored;
- prohibition of anonymous untyped parameters such as `constructor(facing)` without an explicit contract type where the language allows it to be defined.

## 4.6. Node validation rules

**Node validation rules** — a mandatory post-generation/post-refactor verification layer
that must detect a class of violation, classify it as a violation/ambiguity,
suggest the canonical direction for correction, and require re-verification after the fix.

Successful compilation or local operability does not cancel node validation rules.
Any other approach is strictly forbidden.

## 5. Node schema and `props`

**Node schema** — the minimal and stable set of top-level fields of a node spec.

Additional, project-specific, and descriptive node properties must not be added as new top-level fields.
They are placed in `props`.

`props` — the primary extension point of the node spec.

---

## 6. `props.contentType`

`props.contentType` — a spec property in `props`, used to explicitly fix the content type of a node. This is not a separate top-level field of the node schema.

Canonical values:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

### 6.1. `view`
Locally implemented content of this node.

### 6.2. `component`
Black-box content of this node.

### 6.3. `data`
Data-content of this node.

### 6.4. `style`
Style-content of this node.

### 6.5. `animation`
Animation content or animation content-state representation.

### 6.6. `transition`
Transitional content or transition-state representation.

### 6.7. `asset`
Resource content: image, icon, svg, sound, template fragment, etc.

### 6.8. `other`
Fallback type.

---

## 7. Parent / Child

- **Parent** — a node that contains another node as a child.
- **Child** — a node that is part of a parent node.

Parent-child relationships must be typed in both directions.

---


## 7.1. `TreeNode` / `SwitchableTreeNode` / `OpenableTreeNode`

- **`TreeNode`** — the basic structural runtime contract of a node: ownership, navigation, detach lifecycle.
- **`SwitchableTreeNode`** — the parent-side role that owns `openedChild` and the canonical switching path.
- **`OpenableTreeNode`** — the child-side role that can request to open itself and provides local/branch lifecycle hooks.

## 7.2. `ViewNode`

**`ViewNode`** — the visual role in which the view-part builds only its own visual shell and receives child visual content only through the controller.

## 7.3. `DynamicCollectionViewNode`

**`DynamicCollectionViewNode`** — a special `ViewNode` that owns a homogeneous dynamic child collection and has the right to build repeated visual composition through iteration over the direct child nodes of its collection boundary.

## 8. Branch

**Branch** — a subtree starting from a given node and including all its descendants.

---

## 9. Representation Levels and Core Node Terms

### 9.1. Spec tree

**Spec tree** — a formal JSON description of the system structure.

### 9.2. Class tree

**Class tree** — the hierarchy of classes implementing the spec tree.

### 9.3. Instance tree

**Instance tree** — runtime objects materialized in memory during system execution.

### 9.4. Node spec

**Node spec** — a JSON description of a specific node within the spec tree.
Typically contains:
- `type`
- `doc`
- `prompt`
- `props`
- `children`

If a node has content and its type needs to be explicitly fixed, this is done via `props.contentType` inside `props`, not via a separate top-level field.

### 9.5. Node implementation prompt file

**Node implementation prompt file** — a separate project-local prompt file
associated with a single node and describing its implementation.

---

## 10. State Terms

### 10.1. State holder

**State holder** — a switchable node that manages switching between child state nodes.

### 10.2. State node

**State node** — a child node of a state holder, representing one of the possible states.

### 10.3. State tree

**State tree** — a tree that contains at least one state node.

### 10.4. Opened child

**Opened child** — the currently active child of a switchable node.

### 10.5. Opened branch

**Opened branch** — a subtree all of whose ancestors up to the root are in an open state.

### 10.6. State ownership

**State ownership** — the rule by which state belongs to the node
that manages the corresponding entity.

---

## 11. Structural Patterns

### 11.1. Switchable node

**Switchable node** — a node that owns an active/opened child selection, with only one candidate child active at any given moment. The candidate set may be fixed or dynamic if the child policy, source of truth, and lifecycle are explicit.

### 11.2. Dynamic switchable node

**Dynamic switchable node** — a switchable node whose candidate child set is created, removed, or replaced at runtime, while the holder still owns exactly one selected/opened child from that candidate set.

### 11.3. Mutable node

**Mutable node** — a node-container into which the runtime can add and remove
different child nodes.

### 11.4. Single-child mutable node

**Single-child mutable node** — a mutable node that at runtime always has at most one
active child in a given slot, but the concrete child instance can be replaced entirely.

### 11.5. Composite node

**Composite node** — a node containing multiple semantic subparts.

### 11.5. Library node

**Library node** — a reusable template-like or canonical subtree node.

### 11.6. Deferred runtime creation

**Deferred runtime creation** — a scenario in which a child or subtree
is created later upon a runtime trigger.

---

## 12. Ownership and Materialization Terms

### 12.1. Structural parent

**Structural parent** — a parent node according to the strict tree structure.

### 12.2. Logical parent

**Logical parent** — a parent node according to the semantic model.

### 12.3. Materialization parent

**Materialization parent** — the node relative to which the actual
materialization of a subtree occurs in the runtime flow, if the project introduces such a distinction.

### 12.4. Render attachment target

**Render attachment target** — the container or host to which the visual content of a node
or subtree is attached during materialization.

### 12.5. Render host

**Render host** — a node or container that provides the location for render attachment.

### 12.6. Source of truth

**Source of truth** — the authoritative layer of the model or data.

### 12.7. Runtime mutation policy

**Runtime mutation policy** — the set of rules that govern how the runtime tree changes.

---

## 13. Modularity

### 13.1. Module branch

**Module branch** — a self-contained branch of the system with its own interface.

### 13.2. Connector

**Connector** — an adapter that connects a module branch to an external system.

---

## 14. Prompt-based Generation

### 14.1. Prompt-based code generation

**Prompt-based code generation** — the generation or regeneration of code artifacts
based on a node spec and a node implementation prompt file.

### 14.2. Verification loop

**Verification loop** — the cycle:
1. prompt execution
2. code generation
3. comparison with reference behavior/code
4. prompt refinement
5. repeat until stabilization or until the attempt limit is reached

### 14.3. Escalation

**Escalation** — halting the automatic verification loop and passing the question to a human.

---

## 15. Layering Terms

### 15.1. TOP Core

**TOP Core** — the canonical layer of concepts of the paradigm itself.

### 15.2. Skill Conventions

**Skill Conventions** — organizational and workflow rules of a specific skill.
---

## 16. Semantic Generation Terms

### 16.1. Layer A — TOP Structural Truth

**Layer A — TOP Structural Truth** — the canonical structural source of truth: nodes, controllers, content, states, relationships, lifecycle, and invariants.

### 16.2. Layer B — Platform-Neutral Semantic UI Layer

**Layer B — Platform-Neutral Semantic UI Layer** — the portable meaning layer that describes element purpose, user intent, system intent, interaction intent, feedback intent, layout intent, constraints, state model, and accessibility semantics without platform primitives.

Persisted Layer B artifacts are stored under `top/semantic/**/*.semantic.json`.

### 16.3. Layer C — Target Adaptation Layer

**Layer C — Target Adaptation Layer** — a derived, temporary, target-specific mapping from Layer B to native target interactions, layout choices, UI primitives, constraints, and adaptation decisions.

Persisted Layer C artifacts are stored under `top/adaptations/<target>/**/*.adaptation.json` when handoff or review requires it. They are not source truth.

### 16.4. Semantic role

**Semantic role** — the platform-independent purpose of a UI/content element, such as action trigger, content container, target indication, or contextual action access.

### 16.5. Interaction intent

**Interaction intent** — what the user is trying to do and what the system must interpret, independent of the concrete platform event or gesture.

### 16.6. Feedback intent

**Feedback intent** — the meaning of system feedback to the user, independent of whether the target renders it with hover, focus, pressed state, animation, sound, or another native mechanism.

### 16.7. Layout intent

**Layout intent** — semantic placement and grouping requirements, independent of CSS, widget trees, layout classes, or platform layout primitives.

### 16.8. Source-artifact constraint

**Source-artifact constraint** — a constraint extracted from an existing source platform that belongs only to that platform and must be removed from Layer B or quarantined as evidence.

### 16.9. Target adaptation decision

**Target adaptation decision** — an explicit Layer C record that a semantic element was preserved, adapted, or dropped for a specific target, with reasons for adapted and dropped decisions.
