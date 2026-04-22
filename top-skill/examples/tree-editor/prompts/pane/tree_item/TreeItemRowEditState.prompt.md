---
sourcePath: src/pane/tree_item/tree_item_row_edit_state.top
---

# TreeItemRowEditState

## 1. Node Identity and Role

TreeItemRowEditState is the last child of TreeItemRow. It is a switchable container node that manages the row's edit-mode presentation. It has two visual sub-state children: NormalState (default, no hover) and HoverState (on mouse hover). The active child's view is mounted within TreeItemRowEditState's own content area.

## 2. Responsibility

- Switch between NormalState and HoverState based on mouse interaction.
- Delegate `setPaddingLeft`, `setText`, and `updateToggle` to both sub-state children.
- Expose `switchToHover()` and `switchToNormal()` methods for sub-state children to request a switch.

## 3. Inputs and Events

- `switchToHover()` — called by NormalState on hover enter; opens HoverState through the base switchable mechanism.
- `switchToNormal()` — called by HoverState on hover leave; opens NormalState through the base switchable mechanism.
- Pointer/hover leave on own content area — a content-local low-level subscription that forwards `requestNormalState()` if the pointer leaves the edit-state container while HoverState is active.
- `setPaddingLeft(px)` — forwarded to both NormalState and HoverState.
- `setText(text)` — forwarded to both children's label sub-nodes.
- `updateToggle(hasChildren, isExpanded)` — forwarded to both children's icon sub-nodes.

## 4. State Ownership

- Owns the normal/hover sub-state split via `openedChild`.
- Does not own editor mode state. Does not read `isEditMode` — this node IS the edit-mode representation.

## 5. Child Interaction Rules

- Two children: TreeItemRowEditStateNormalState (`_normalState`, default) and TreeItemRowEditStateHoverState (`_hoverState`).
- During initial child materialization, assign `_normalState` as the active child and place its view without firing child lifecycle hooks.
- All data updates (`setPaddingLeft`, `setText`, `updateToggle`) are forwarded to both children regardless of which is active.
- NormalState calls `parent.switchToHover()` on hover enter.
- HoverState calls `parent.switchToNormal()` on hover leave.
- Switches are performed via `openChild(this._hoverState)` / `openChild(this._normalState)`. The base switchable mechanism mounts and unmounts the active child's view automatically.

## 6. Lifecycle

1. Constructor: creates the edit-state content boundary with `setContent(...)`.
2. `buildChildren()`: creates both sub-state children. `_normalState` is assigned as the default active child and its view is placed without calling `openChild()`.
3. The content boundary owns the low-level hover-leave subscription for its lifetime and forwards semantic requests through the controller access contract.
4. On deactivation, own view is removed by the parent switcher; no lifecycle-level handler detachment is required unless the target implementation requires explicit disposal when content is destroyed.
5. Hover/normal transitions happen via `switchToHover()` and `switchToNormal()`.

## 7. Side Effects

- Switching `openedChild` via `switchToHover()`/`switchToNormal()` causes the active sub-state's view to swap within the content area.

## 8. Constraints and Invariants

- Must not read `isEditMode`.
- Both sub-state children must always have current data (indentation, text, toggle state) regardless of which is active.
- Initial default-child assignment must not call child `onOpen()` because the surrounding tree may still be materializing.

## 9. Non-Goals

- Does not implement drag logic; drag forwarding is handled by the sub-state children.
- Does not manage expand/collapse.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item-row-edit-state`.
- `switchToHover()`: `this.openChild(this._hoverState)`.
- `switchToNormal()`: `this.openChild(this._normalState)`.
- Mouse leave: content-local low-level subscription forwards `requestNormalState()` to the controller access contract.
- Lifecycle hooks do not perform low-level subscription management in this materialization.
- `_handleMouseLeave` is a bound arrow function; `_onMouseLeave()` calls `switchToNormal()` only if `openedChild === _hoverState`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item_row_edit_state.top`
- Public node class: `TreeItemRowEditStateNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemRowEditStateContentAccess
  - Content-to-controller: TreeItemRowEditStateControllerAccess
- Companion artifact stems: none
