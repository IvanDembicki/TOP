---
sourcePath: src/pane/tree_item/node_label.top
---

# NodeLabel

## 1. Node Identity and Role

NodeLabel is a read-only text visual part that displays the type name of a tree item. It is a child of TreeItemRowViewState and the edit-state row sub-nodes. It has no interactivity.

## 2. Responsibility

- Render the text of the item's type name.
- Expose `setText(text)` to update the displayed text.

## 3. Inputs and Events

- `setText(text)` — called by TreeItemRow delegating from TreeItem; updates the visible label.
- No user interaction events.

## 4. State Ownership

Owns no explicit state. The displayed text is held implicitly by the visual content.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: creates the label content boundary with `setContent(...)`.
2. Text is set on initial `reset` via `setText` and may be updated at any time thereafter.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must only display text; no interactive behavior.
- Must not allow inline editing.

## 9. Non-Goals

- Does not support inline editing of the node type.
- Does not manage its own visibility.

## 10. Platform Implementation Notes

- Visual element: `span` with CSS class `node-label`.
- `setText(text)`: delegated through `NodeLabelContentAccess`; sets `el.textContent = text` on the content.
- View is placed by the parent node during `buildChildren()`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/node_label.top`
- Public node class: `NodeLabelNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: NodeLabelContentAccess
  - Content-to-controller: NodeLabelControllerAccess with zero-contract implementation NodeLabelControllerAccessZero
- Companion artifact stems: none
