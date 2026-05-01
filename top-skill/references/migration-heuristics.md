# Migration Heuristics

Heuristics for identifying decomposition opportunities during TOP migration.

These are signals — observable patterns that suggest where a branch boundary may
belong. They are not architectural rules and must not be applied mechanically.
Every signal must be confirmed against lifecycle ownership and mutation authority
before a decomposition decision is made.

A heuristic that is not confirmed by ownership analysis is a false positive. Do
not decompose on a heuristic signal alone.

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

---

## How to use these heuristics

1. Identify which heuristics apply to the controller under analysis.
2. For each signal, confirm through ownership analysis: does the candidate
   sub-part own distinct lifecycle responsibilities, distinct mutation authority,
   or a distinct integration point?
3. If ownership analysis confirms the signal → the sub-part is a decomposition
   candidate.
4. If ownership analysis does not confirm the signal → the heuristic is a false
   positive for this case; do not decompose.
