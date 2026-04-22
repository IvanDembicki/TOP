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

## 3. Inputs and Events

None. All interaction is handled by child nodes.

## 4. State Ownership

Owns no state.

## 5. Child Interaction Rules

- Has two direct children: EditToggleBtn and BuildInfo.
- EditorToolbar places child views through its content boundary in `buildChildren()`.
- EditorToolbar does not call methods on its children.

## 6. Lifecycle

1. Constructor: no toolbar state is initialized.
2. Constructor: creates the toolbar content boundary with `setContent(...)`.
3. `buildChildren()`: creates EditToggleBtn and BuildInfo and places their views through the toolbar content boundary.
4. No further changes to its own visual content or children after child materialization.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Structurally immutable after child materialization: no dynamic addition or removal of child nodes.
- TreeEditor places the toolbar's view in its own `buildChildren()`.

## 9. Non-Goals

- Does not toggle editor mode.
- Does not render action content or icons directly.
- Does not react to mode changes.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `editor-toolbar`.
- Child mounting uses `this.content.mount(child.getView())`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/toolbar.top`
- Public node class: `EditorToolbarNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditorToolbarContentAccess
  - Content-to-controller: EditorToolbarControllerAccess with zero-contract implementation EditorToolbarControllerAccessZero
- Companion artifact stems: none
