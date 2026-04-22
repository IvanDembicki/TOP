# History and Undo

---

## State change history in TOP

In TOP, the current system state is determined by the configuration of the instance tree.
This property makes it possible to implement history and undo as management of
a sequence of tree configurations.

---

## What is recorded in history

A history entry consists of changes to the tree configuration:

- **Switching**: changing `openedChild` on a switchable node.
- **Structural changes**: adding or removing node instances
  in mutable nodes.
- **Data changes**: changing content in data nodes
  (if the system records such changes).

---

## History model

History is represented as a stack of operations:

```
[op_1, op_2, op_3, ..., op_N]  ← current state
```

Each operation describes an atomic change to the tree configuration.

**Undo** — reverting the last operation: returning to the configuration before `op_N`.
**Redo** — re-applying a reverted operation.

---

## Operation record formats

An operation can be recorded in one of the following formats:

**Forward/backward (direct and inverse operation)**:
```json
{
  "type": "switch",
  "nodeId": "TabPanel",
  "from": "Tab1",
  "to": "Tab2"
}
```

Undo applies the inverse operation: `from` and `to` are swapped.

**Snapshot**:
A full or partial copy of the tree configuration before and after the change.
On undo, the previous snapshot is restored.

---

## Transactions (compound operations)

Multiple changes can be grouped into a transaction — a single history unit.

Example: moving a node in the tree may include:
1. Removing the node from its source parent.
2. Adding the node to its target parent.

As a transaction, this is a single history entry.
Undo reverts both operations as a single unit.

---

## What is NOT recorded

- Intermediate states during transition animations.
- Technical calls to `onBranchOpen()` / `onBranchClose()` — these are
  consequences of switching, not independent operations.
- Temporary states that are not part of the application logic.

---

## Relationship with the instance tree

History and undo operate at the instance tree level.
On undo, the instance tree configuration is reverted to the previous state,
which automatically triggers the corresponding lifecycle events:
`onBranchClose()`, `onBranchOpen()`, `onClose()`, `onOpen()`.
