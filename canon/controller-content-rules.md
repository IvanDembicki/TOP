# Controller / Content Rules

## Rule 1 — External access goes through Controller

If a node exposes behavior, orchestration, or interaction to the outside,
that access should be modeled through `Controller`.

## Rule 2 — Content stays hidden behind the boundary

`Content` is implementation-side structure.
It must not be treated as a second public interface by convenience.

## Rule 3 — Do not flatten the split into naming only

The pair `Controller` / `Content` must not be reduced to decorative labels.
If the split is declared, it must correspond to a real architectural boundary.

## Rule 4 — Generation must preserve the split

When generating code, docs, or node prompts, the system must preserve:

- what belongs to controller responsibility;
- what belongs to content responsibility;
- what is public contract;
- what is hidden implementation.

## Rule 5 — Validation must check boundary leaks

A valid TOP review should explicitly look for:

- controller logic leaking into content assumptions;
- content details exposed as public contract;
- ownership violations caused by bypassing the controller boundary.

## Rule 6 — Content must not initiate interactions outside its controller

Content must not directly call, signal, or otherwise initiate communication
with any node, system, or external boundary other than its own controller.

All outward interaction from a content unit must be routed through
the controller boundary.

Content may subscribe/unsubscribe to low-level events of its own platform
primitive and perform analogous platform commands on its own implementation
material. This is execution, not ownership: content may forward a narrow event
to its controller, but the controller owns interpretation, state transitions,
lifecycle, structure, and orchestration.
