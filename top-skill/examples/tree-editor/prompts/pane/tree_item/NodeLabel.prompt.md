---
sourcePath: src/pane/tree_item/node_label.top
---

# NodeLabel

## 1. Node Identity and Role

NodeLabel is a static label part inside a tree item row.

## 2. Responsibility

- Materialize the label structure.
- Pull the already-resolved label text from the owning controller access
  contract during refresh/materialization.
- Own no decision logic and no label derivation.

## 3. Inputs and Events

- `getLabelText()` - returns the already-resolved label text by delegating through
  the parent/context chain.

No user interaction events.

## 4. State Ownership

Owns no state. The label text is owned by the TreeItem controller that resolves
the primitive value from its attached data context.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

1. Constructor receives only parent/context.
2. Constructor creates static label content.
3. Refresh/materialization pulls `getLabelText()` through controller access and
   applies the primitive text value to the static label structure.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- No text setter or equivalent presentation mutation method.
- No constructor text, data, config, callbacks, props, stores, or services.
- Locally implemented content contains no conditional selection logic.

## 9. Non-Goals

- Does not support inline editing.
- Does not decide visibility, style, or label text.

## 10. Platform Implementation Notes

- Visual primitive: static label element.
- Text is an already-resolved primitive pulled through `NodeLabelControllerAccess`.
- Content-local mechanics may apply the pulled primitive value to the static
  materialization, but must not derive it.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/node_label.top`
- Public node class: `NodeLabelNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `NodeLabelContentAccess`
  - Content-to-controller: `NodeLabelControllerAccess`
- Companion artifact stems: none
