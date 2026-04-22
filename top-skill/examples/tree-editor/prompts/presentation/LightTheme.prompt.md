---
sourcePath: src/presentation/light_theme.top
---

# LightTheme

## 1. Node Identity and Role

LightTheme is the target-optional light presentation state.

## 2. Responsibility

- Provide platform-neutral theme values for the light theme.
- Expose the light theme model to ThemeHolder.

## 3. Inputs and Events

Active theme lookup.

## 4. State Ownership

Owns light-theme values only.

## 5. Child Interaction Rules

Has no child nodes.

## 6. Lifecycle

No special lifecycle behavior is required.

## 7. Side Effects

None.

## 8. Constraints and Invariants

- Must not apply styles directly to feature nodes.
- Must expose TOP presentation values as the canonical model.

## 9. Non-Goals

Does not switch themes.

## 10. Platform Implementation Notes

May materialize to target presentation output.

## 11. Expected Materialization

- Primary artifact stem: `src/presentation/light_theme.top`
- Public node class: `LightThemeNode`
- Base class / base role: presentation state node
- Materialization policy: target-optional-runtime
- Internal contracts:
  - Controller-to-content: not applicable (no separate content boundary)
  - Content-to-controller: not applicable (no separate content boundary)
- Companion artifact stems: none
