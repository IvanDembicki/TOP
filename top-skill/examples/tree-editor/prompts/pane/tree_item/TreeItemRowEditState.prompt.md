---
sourcePath: src/pane/tree_item/tree_item_row_edit_state.top
---

# TreeItemRowEditState

## 1. Node Identity and Role

TreeItemRowEditState is the edit-mode row representation holder. It switches
between normal and hover row states.

## 2. Responsibility

- Own the normal/hover active child selection.
- Receive semantic hover requests from child state controllers.
- Expose resolved row values to child states by delegating to TreeItemRow.

## 3. Inputs and Events

- `requestHoverState()` - opens HoverState.
- `requestNormalState()` - opens NormalState.
- `refresh()` - requests the active child to refresh from current resolved
  values.
- `getLabelText()` / `getIndentToken()` / `getIconToken()` / `getDragToken()` /
  `getDeleteActionToken()` - delegated pull methods.

## 4. State Ownership

Owns only the active normal/hover child state.

## 5. Child Interaction Rules

- Static children: NormalState and HoverState.
- Child constructors receive only TreeItemRowEditState as parent/context.
- No setter-style propagation into sub-state children.

## 6. Lifecycle

1. Constructor creates edit-state holder content.
2. `buildChildren()` creates both sub-state children and places NormalState by
   default.
3. Hover/normal changes happen through semantic requests and `openChild`.

## 7. Side Effects

- Active child state switch.

## 8. Constraints and Invariants

- Does not read `isEditMode`; this node is already the edit-mode representation.
- No presentation commands into content.

## 9. Non-Goals

- Does not implement drag/drop semantics.
- Does not own item data.

## 10. Platform Implementation Notes

- Visual primitive: static edit-state holder container.
- Mouse leave from local content is reported as `requestNormalState()`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state.top`
- Public node class: `TreeItemRowEditStateNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemRowEditStateContentAccess`
  - Content-to-controller: `TreeItemRowEditStateControllerAccess`
- Companion artifact stems: none
