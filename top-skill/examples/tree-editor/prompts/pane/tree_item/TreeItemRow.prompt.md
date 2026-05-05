---
sourcePath: src/pane/tree_item/tree_item_row.top
---

# TreeItemRow

## 1. Node Identity and Role

TreeItemRow is a switchable container node that holds the view-mode row
representation and the edit-mode row representation for one TreeItem.

## 2. Responsibility

- Own the active row state selection between TreeItemRowViewState and
  TreeItemRowEditState.
- Pull `isEditMode` from the guaranteed TreeEditor ancestor and switch the active
  child accordingly during refresh.
- Expose resolved row geometry/drop values to TreeItem through typed methods.
- Expose TreeItem-derived primitive values to row state children through
  pull-through methods.

## 3. Inputs and Events

- `refresh()` - selects the active child state and requests child refresh.
- `getLabelText()` - delegates to owning TreeItem.
- `getIndentToken()` - delegates to owning TreeItem.
- `getIconToken()` - delegates to owning TreeItem.
- `getDragToken()` - delegates to owning TreeItem.
- `getDropHintToken()` - delegates to owning TreeItem.
- `requestRowMidpoint()` - asks content for measurement through lifecycle/
  materialization access only.

## 4. State Ownership

Owns only the active row representation child. Does not own item data, editor
mode, or drop state.

## 5. Child Interaction Rules

- Two children: TreeItemRowViewState and TreeItemRowEditState.
- Child constructors receive only TreeItemRow as parent/context.
- TreeItemRow does not push label, indentation, icon, or toggle values into
  children. Children pull resolved values through their parent/context contract.

## 6. Lifecycle

1. Constructor creates row holder content.
2. `buildChildren()` creates both row states and places the default child.
3. `refresh()` opens the correct child state and requests active child refresh.

## 7. Side Effects

- Switches active child through the base switchable mechanism.

## 8. Constraints and Invariants

- No setter-style propagation into children.
- No presentation command methods for drop hints. Drop hint is a resolved token
  pulled by content.
- `isEditMode` is used only by the controller to select the child state.

## 9. Non-Goals

- Does not own expand/collapse.
- Does not handle drag semantics directly.

## 10. Platform Implementation Notes

- Visual primitive: static row-state holder container.
- Drop-hint presentation is an already-resolved primitive token pulled by
  content.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row.top`
- Public node class: `TreeItemRowNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemRowContentAccess`
  - Content-to-controller: `TreeItemRowControllerAccess`
- Companion artifact stems: none
