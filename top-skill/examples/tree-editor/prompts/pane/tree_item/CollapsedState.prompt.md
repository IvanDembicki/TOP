---
sourcePath: src/pane/tree_item/collapsed_state.top
---

# CollapsedState

## 1. Node Identity and Role

CollapsedState is the last child of ExpandCollapseHolder. When active, it represents the collapsed state of a tree item. It is a logical node with no visual content and no children of its own. It has no content — its role is purely representational.

## 2. Responsibility

- Exist as the collapsed state within ExpandCollapseHolder.
- Notify the ancestor TreeItem when this state becomes active so the row icon refreshes after `openedChild` has already changed to collapsed.
- Do not deactivate ChildrenList; that is handled by ExpandedState's `onClose()`.

## 3. Inputs and Events

- `onOpen()` — fired when this state becomes the active child of ExpandCollapseHolder; calls `notifyToggle()` on ancestor TreeItem.
- `onClose()` — no action required.

## 4. State Ownership

Owns no state. It is itself a state representation.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: no state or content initialization.
2. On `onOpen()`: calls `notifyToggle()` on ancestor TreeItem.
3. On `onClose()`: no action.

## 7. Side Effects

Updates the row icon to the collapsed folder state.

## 8. Constraints and Invariants

- Must not attempt to hide or destroy ChildrenList; that is handled by ExpandedState and the base switching lifecycle.
- Icon refresh must happen after CollapsedState is active, not during ExpandedState's outgoing `onClose()`.

## 9. Non-Goals

- Does not hide ChildrenList.
- Does not render any visual content.
- Does not own expand/collapse state.

## 10. Platform Implementation Notes

- No DOM element. Extends `SwitchableNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/collapsed_state.top`
- Public node class: `CollapsedStateNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: none (logical node with no content boundary)
  - Content-to-controller: none (logical node with no content boundary)
- Companion artifact stems: none
