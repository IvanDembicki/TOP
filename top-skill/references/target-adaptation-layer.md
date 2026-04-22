# Target Adaptation Layer

## Purpose

The Target Adaptation Layer converts the Platform-Neutral Semantic UI Layer into a target-specific implementation plan.

It is not source truth.
It is derived, temporary, target-specific, and replaceable.

## Input

Target adaptation requires:

- approved TOP structural truth;
- approved semantic UI layer;
- target platform and target constraints;
- target generation rules.

## Output

The adaptation output must describe:

- native interaction mapping;
- native layout decisions;
- native UI primitive choices;
- target-specific constraints;
- explicit adaptation decisions;
- target risks and validation checks.

## Adaptation decision record

For each semantic element, record one decision:

- `preserved` — semantic intent maps directly to a target-native mechanism;
- `adapted` — semantic intent is preserved with a target-specific form;
- `dropped` — source artifact or optional detail is intentionally removed, with reason.

Every `adapted` or `dropped` decision must include the reason.

## Rules

Target adaptation must:

- preserve semantic intent;
- reinterpret interactions according to the target's native model;
- choose target-native primitives;
- keep TOP ownership, lifecycle, content, and controller boundaries intact;
- keep adaptation decisions explicit and reviewable.

Target adaptation must not:

- copy source-platform behavior mechanically;
- introduce new business logic;
- change ownership, controller/content boundaries, or lifecycle semantics;
- push target primitives back into the semantic layer;
- treat generated target output as source truth.

## Interaction adaptation examples

These examples are illustrative, not a fixed mapping table:

| Semantic intent | Possible target adaptation |
|---|---|
| contextual action access | right-click on desktop, long press on touch, visible menu button where discoverability is required |
| target-indication feedback | hover state on pointer targets, pressed/focused state on touch or keyboard-first targets |
| drag reorder intent | pointer drag on desktop, long-press drag handle on touch if the platform expects it |
| activation intent | button, menu item, keyboard command, gesture, or platform-native action surface |

## Validation requirement

A target adaptation is invalid if it preserves target syntax while losing semantic intent, or if it preserves a source primitive that is not native to the target.