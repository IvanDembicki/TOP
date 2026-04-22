# Event Model

---

## The role of events in TOP

Events are the communication mechanism between nodes within the strict
parent-child rules of TOP.

Events do not violate tree discipline:
- a node does not directly call methods on arbitrary remote nodes;
- instead, a node generates an event, and its parent or another
  authorized node responds to it.

---

## Event propagation directions

### Bottom-up (bubbling)

A child node generates an event and passes it to the parent.
The parent handles or forwards the event further up.

Example: a child node signals to the parent that data loading is complete.
The parent responds by switching state.

### Top-down (propagation)

A parent or another owner node may pass a command or notification to child nodes.
Such top-down propagation is possible, including for `onBranchOpen(node)` and
`onBranchClose(node)`, but the specific propagation policy is not automatically
defined by the base canon.

---

## Branch events

When switching a state tree, special branch-level hooks may be used:

### onBranchClose(node)

Semantically means that the branch rooted at `node` has left the opened branch.
`node` is the branch-root of the closing branch. For descendants of this branch it is self or ancestor.

Allows a node to:
- release resources;
- save local state;
- stop active operations.

### onBranchOpen(node)

Semantically means that the branch rooted at `node` has entered the opened branch.
`node` is the branch-root of the opening branch. For descendants of this branch it is self or ancestor.

Allows a node to:
- initialize or restore state;
- start necessary processes;
- prepare content for display.

### Why automatic propagation policy is not canonized

The base canon does not mandate automatic traversal of descendants for these hooks.
The reason is that the actual propagation policy depends on the nature of the subtree: sometimes
the entire branch must be notified, sometimes only certain child nodes, and sometimes branch hooks
are not needed at all.

For this reason, the canon only establishes the extension points themselves and their meaning,
while the invocation method, propagation scope, and traversal order must be defined explicitly
in each concrete implementation.

---

## onClose() and onOpen() at the node level

When switching a specific switchable node:

- `onClose()` is called on the previous `openedChild` — notifying the node of its closing.
- Switching `openedChild` is performed by the parent after `onClose()`.

---

## Event handling rules

- Do not access remote nodes directly to transfer data.
  Use events or the module interface.
- A child must not know about the structure above its parent.
- A parent must not know about the internal structure of a child beyond the first level.
- Events between non-adjacent nodes are passed through the chain of parent nodes.

---

## Events and module branches

A module branch interacts with the external system through the module interface,
which may include:
- methods for calling into the module;
- events that the module generates outward.

The module branch connector subscribes to module events
and transforms them into calls to the main system.

Direct access to a module's internal nodes via events from outside is **forbidden**.
All events pass through the module interface.
