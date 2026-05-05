---
sourcePath: src/pane/tree_item/drag_handle.top
---

# DragHandle

## 1. Node Identity and Role

DragHandle is a static affordance node inside edit-mode row states.

## 2. Responsibility

- Materialize the drag affordance structure.
- Pull the already-resolved drag affordance token from the owning controller
  access contract.
- Carry no drag/drop decision logic.

## 3. Inputs and Events

None. Drag events are reported by the containing row state content.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor receives only parent/context.
2. Constructor creates static content.
3. Refresh pulls the current drag affordance token.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must not check `isEditMode` or `isRoot`.
- Must not decide visibility or interactivity.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not initiate or handle drag operations.

## 10. Platform Implementation Notes

- Visual primitive: static affordance element.
- Display token is pulled as an already-resolved primitive.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/drag_handle.top`
- Public node class: `DragHandleNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `DragHandleContentAccess`
  - Content-to-controller: `DragHandleControllerAccess`
- Companion artifact stems: none
