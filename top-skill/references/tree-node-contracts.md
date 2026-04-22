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
- `openChild(child)`

### Invariants
- if the child collection is empty, `openedChild == null`;
- if the child collection is non-empty, the first child is open by default;
- direct external modification of `openedChild` must not create a separate public semantics;
- `openChild(child)` is the canonical switching path.

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
- `open()` does not change state directly and delegates to the canonical switching path of the owner;
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

Update the display-only parts of a node from the current state of the data model, without changing structure or switching state.

### When invoked

- A parent/holder calls `refresh()` on a node when the data displayed by that node has changed.
- A node may call `refresh()` on itself after processing an event.
- Calling `refresh()` is permitted at any point in the node's lifetime, not only after structural events.

### Propagation

- A holder calling `refresh()` explicitly decides which children to propagate the call to.
- There is no automatic propagation — each holder explicitly controls propagation.
- If propagation is used, it must be described explicitly.

### Allowed operations

- Read from the data model (source of truth) and update display-only output: text, label, count, icon, numeric state.
- Call `refresh()` on children.

### Forbidden operations

- Create or delete child nodes.
- Register or remove listeners.
- Switch `openedChild`.
- Read architectural state (isEditMode, openedChild, lifecycle phase) in order to conditionally change the visibility or behavior of UI elements.
- Manage content lifecycle (activate, deactivate, mount, unmount).

### Idempotency

Must be safe to call repeatedly: a repeated `refresh()` updates the display to the current state of the data without accumulating side effects.

### Default

Empty body (`refresh() {}`). Override only if the node has data-dependent display.

### Distinguished from

- `onOpen()` / `onClose()` — structural lifecycle (node becomes active/inactive); refresh() operates within an already-active context
- content materialization / child materialization — one-time initialization at node creation
- `switchToX()` / `openChild()` — changing structural/state configuration

### Anti-pattern: hidden switchable in refresh()

If `refresh()` reads architectural state (isEditMode, openedChild, etc.) and on that basis shows/hides elements or changes available behavior — this is a `core_violation: hidden switchable`.

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
