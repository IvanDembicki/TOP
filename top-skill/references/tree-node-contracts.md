# Tree Node Contracts

This document captures the canonical runtime contracts for `TreeNode`, `SwitchableTreeNode`, and `OpenableTreeNode`.

---

## 1. Base `TreeNode`

`TreeNode` defines only structural ownership, navigation, and the detach lifecycle.

It does not define visual API, selection API, rendering strategy, or branch propagation policy.

Where a visual API (`getView()`) exists on a node, only the direct parent is entitled
to call it. See `canon/architectural-invariants.md` — **View Access Invariant**.

### Properties
- `nodeType`
- `parent`
- `children`
- `root`
- `depth`
- `firstChild`
- `lastChild`
- `previousSibling`
- `nextSibling`

### Methods
- `addChild(child)`
- `insertChild(index, child)`
- `removeChild(child)`
- `removeChildAt(index)`
- `removeFromParent()`
- `clearChildren()`
- `getChildAt(index)`
- `indexOfChild(child)`
- `getIndex()`
- `setIndex(index)`
- `setChildIndex(child, index)`
- `findParentByType(type)`
- `findChildByType(type)`
- `findDescendantByType(type)`

### Detach lifecycle
- `onDetachedFrom(node)`

`onDetachedFrom(node)` is called when a branch loses its connection to the tree.
`node` is the nearest ancestor that remained in the tree after detachment.

### Invariants
- a node has at most one parent;
- a child belongs to exactly one parent;
- attach occurs only at creation;
- reattach is forbidden;
- a detached branch is destroyed irreversibly;
- root deletion is forbidden.

---

## 2. `SwitchableTreeNode`

`SwitchableTreeNode` — a parent-side role that owns `openedChild`.

### Property
- `openedChild`

### Methods
- `getOpenedChild()`
- `openChild(child)` as the owner-side commit primitive, called only by the
  child being opened as `parent.openChild(this)`

### Invariants
- a valid switchable node has at least one switchable state/candidate child;
- `openedChild` is never null for a valid switchable node;
- if no child is explicitly selected, the first state/candidate child is open
  by default;
- if the child collection is empty, the node is not a switchable node;
- runtime/library collection children do not make a node switchable unless they
  are explicitly modeled as the switchable candidate set with one selected/opened
  child;
- direct external modification of `openedChild` must not create a separate public semantics;
- the public switching request is `child.open()`;
- `openChild(child)` is the canonical owner commit path used by `child.open()`;
- the only valid direct call shape is the child opening itself through its
  parent: `parent.openChild(this)`;
- calls such as `holder.openChild(target)`, `this.openChild(target)`, or
  `parent.openChild(otherChild)` must not be used as public switching requests.

---

## 3. `OpenableTreeNode`

`OpenableTreeNode` — a child-side role. It may request opening itself through the parent-owned switching path and provides lifecycle hooks.

### Methods
- `open()`
- `isOpened()`
- `isBranchOpened()`

### Local lifecycle hooks
- `onOpen()`
- `onClose()`

### Branch extension hooks
- `onBranchOpen(node)`
- `onBranchClose(node)`

### Semantics
- `open()` may be overridden by the child to run child-owned opening protocol,
  but it does not change owner state directly;
- `open()` delegates the state commit to the canonical owner-side commit path
  by calling exactly `parent.openChild(this)`;
- `isOpened()` checks only local opened ownership relative to the parent;
- `isBranchOpened()` checks membership in the opened branch up to the root;
- `onBranchOpen(node)` and `onBranchClose(node)` exist as extension points; their invocation strategy and propagation policy are defined explicitly in a subclass/policy.

---

## 4. Relationship between roles

The same concrete node may simultaneously implement `OpenableTreeNode` and `SwitchableTreeNode`.
In that case these are two distinct roles:
- as a child relative to its own parent;
- as a state-holder relative to its own children.

---

## 5. `refresh()` — Data sync hook

`refresh()` — a universal data sync hook present on all nodes.

### Semantic role

Synchronize already-resolved primitive output values from the current state of
the data model, without changing structure or switching state.

### When invoked

- A parent/holder calls `refresh()` on a node when the data displayed by that node has changed.
- A node may call `refresh()` on itself after processing an event.
- Calling `refresh()` is permitted at any point in the node's lifetime, not only after structural events.

### Propagation

- A holder calling `refresh()` explicitly decides which children to propagate the call to.
- There is no automatic propagation — each holder explicitly controls propagation.
- If propagation is used, it must be described explicitly.

### Allowed operations

- Read from the data model (source of truth) in controller-owned logic and apply
  already-resolved primitive output values such as text, label, count, icon, or
  numeric state.
- Call `refresh()` on children.

### Forbidden operations

- Create or delete child nodes.
- Register or remove listeners.
- Switch `openedChild`.
- Read architectural state (isEditMode, mode, status, openedChild, lifecycle
  phase, owner-held mode flag, etc.) in order to conditionally change the
  visibility, representation, hit targets, context actions, capability surface,
  or behavior of UI elements.
- Manage content lifecycle (activate, deactivate, mount, unmount).

### Idempotency

Must be safe to call repeatedly: a repeated `refresh()` updates the display to the current state of the data without accumulating side effects.

### Default

Empty body (`refresh() {}`). Override only if the node has data-dependent display.

### Distinguished from

- `onOpen()` / `onClose()` — structural lifecycle (node becomes active/inactive); refresh() operates within an already-active context
- content materialization / child materialization — one-time initialization at node creation
- `switchToX()` / `child.open()` — changing structural/state configuration

### Anti-pattern: hidden switchable in refresh()

If `refresh()` reads architectural state (isEditMode, mode, status, openedChild,
owner-held mode flag, etc.) and on that basis shows/hides elements, changes hit
targets, changes context actions, changes capability availability, or changes
available behavior — this is a `core_violation: hidden switchable`.

Test: if everything except data-reads and display-updates is removed from `refresh()` and the logic remains complete — the implementation is correct. If `refresh()` loses meaning without reading architectural state — it is a violation.

---

## 6. What base canon does not regulate

Base canon does not regulate:
- traversal strategy for branch hooks;
- visual rendering strategy;
- cache/diff/rebuild policy;
- selection API;
- framework-specific handles.

Such policies must be defined explicitly in the corresponding subclass contracts.
