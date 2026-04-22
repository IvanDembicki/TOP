# Node Model Definition

## Node State Switching

State switching is the replacement of the active child node inside a switcher node.
During switching, the currently active branch is deactivated and the new branch is activated.

Deactivation means the node stops participating in active interaction: it disables user event handling and any other mechanisms that belong to the active state.
Activation means the new node becomes the current source of behavior and presentation: it enables the necessary subscriptions and begins handling interaction.

At any point in time only one child node is active, and that node defines the current state of the system.

---

## Node as architectural unit

In TOP, a node is an architectural unit, not merely a serialized tree element.

A node should be describable through:

- role in the tree;
- ownership position;
- external control boundary;
- internal content boundary;
- allowed child composition;
- state and switching semantics when relevant;
- interaction and connector rules.

## Controller / Content split

When a node is modeled at the architectural level, it should preserve a strict
split between:

- `Controller` — the externally visible, contract-bearing side of the node;
- `Content` — the internal implementation side hidden behind that contract.

This split is not equivalent to MVC and should not be reduced to a mere naming
convention.
It expresses encapsulation at the level of TOP node semantics.

## Ownership discipline

A node is responsible for its subtree according to explicit parent-child rules.

The same ownership boundary governs view access: only the direct parent may call
`getView()` on a node. No ancestor above the parent, and no sibling, has the right
to access a node's view directly.
See `canon/architectural-invariants.md` — **View Access Invariant**.

This means:

- ownership should follow tree position;
- child participation should not bypass the parent boundary silently;
- hidden cross-links should be treated as architectural debt unless modeled
  canonically.

## State discipline

TOP should model state explicitly at the tree level whenever state affects
behavior, switching, visibility, lifecycle, or ownership.

This often involves:

- `state holder`;
- `state node`;
- opened/closed branch semantics;
- switching rules.

This does not imply that every low-level value becomes a separate node.
It means architecturally relevant state must not stay implicit.
