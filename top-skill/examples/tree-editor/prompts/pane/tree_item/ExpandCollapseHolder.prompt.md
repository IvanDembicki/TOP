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

- `toggle()` — called by `TreeItem._toggle()`. If the active child is `_expandedState`, opens `_collapsedState`; otherwise opens `_expandedState`. The base switching path unmounts the outgoing child view and mounts the incoming child view.

## 4. State Ownership

- Is the exclusive owner of the expand/collapse state.
- State is represented solely by which child is `openedChild`.
- No boolean flags. No external variables store this state.

## 5. Child Interaction Rules

- Two children: ExpandedState (`_expandedState`, default) and CollapsedState (`_collapsedState`).
- `_expandedState` is active by default. During initial child materialization, assign it as the active child and place its view without firing child lifecycle hooks.
- Switching via `this.openChild(newChild)` called directly in `toggle()`, firing `onClose()` on the outgoing child and `onOpen()` on the incoming child.
- ChildrenList view is exposed by ExpandedState.getView() and mounted/unmounted by the base switcher through ExpandCollapseHolder content.
- Does not call methods on children directly other than through lifecycle hooks.

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
- `toggle()`: `if (this.isExpanded) { this.openChild(this._collapsedState); } else { this.openChild(this._expandedState); }` where `isExpanded` is a getter returning `this.openedChild === this._expandedState`.
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
  - Content-to-controller: ExpandCollapseHolderControllerAccess with zero-contract implementation ExpandCollapseHolderControllerAccessZero
- Companion artifact stems: none
