---
sourcePath: src/presentation/theme_holder.top
---

# ThemeHolder

## 1. Node Identity and Role

ThemeHolder is the target-optional switchable state holder for active presentation theme.

## 2. Responsibility

- Own which theme child is active.
- Expose the active platform-neutral theme model to runtime-materialized Presentation.
- Switch between theme states without storing duplicate boolean theme flags.

## 3. Inputs and Events

- `switchToLight()` request.
- `switchToDark()` request.
- Active theme lookup from runtime-materialized Presentation or target presentation boundary.

## 4. State Ownership

The active theme is represented by the active child, not by a separate enum or boolean.

## 5. Child Interaction Rules

- First child: `LightTheme`, default active child.
- Second child: `DarkTheme`.
- Theme switching goes through the switchable child mechanism.

## 6. Lifecycle

Initial child assignment must not fire active-child lifecycle hooks. Explicit switches may fire them.

## 7. Side Effects

May notify runtime-materialized Presentation that active theme changed.

## 8. Constraints and Invariants

- Must not parse source presentation files.
- Must not know feature-node internals.

## 9. Non-Goals

- Does not apply styles to TreeEditor directly.

## 10. Platform Implementation Notes

Targets may represent active theme using their own generated presentation implementation.

## 11. Expected Materialization

- Primary artifact stem: `src/presentation/theme_holder.top`
- Public node class: `ThemeHolderNode`
- Base class / base role: switchable presentation state holder
- Materialization policy: target-optional-runtime
- Internal contracts:
  - Controller-to-content: not applicable (no separate content boundary)
  - Content-to-controller: not applicable (no separate content boundary)
- Companion artifact stems: none
