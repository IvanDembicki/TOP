---
sourcePath: src/pane/tree_item/expand_collapse_holder.top
---

# ExpandCollapseHolder

## 1. Node Identity and Role

ExpandCollapseHolder is the exclusive owner of the expanded/collapsed state of a tree item. It is a switchable node with two children: ExpandedState (first, default active) and CollapsedState (last). The active child determines the current expansion state.

## 2. Responsibility

- Hold the current expand/collapse state as the identity of the active child (`openedChild`).
- Expose `toggle()` to switch between expanded and collapsed states. The base switcher mounts/unmounts the active child's view; ExpandedState supplies the ChildrenList view via `getView()` and manages ChildrenList activate/deactivate lifecycle.
- Fire lifecycle hooks on child nodes when the active child changes.

## 3. Inputs and Events

- `toggle()` — called by `TreeItem._toggle()`. If the active child is
  `_expandedState`, calls `_collapsedState.open()`; otherwise calls
  `_expandedState.open()`. The child `open()` path delegates to the base
  switching commit path, which unmounts the outgoing child view and mounts the
  incoming child view.

## 4. State Ownership

- Is the exclusive owner of the expand/collapse state.
- State is represented solely by which child is `openedChild`.
- No boolean flags. No external variables store this state.

## 5. Child Interaction Rules

- Two children: ExpandedState (`_expandedState`, default) and CollapsedState (`_collapsedState`).
- `_expandedState` is active by default. During initial child materialization, assign it as the active child and place its view without firing child lifecycle hooks.
- Switching uses `target.open()` from `toggle()`, allowing the target state node
  to run its own opening protocol before it delegates as `parent.openChild(this)`.
  The `parent.openChild(this)` commit then fires `onClose()` on the outgoing child and
  `onOpen()` on the incoming child.
- The active child's opaque view handle is pulled from the direct child via `getView()` and mounted/unmounted by the base switcher through ExpandCollapseHolder content. ExpandedState may internally pull ChildrenList's handle because ExpandedState is ChildrenList's direct parent.
- Does not call child methods directly except declared state requests such as
  `open()` and lifecycle/materialization hooks owned by the switchable path.

## 6. Lifecycle

1. Constructor: creates the holder content boundary with `setContent(...)`.
2. `buildChildren()`: creates ExpandedState and CollapsedState as children; assigns ExpandedState as the initial active child and places the ChildrenList view into content without calling `openChild()`.
3. Each call to `toggle()` switches the active child and fires lifecycle hooks.

## 7. Side Effects

Switching changes the mounted child view through the base switcher. ChildrenList activate/deactivate is handled by ExpandedState. Row icon updates are handled by the state that becomes active, after `openedChild` has changed.

## 8. Constraints and Invariants

- Must not interact with ChildrenList content directly.
- Must not store expand/collapse state as a boolean.
- Every switch fires `onClose()` on the outgoing child and `onOpen()` on the incoming child.
- Initial default-child assignment is not a switch and must not fire `onOpen()` / `onClose()`.

## 9. Non-Goals

- Does not render anything beyond its own container content.
- Does not react to mode changes.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `expand-collapse-holder`.
- `toggle()`: `if (this.isExpanded) { this._collapsedState.open(); } else { this._expandedState.open(); }` where `isExpanded` is a getter returning `this.openedChild === this._expandedState`.
- `childrenList` accessor delegates to `this._expandedState.childrenList`.
- Initial mount of ChildrenList: `buildChildren()` creates both states and assigns ExpandedState as the initial active child without calling `openChild()`.
- Extends `DomNode`.
- Located as the second direct child of TreeItem (after TreeItemRow).

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/expand_collapse_holder.top`
- Public node class: `ExpandCollapseHolderNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: ExpandCollapseHolderContentAccess
  - Content-to-controller: ExpandCollapseHolderControllerAccess empty zero-contract interface implemented by the owning node/controller
- Companion artifact stems: none
