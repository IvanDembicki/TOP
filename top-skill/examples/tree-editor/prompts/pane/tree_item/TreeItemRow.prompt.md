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
- Expose explicit row-mode synchronization methods. `syncRowModeState()` reads
  `isEditMode` from the guaranteed TreeEditor ancestor and calls
  `showEditRow()` or `showViewRow()`. Those methods open the target child
  through `child.open()`.
- Expose resolved row geometry/drop values to TreeItem through typed methods.
- Expose TreeItem-derived primitive values to row state children through
  pull-through methods.

## 3. Inputs and Events

- `syncRowModeState()` - explicit structural synchronization request called
  after editor mode changes; it is not a refresh hook.
- `showEditRow()` - calls `_editState.open()`.
- `showViewRow()` - calls `_viewState.open()`.
- `refresh()` - requests the currently active child state to refresh resolved
  primitive values only; it does not switch state.
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
3. `syncRowModeState()` opens the correct child state through the target child's
   `open()` method.
4. `refresh()` requests active child data/display refresh only.

## 7. Side Effects

- Explicit row-mode synchronization switches active child through the target
  child's `open()` method.

## 8. Constraints and Invariants

- No setter-style propagation into children.
- No presentation command methods for drop hints. Drop hint is a resolved token
  pulled by content.
- `isEditMode` is used only by the explicit `syncRowModeState()` transition
  method, never by `refresh()`.

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
