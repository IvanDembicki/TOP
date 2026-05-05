---
sourcePath: src/pane/tree_item/tree_item_row_edit_state_normal_state.top
---

# TreeItemRowEditStateNormalState

## 1. Node Identity and Role

TreeItemRowEditStateNormalState is the default edit-mode row state. It contains a
static row structure with DragHandle, NodeIcon, and NodeLabel.

## 2. Responsibility

- Materialize the normal edit-mode row structure.
- Report hover-enter intent to TreeItemRowEditState.
- Report drag/drop semantic requests upward through controller access.
- Expose resolved label, icon, indentation, and drag affordance tokens to local
  content and child controllers by pulling from parent/context.

## 3. Inputs and Events

- `requestHoverState()` - forwarded to parent TreeItemRowEditState.
- `requestDragStart(eventInfo)`, `requestDragEnd(eventInfo)`,
  `requestDragOver(eventInfo)`, `requestDragLeave(eventInfo)`,
  `requestDrop(eventInfo)` - forwarded to the owning TreeItem.
- `getLabelText()` / `getIndentToken()` / `getIconToken()` /
  `getDragToken()` - pull resolved values from the parent/context chain.

## 4. State Ownership

Owns no model state. This node is the normal edit-mode representation.

## 5. Child Interaction Rules

- Static children: DragHandle, NodeIcon, NodeLabel.
- Child constructors receive only this node as parent/context.
- DragHandle may pull a resolved affordance token. It is not conditionally
  created for root items.

## 6. Lifecycle

1. Constructor creates static row content.
2. `buildChildren()` creates DragHandle, NodeIcon, and NodeLabel and places their
   opaque handles.
3. Local content subscriptions report semantic requests through controller
   access.

## 7. Side Effects

- Hover and drag/drop requests may cause parent/controller state changes.

## 8. Constraints and Invariants

- Does not read `isEditMode`.
- Does not create children conditionally based on root/item state.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not implement drag/drop decisions.
- Does not manage hover state directly.

## 10. Platform Implementation Notes

- Visual primitive: static edit row container.
- Low-level hover/drag events are translated to semantic requests.
- Drag affordance and interaction tokens are already-resolved controller values.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state_normal_state.top`
- Public node class: `TreeItemRowEditStateNormalStateNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemRowEditStateNormalStateContentAccess`
  - Content-to-controller: `TreeItemRowEditStateNormalStateControllerAccess`
- Companion artifact stems: none
