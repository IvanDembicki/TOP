---
sourcePath: src/pane/tree_item/tree_item_row_view_state.top
---

# TreeItemRowViewState

## 1. Node Identity and Role

TreeItemRowViewState is the first child of TreeItemRow. It provides the visual row for view mode. It contains NodeIcon and NodeLabel as its children. Drag capability and edit controls are architecturally absent from this state — not hidden or disabled, but genuinely not present.

## 2. Responsibility

- Create and own the view-mode row visual content.
- Apply indentation via `setPaddingLeft`.
- Expose `updateToggle(hasChildren, isExpanded)` by delegating to NodeIcon.
- Expose `setText(text)` by delegating to NodeLabel.

## 3. Inputs and Events

- `setPaddingLeft(px)` — sets left indentation on the row view.
- `setText(text)` — delegated to NodeLabel.
- `updateToggle(hasChildren, isExpanded)` — delegated to NodeIcon.

## 4. State Ownership

Owns no state. Does not read `isEditMode` — this node IS the view mode representation.

## 5. Child Interaction Rules

- Two children: NodeIcon and NodeLabel.
- Children's views are placed into this node's content area during child materialization.

## 6. Lifecycle

1. Constructor: creates the row content boundary with `setContent(...)`.
2. `buildChildren()`: creates NodeIcon and NodeLabel as children and places their views through the row content boundary.
3. Placement and removal of this node's own view are handled by the parent TreeItemRow's base switchable mechanism.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must not contain DragHandle, AddBtn, or DeleteBtn.
- Must not read `isEditMode`.

## 9. Non-Goals

- Does not manage drag interactions.
- Does not manage expand/collapse.
- Does not enable drag capability.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item-row`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_view_state.top`
- Public node class: `TreeItemRowViewStateNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemRowViewStateContentAccess
  - Content-to-controller: TreeItemRowViewStateControllerAccess with zero-contract implementation TreeItemRowViewStateControllerAccessZero
- Companion artifact stems: none