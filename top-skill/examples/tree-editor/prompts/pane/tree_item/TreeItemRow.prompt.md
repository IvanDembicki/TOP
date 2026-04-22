---
sourcePath: src/pane/tree_item/tree_item_row.top
---

# TreeItemRow

## 1. Node Identity and Role

TreeItemRow is a switchable container node that holds two row representations for a tree item: one for view mode (TreeItemRowViewState) and one for edit mode (TreeItemRowEditState). It has its own content area into which the active child's view is mounted.

## 2. Responsibility

- Maintain the correct active child based on the current editor mode.
- Delegate `setPaddingLeft`, `setText`, and `updateToggle` to both children unconditionally so that both are always up-to-date regardless of which is currently active.
- Expose row measurement and drop-hint commands through its content boundary for drag-and-drop coordination.

## 3. Inputs and Events

- `refresh()` — reads `isEditMode` from the ancestor TreeEditor; if the active child does not match the mode, opens the matching child through the base switchable mechanism.
- `setPaddingLeft(px)` — forwarded to both TreeItemRowViewState and TreeItemRowEditState.
- `setText(text)` — forwarded to both children's label sub-nodes.
- `updateToggle(hasChildren, isExpanded)` — forwarded to both children's icon sub-nodes.
- `getRowMidpointY()` — asks content for the row midpoint in host/platform coordinates.
- `setDropHint(position)` — asks content to materialize the current drop hint.
- `clearDropHint()` — asks content to clear any materialized drop hint.

## 4. State Ownership

- Owns the view/edit row split via `openedChild`.
- Does not own the editor mode; reads it only to make the switching decision.

## 5. Child Interaction Rules

- Two children: TreeItemRowViewState (`_viewState`, default) and TreeItemRowEditState (`_editState`).
- During initial child materialization, assign `_viewState` as the active child and place its view without firing child lifecycle hooks.
- All data updates (`setPaddingLeft`, `setText`, `updateToggle`) are sent to both children regardless of which is active.
- Switching is performed via `openChild(target)` in `refresh()`. The base switchable mechanism mounts and unmounts the active child's view automatically.

## 6. Lifecycle

1. Constructor: captures the ancestor TreeEditor reference if required by the generated implementation.
2. Constructor: creates the row-holder content boundary with `setContent(...)`.
3. `buildChildren()`: creates both children. `_viewState` is assigned as the default active child and its view is placed into the content area without calling `openChild()`.
4. On `refresh()`: if `isEditMode` is true, calls `openChild(this._editState)`; if false, calls `openChild(this._viewState)`. No switch is made if the correct child is already active.

## 7. Side Effects

- Switching `openedChild` in `refresh()` via `openChild()`: the base switcher unmounts the outgoing child's view and mounts the incoming child's view.

## 8. Constraints and Invariants

- `isEditMode` must only be read for the purpose of switching `openedChild`; no other logic should depend on it at this level.
- Both children must receive all data updates regardless of active state.
- Initial default-child assignment must not call child `onOpen()` because the surrounding tree may still be materializing.
- Controller code must not inspect or mutate the row holder primitive directly for measurement or drop-hint presentation; it must use named content commands.

## 9. Non-Goals

- Does not manage expand/collapse.
- Does not handle drag events.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item-row-holder`.
- Row midpoint: content reads the holder element geometry and returns the vertical midpoint.
- Drop hint: content toggles CSS classes `drop-top` and `drop-bottom` on the holder element.
- Ancestor lookup: `this._editor = this.findUpByType(TreeEditorNode)` captured in constructor; `refresh()` reads `this._editor?.isEditMode ?? false`.
- On `refresh()`: `const target = isEdit ? this._editState : this._viewState; if (this.openedChild !== target) this.openChild(target);`
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row.top`
- Public node class: `TreeItemRowNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemRowContentAccess
  - Content-to-controller: TreeItemRowControllerAccess with zero-contract implementation TreeItemRowControllerAccessZero
- Companion artifact stems: none