---
sourcePath: src/pane/tree_item/delete_btn.top
---

# DeleteBtn

## 1. Node Identity and Role

DeleteBtn is a static action part inside the hover edit-mode row state.

## 2. Responsibility

- Materialize the delete action structure.
- Pull the already-resolved delete affordance token from controller access.
- Report semantic delete intent upward through controller access.

## 3. Inputs and Events

- `getDeleteActionToken()` - returns the already-resolved delete affordance token.
- `requestDeleteSelf()` - semantic request raised by local activation.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor receives only parent/context.
2. Constructor creates static action content.
3. Refresh/materialization pulls the delete action token.
4. Local activation reports `requestDeleteSelf()`.

## 7. Side Effects

The button has no direct removal side effect. The owning TreeItem controller
decides whether deletion is allowed and routes the mutation to the proper data
controller/container.

## 8. Constraints and Invariants

- DeleteBtn is structurally present in the hover edit-mode row. Root/non-root
  availability is represented by a resolved token; content does not decide it.
- No captured TreeItem callback, constructor callback, or handler bundle.
- No direct call to private ancestor methods.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not remove data directly.
- Does not decide its own visibility.

## 10. Platform Implementation Notes

- Visual primitive: static action element.
- Local event mechanics may stop target-local propagation when required, then
  report `requestDeleteSelf()` through controller access.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/delete_btn.top`
- Public node class: `DeleteBtnNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `DeleteBtnContentAccess`
  - Content-to-controller: `DeleteBtnControllerAccess`
- Companion artifact stems: none
