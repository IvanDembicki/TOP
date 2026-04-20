---
sourcePath: src/pane/tree_item/node_icon.top
---

# NodeIcon

## 1. Node Identity and Role

NodeIcon is a visual part within a tree item row that displays an icon indicating whether the item is a file (no children) or a folder (has children), and whether a folder is expanded or collapsed. It is a child of TreeItemRowViewState and TreeItemRowEditStateNormalState / TreeItemRowEditStateHoverState.

## 2. Responsibility

- Render an icon that reflects the item's child-bearing status and current expansion state.
- Respond to user activation by triggering expand/collapse on the ancestor TreeItem — but only when the item has children.
- Update its visual appearance when `update(hasChildren, isExpanded)` is called.

## 3. Inputs and Events

- `update(hasChildren, isExpanded)` — called by the parent row state on toggle notification; updates the icon appearance and activation affordance based on the new values.
- Click on own view (only effective when `hasChildren` is true) → calls `treeItem._toggle()` via upward type-based lookup. Click propagation is stopped so the event does not bubble to the row.

## 4. State Ownership

- Internally tracks `_hasChildren` to guard activation behavior (activation only triggers toggle when there are children).
- Does not own expand/collapse state; that is owned by ExpandCollapseHolder.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: creates the icon content boundary with `setContent(...)`.
2. Content owns the low-level activation subscription for its lifetime and forwards a semantic toggle request through the controller access contract.
3. Default icon state: file icon (no children assumed).
4. On each `update(hasChildren, isExpanded)` call: updates the icon content and activation affordance.

## 7. Side Effects

- Click (when `hasChildren` is true): calls `treeItem._toggle()`, which causes expand/collapse state to change.

## 8. Constraints and Invariants

- Click must be a no-op when `hasChildren` is false.
- Click must not propagate to ancestor elements.
- Icon must reflect three mutually exclusive states: file (no children), folder-closed (has children, collapsed), folder-open (has children, expanded).

## 9. Non-Goals

- Does not own or track expand/collapse state.
- Does not manage label text.
- Does not apply edit mode appearance.

## 10. Platform Implementation Notes

- Visual element: `span` with CSS class `node-icon`.
- Three icon variants are SVG strings: `FILE_SVG`, `FOLDER_SVG` (closed), `FOLDER_OPEN_SVG` (open).
- Default inner content: `FILE_SVG`.
- On `update`: set `innerHTML` to the appropriate SVG and toggle the activation presentation marker according to `hasChildren`.
- Click: `event.stopPropagation()` before calling `this._treeItem._toggle()`.
- TypeScript/DOM constructor note: create content-local handlers before passing them into content, or pass the node/controller access object directly to the content boundary.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/node_icon.top`
- Public node class: `NodeIconNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: NodeIconContentAccess
  - Content-to-controller: NodeIconControllerAccess
- Companion artifact stems: none
