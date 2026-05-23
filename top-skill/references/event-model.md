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

## Event/request propagation directions

### Downward query/event propagation

A downward query or event enters the tree through an approved propagation
entrypoint. The entrypoint does not have to be the whole application root. It
may be a tree root, branch root, interaction-layer node, viewport/canvas node,
connector boundary, or another declared subroot when the caller already has an
architecturally valid scope.

After entry, propagation is node-owned. The external mechanism makes the typed
call and stops controlling internal traversal. Each node decides locally whether
to:
- answer;
- return no-result;
- stop propagation;
- delegate to `openedChild`;
- delegate to a selected child set;
- delegate through a connector or adapter;
- translate the request to an attached external tree through its boundary.

The external propagation mechanism must not inspect internal node modes,
state-child siblings, child policies, platform representation, or external-tree
internals to decide where the query goes next. It must not be a global walker
that "knows" which children are view-capable, which state is unavailable, which
adapter should be called, or which closed siblings should be skipped.

Nodes own those decisions through their declared contracts. For example, a
presentation-only node may return no-result for a data query, a switchable
holder delegates active-state behavior to its non-null `openedChild`, and a
connector node may forward through an explicit adapter that speaks to an
external tree.

This pattern applies to result-producing queries such as target lookup and
hit-test as well as to event/request routing. The return type, no-result value,
and traversal order are project-specific; the ownership rule is not.

### Bottom-up (bubbling)

A child node or locally implemented content reports a semantic event/request to
its owning controller or parent controller through the declared contract. The
controller handles the request or forwards it further up through allowed
controller contracts.

Example: a child node signals to the parent that data loading is complete.
The parent responds by switching state.

### Allowed parent-to-child calls

A parent or owner may invoke explicitly declared child controller lifecycle or
domain methods when that relationship is allowed by TOP access rules, for
example direct parent-to-child lifecycle hooks such as `onBranchOpen(node)` and
`onBranchClose(node)`.

This is not a data/config/presentation push channel. Events/requests may move
through the tree, but data packets, config, presentation state, callbacks,
props, stores, services, and imperative mutation commands must not be pushed
into child nodes or locally implemented content.

If a child needs data, it pulls it through its contextual contract. If a child
reports user/system intent, it sends a semantic event/request to its controller
or upward through allowed controller contracts.

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

- Do not access remote nodes directly to transfer data. Use semantic
  events/requests, typed controller/domain methods, or the module interface.
- A child must not know about the structure above its parent.
- A parent must not know about the internal structure of a child beyond the first level.
- Events between non-adjacent nodes are passed through the chain of parent nodes.
- Parent/owner code must not push arbitrary state, props, config, callbacks,
  presentation values, mutation packets, or data packets into child objects.
- A data node controller may expose typed domain methods such as `setAge(value)`
  or `replaceRecord(record)` when the relationship is architecturally allowed.
  The data controller validates and mutates its own private data content; callers
  do not mutate that content directly.
- Presentation content reports intent. Controllers make decisions. Data
  controllers mutate data. Presentation content later pulls resolved values.

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
