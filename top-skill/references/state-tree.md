# State Tree

---

## Definition of state tree

A state tree is a tree that contains at least one state node.

A state tree is **not a separate kind of tree** and not a content type.
It is a characteristic of a tree.

Any tree can be a state tree:
- `*ui-tree*` can be a state tree;
- `*data-tree*` can be a state tree;
- other specialized trees can also have this property.

---

## State holder

A state holder is a switchable node acting as the managing container of states.

A state holder:
- contains child state nodes;
- manages switching between them;
- keeps only one of them open at any given moment.

Examples:
- `SendButton` — a state holder with state nodes `Normal`, `Hover`, `Down`, `Disabled`;
- `UploadPage` — a state holder with state nodes `InputForm`, `Loading`, `Loaded`, `Error`.

A state holder is a **switchable node**.
Not every switchable node is a state holder — switchability applies more broadly.

---

## State node

A state node is a tree node representing one of the possible states of an element,
component, or larger part of the system.

The contents of a state node depend on the tree type:
- in `*ui-tree*` — a view;
- in `*data-tree*` — data;
- in other trees — the corresponding content.

State nodes in the description and in the implementation represent the same structural entity.

---

## Current system state

The current system state is determined by the current tree configuration:
- which nodes are open (`opened nodes`);
- which branch is the `opened branch`;
- what the current tree structure is (when mutable nodes are present).

The tree defines the **space of possible states** of the system.
The specific tree configuration at any given moment defines the **current state** of the system.

---

## Opened node / Closed node

**Opened node** — a node that is in the opened state in the current configuration.
**Closed node** — a node that is in the closed state.

Rules:
- In a non-switchable node, all child nodes are opened simultaneously.
- In a switchable node, only one child node is opened — the one pointed to by
  the parent's `openedChild`.
- All other child nodes of the switchable node are considered closed.
- The root node of the state tree is considered opened by definition.

---

## State switching

In a switchable node, the current state is stored in the `openedChild` reference,
which points to the current opened child node.

Switching is performed by calling `open()` on a child node.
This call **does not perform switching directly** — it delegates switching to the parent.

Canonical switching sequence:
1. Parent calls `onClose()` on the previous `openedChild`.
2. Parent reassigns `openedChild` to the new child node.
3. Parent calls `onOpen()` on the new `openedChild`.

Branch extension hooks (`onBranchClose` / `onBranchOpen`) are not part of the canonical sequence. They are optional and are called only if a specific subclass explicitly declares a branch propagation policy.

To open the entire branch up to the root, `openBranch()` is used —
it sequentially opens the node and all its ancestors.

---

## Opened branch

The opened branch is the subtree of all nodes whose every ancestor up to the root is opened.

It **is not a single path** — it is a subtree.

If any ancestor node is closed, that node does not belong to the opened branch.

Important: a node can be opened **locally** but not belong to the opened branch
if at least one of its ancestors is closed.

---

## What is NOT a state tree

- A tree with no state nodes is not a state tree, even if it is a *ui-tree*.
- Content type (`*ui-tree*`, `*data-tree*`) is not a synonym for state tree.
- Representation level (`spec tree`, `instance tree`) is not a synonym for state tree.

Do not call any tree a `state tree` without verifying that it contains at least one state node.

---

## See also

Detailed branch mechanics — opened/closed node, openedChild, switching sequence, openBranch(), branch hooks:
`references/branch-state-model.md`
