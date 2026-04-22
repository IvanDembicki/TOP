---
sourcePath: src/pane/tree_item/expanded_state.top
---

# ExpandedState

## 1. Node Identity and Role

ExpandedState is the first (default active) child of ExpandCollapseHolder. When active, it represents the expanded state of a tree item. It is a logical state node with no visual content of its own. It contains ChildrenList as its only child and exposes the ChildrenList view through `getView()`.

## 2. Responsibility

- Own the expanded-state branch below ExpandCollapseHolder.
- Create ChildrenList as its static child.
- Expose `getView()` so the parent switcher can mount the ChildrenList view into ExpandCollapseHolder content.
- Re-activate ChildrenList in `getView()` if its visual content was previously destroyed by collapse.
- On `onOpen()`: notify the ancestor TreeItem so its toggle icon can refresh.
- On `onClose()`: deactivate ChildrenList, preserving logical child TreeItem nodes. The collapsed icon update is performed by CollapsedState after it becomes active.

## 3. Inputs and Events

- `getView()` — called by the parent switcher when ExpandedState is mounted or unmounted.
- `onOpen()` — fired when this state becomes the active child of ExpandCollapseHolder.
- `onClose()` — fired when this state is deactivated.
- `initChildren(data[])` — delegates initialization to ChildrenList.
- `addChildItem(data)` — delegates child creation to ChildrenList.

## 4. State Ownership

Owns no independent state. It is itself the expanded state representation. The current expanded/collapsed state is owned by ExpandCollapseHolder through `openedChild`.

## 5. Child Interaction Rules

- One static child: ChildrenList, stored as `_childrenList`.
- `getView()` checks whether ChildrenList is active. If not, it calls `_childrenList.activate()` before returning `_childrenList.getView()`.
- `onClose()` calls `_childrenList.deactivate()` after the switcher has already captured the outgoing view for unmounting.
- Logical child TreeItem nodes owned by ChildrenList must survive deactivate/activate cycles.

## 6. Lifecycle

1. `buildChildren()`: creates ChildrenList as its only child.
2. When placed by the parent switcher: `getView()` returns the live ChildrenList view, activating it if needed.
3. On `onOpen()`: calls `notifyToggle()` on ancestor TreeItem.
4. On `onClose()`: deactivates ChildrenList content without updating the row icon from the stale outgoing state.

## 7. Side Effects

- `getView()` may re-create ChildrenList content when the expanded branch is opened again.
- `onClose()` destroys ChildrenList content while keeping logical child nodes.
- `onOpen()` calls `notifyToggle()` on ancestor TreeItem, updating the row icon state after the expanded state is active.

## 8. Constraints and Invariants

- Must locate TreeItem via upward type-based lookup, not a hardcoded chain.
- Must not store expand/collapse state as a boolean.
- Must not use visibility toggling as the semantic model; content lifecycle uses destroy/activate semantics.
- `getView()` is allowed to activate ChildrenList. The switcher must not call `getView()` for the outgoing child after `onClose()` without first capturing the old view.
- Logical children of ChildrenList must survive across deactivate/activate cycles.

## 9. Non-Goals

- Does not render visual content of its own.
- Does not mount ChildrenList manually; mounting/unmounting is performed by the parent switcher through the active child's view.
- Does not manage the visual row; that is TreeItemRow's responsibility.

## 10. Platform Implementation Notes

- Extends `SwitchableNode`.
- `buildChildren()`: creates `this._childrenList = new ChildrenListNode(this)`.
- `getView()`: activates ChildrenList if inactive, then returns `this._childrenList?.getView() ?? null`.
- TreeItem lookup: `this._treeItem = this.findUpByType(TreeItemNode)` captured in constructor.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/expanded_state.top`
- Public node class: `ExpandedStateNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: none (logical node with no content boundary)
  - Content-to-controller: none (logical node with no content boundary)
- Companion artifact stems: none
