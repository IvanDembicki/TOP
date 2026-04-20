# Example: EditToggleBtn — End-to-End

Source: Tree Editor project (current TypeScript/DOM materialization).
Validated against: current TOP skill rules.

This example is derived from the node spec and implementation prompts. The code is a target-specific artifact; the architecture lives in the spec and prompts.

---

## What this example demonstrates

- Switchable state holder with two visual child states
- Controller / Content split with named access contracts
- Parent-owned child view placement through the switchable mechanism
- Content-local low-level activation subscriptions
- Full pipeline: `spec → prompt → code`

---

## Tree structure

```text
EditToggleBtn                         ← switchable holder, owns openedChild
  ├── EditToggleBtnViewModeState      ← default state, "Edit mode" action
  └── EditToggleBtnEditModeState      ← active in edit mode, "View mode" action
```

---

## Pipeline

| Step | Artifact | Location |
|---|---|---|
| 1. Spec | Node definition in tree | `spec.json` |
| 2. Prompt | Implementation intent | `prompts/EditToggleBtn.prompt.md` |
| 3. Code | Target artifact | `code/edit_toggle_btn.top.*` |

Each child node has its own prompt and code file. File extensions are target-specific; the canonical artifact stem is `.top.*`.

---

## Spec → Prompt → Code mapping

| spec field / prompt section | Code responsibility |
|---|---|
| `spec.type = "EditToggleBtn"` | class name `EditToggleBtnNode` |
| `spec.props.contentType = "view"` | content exposes an opaque view handle via `getView()` |
| prompt §1 — Role: switchable holder | class extends `SwitchableNode` |
| prompt §4 — State ownership via `openedChild` | active child is stored in `openedChild` |
| prompt §3 — `refresh()` reads `isEditMode` | `findUpByType(TreeEditorNode).isEditMode` |
| prompt §5 — parent-owned placement | `openChild(target)` mounts the active child view |
| prompt §6 — initial child without lifecycle hooks | `setInitialChild(this._viewMode)` |
| prompt §8 — must not cache editor mode | no local boolean for mode state |

---

## Regeneration guarantee

This node can be regenerated from `spec.json` + `prompts/EditToggleBtn.prompt.md`.

```text
delete code/edit_toggle_btn.top.*
→ regenerate from spec + prompt
→ the node must be behaviorally equivalent on the selected target
```

Preserved across regeneration:
- holder owns `openedChild`, not editor mode
- `refresh()` reads mode from an ancestor public contract
- child placement is driven by the switchable mechanism
- the concrete action control belongs to child state nodes
- low-level activation subscriptions stay inside content boundaries

Target-specific details are declared in prompt §10 and may differ across platforms.

---

## Boundary validation

### Holder content is only a mount area

`EditToggleBtnContent` creates the target-specific holder view and exposes it through `IContentAccess`. It does not decide editor behavior.

### Child content owns low-level activation

`EditToggleBtnViewModeStateContent` and `EditToggleBtnEditModeStateContent` own their platform activation subscriptions. In the current DOM target this is a `click` listener.

### Semantic requests cross through controller access

Content forwards activation as a semantic request to its controller access contract. The node layer then calls `TreeEditor.toggleEditMode()`.

### Children don't mount themselves

State children expose their view. The parent switchable mechanism decides which child view is mounted.

---

## Locality

Required to understand this node:
- its own `spec.json` entry
- its own prompt
- the two child state prompts
- the public `TreeEditorNode.isEditMode` / `TreeEditorNode.toggleEditMode()` contract

Not required:
- knowledge of `EditorModeHolder` internals
- knowledge of the full application tree
- knowledge of sibling toolbar implementation details

---

## Failure case

```ts
// Violation: content reads editor mode and makes an architectural decision.
class EditToggleBtnContent extends DomContent {
  mount(view: HTMLElement | null): void {
    if (this.controller.isEditMode()) {
      // content has crossed the controller boundary
    }
    super.mount(view);
  }
}
```

If logic affects editor behavior, it belongs to the node/controller side, not to content.

---

## Key architectural decisions

### Why the holder does not own the concrete action control

EditToggleBtn is the switching mechanism. Each child state owns the action representation for that state.

### Why content is only a view boundary

Content handles target primitives and low-level subscriptions. Architectural decisions stay in node/controller code.

### Why upward lookup is acceptable here

`findUpByType(TreeEditorNode)` is acceptable because this branch has an architectural guarantee that a `TreeEditor` ancestor exists. The accessed members are public TreeEditor contract members named in the prompt.

For untyped library insertion where that ancestor is not guaranteed, the node must use an explicit connector contract instead of assuming a concrete ancestor.