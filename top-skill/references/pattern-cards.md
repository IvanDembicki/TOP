# Pattern Cards

Short practical cards for recurring TOP patterns.
Cards are intended for:
- analyzing existing projects;
- designing new trees;
- reducing terminological confusion;
- quick invariant verification.

For common interpretation mistakes and symmetric anti-patterns, see `anti-patterns.md`.

---

## 1. Switchable Node

### Definition
A node that owns an active/opened child selection, with only one candidate child active at any given moment.

A switchable node may be fixed or dynamic:
- **fixed switchable** — the candidate children are a fixed architectural set of alternative states;
- **dynamic switchable** — the candidate children are created, removed, or replaced at runtime, but the holder still owns a single selected/opened child chosen from that candidate set.

### When to use
- the node has mutually exclusive candidate children;
- exactly one candidate is selected/opened at a time;
- a lifecycle-consistent transition is required when the active/opened child changes;
- UI and behavior depend on the active/opened child;
- for dynamic switchable, the candidate set has an explicit source of truth and creation/removal policy.

### When not to use
- there is no active/opened selection semantics;
- a list of children is shown or processed without selecting one active/opened child;
- the node simply stores a flag without a separate state/candidate structure;
- the child position is replaced by a single runtime instance rather than selected from a candidate set — use `single-child mutable node`.

### Invariants
- there is a switchable holder;
- there is a candidate child set, fixed or dynamic;
- only one candidate child is active/opened at a time;
- a valid switchable holder always has one opened child; missing/null
  `openedChild` is invalid, not a no-result behavior;
- switching follows a lifecycle-consistent path;
- for dynamic switchable, the candidate-set source of truth, child type policy, creation/removal lifecycle, ordering if relevant, and replacement/empty-state behavior when the opened child disappears are explicitly described.

### Common confusion
- confusion with `single-child mutable node`;
- confusion with `mutable collection node`;
- confusion between a visual tab/dropdown/list control and the actual state owner.

---


## 1a. Dynamic Switchable Node

### Definition
A switchable node whose candidate child set is dynamic, while the holder still owns exactly one active/opened child selected from that set.

Example: a printer selector whose available printer children are discovered at runtime, while `openedChild` points to the currently selected printer option.

### When to use
- available candidates are data-driven or externally discovered;
- several candidate children may coexist;
- one candidate is selected/opened at a time;
- selection changes must follow the canonical switching path.

### Invariants
- candidate child type or base type is declared, for example through `childrenType` or an equivalent child policy;
- source of truth for the candidate set is explicit;
- source of truth for the selected/opened child is explicit;
- create/remove/reorder lifecycle is explicit;
- behavior is explicit when the currently opened child is removed: select
  another candidate, open an explicit empty/unavailable state candidate, or use
  another declared lifecycle transition. The holder must not remain with null
  `openedChild` during active behavior propagation.

### Common confusion
- treating any mutable collection with a selected row as dynamic switchable when the collection itself does not own opened-child lifecycle;
- treating single-child replacement as dynamic switchable even though no candidate set is retained.
- treating a runtime/library collection as a switchable holder without modeling
  its children as a switchable candidate set with one selected/opened child.
## 2. Single-Child Mutable Node

### Definition
A node that allows only one child at a given child position at a time,
but that child can be replaced, recreated, or loaded at runtime.

### When to use
- one active child instance is needed;
- the child is created dynamically;
- the child can be replaced by another instance of the same semantic child position;
- child composition is mutable, not fixed-state based.

### When not to use
- there is a fixed set of states;
- this is a regular immutable single child;
- this is a list-like mutable container.

### Invariants
- no more than one child occupies the child position at a time;
- child policy is explicitly described;
- child replacement has clear lifecycle semantics;
- the owner of child instances is unambiguously defined.

### Common confusion
- confusion with switchable node;
- confusion with a list container holding a single element.

---

## 3. Mutable Collection Node

### Definition
A node whose child set can change over time:
addition, removal, reorder, runtime creation, runtime cleanup.

### When to use
- children are managed by data or user actions;
- child count is not fixed;
- add/remove/reorder support is needed;
- the system resembles an editor, list builder, or dynamic subtree host.

### When not to use
- the child set is fixed;
- only single-child replacement is needed;
- there is a selected/opened child semantics over the dynamic set — use dynamic switchable instead.

### Invariants
- child owner is defined;
- create/remove/cleanup policy is defined;
- child ordering is controlled;
- the relationship to the source of truth is defined;
- re-init semantics are not hidden.

### Common confusion
- `childrenType` is not described;
- the runtime tree changes while the authoritative model does not.

---

## 4. Library Node (lib:true)

### Definition
A child node whose instances are created via a library — at runtime or deferred.

### When to use
- children are created dynamically during application runtime;
- the child is effectively static but is created after parent initialization.

### When not to use
- the child always exists alongside the parent — use a static child instead;
- the library marker is used without a declared base type.

### Invariants
- the base type of the lib entry is declared in the spec;
- there is only one lib entry per parent;
- the parent has a children array typed by the base type;
- all runtime instances inherit from the base type.

### Common confusion
- mixing static and lib:true children under the same parent;
- using lib:true without declaring a base type.

---

## 5. Deferred Runtime Creation

### Definition
A child or subtree is not materialized immediately but is created later on a runtime trigger.

### When to use
- the child is not always needed;
- creation is expensive or conditional;
- the subtree appears on a user action, state transition, or data availability.

### When not to use
- the subtree must always exist;
- deferred creation is used only to conceal an unclear model.

### Invariants
- logical ownership is defined in advance;
- the creation trigger is defined;
- repeated creation policy is defined;
- cleanup/removal semantics are defined.

### Common confusion
- deferred children are treated as "not children at all";
- render attachment is confused with ownership.

---

## 6. Inherited Context

### Definition
A node accesses inherited context such as path, environment, placement policy, or
shared configuration through an explicit ancestor/context contract.

The node is attached to context and pulls what it needs through the allowed
contract. It must not receive inherited configuration as constructor data,
props, config/options objects, callbacks, services, stores, or post-construction
setter packets.

### When to use
- descendants must share a common context;
- a shared path/layout/environment is needed;
- child nodes should not repeat the same configuration locally.

### When not to use
- inheritance hides important local differences;
- the context is too implicit and makes analysis non-obvious.

### Invariants
- the source of the inherited context is clear;
- override rules are understood;
- descendants do not interpret inheritance in contradictory ways.
- inherited context travels through explicit contracts, not injection packets.

### Common confusion
- inheritance is perceived as a local property of the child;
- cascading behavior of `props.dir` and similar rules is not accounted for.

---

## 7. Connector

### Definition
A node or relationship that connects parts of the model without breaking the tree nature of the system.

### When to use
- coordination between branches needs to be expressed;
- an explicit semantic connection is needed;
- the relationship must not turn the tree into a graph.

### When not to use
- the relationship is implemented as arbitrary deep navigation chains;
- the connector is used as justification for a hidden graph-like design.

### Invariants
- tree ownership is preserved;
- the connector does not replace the parent-child relation;
- navigation remains explainable.

### Common confusion
- connectors are confused with arbitrary cross-linking logic.

---

## 8. Independent Branch

### Definition
A separate subtree/branch with its own local responsibility and internal logic,
while remaining part of the overall TOP tree.

### When to use
- a modular fragment of the system is needed;
- the branch has its own lifecycle or content domain;
- the branch can be analyzed as a semi-independent unit.

### When not to use
- the branch is separated only by file structure without a semantic basis;
- the branch has no clear boundaries of responsibility.

### Invariants
- the branch role is clear;
- branch boundaries are clear;
- the branch does not conceal an accidental mix of different responsibilities.

### Common confusion
- the branch is treated as a separate system with no connection to the overall tree.

---

## 9. Logical Child with External Render Attachment

### Definition
A node is the logical child of one parent, but materializes its content
in the render host of another node or ancestor.

### When to use
- the logical tree and visual placement must differ;
- a state node or helper node has no own host;
- child content must attach to a shared/ancestor container.

### When not to use
- the attachment rule cannot be explained;
- the render shortcut breaks understanding of ownership;
- visual structure accidentally substitutes the tree model.

### Invariants
- logical ownership is explicit;
- the render attachment target is explicit;
- the child lifecycle is controlled by the correct owner;
- visual placement does not override tree relations.

### Common confusion
- it is assumed that if the DOM parent is different, the TOP parent is also different.

---

## 10. How to use Pattern Cards

When analyzing a project:
1. find candidate nodes;
2. match them against the cards;
3. verify invariants;
4. record common confusion;
5. do not confuse the pattern with an implementation detail.

When designing:
1. choose a pattern by semantic role;
2. record invariants in the spec;
3. record runtime semantics in prompts/references;
4. separately describe the source of truth and ownership if the pattern is mutable.

---

## 11. Runtime Branch Binding Pattern

### Definition

A runtime-created branch is attached to an entity context. It is not filled with
scattered data packets.

Static nodes are parent/context-only. Runtime-created branch roots may receive
parent/context plus one canonical binding input under this pattern.

### Preferred binding

Entity Context Binding: the runtime branch root receives a narrow entity context
reference such as a data-node controller, entity access interface, or model
controller.

### Allowed bindings

Identity Key Binding: the branch root receives a stable identity key only when
the branch itself resolves or loads its entity context.

Typed DTO Binding: the branch root receives a typed immutable DTO only when no
entity context exists yet. The DTO must be converted into owned data
content/model as early as possible.

### Forbidden

- scattered constructor data;
- props/config/callback bags;
- mutable raw model objects;
- presentation values;
- direct services/stores as arbitrary arguments.

### Examples

Allowed:
- `new RuntimeItemNode(parent, entityAccess)`
- `new RuntimeItemNode(parent, stableEntityId)`
- `new RuntimeItemNode(parent, typedImmutableDto)`

Forbidden:
- `new RuntimeItemNode(parent, id, name, status, callbacks, config)`
- `new ChildNode(parent, props)`
- `child.setData(...)`
- `child.applyConfig(...)`

### Invariants

- the branch has one binding source;
- the binding deterministically identifies or creates entity context;
- semantic data is pulled through contracts after attachment;
- binding does not become a general constructor injection channel.

### Common confusion

- passing many fields because the runtime item is dynamic;
- treating a list item DTO as the permanent owner of state;
- using framework props/config as the TOP branch API.

---

## 12. Library Object External Context Boundary

### Definition

Recommended pattern: a runtime/library object root is the external context
boundary of its runtime branch.

The root is the preferred attachment point for branch-external dependencies:
parent context, data tree access, presentation/style tree access, asset tree
access, permission context, runtime services, external connectors, and other
external trees or contextual structures.

This pattern is not limited to data models. The root represents the outside
world to the internal runtime/library subtree.

### When to use

- a runtime/library branch is instantiated from a reusable type;
- descendants inside the branch need branch-owned entity/context values;
- descendants need environment values, permissions, style/presentation context,
  assets, services, or connector capabilities;
- the branch should remain reusable across different parent environments.

### Preferred flow

- branch root attaches to parent/context and approved external context contracts;
- branch root obtains external information from its parent, explicit context
  contracts, or approved connectors;
- descendants request needed values or capabilities through the branch root or
  through narrow contracts derived from the root;
- the root exposes only the minimal resolved access needed internally.

### Smell

A descendant inside a runtime/library branch directly reaches an ancestor,
global store, data tree, presentation/style tree, asset tree, service,
permission source, or connector.

Review:
- is this external dependency part of the explicit branch-root contract?
- should the root obtain the access and re-expose a narrower resolved
  contract/value/capability to the descendant?
- is external context leaking into the library branch through accidental direct
  dependencies?

### Status

This is a strong recommended modeling pattern / canonical heuristic, not a hard
invariant. Exceptions are allowed when explicitly described in the spec, prompt,
or branch contract.

### Common confusion

- reducing the pattern to "the root holds the data model";
- allowing every descendant to independently discover the external world;
- treating direct global store, service, asset, style, or connector access as
  normal because the branch is runtime-created.

---

## 13. Tell-Only Downward Propagation

### Definition

A downward query or event is invoked at a node boundary, and the receiving node
owns the local propagation decision.

The caller does not ask whether the node or its children can handle the event
before invoking it. The caller says "handle/query this" through the declared
contract; the node answers, returns no-result, no-ops, stops, delegates to an
active/selected child, or delegates through a connector.

### When to use

- result-producing queries such as target lookup, hit-test, focus target
  lookup, command availability, or capability output;
- downward events/commands that may or may not matter to a subtree;
- propagation through switchable state holders;
- propagation across connector/adapted external tree boundaries.

### Invariants

- propagation starts at an architecturally approved entrypoint;
- after entry, each node owns the next local step;
- no external walker inspects node modes, child policies, state-child names, or
  connector internals;
- no external `canHandle`/capability preflight is used to choose internal
  descendants;
- no-op/no-result is a valid response owned by the receiving node;
- no-op/no-result should be placed at the highest owning node boundary that can
  know the subtree has no relevant active behavior.

### Common confusion

- `if child.canHandle(event) child.handle(event)` looks efficient but moves the
  propagation decision outside the child node;
- a capability/status method becomes non-canonical when it is used by external
  traversal as a preflight gate;
- switchable holders are walked through all state siblings instead of delegating
  active behavior to the non-null `openedChild`.
