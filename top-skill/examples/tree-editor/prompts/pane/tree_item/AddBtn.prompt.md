---
sourcePath: src/pane/tree_item/add_btn.top
---

# AddBtn

## 1. Node Identity and Role

AddBtn is a static action part inside the hover edit-mode row state.

## 2. Responsibility

- Materialize the add-child action structure.
- Pull the already-resolved add affordance token from controller access.
- Report semantic add-child intent upward through controller access.

## 3. Inputs and Events

- `getAddActionToken()` - returns the already-resolved action/affordance token.
- `requestAddChild()` - semantic request raised by local activation.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor receives only parent/context.
2. Constructor creates static action content.
3. Refresh/materialization pulls the add action token.
4. Local activation reports `requestAddChild()`.

## 7. Side Effects

The button has no direct data mutation side effects. The owning TreeItem
controller decides whether and how to add child data.

## 8. Constraints and Invariants

- No captured TreeItem callback, constructor callback, or handler bundle.
- No direct call to private ancestor methods.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not create child data directly.
- Does not manage expand/collapse.
- Does not decide its own visibility.

## 10. Platform Implementation Notes

- Visual primitive: static action element.
- Local event mechanics may stop target-local propagation when required, then
  report `requestAddChild()` through controller access.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/add_btn.top`
- Public node class: `AddBtnNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `AddBtnContentAccess`
  - Content-to-controller: `AddBtnControllerAccess`
- Companion artifact stems: none
