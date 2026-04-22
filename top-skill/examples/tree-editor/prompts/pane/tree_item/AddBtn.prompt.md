---
sourcePath: src/pane/tree_item/add_btn.top
---

# AddBtn

## 1. Node Identity and Role

AddBtn is an action control that triggers adding a new child node to the current tree item. It exists only inside TreeItemRowEditStateHoverState — it is architecturally absent from view mode and from the normal (non-hover) edit-state row.

## 2. Responsibility

- Render the add-child action control.
- On user activation, stop local event propagation where the target platform requires it and delegate `_onAddClick()` to the ancestor TreeItem.

## 3. Inputs and Events

- Click on own view → stops propagation; calls `_onAddClick()` on `this._treeItem` captured in the constructor.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: captures ancestor TreeItem as `this._treeItem` via `findUpByType`.
2. Constructor: creates the action control content boundary with `setContent(...)`.
3. Content owns the low-level activation subscription for its lifetime and forwards a semantic add request through the controller access contract.
4. No dynamic changes after child materialization.

## 7. Side Effects

- Click delegates to `TreeItem._onAddClick()`, which creates a new child, expands the item if collapsed, and triggers a full refresh.

## 8. Constraints and Invariants

- Must not check `isEditMode` — architectural placement guarantees this node is only present in edit mode hover state.
- Click propagation must be stopped before delegating.
- Ancestor TreeItem is captured once in the constructor as `this._treeItem`; must not call `findUpByType` on every activation.

## 9. Non-Goals

- Does not create child data directly.
- Does not manage expand/collapse.
- Does not manage its own visibility based on mode.

## 10. Platform Implementation Notes

- Visual element: `button` with CSS classes `edit-btn` and `add-btn`, text content `+`, `title` attribute `"Add child"`.
- View is placed by the parent node during `buildChildren()`.
- Click: `event.stopPropagation()` then `this._treeItem._onAddClick()`.
- TypeScript/DOM constructor note: create content-local handlers before passing them into content, or pass the node/controller access object directly to the content boundary.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/add_btn.top`
- Public node class: `AddBtnNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: AddBtnContentAccess
  - Content-to-controller: AddBtnControllerAccess
- Companion artifact stems: none
