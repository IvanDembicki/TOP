---
sourcePath: src/presentation/presentation.top
---

# Presentation

## 1. Node Identity and Role

Presentation is a target-optional presentation branch. It owns/describes the platform-neutral style/theme model derived from `top/presentation` source artifacts. Depending on target policy, it may be materialized as runtime nodes or compiled into target presentation artifacts.

## 2. Responsibility

- Own or describe presentation state and theme selection through child nodes.
- When runtime-materialized, expose typed presentation access to other runtime branches through an application-level connector.
- Coordinate source presentation artifacts with generated target presentation output.

## 3. Inputs and Events

- Theme change request from an application-level connector, user-facing theme control, or target presentation boundary.
- Style lookup requests from application nodes through typed presentation access or target presentation boundary.

## 4. State Ownership

When runtime-materialized, Presentation owns active theme state and interpreted presentation models. In target-compiled mode, the target presentation boundary owns equivalent generated state or lookup artifacts. Application feature nodes do not own or parse source presentation artifacts.

## 5. Child Interaction Rules

- When runtime-materialized, has `ThemeHolder` as the state owner for active theme.
- When runtime-materialized, has `TreeEditorPresentation` as the provider for TreeEditor style roles.
- External branches must not traverse into Presentation internals directly; they use a typed connector or target presentation boundary supplied by the application/root composition.

## 6. Lifecycle

1. Constructor creates content/model boundary if the target materializes Presentation as runtime nodes.
2. Builds child presentation providers when the target uses runtime presentation nodes.
3. Exposes connector methods after children are available, or lets the target presentation boundary expose equivalent lookup methods.

## 7. Side Effects

May notify subscribers when the active theme changes in runtime-materialized targets. Does not mutate feature node content directly.

## 8. Constraints and Invariants

- Must follow normal TOP controller/content/contract rules.
- Must expose the interpreted TOP presentation model as the canonical internal model.
- May materialize target implementation output from the TOP presentation model.
- Feature nodes obtain styles through typed presentation contracts or target presentation boundary, not by reading `top/presentation` files directly.

## 9. Non-Goals

- Does not own TreeEditor behavior.
- Does not replace node-specific content boundaries.

## 10. Platform Implementation Notes

- Generated target output is derived from the TOP presentation model.
- Each target independently decides whether presentation is runtime-materialized or compiled into target presentation artifacts.

## 11. Expected Materialization

- Primary artifact stem: `src/presentation/presentation.top`
- Public node class: `PresentationNode`
- Base class / base role: target-optional presentation branch node
- Materialization policy: target-optional-runtime
- Internal contracts:
  - Controller-to-content: not applicable (no separate content boundary)
  - Content-to-controller: not applicable (no separate content boundary)
- Companion artifact stems: none
