---
sourcePath: src/toolbar/toolbar.top
---

# EditorToolbar

## 1. Node Identity and Role

EditorToolbar is the horizontal toolbar container of the tree editor. It is a structurally immutable node that owns the toolbar's visual content and serves as the attachment point for toolbar controls.

## 2. Responsibility

- Create and expose the toolbar visual content.
- Serve as the structural parent for EditToggleBtn.
- Provide its content area as the mounting target for child action nodes.
- Expose explicit mode-action synchronization methods that delegate to
  EditToggleBtn's public controller contract.

## 3. Inputs and Events

- `showEditModeAction()` - called by TreeEditor after edit mode becomes active;
  delegates to EditToggleBtn.
- `showViewModeAction()` - called by TreeEditor after view mode becomes active;
  delegates to EditToggleBtn.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

- Has two direct children: EditToggleBtn and BuildInfo.
- EditorToolbar constructs its direct children in `buildChildren()`, obtains their opaque view handles from the child controllers, and places those handles through its own content boundary.
- EditorToolbar does not inspect child internals. It may call declared public
  controller methods on direct child nodes, such as EditToggleBtn's
  mode-action synchronization methods.

## 6. Lifecycle

1. Constructor: no toolbar state is initialized.
2. Constructor: creates the toolbar content boundary with `setContent(...)`.
3. `buildChildren()`: creates EditToggleBtn and BuildInfo and places their views through the toolbar content boundary.
4. Mode-action synchronization calls are delegated to EditToggleBtn and do not
   mutate EditorToolbar content or child structure.
5. No further changes to its own visual content or children after child materialization.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Structurally immutable after child materialization: no dynamic addition or removal of child nodes.
- TreeEditor places the toolbar's view in its own `buildChildren()`.

## 9. Non-Goals

- Does not toggle editor mode.
- Does not render action content or icons directly.
- Does not choose EditToggleBtn's internal child directly and does not call
  `openChild()` on descendants.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `editor-toolbar`.
- Child mounting may use `this.content.mount(child.getView())` only as the toolbar controller's own parent-owned placement primitive for direct child opaque handles; it is not a slot/props injection pattern.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/toolbar.top`
- Public node class: `EditorToolbarNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditorToolbarContentAccess
  - Content-to-controller: EditorToolbarControllerAccess empty zero-contract interface implemented by the owning node/controller
- Companion artifact stems: none
