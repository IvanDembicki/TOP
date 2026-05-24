---
sourcePath: src/toolbar/edit_mode_state.top
---

# EditModeState

## 1. Node Identity and Role

EditModeState is the child of EditorModeHolder that represents the edit mode. When it is the active child of EditorModeHolder, the editor is in edit mode. It is a logical node with no visual representation.

## 2. Responsibility

- Notify TreeEditor when edit mode becomes active.
- Let TreeEditor coordinate explicit structural synchronization and subsequent
  data refresh.

## 3. Inputs and Events

- `onOpen()` — fired by the base switchable mechanism when this state becomes the active child of EditorModeHolder.

## 4. State Ownership

Owns no independent state. It is itself a state representation; the active mode is owned by EditorModeHolder through `openedChild`.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

- Inactive (non-default) child of EditorModeHolder on construction.
- When the editor switches from view mode to edit mode, `onOpen()` fires.
- On `onOpen()`: calls `TreeEditor.requestEditMode(true)`.
- No `onClose()` behavior is required.

## 7. Side Effects

On `onOpen()`:
- Notifies TreeEditor that edit mode is now active.
- TreeEditor synchronizes dependent structural state explicitly and then calls
  `refreshAll()` for data/display refresh.

## 8. Constraints and Invariants

- Must locate TreeEditor via upward type-based lookup, not a hardcoded navigation chain.
- Must cache the TreeEditor reference once in the constructor.
- Must not own any independent mode state.
- Must not call `toggle()` or any navigation method.
- Must not directly manipulate TreeEditor's content or platform primitive.
- Must not directly update individual child nodes; TreeEditor owns mode-change
  coordination.

## 9. Non-Goals

- Does not toggle between modes.
- Does not render any visual content.
- Does not directly update individual child nodes.

## 10. Platform Implementation Notes

- No DOM element. Extends `SwitchableNode`.
- TreeEditor lookup: `this._editor = this.findUpByType(TreeEditorNode)` captured in constructor.
- `onOpen()`: `this._editor.requestEditMode(true);`

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/edit_mode_state.top`
- Public node class: `EditModeStateNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: none (logical node with no content boundary)
  - Content-to-controller: none (logical node with no content boundary)
- Companion artifact stems: none
