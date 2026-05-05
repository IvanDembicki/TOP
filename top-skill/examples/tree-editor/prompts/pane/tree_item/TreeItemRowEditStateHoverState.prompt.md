---
sourcePath: src/pane/tree_item/tree_item_row_edit_state_hover_state.top
---

# TreeItemRowEditStateHoverState

## 1. Node Identity and Role

TreeItemRowEditStateHoverState is the hover edit-mode row state. It contains a
static row structure with DragHandle, NodeIcon, NodeLabel, AddBtn, and DeleteBtn.

## 2. Responsibility

- Materialize the hover edit-mode row structure.
- Report hover-leave intent to TreeItemRowEditState.
- Report drag/drop semantic requests upward through controller access.
- Expose resolved label, icon, indentation, drag, add, and delete tokens through
  pull methods.

## 3. Inputs and Events

- `requestNormalState()` - forwarded to parent TreeItemRowEditState.
- `requestAddChild()` - forwarded to owning TreeItem.
- `requestDeleteSelf()` - forwarded to owning TreeItem.
- drag/drop semantic requests - forwarded to owning TreeItem.
- resolved primitive getter methods delegate through the parent/context chain.

## 4. State Ownership

Owns no model state. This node is the hover edit-mode representation.

## 5. Child Interaction Rules

- Static children: DragHandle, NodeIcon, NodeLabel, AddBtn, DeleteBtn.
- Child constructors receive only this node as parent/context.
- DeleteBtn is always structurally present in this state. For root items it pulls
  an already-resolved disabled/hidden-action token from its controller access
  contract; content does not decide root visibility.

## 6. Lifecycle

1. Constructor creates static row content.
2. `buildChildren()` creates all static children and places their opaque handles.
3. Local content subscriptions report semantic requests through controller
   access.

## 7. Side Effects

- Hover, add, delete, and drag/drop requests may cause controller/data changes.

## 8. Constraints and Invariants

- Does not read `isEditMode`.
- Does not create children conditionally based on root/item state.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not implement add/delete decisions directly.
- Does not own item data.

## 10. Platform Implementation Notes

- Visual primitive: static hover edit row container.
- Add/delete availability is represented by already-resolved primitive tokens
  pulled by button content.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state_hover_state.top`
- Public node class: `TreeItemRowEditStateHoverStateNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemRowEditStateHoverStateContentAccess`
  - Content-to-controller: `TreeItemRowEditStateHoverStateControllerAccess`
- Companion artifact stems: none
