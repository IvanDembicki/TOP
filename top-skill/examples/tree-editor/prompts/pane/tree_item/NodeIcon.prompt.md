---
sourcePath: src/pane/tree_item/node_icon.top
---

# NodeIcon

## 1. Node Identity and Role

NodeIcon is a static icon part inside a tree item row.

## 2. Responsibility

- Materialize the icon structure.
- Pull the already-resolved icon token and activation affordance token from the
  owning controller access contract.
- Report semantic toggle requests upward through controller access.

## 3. Inputs and Events

- `getIconToken()` - returns the already-resolved icon token.
- `getIconActivationToken()` - returns the already-resolved activation affordance
  token.
- `requestToggle()` - semantic request raised when local activation occurs.

## 4. State Ownership

Owns no state. The owning TreeItem controller resolves whether the item is a
leaf, expanded branch, or collapsed branch.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor receives only parent/context.
2. Constructor creates static icon content.
3. Refresh/materialization pulls icon and activation tokens through controller
   access.
4. Local activation reports `requestToggle()` to the controller. The controller
   decides whether toggle is allowed.

## 7. Side Effects

The node itself has no direct side effects. A semantic toggle request may cause
the owning TreeItem controller to update expand/collapse state.

## 8. Constraints and Invariants

- No `update(hasChildren, isExpanded)` or equivalent data packet method.
- No locally stored `hasChildren`/`isExpanded` flags for presentation decisions.
- No direct ancestor mutation such as calling private TreeItem methods.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not own expand/collapse state.
- Does not choose icon variants locally.
- Does not manage label text or edit mode appearance.

## 10. Platform Implementation Notes

- Visual primitive: static icon element.
- Icon representation is selected by the controller and exposed as an
  already-resolved primitive token.
- Content-local activation handlers call the narrow controller access method;
  callbacks are not injected through constructors.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/node_icon.top`
- Public node class: `NodeIconNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `NodeIconContentAccess`
  - Content-to-controller: `NodeIconControllerAccess`
- Companion artifact stems: none
