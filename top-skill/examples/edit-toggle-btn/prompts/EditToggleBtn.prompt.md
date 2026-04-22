---
sourcePath: src/toolbar/edit_toggle_btn.top
---

# EditToggleBtn

## 1. Node Identity and Role

EditToggleBtn is a logical switchable node in the toolbar that controls which visual sub-state of the mode toggle action is currently mounted. It has two visual sub-state children: one for view mode (showing the edit-mode action label) and one for edit mode (showing the view-mode action label). The active child is selected from the current editor mode.

## 2. Responsibility

- Switch which action sub-state is displayed based on the current editor mode.
- Keep editor mode ownership outside this node.
- Do not handle low-level activation events directly; activation behavior belongs to the child state nodes.

## 3. Inputs and Events

- `refresh()` — reads `isEditMode` from the stored ancestor TreeEditor reference and switches `openedChild` to the matching sub-state if it is not already active.

## 4. State Ownership

- Owns the active visual sub-state via `openedChild`.
- Does not own or cache the editor mode; reads it from the stored `_editor` reference on each `refresh()` call.

## 5. Child Interaction Rules

- Two children: EditToggleBtnViewModeState (`_viewMode`) and EditToggleBtnEditModeState (`_editMode`).
- `_viewMode` is the default active child. During initial child materialization, assign it as the active child without firing child lifecycle hooks.
- On `refresh()`: choose `_editMode` when `isEditMode` is true, otherwise `_viewMode`; call `openChild(target)` to switch only when needed by the base switchable mechanism.
- The base switchable mechanism mounts and unmounts the active child's view in this node's content area.
- Child state nodes own their low-level content subscriptions; EditToggleBtn only switches which child view is mounted.

## 6. Lifecycle

1. Constructor: captures `_editor = this.findUpByType(TreeEditorNode)`, creates the content boundary with `setContent(...)`, then creates both child state nodes.
2. `buildChildren()`: creates both child state nodes and assigns `_viewMode` as the initial active child via `setInitialChild(...)`.
3. On `refresh()`: calls `openChild(target)` if the editor mode has changed. The base switching path unmounts the outgoing child view, mounts the incoming child view, and calls the child lifecycle hooks.

## 7. Side Effects

- Switching active child during `refresh()` changes the mounted child view and triggers child lifecycle hooks (`onClose()` on the outgoing child, `onOpen()` on the incoming child).

## 8. Constraints and Invariants

- Must not render the concrete action control itself.
- Must not access the content's platform primitive (`el`) directly.
- Must not perform manual child mount/unmount inside EditToggleBtn itself.
- Must not handle low-level activation events directly.
- Must not cache editor mode as a local boolean.
- Initial default-child assignment must not call child `onOpen()` because the surrounding tree may still be materializing.
- `openedChild` must always match the current editor mode after `refresh()` completes.

## 9. Non-Goals

- Does not own editor mode.
- Does not call `toggleEditMode()` itself.
- Does not apply platform visual mode markers to the editor root.
- Does not trigger tree refresh.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `edit-toggle-btn`.
- Extends `SwitchableNode`.
- Ancestor lookup: `this._editor = this.findUpByType(TreeEditorNode)` captured in constructor.
- Constructor materialization: `this.setContent(new EditToggleBtnContent(new EditToggleBtnControllerAccessZero()))`.
- On `refresh()`: `const target = this._editor.isEditMode ? this._editMode : this._viewMode; this.openChild(target);`

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/edit_toggle_btn.top`
- Public node class: `EditToggleBtnNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditToggleBtnContentAccess
  - Content-to-controller: EditToggleBtnControllerAccess with zero-contract implementation EditToggleBtnControllerAccessZero
- Companion artifact stems: none