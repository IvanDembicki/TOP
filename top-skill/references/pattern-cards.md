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
- the child slot is replaced by a single runtime instance rather than selected from a candidate set — use `single-child mutable node`.

### Invariants
- there is a switchable holder;
- there is a candidate child set, fixed or dynamic;
- only one candidate child is active/opened at a time;
- switching follows a lifecycle-consistent path;
- for dynamic switchable, the candidate-set source of truth, child type policy, creation/removal lifecycle, ordering if relevant, and fallback behavior when the opened child disappears are explicitly described.

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
- behavior is explicit when the currently opened child is removed: fallback selection, null/empty state, or another declared policy.

### Common confusion
- treating any mutable collection with a selected row as dynamic switchable when the collection itself does not own opened-child lifecycle;
- treating single-child replacement as dynamic switchable even though no candidate set is retained.
## 2. Single-Child Mutable Node

### Definition
A node that allows only one child at a given child position at a time,
but that child can be replaced, recreated, or loaded at runtime.

### When to use
- one active child instance is needed;
- the child is created dynamically;
- the child can be replaced by another instance of the same semantic slot;
- child composition is mutable, not fixed-state based.

### When not to use
- there is a fixed set of states;
- this is a regular immutable single child;
- this is a list-like mutable container.

### Invariants
- no more than one child occupies the slot at a time;
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
A node receives part of its configuration, path, environment, or placement rules
from an ancestor node through inheritance.

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
