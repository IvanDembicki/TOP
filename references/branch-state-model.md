# Branch State Model

Basic definitions (state tree, state holder, state node) — see `references/state-tree.md`.
This file describes the detailed mechanics: opened/closed node, opened branch, switching, branch hooks.

---

## Opened node and Closed node

**Opened node** — a node in the opened state in the current state tree configuration.
**Closed node** — a node in the closed state.

### Openness rules

| Node type | Child node behavior |
|---|---|
| Non-switchable | All child nodes are opened simultaneously |
| Switchable | Only one child node is opened; the rest are closed |

The root node of the state tree is considered opened by definition.

---

## Opened branch

**Opened branch** — the subtree of all nodes whose every ancestor up to the root is opened.

This is not a path but a subtree: all nodes reachable through a chain of opened ancestors
from root to leaf belong to the opened branch.

Formally: node `N` belongs to the opened branch if and only if
all its ancestors (from parent to root) are opened.

---

## Local openness vs belonging to the opened branch

These two concepts are distinct:

- A node can be **locally opened** (a switchable parent has assigned it as its `openedChild`),
  but **not belong to the opened branch** if at least one of its ancestors is closed.

- A node belongs to the opened branch only when the entire chain up to the root is open.

Example:
```
Root (opened)
  └── TabPanel (switchable, openedChild = Tab2)
        ├── Tab1 (closed)
        └── Tab2 (opened)
              └── Section (switchable, openedChild = SectionA)
                    ├── SectionA (opened locally, in opened branch)
                    └── SectionB (closed)
```

If TabPanel switches to Tab1, Tab2 becomes closed.
SectionA remains locally opened but no longer belongs to the opened branch.

---

## openedChild

In a switchable node, the current opened child is stored in the `openedChild` reference.

`openedChild` points to the child node that defines the behavior and representation
of the parent in the current state.

---

## Switching — mechanics

Switching is initiated by calling `open()` on a child node.
This call **delegates switching to the parent node** — the child does not perform switching itself.

Sequence:
1. `child.open()` — the child requests switching from the parent.
2. Parent calls `onClose()` on the previous `openedChild`.
3. Parent reassigns `openedChild = newChild`.
4. Parent calls `onOpen()` on the new `openedChild`.

Branch-level hooks `onBranchOpen(node)` and `onBranchClose(node)` are not a mandatory
automatic part of the base canonical switching path. They exist as extension points,
but their invocation and propagation policy are defined only by a specific implementation.

---

## openBranch()

`openBranch()` — an operation that opens the entire branch containing the node.

It sequentially opens the node and all its ancestors up to the root.
Used when it is not enough to switch the local state alone —
the node must also be guaranteed to belong to the opened branch.

---

## onBranchOpen(node) and onBranchClose(node)

These methods are defined in the canon as branch-level extension hooks:

- **`onBranchOpen(node)`** semantically means that the branch rooted at `node`
  has entered the opened branch.

- **`onBranchClose(node)`** semantically means that the branch rooted at `node`
  has left the opened branch.

Here `node` is the branch-root of the branch being opened or closed. For descendants of this branch
it is self or an ancestor. The external node is not passed to branch children unless it is
their ancestor or self.

### Why automatic propagation policy is not canonized

Automatic propagation policy is not part of the base canon because branch propagation
depends on the specific subtree policy and is not universal across all technologies and nodes.
Some implementations require notifying the entire branch, others only part of the descendants,
others need to exclude always-open nodes or use a special traversal order.

If a single mandatory automatic propagation method were fixed in the canon,
the base contract would begin imposing unnecessary traversals, useless lifecycle calls,
and an inappropriate traversal policy for cases where branch hooks are either not needed
or should propagate only partially.

Therefore the canon fixes only:
- the existence of branch hooks;
- their semantic meaning;
- the requirement that the specific invocation/propagation policy must be explicitly defined
  in the subclass or implementation contract, if it is actually needed.

---

## Difference from the flag model

In TOP, state is not stored as a set of boolean flags on a node.
State is defined by the structural configuration of the tree:
- `openedChild` on each switchable node;
- membership in the opened branch.

This makes the state space explicit, bounded, and easy to analyze.
