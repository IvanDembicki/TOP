---
sourcePath: src/pane/tree_item/tree_item_row_view_state.top
---

# TreeItemRowViewState

## 1. Node Identity and Role

TreeItemRowViewState is the view-mode row representation for a TreeItem. It
contains NodeIcon and NodeLabel as static children.

## 2. Responsibility

- Materialize the view-mode row structure.
- Expose resolved label, indentation, and icon values to child controllers by
  delegating to TreeItemRow.
- Forward semantic toggle intent from NodeIcon upward when requested.

## 3. Inputs and Events

- `refresh()` - requests child refresh after pulling current resolved values from
  parent/context.
- `getLabelText()` / `getIndentToken()` / `getIconToken()` - delegated pull
  methods.
- `requestToggle()` - forwards to the owning TreeItem through the parent chain.

## 4. State Ownership

Owns no state. This node is the view-mode representation.

## 5. Child Interaction Rules

- Static children: NodeIcon and NodeLabel.
- Child constructors receive only TreeItemRowViewState as parent/context.
- No setter-style updates are sent to NodeIcon or NodeLabel.

## 6. Lifecycle

1. Constructor creates static row content.
2. `buildChildren()` creates NodeIcon and NodeLabel and places their opaque
   handles.
3. `refresh()` requests children to pull current resolved values.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- No DragHandle, AddBtn, or DeleteBtn.
- Does not read `isEditMode`.
- Locally implemented content has no conditional selection logic.

## 9. Non-Goals

- Does not manage drag interactions or edit actions.

## 10. Platform Implementation Notes

- Visual primitive: static row container.
- Indentation token is pulled by local content through controller access.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_view_state.top`
- Public node class: `TreeItemRowViewStateNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemRowViewStateContentAccess`
  - Content-to-controller: `TreeItemRowViewStateControllerAccess`
- Companion artifact stems: none
