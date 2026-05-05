---
sourcePath: src/toolbar/build_info.top
---

# BuildInfo

## 1. Node Identity and Role

BuildInfo is an informational leaf node in the editor toolbar. It materializes a
static build-information label and has no interaction behavior.

## 2. Responsibility

- Own the build-information label structure.
- Resolve the final build-information text in the controller.
- Expose the already-resolved build-information text through controller access
  for locally implemented content to apply during materialization/refresh.

## 3. Inputs and Events

- `getBuildInfoText()` - returns the final already-resolved display text.

No user interaction events.

## 4. State Ownership

Owns no runtime state. The build metadata source is provided by the declared
build/asset adapter outside locally implemented content. The controller resolves
the final primitive text value.

## 5. Child Interaction Rules

No children.

## 6. Lifecycle

1. Constructor creates `BuildInfoContent` and installs it through
   `IContentAccess`.
2. `BuildInfoContent` creates static label content.
3. Refresh/materialization pulls `getBuildInfoText()` through
   `BuildInfoControllerAccess` and applies the already-resolved primitive text
   value.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must remain a leaf node.
- Must not handle user interaction.
- Must not own or change editor mode.
- Must not trigger tree refresh.
- Locally implemented content must not format, concatenate, or derive the build
  text from constants, runtime values, environment values, or platform values.

## 9. Non-Goals

- Does not display application data.
- Does not participate in mode switching.
- Does not communicate with other toolbar nodes.

## 10. Platform Implementation Notes

- Visual primitive: static build-information label element.
- The controller may resolve the final text from target-provided build metadata.
  Content only applies the returned `getBuildInfoText()` value.
- Constructor materialization: `this.setContent(new BuildInfoContent(this))`.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/build_info.top`
- Public node class: `BuildInfoNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `BuildInfoContentAccess`
  - Content-to-controller: `BuildInfoControllerAccess`
- Companion artifact stems: none
