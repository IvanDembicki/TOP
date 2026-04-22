---
sourcePath: src/tree_editor.top
---

# TreeEditor

## 1. Node Identity and Role

TreeEditor is the executable editor branch root. In the current target it is bootstrapped directly by the host entry point; after AppNode materialization it should be created by the application composition root. It owns the editor toolbar, mode holder, and pane. It is the integration point between the editor branch and the host container, not the root of all project branches.

## 2. Responsibility

- Provide the top-level visual container for the editor.
- Accept `mount(container, sourceData)` to attach the editor to the host environment and seed the tree with data.
- Own the drag-and-drop session state (which item is currently being dragged).
- Expose `isEditMode` as a derived read-only property for descendant nodes.
- Expose `setEditMode(value)` to apply the editor-level visual mode marker through its content boundary.
- Expose `refreshAll()` to trigger a full recursive refresh of every node in the subtree.

## 3. Inputs and Events

- `mount(container, sourceData)` — current target bootstrap entry point. Attaches the editor branch view to the host container, then delegates data initialization to RootItemHolder. In a materialized AppNode target this call may be delegated by the application composition root.
- `setDraggedItem(item)` — called by drag-aware descendants to register the item being dragged.
- `getDraggedItem()` — called by descendants during drag events to query the current dragged item.
- `clearDraggedItem()` — called at drag end to reset drag state.
- `setEditMode(value)` — called by editor mode states to update the editor-level visual mode marker; the controller delegates this operation to content through `IContentAccess`.
- `refreshAll()` — may be called by any descendant to cascade a refresh to all nodes.

## 4. State Ownership

- **draggedItem** — the tree node currently being dragged, or null. The only mutable state owned directly by TreeEditor.
- **isEditMode** (derived) — computed from EditorModeHolder's active child. TreeEditor never caches this value; it always derives it live.

## 5. Child Interaction Rules

TreeEditor has exactly three direct children, created in this order:
1. EditorToolbar
2. EditorModeHolder
3. EditorPane

TreeEditor queries EditorModeHolder via the private `_editorModeHolder` reference when computing `isEditMode`. It delegates data initialization during `mount` to EditorPane via the private `_editorPane` reference, which in turn delegates to RootItemHolder. Children's views are placed by TreeEditor into its own content area during the child materialization phase.

## 6. Lifecycle

1. Constructor: initializes TreeEditor-owned runtime state only.
2. Constructor: creates the editor content boundary with `setContent(...)`.
3. `buildChildren()`: creates EditorToolbar, EditorModeHolder, and EditorPane in the declared order; places the visual child views through TreeEditor's content boundary.
4. `mount(container, sourceData)`: attaches the editor view to the host container; delegates data initialization to EditorPane, which in turn calls `rootItemHolder.init(sourceData)`.
5. `refreshAll()`: performs a synchronous depth-first traversal of the full node subtree and calls `refresh()` on each node.

## 7. Side Effects

- Attaching the editor view to the host container during `mount`.
- `refreshAll()` causes the subtree to re-evaluate and update its materialized presentation where needed.

## 8. Constraints and Invariants

- Exactly one EditorModeHolder, one EditorToolbar, and one EditorPane exist as direct children at all times.
- `draggedItem` is null outside of an active drag operation.
- `isEditMode` is always derived live; never stored as a cached boolean.
- `refreshAll()` must visit all nodes in the subtree, not only direct children.
- Controller code must not mutate the editor visual primitive directly when changing edit-mode presentation; it must call a named content command.

## 9. Non-Goals

- Does not manage item selection.
- Does not serialize or deserialize tree data.
- Does not manage scroll position.
- Does not observe external resize events.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-editor`.
- Edit-mode marker: content command toggles CSS class `edit-mode` on the editor element.
- `isEditMode` reads `this._editorModeHolder.isEditMode`.
- `mount` attaches the editor branch view to the host container; a DOM target may use `replaceChildren(this.getView())` to keep the host surface single-rooted.
- `refreshAll()` is a synchronous recursive walk; no async scheduling.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/tree_editor.top`
- Public node class: `TreeEditorNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeEditorContentAccess
  - Content-to-controller: TreeEditorControllerAccess with zero-contract implementation TreeEditorControllerAccessZero
- Companion artifact stems: none