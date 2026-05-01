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

## Rule 7 — Controller is the sole derivation boundary for integration data

Integration-layer types — API response shapes, SDK types, database record types,
and any other types that originate outside the node's own domain — must not appear
in content.

The controller is responsible for receiving integration data and deriving a
typed view-model from it. Content receives only the derived view-model.
Content must have no structural dependency on integration-layer types:
no structural reference, no implicit shape compatibility.

The view-model is the only integration artifact that crosses the
controller/content boundary.

## Rule 8 — Secondary surface belongs entirely within the branch that owns it

A secondary surface — an overlay, modal, popup, or equivalent transient layer
that belongs to a specific branch — must be implemented and owned entirely within
that branch's content.

The controller owns the activation policy: it decides when and whether the
secondary surface is shown, and receives back any semantic result through
`IControllerAccess`. Content executes the show/hide command through `IContentAccess`
and forwards results without interpreting them.

A secondary surface must not be extracted into a sibling or ancestor controller
simply because it visually overlaps other branches at render time.
Visual overlap does not determine ownership. The logical source of the secondary
surface — the branch that holds the data, triggers the action, and processes the
result — is the owner.
