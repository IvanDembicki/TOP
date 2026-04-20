# Platform-Neutral Semantic UI Layer

## Purpose

The Platform-Neutral Semantic UI Layer is the portable meaning layer between the TOP structural model and any concrete target implementation.

It prevents platform artifacts from becoming source truth.

## Three-layer model

TOP generation uses three distinct layers:

1. **Layer A — TOP Structural Truth**
   - nodes
   - controllers
   - content
   - states
   - relationships
   - lifecycle
   - invariants

2. **Layer B — Platform-Neutral Semantic UI Layer**
   - element purpose and role
   - user intent
   - system intent
   - interaction intent
   - state model
   - feedback intent
   - layout intent
   - constraints
   - accessibility semantics

3. **Layer C — Target Adaptation Layer**
   - target-native UI primitives
   - target-native interaction mapping
   - target layout decisions
   - target constraints
   - explicit adaptation decisions

Layer A and Layer B are source truth.
Layer C is derived, target-specific, temporary, and replaceable.

## Semantic UI source of truth

Semantic UI descriptions must describe what the system means and does, not how a previous target rendered it.

Allowed semantic categories are open, but must belong to meaning:

- structure
- interaction
- feedback
- layout intent
- accessibility
- state representation
- constraint semantics

A semantic term may be added only if:

- it represents platform-independent meaning;
- it can be mapped to more than one target;
- it does not name a native primitive, framework type, CSS property, platform event API, or target-specific layout mechanism.

## Required semantic fields

For each semantic UI element or content role, capture what is relevant:

- `semantic_role`
- `user_intent`
- `system_intent`
- `interaction_intent`
- `state_model`
- `feedback_intent`
- `layout_intent`
- `constraints`
- `accessibility_semantics`

Not every element needs every field, but omitted fields must be genuinely not applicable, not merely unknown.

## Constraint classification

Every constraint extracted from a platform-biased source must be classified:

- `essential` — required to preserve meaning;
- `adaptive` — must be preserved in intent but may change implementation form;
- `optional` — may be omitted if target conventions make it unnecessary;
- `source-artifact` — belongs only to the source platform and must be removed from Layer B.

## Platform artifact rule

Layer B must not contain:

- DOM elements or HTML tags;
- CSS selectors, classes, properties, or layout primitives;
- Flutter widgets or widget tree assumptions;
- UIKit, Android, SwiftUI, Jetpack Compose, React, Vue, or framework class names;
- native event names when the event name is platform-specific rather than semantic;
- target file names, APIs, framework lifecycle hooks, or implementation classes.

If such material is present in an input prompt or spec, it must be treated as source evidence for the Semantic Interpreter, not as semantic truth.

## Examples of semantic normalization

These examples are illustrative, not a fixed vocabulary:

| Source-platform artifact | Semantic interpretation |
|---|---|
| button | action trigger |
| edit button | edit-mode action trigger |
| div container | content container / layout group |
| hover highlight | target-indication feedback |
| CSS class `dragging` | drag-in-progress feedback |
| right-click menu | contextual action access |
| long press | contextual action access on touch-first targets |

## Canonical rule

If platform detail conflicts with semantic intent, preserve intent and discard or adapt the platform detail.