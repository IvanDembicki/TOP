# Migration Heuristics

Heuristics for identifying decomposition opportunities during TOP migration.

These are signals — observable patterns that suggest where a branch boundary may
belong. They are not architectural rules and must not be applied mechanically.
Every signal must be confirmed against lifecycle ownership and mutation authority
before a decomposition decision is made.

A heuristic that is not confirmed by ownership analysis is a false positive. Do
not decompose on a heuristic signal alone.

The inverse is also forbidden: do not keep a large legacy scope as one TOP node
without running the heuristic review. Migration means discovering and
externalizing hidden structure, not wrapping a legacy file or screen.

---

## H-1. Lifecycle responsibility count as decomposition signal

When a single controller accumulates multiple lifecycle concerns, each tied to a
distinct data domain or integration source, this is a signal that the controller
may be a decomposition candidate.

The signal is the independence of the concerns, not the count alone. Two concerns
are independent when:
- they subscribe to different data sources or integration endpoints;
- their initialization, cleanup, and recovery logic does not share state;
- one could be removed or replaced without affecting the other.

A controller with many lifecycle responsibilities that share data and state is not
a decomposition signal — it may be a legitimately complex node that should remain
a single branch.

---

## H-2. Async orchestration cluster as decomposition signal

When a group of async operations, external subscriptions, or coordination flows
within a controller are cohesive with each other but independent from the rest of
the controller's logic, this cluster is a decomposition candidate.

The cluster is a candidate for a separate child branch when:
- it has its own lifecycle (can be initialized, stopped, or reset independently);
- other parts of the controller depend only on results it produces, not on its
  internal state;
- extracting it would leave the root controller with cleaner cross-cutting
  coordination and no hidden coupling.

---

## H-3. Duplicated content primitives as pre-library signal

When structural content primitives — layout fragments, visual building blocks,
style constants — appear in multiple content files within the same branch, this
is a signal of a pre-library pattern.

This is not a rule violation in the current migration state. It is a signal that
a shared utility or library branch may be appropriate as the branch stabilizes.

Do not extract a library branch prematurely during migration. Record the signal;
evaluate it when the branch has stabilized and the shared primitives are confirmed
as stable and general.

## H-4. Giant controller access surface

A large `IControllerAccess`/target-equivalent surface is a decomposition smell.
It often means that one hub node is exposing the responsibilities of several
hidden child nodes.

Review for extraction when the surface contains:
- many unrelated display getters;
- many action methods from unrelated workflows;
- many modal/form/list responsibilities;
- many pending actions or pending mutations;
- many bridge/update callbacks from different integration sources.

The review must classify the hidden candidates before precheck can pass.

## H-5. PanelDisplayStyle cluster

Many `PanelDisplayStyle` or equivalent display-token methods in one node are a
signal of hidden state tree.

Confirm whether each section is a stable structural section. If a section has
its own lifecycle, action set, async process, modal/form validation flow,
permission-gated capability, or data ownership boundary, model it as a node or
state branch instead of a display-token method.

## H-6. Hook bridge cluster inside content

Multiple target-framework hooks, effect workflows, pending action execution,
mutation body construction, routing, alerts, or store writes inside locally
implemented content indicate possible content orchestration.

Classify the bridge as a connector, bridge component, black-box boundary, data
bridge node, or adapter residual. Do not let locally implemented content own the
workflow.

## H-7. Modal/form/list/helper candidates

Modals, forms, lists, list items, cards, rows, tiles, banners, selectors, status
panels, and action panels are candidate nodes or reusable library nodes until
classified.

Repeated structures should be evaluated horizontally for library extraction.
Keep a helper component only when it has no independent responsibility,
lifecycle, state, behavior, or reusable role, and when extraction would require a
wide props/config object or create a generic god-component.

---

## How to use these heuristics

1. Identify which heuristics apply to the controller under analysis.
2. For each signal, confirm through ownership analysis: does the candidate
   sub-part own distinct lifecycle responsibilities, distinct mutation authority,
   or a distinct integration point?
3. For migration, record the candidate classification even if the candidate is
   left local.
4. If ownership analysis confirms the signal → the sub-part is a decomposition
   candidate.
5. If ownership analysis does not confirm the signal → the heuristic is a false
   positive for this case; do not decompose.
