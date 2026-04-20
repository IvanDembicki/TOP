---
sourcePath: src/pane/tree_item/drag_handle.top
---

# DragHandle

## 1. Node Identity and Role

DragHandle is a visual affordance that signals to the user that a tree item row can be dragged. It exists only inside TreeItemRowEditStateNormalState and TreeItemRowEditStateHoverState — it is architecturally absent from view mode. It is only created for non-root items.

## 2. Responsibility

- Render the drag affordance visual.
- Provide a grab-cursor signal to the user.
- Carry no interaction logic; drag events are handled by the parent row state node.

## 3. Inputs and Events

None. DragHandle has no event handlers.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: creates the visual content boundary with `setContent(...)`.
2. Created only when `treeItem.isRoot` is false — the parent row node conditionally instantiates it during `buildChildren`.
3. No dynamic changes after child materialization.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must not check `isEditMode` — this node is architecturally present only in edit-state row nodes, so the check is redundant and forbidden.
- Must not initiate drag; drag is handled entirely by the containing row state node.

## 9. Non-Goals

- Does not initiate or handle drag operations.
- Does not manage visibility dynamically — visibility is guaranteed by architectural placement (only created for non-root items in edit-state rows).

## 10. Platform Implementation Notes

- Visual element: `span` with CSS class `drag-handle`, text content `⠿`.
- View is placed by the parent node during `buildChildren()`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/drag_handle.top`
- Public node class: `DragHandleNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: DragHandleContentAccess
  - Content-to-controller: DragHandleControllerAccess with zero-contract implementation DragHandleControllerAccessZero
- Companion artifact stems: none