---
sourcePath: src/toolbar/build_info.top
---

# BuildInfo

## 1. Node Identity and Role

BuildInfo is an informational leaf node in the editor toolbar. It renders the build timestamp and has no interaction behavior.

## 2. Responsibility

- Create and own a small visual label for build information.
- Display the current build timestamp provided by the platform build constant.

## 3. Inputs and Events

None.

## 4. State Ownership

Owns no runtime state. The displayed value is initialized from `__BUILD_TIME__` when the content boundary is constructed.

## 5. Child Interaction Rules

No children.

## 6. Lifecycle

1. Constructor: creates `BuildInfoContent` and installs it through `setContent(...)`.
2. `BuildInfoContent` creates the platform visual content for the build info label.
3. `refresh()` does nothing.

## 7. Side Effects

None beyond rendering the build timestamp text into its own content.

## 8. Constraints and Invariants

- Must remain a leaf node.
- Must not handle user interaction.
- Must not own or change editor mode.
- Must not trigger tree refresh.

## 9. Non-Goals

- Does not display application data.
- Does not participate in mode switching.
- Does not communicate with other toolbar nodes.

## 10. Platform Implementation Notes

- Visual element: `span` with CSS class `build-info`.
- Text content format: `build: ` plus `__BUILD_TIME__`.
- Extends `DomNode`.
- Content extends `DomContent`.
- Constructor materialization: `this.setContent(new BuildInfoContent(new BuildInfoControllerAccessZero()))`.

## 11. Expected Materialization

- Primary artifact stem: `src/toolbar/build_info.top`
- Public node class: `BuildInfoNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: BuildInfoContentAccess
  - Content-to-controller: BuildInfoControllerAccess with zero-contract implementation BuildInfoControllerAccessZero
- Companion artifact stems: none