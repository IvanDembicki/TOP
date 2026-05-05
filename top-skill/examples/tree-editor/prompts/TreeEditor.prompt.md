---
sourcePath: src/tree_editor.top
---

# TreeEditor

## 1. Node Identity and Role

TreeEditor is the executable editor branch root. In the current target it is
bootstrapped by the host entry point; after AppNode materialization it should be
created by the application composition root. It owns the editor toolbar, mode
holder, and pane.

## 2. Responsibility

- Provide the top-level editor content container.
- Attach its opaque content handle to the host boundary through the current
  bootstrap adapter.
- Pull the root tree record through the declared demo-data/asset branch contract
  and expose it to EditorPane through a narrow controller/domain method.
- Own drag session state for the currently dragged TreeItem controller.
- Expose `isEditMode` as a derived read-only property from EditorModeHolder.
- Expose already-resolved editor presentation tokens through controller access
  so locally implemented content can apply them during refresh.
- Expose `refreshAll()` to request a full subtree refresh after state or data
  changes.

## 3. Inputs and Events

- `attachToHost(hostBoundary)` - attaches the editor opaque content handle to
  the host integration boundary. It does not receive semantic data.
- `getRootRecord()` - returns the current root tree record to EditorPane or
  RootItemHolder through the allowed direct-child chain. The record is pulled
  from the declared data/asset context, not injected through this node API.
- `setDraggedItem(item)` / `getDraggedItem()` / `clearDraggedItem()` - manage
  the current drag session.
- `requestEditMode(value)` - called by editor mode state controllers. Updates
  mode state through EditorModeHolder and requests refresh; it does not command
  content to toggle classes.
- `refreshAll()` - requests every node in the subtree to refresh from current
  controller/data state.

## 4. State Ownership

- `rootRecord` - resolved root record pulled through the declared data/asset
  context.
- `draggedItem` - current TreeItem controller being dragged, or null.
- `isEditMode` - derived live from EditorModeHolder, never cached.
- Editor-level presentation tokens are resolved by the controller and pulled by
  TreeEditor content during materialization/refresh.

## 5. Child Interaction Rules

TreeEditor has exactly three direct children:
1. EditorToolbar
2. EditorModeHolder
3. EditorPane

Child constructors receive only TreeEditor as parent/context. TreeEditor exposes
`getRootRecord()`, `isEditMode`, drag-session methods, and refresh methods
through its controller/domain surface. It does not receive or pass source data,
mode flags, callbacks, config, or presentation values through constructors or
runtime entrypoints.

## 6. Lifecycle

1. Constructor initializes TreeEditor-owned state only.
2. Constructor creates content typed through `IContentAccess`.
3. `buildChildren()` creates the three direct children and places their opaque
   handles through parent-owned materialization.
4. `attachToHost(hostBoundary)` attaches the editor opaque handle to the host
   boundary and requests refresh/materialization of the pane branch. Raw demo
   data is initialized outside the TOP node API through the declared data/asset
   bootstrap adapter.
5. `refreshAll()` performs a synchronous depth-first refresh request.

## 7. Side Effects

- Host attachment during `attachToHost`.
- Subtree refresh after data context, mode state, drag state, or tree structure
  changes.

## 8. Constraints and Invariants

- TreeEditor does not mutate its presentation content to show/hide/update mode
  state. It resolves presentation tokens and requests refresh.
- TreeEditor does not pass data/config/callback/state packets into children.
- TreeEditor public runtime entrypoints do not receive semantic data packets.
- The host container is an integration boundary, not a TOP child.
- `isEditMode` is derived live from EditorModeHolder.

## 9. Non-Goals

- Does not serialize changes back to the demo asset/data branch.
- Does not manage scroll position.
- Does not own item-level expand/collapse state.

## 10. Platform Implementation Notes

- Visual primitive: `div` with role/class generated from already-resolved
  controller tokens.
- A DOM target may attach the editor opaque handle using host integration
  mechanics such as replacing the host's single child.
- If demo JSON is loaded by target startup code, that loader is an external
  bootstrap adapter. It initializes the data/asset branch through an explicit
  data-controller contract before or alongside TreeEditor attachment; it is not
  a TreeEditor runtime parameter.
- Edit-mode styling is an already-resolved primitive token pulled by content
  through controller access.
- `refreshAll()` is a synchronous recursive walk.

## 11. Expected Materialization

- Primary artifact stem: `src/tree_editor.top`
- Public node class: `TreeEditorNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeEditorContentAccess`
  - Content-to-controller: `TreeEditorControllerAccess`
- Companion artifact stems: none
