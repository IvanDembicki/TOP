---
sourcePath: src/toolbar/edit_toggle_btn_view_mode_state.top
---

# EditToggleBtnViewModeState

## 1. Node Identity and Role

EditToggleBtnViewModeState is the first child of EditToggleBtn. It represents the action control visible when the editor is in view mode. When activated, it asks TreeEditor to switch the editor into edit mode. This node is the default active child of EditToggleBtn.

## 2. Responsibility

- Create and own the "Edit mode" action content.
- Own the low-level activation subscription inside its content boundary.
- Forward the semantic mode-switch request through the controller path; content must not decide editor behavior.
- Delegate mode-switch requests through the public TreeEditor method `toggleEditMode()`.

## 3. Inputs and Events

- User activation → calls `this._editor.toggleEditMode()`.

## 4. State Ownership

Owns no editor mode state. This is a visual/action state node selected by EditToggleBtn.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor: captures `_editor = this.findUpByType(TreeEditorNode)`.
2. Constructor: creates the action content boundary with `setContent(...)`; the content owns the low-level activation subscription and forwards a semantic activation request through the controller access contract.
3. No `onOpen()` subscription step is required for this materialization; the subscription is content-local and exists for the content lifetime.
4. No `onClose()` unsubscription step is required unless the target implementation requires explicit disposal when content is destroyed.
5. View placement and removal are performed by the parent EditToggleBtn through the base switchable mechanism.

## 7. Side Effects

- Click calls `TreeEditor.toggleEditMode()`, which delegates the mode change to the editor's public coordination path.

## 8. Constraints and Invariants

- Must locate `_editor` via `findUpByType(TreeEditorNode)` captured once in the constructor.
- Must not call EditorModeHolder directly.
- Must not store the editor mode state locally.
- Must not mount or unmount itself manually in `onOpen()` / `onClose()`.
- Initial default placement by the parent may not call `onOpen()`, so the generated implementation must ensure the initially active action control can receive user activations.

## 9. Non-Goals

- Does not apply the editor-level visual edit-mode marker; that is done by EditModeState.
- Does not manage any other toolbar controls.
- Does not trigger refresh directly.

## 10. Platform Implementation Notes

- Visual element: `button` with CSS class `edit-toggle-btn-state`, text content "Edit mode".
- Click request: content forwards a semantic request to the controller access contract; the node calls `this._editor.toggleEditMode()`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/edit_toggle_btn_view_mode_state.top`
- Public node class: `EditToggleBtnViewModeStateNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditToggleBtnViewModeStateContentAccess
  - Content-to-controller: EditToggleBtnViewModeStateControllerAccess
- Companion artifact stems: none
