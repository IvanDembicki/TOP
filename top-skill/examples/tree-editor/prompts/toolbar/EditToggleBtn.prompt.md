---
sourcePath: src/toolbar/edit_toggle_btn.top
---

# EditToggleBtn

## 1. Node Identity and Role

EditToggleBtn is a logical switchable node in the toolbar that controls which
visual sub-state of the mode toggle action is currently mounted. It has two
visual sub-state children: one for view mode and one for edit mode. Each state
controller resolves its own final action label; locally implemented content only
pulls and applies that already-resolved value.

## 2. Responsibility

- Switch which action sub-state is displayed based on the current editor mode.
- Keep editor mode ownership outside this node.
- Do not handle low-level activation events directly; activation behavior belongs to the child state nodes.

## 3. Inputs and Events

- `syncActionForCurrentEditorMode()` — explicit structural synchronization
  request called after editor mode changes. It reads `isEditMode` from the
  stored ancestor TreeEditor reference and delegates to `showEditModeAction()`
  or `showViewModeAction()`.
- `showEditModeAction()` — opens `_editMode` through `_editMode.open()`.
- `showViewModeAction()` — opens `_viewMode` through `_viewMode.open()`.

## 4. State Ownership

- Owns the active visual sub-state via `openedChild`.
- Does not own or cache the editor mode; explicit synchronization reads it from
  the stored `_editor` reference only when the editor mode transition has
  already occurred.

## 5. Child Interaction Rules

- Two children: EditToggleBtnViewModeState (`_viewMode`) and EditToggleBtnEditModeState (`_editMode`).
- `_viewMode` is the default active child. During initial child materialization, assign it as the active child without firing child lifecycle hooks.
- On explicit synchronization: choose `_editMode` when `isEditMode` is true,
  otherwise `_viewMode`; call `target.open()` so the target child runs its own
  opening contract before delegating as `parent.openChild(this)` to change
  `openedChild`.
- The base switchable mechanism mounts and unmounts the active child's view in this node's content area.
- Child state nodes own their low-level content subscriptions; EditToggleBtn only switches which child view is mounted.

## 6. Lifecycle

1. Constructor: captures `_editor = this.findUpByType(TreeEditorNode)`, creates the content boundary with `setContent(...)`, then creates both child state nodes.
2. `buildChildren()`: creates both child state nodes and assigns `_viewMode` as the initial active child via `setInitialChild(...)`.
3. `syncActionForCurrentEditorMode()` calls the selected child's `open()` if
   the visual action state must follow a completed editor mode transition. The
   child `open()` path delegates as `parent.openChild(this)` and triggers the
   switchable lifecycle.

## 7. Side Effects

- Explicit action-state synchronization changes the mounted child view and
  triggers child lifecycle hooks (`onClose()` on the outgoing child, `onOpen()`
  on the incoming child).

## 8. Constraints and Invariants

- Must not render the concrete action control itself.
- Must not access the content's platform primitive (`el`) directly.
- Must not perform manual child mount/unmount inside EditToggleBtn itself.
- Must not handle low-level activation events directly.
- Must not cache editor mode as a local boolean.
- Must not switch action states from `refresh()`.
- Initial default-child assignment must not call child `onOpen()` because the surrounding tree may still be materializing.
- `openedChild` must match the current editor mode after explicit
  action-state synchronization completes.

## 9. Non-Goals

- Does not own editor mode.
- Does not call `toggleEditMode()` itself.
- Does not apply platform visual mode markers to the editor root.
- Does not trigger tree refresh.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `edit-toggle-btn`.
- Extends `SwitchableNode`.
- Ancestor lookup: `this._editor = this.findUpByType(TreeEditorNode)` captured in constructor.
- Constructor materialization: `this.setContent(new EditToggleBtnContent(this))`.
- `syncActionForCurrentEditorMode()`: `if (this._editor.isEditMode) { this.showEditModeAction(); } else { this.showViewModeAction(); }`
- `showEditModeAction()`: `this._editMode.open();`
- `showViewModeAction()`: `this._viewMode.open();`

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/edit_toggle_btn.top`
- Public node class: `EditToggleBtnNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditToggleBtnContentAccess
  - Content-to-controller: EditToggleBtnControllerAccess empty zero-contract interface implemented by the owning node/controller
- Companion artifact stems: none
