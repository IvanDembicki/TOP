---
sourcePath: src/toolbar/view_mode_state.top
---

# ViewModeState

## 1. Node Identity and Role

ViewModeState is the child of EditorModeHolder that represents the view mode. When it is the active child of EditorModeHolder, the editor is in view mode. It is a logical node with no visual representation.

## 2. Responsibility

- Apply view-mode state to TreeEditor when activated.
- Trigger a full tree refresh so all nodes can update their visual state for view mode.

## 3. Inputs and Events

- `onOpen()` — fired by the base switchable mechanism when this state becomes the active child of EditorModeHolder.

## 4. State Ownership

Owns no independent state. It is itself a state representation; the active mode is owned by EditorModeHolder through `openedChild`.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

- Default active child of EditorModeHolder.
- When the editor switches from edit mode to view mode, `onOpen()` fires.
- On `onOpen()`: calls `TreeEditor.setEditMode(false)` and then `TreeEditor.refreshAll()`.
- No `onClose()` behavior is required.

## 7. Side Effects

On `onOpen()`:
- Updates TreeEditor to view mode through `setEditMode(false)`.
- Calls `refreshAll()` on TreeEditor, which triggers `refresh()` on every node in the subtree.

## 8. Constraints and Invariants

- Must locate TreeEditor via upward type-based lookup, not a hardcoded navigation chain.
- Must cache the TreeEditor reference once in the constructor.
- Must not own any independent mode state.
- Must not call `toggle()` or any navigation method.
- Must not directly manipulate TreeEditor's content or platform primitive.

## 9. Non-Goals

- Does not toggle between modes.
- Does not render any visual content.
- Does not directly update individual child nodes (that is done through `refreshAll()`).

## 10. Platform Implementation Notes

- No DOM element. Extends `SwitchableNode`.
- TreeEditor lookup: `this._editor = this.findUpByType(TreeEditorNode)` captured in constructor.
- `onOpen()`: `this._editor.setEditMode(false); this._editor.refreshAll();`

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/view_mode_state.top`
- Public node class: `ViewModeStateNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: none (logical node with no content boundary)
  - Content-to-controller: none (logical node with no content boundary)
- Companion artifact stems: none