---
sourcePath: src/pane/tree_item/tree_item_row_edit_state_hover_state.top
---

# TreeItemRowEditStateHoverState

## 1. Node Identity and Role

TreeItemRowEditStateHoverState is the last child of TreeItemRowEditState. It provides the row visual for edit mode when the mouse is hovering over the item. It is the expanded version of the normal state: it shows DragHandle (non-root only), NodeIcon, NodeLabel, AddBtn, and DeleteBtn (non-root only).

## 2. Responsibility

- Create and own the hover edit-mode row view.
- Own low-level drag and mouse-leave subscriptions inside the content boundary; forward semantic events through the controller access contract.
- On hover leave, request the parent TreeItemRowEditState to switch to normal mode.
- Expose `setPaddingLeft`, `updateToggle(hasChildren, isExpanded)`, and `setText(text)` for delegation from the parent.

## 3. Inputs and Events

- Hover leave on own view → calls `this.parent.switchToNormal()` (switches back to NormalState).
- Drag events (start, end, over, leave, drop) on own view → forwarded to ancestor TreeItem.
- `setPaddingLeft(px)` — sets left indentation on own view.
- `setText(text)` — delegated to NodeLabel.
- `updateToggle(hasChildren, isExpanded)` — delegated to NodeIcon.

## 4. State Ownership

Owns no state. Does not read `isEditMode`.

## 5. Child Interaction Rules

- Children created conditionally during child materialization:
  - DragHandle: created only when `treeItem.isRoot` is false.
  - NodeIcon: always created.
  - NodeLabel: always created.
  - AddBtn: always created.
  - DeleteBtn: created only when `treeItem.isRoot` is false.
- Children's views are placed into this node's content area during child materialization.

## 6. Lifecycle

1. Constructor: creates the row visual content with `setContent(...)`.
2. `buildChildren()`: captures `_treeItem` via `findUpByType(TreeItemNode)`; enables drag capability only for non-root items; creates children (DragHandle if non-root, NodeIcon, NodeLabel, AddBtn, DeleteBtn if non-root).
3. Content owns hover-leave and drag subscriptions for the content lifetime; mounting is handled by the parent's base switchable mechanism.
4. `onClose()` does not perform low-level unsubscription unless the target implementation requires explicit disposal when content is destroyed.

## 7. Side Effects

- Hover leave causes a parent state switch back to NormalState.
- Drag events forwarded to TreeItem may cause item reordering.

## 8. Constraints and Invariants

- Drag and hover-leave are low-level content subscriptions. They forward semantic events through the controller access contract and do not make architectural decisions.
- Initial default placement rules mean a switchable child must not rely exclusively on `onOpen()` for local event subscriptions that are required immediately when its view is placed.
- Must not be opened or placed as the active sub-state during default child materialization.
- Must not read `isEditMode`.

## 9. Non-Goals

- Does not implement drag logic; only forwards drag events to TreeItem.
- Does not manage the overall view/edit mode switch.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item-row`.
- Draggable: `this.content.setDraggable(!treeItem.isRoot)` called in `buildChildren()`.
- Mouse leave: content-local subscription forwards a normal-state request through the controller access contract.
- Drag forwarding: content-local subscriptions forward drag events through the controller access contract.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state_hover_state.top`
- Public node class: `TreeItemRowEditStateHoverStateNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemRowEditStateHoverStateContentAccess
  - Content-to-controller: TreeItemRowEditStateHoverStateControllerAccess
- Companion artifact stems: none
