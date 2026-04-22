---
sourcePath: src/presentation/tree_editor_presentation.top
---

# TreeEditorPresentation

## 1. Node Identity and Role

TreeEditorPresentation is the target-optional presentation provider for TreeEditor-related style roles.

## 2. Responsibility

- Interpret `presentation/tree-editor.presentation.json` as the canonical platform-neutral presentation source.
- Expose platform-neutral style roles for TreeEditor nodes.
- Provide presentation materialization helpers for the generated target when required.

## 3. Inputs and Events

- Style lookup by semantic role.
- Active theme model from ThemeHolder/Presentation when runtime-materialized, or from the target presentation boundary in target-compiled mode.

## 4. State Ownership

Owns the interpreted TreeEditor presentation model, not TreeEditor behavior.

## 5. Child Interaction Rules

Has no required child nodes.

## 6. Lifecycle

Loads or receives interpreted presentation source during runtime construction or target presentation materialization.

## 7. Side Effects

None directly. May provide values consumed by feature nodes through Presentation connector methods or target presentation boundary methods.

## 8. Constraints and Invariants

- Must not require feature nodes to parse presentation source artifacts.
- Must expose semantic style roles, not raw selector strings as the only contract.
- Target materialization returns presentation data appropriate for the generated target.

## 9. Non-Goals

Does not own theme switching.

## 10. Platform Implementation Notes

Generated presentation output is produced from the platform-neutral presentation source artifact and belongs to the target project, not to `top/presentation`.

## 11. Expected Materialization

- Primary artifact stem: `src/presentation/tree_editor_presentation.top`
- Public node class: `TreeEditorPresentationNode`
- Base class / base role: presentation provider node
- Materialization policy: target-optional-runtime
- Internal contracts:
  - Controller-to-content: not applicable (no separate content boundary)
  - Content-to-controller: not applicable (no separate content boundary)
- Companion artifact stems: none
