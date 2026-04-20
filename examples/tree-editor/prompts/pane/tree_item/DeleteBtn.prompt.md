---
sourcePath: src/pane/tree_item/delete_btn.top
---

# DeleteBtn

## 1. Node Identity and Role

DeleteBtn is an action control that triggers deletion of the current tree item. It exists only inside TreeItemRowEditStateHoverState, and only for non-root items — it is architecturally absent from view mode, from the normal (non-hover) edit-state row, and from root items.

## 2. Responsibility

- Render the delete action control.
- On user activation, stop local event propagation where the target platform requires it and delegate `_onDeleteClick()` to the ancestor TreeItem.

## 3. Inputs and Events

- Click on own view → stops propagation; calls `_onDeleteClick()` on `this._treeItem` captured in the constructor.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: captures ancestor TreeItem as `this._treeItem` via `findUpByType`.
2. Constructor: creates the action control content boundary with `setContent(...)`.
3. Content owns the low-level activation subscription for its lifetime and forwards a semantic delete request through the controller access contract.
4. Created only when `treeItem.isRoot` is false — the parent HoverState node conditionally instantiates it during `buildChildren`.
5. No dynamic changes after child materialization.

## 7. Side Effects

- Click delegates to `TreeItem._onDeleteClick()`, which removes the item from the materialized view and node tree, notifies the parent TreeItem, and triggers editor refresh through TreeItem.

## 8. Constraints and Invariants

- Must not check `isEditMode` — architectural placement guarantees this node is only present in edit-mode hover state.
- Must not check `isRoot` dynamically — root exclusion is guaranteed by conditional instantiation in the parent.
- Click propagation must be stopped before delegating.
- Ancestor TreeItem is captured once in the constructor as `this._treeItem`; must not call `findUpByType` on every activation.

## 9. Non-Goals

- Does not perform removal directly; removal is handled by TreeItem.
- Does not manage its own visibility based on mode.

## 10. Platform Implementation Notes

- Visual element: `button` with CSS classes `edit-btn` and `delete-btn`, text content `×`, `title` attribute `"Delete node"`.
- View is placed by the parent node during `buildChildren()`.
- Click: `event.stopPropagation()` then `this._treeItem._onDeleteClick()`.
- TypeScript/DOM constructor note: create content-local handlers before passing them into content, or pass the node/controller access object directly to the content boundary.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/delete_btn.top`
- Public node class: `DeleteBtnNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: DeleteBtnContentAccess
  - Content-to-controller: DeleteBtnControllerAccess
- Companion artifact stems: none
