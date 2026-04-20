---
sourcePath: src/pane/tree_item/tree_item_row_edit_state_normal_state.top
---

# TreeItemRowEditStateNormalState

## 1. Node Identity and Role

TreeItemRowEditStateNormalState is the first (default) child of TreeItemRowEditState. It provides the row visual for edit mode when the mouse is not hovering over the item. It contains DragHandle (for non-root items), NodeIcon, and NodeLabel. It does not show AddBtn or DeleteBtn — those appear only in hover state.

## 2. Responsibility

- Create and own the normal (non-hover) edit-mode row view.
- Own low-level drag and mouse-enter subscriptions inside the content boundary; forward semantic events through the controller access contract.
- On hover enter, request the parent TreeItemRowEditState to switch to hover mode.
- Expose `setPaddingLeft`, `updateToggle(hasChildren, isExpanded)`, and `setText(text)` for delegation from the parent.

## 3. Inputs and Events

- Hover enter on own view → calls `this.parent.switchToHover()` (switches to HoverState).
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
- Children's views are placed into this node's content area during child materialization.

## 6. Lifecycle

1. Constructor: creates the row visual content with `setContent(...)`.
2. `buildChildren()`: captures `_treeItem` via `findUpByType(TreeItemNode)`; enables drag capability only for non-root items; creates children (DragHandle if non-root, NodeIcon, NodeLabel).
3. Content owns hover-enter and drag subscriptions for the content lifetime; mounting is handled by the parent's base switchable mechanism.
4. `onClose()` does not perform low-level unsubscription unless the target implementation requires explicit disposal when content is destroyed.

## 7. Side Effects

- Hover enter causes a parent state switch to HoverState.
- Drag events forwarded to TreeItem may cause item reordering.

## 8. Constraints and Invariants

- Drag and hover-enter are low-level content subscriptions. They forward semantic events through the controller access contract and do not make architectural decisions.
- Initial default placement by the parent may not call `onOpen()`, so the generated implementation must ensure the initially active normal row can receive hover and drag events.
- Must not contain AddBtn or DeleteBtn — these belong to HoverState only.
- Must not read `isEditMode`.

## 9. Non-Goals

- Does not implement drag logic; only forwards drag events to TreeItem.
- Does not show edit action controls (those are in HoverState).

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item-row`.
- Draggable: `this.content.setDraggable(!treeItem.isRoot)` called in `buildChildren()`.
- Mouse enter: content-local subscription forwards a hover request through the controller access contract.
- Drag forwarding: content-local subscriptions forward drag events through the controller access contract.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state_normal_state.top`
- Public node class: `TreeItemRowEditStateNormalStateNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemRowEditStateNormalStateContentAccess
  - Content-to-controller: TreeItemRowEditStateNormalStateControllerAccess
- Companion artifact stems: none
