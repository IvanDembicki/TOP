---
sourcePath: src/toolbar/editor_mode_holder.top
---

# EditorModeHolder

## 1. Node Identity and Role

EditorModeHolder is the exclusive owner of the editor's view/edit mode state. It is a logical switchable node with two children: ViewModeState (first, default) and EditModeState (last). The active child determines the current mode.

## 2. Responsibility

- Hold the current editor mode as the identity of the active child (`openedChild`).
- Expose `toggle()` to switch between view mode and edit mode.
- Use the base switchable lifecycle when the active child changes.

## 3. Inputs and Events

- `toggle()` — called by TreeEditor as part of its public coordination path. If the current active child is `_viewModeState`, calls `_editModeState.open()`; otherwise calls `_viewModeState.open()`.

## 4. State Ownership

- Is the exclusive owner of the view/edit mode state.
- State is represented solely by which child is `openedChild`.
- No boolean mode flags are stored inside EditorModeHolder.

## 5. Child Interaction Rules

- Two children: ViewModeState (`_viewModeState`) and EditModeState (`_editModeState`).
- ViewModeState is the default active child. During initial child materialization, set the initial active child without calling `openChild()` and without firing child lifecycle hooks.
- On `toggle()`: computes the target child and calls `target.open()`, allowing
  the target state node's opening protocol to run before it delegates as
  `parent.openChild(this)`.
- The child `open()` path delegates to the base switchable commit path through
  `parent.openChild(this)`, which calls `onClose()` on the outgoing child and
  `onOpen()` on the incoming child.
- State children are logical nodes with no view; mount/unmount calls are no-ops for them.

## 6. Lifecycle

1. Constructor: no platform content is created.
2. `buildChildren()`: creates ViewModeState and EditModeState as children and assigns ViewModeState as the initial active child without calling `openChild()`.
3. Initial activation must not call `ViewModeState.onOpen()` because the parent TreeEditor may still be materializing its direct children.
4. Each call to `toggle()` switches the active child via `target.open()`.
5. The incoming state node's `onOpen()` notifies TreeEditor via
   `requestEditMode(value)`; TreeEditor coordinates dependent structural sync
   and then triggers `refreshAll()`.

## 7. Side Effects

None directly. Child state nodes notify TreeEditor from their `onOpen()` hooks;
TreeEditor owns dependent structural synchronization and full tree refresh.

## 8. Constraints and Invariants

- Must not apply platform visual mode markers or call TreeEditor mode update methods directly.
- Must not store mode state in any variable other than `openedChild`.
- Every explicit mode switch must request opening on the target child through
  `target.open()`.
- Initial default-child assignment is not an explicit mode switch and must not fire `onOpen()` / `onClose()`.
- Child state nodes are the only nodes that perform mode-activation side effects.

## 9. Non-Goals

- Does not read or write tree data.
- Does not apply any visual changes directly.
- Does not have visible content.

## 10. Platform Implementation Notes

- Extends `SwitchableNode`. No content, no DOM element.
- Children (ViewModeStateNode, EditModeStateNode) are logical nodes with no view.
- Located as a direct child of TreeEditor.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/editor_mode_holder.top`
- Public node class: `EditorModeHolderNode`
- Base class / base role: `SwitchableNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: EditorModeHolderContentAccess
  - Content-to-controller: EditorModeHolderControllerAccess empty zero-contract interface implemented by the owning node/controller
- Companion artifact stems: none
