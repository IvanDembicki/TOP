# Golden Scenarios

## 1. analysis-only audit
Task: verify architecture without generation.
Expected mode: `analysis-only`

## 2. refactor-to-top without generation
Task: restructure the model and boundaries without materialized code.
Expected mode: `modeling-refactor`

## 3. full generation pipeline
Task: generate an implementation artifact from an approved model.
Expected mode: `generation-pipeline`

## 4. Tier 1 leaf change
Task: local leaf-level change with no impact on ownership or boundaries.

Two valid options:
- `generation-pipeline` — if an actual implementation artifact is needed
- `analysis-only` — if only a review / audit is needed without generation

Expected rule:
- `Mode` determines the type of work
- `Tier = 1` determines only the depth of the architectural change

This scenario demonstrates that `Mode` and `Tier` are independent axes.

## 5. blocked ambiguity case
Task: ambiguity affects ownership or lifecycle.
Expected result: pipeline stop until explicit resolution

## 6. Hidden switchable — TreeItemRow

Task: refactor a node that has two behavioral modes (view / edit).

**Tier:** 2 (subtree of TreeItemRow is affected)
**Mode:** `generation-pipeline`

**Diagnosis:**
`TreeItemRowNode` reads `isEditMode` in `refresh()` and hides/shows `DragHandle`, `AddBtn`, `DeleteBtn`, manages `draggable` and drag listeners. This is a `core_violation`: hidden behavior ownership, hidden lifecycle.

Classification per `rules/pattern-recognition.md` — Pattern #1: Hidden switchable.

**Modeling result:**
`TreeItemRowNode` becomes a switchable holder. Two state nodes carry separate responsibilities:
- `TreeItemRowViewStateNode` — toggle and label only; drag is architecturally absent
- `TreeItemRowEditStateNode` — drag handle, add, delete, draggable, drag listeners

Neither state node accesses `isEditMode`.
Switching happens via `onBranchOpen()` from an external mode holder.
