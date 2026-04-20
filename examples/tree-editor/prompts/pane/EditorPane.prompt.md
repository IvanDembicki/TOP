---
sourcePath: src/pane/editor_pane.top
---

# EditorPane

## 1. Node Identity and Role

EditorPane is the main content area of the tree editor. It is a structurally immutable container node that provides the visual region for tree content. It is a direct child of TreeEditor and the parent of RootItemHolder.

## 2. Responsibility

- Create and expose the pane visual content.
- Serve as the structural parent for RootItemHolder.
- Expose `init(sourceData)` to delegate data initialization to RootItemHolder.

## 3. Inputs and Events

- `init(sourceData)` — called by TreeEditor during `mount()`. Delegates to `rootItemHolder.init(sourceData)`.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

- Has exactly one direct child: RootItemHolder.
- RootItemHolder's view is placed into EditorPane's content area during child materialization.
- EditorPane calls `init(sourceData)` on RootItemHolder when instructed by TreeEditor.

## 6. Lifecycle

1. Constructor: no pane state is initialized.
2. Constructor: creates the pane content boundary with `setContent(...)`.
3. `buildChildren()`: creates RootItemHolder and places RootItemHolder's view through the pane content boundary.
4. On `init(sourceData)`: delegates to `rootItemHolder.init(sourceData)`.
5. No further structural changes after child materialization.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Structurally immutable after child materialization.

## 9. Non-Goals

- Does not manage tree data directly.
- Does not handle expand/collapse.
- Does not react to mode changes.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `editor-pane`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/editor_pane.top`
- Public node class: `EditorPaneNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditorPaneContentAccess
  - Content-to-controller: EditorPaneControllerAccess with zero-contract implementation EditorPaneControllerAccessZero
- Companion artifact stems: none