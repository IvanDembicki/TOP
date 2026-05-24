---
sourcePath: src/pane/root_item_holder.top
---

# RootItemHolder

## 1. Node Identity and Role

RootItemHolder is a mutable container holding exactly one root TreeItem instance.
It attaches the root TreeItem to the tree and exposes the root record through a
context contract.

## 2. Responsibility

- Maintain exactly one root TreeItem child when a root record exists.
- Pull the root record from EditorPane through `getRootRecord()`.
- Create the root TreeItem from the project Library with this node as parent.
- Record the child-to-record association internally before refresh.
- Expose `getRecordForTreeItem(child)` to the direct root TreeItem child.

## 3. Inputs and Events

- `refresh()` - pulls the current root record. If the record identity changed,
  replaces the existing root child and creates a new TreeItem attached only to
  this holder as parent/context.
- `syncEditorModeState()` - if the root TreeItem exists, forwards explicit
  editor-mode structural synchronization to that child.
- `getRecordForTreeItem(child)` - returns the record associated with the root
  child. This is a pull-through contract, not constructor injection.
- `requestRefresh()` - forwards a refresh request to EditorPane/TreeEditor.

## 4. State Ownership

Owns the root-child association map and the single root TreeItem child reference.
It does not own the source root record itself.

## 5. Child Interaction Rules

- Root TreeItem constructor receives only RootItemHolder as parent/context.
- No post-construction data setter exists.
- RootItemHolder may replace its child when the root record identity changes.
- RootItemHolder places the root child's opaque handle through parent-owned
  materialization.

## 6. Lifecycle

1. Constructor creates the holder content boundary.
2. Constructor creates no root item until a root record is available.
3. `refresh()` pulls the root record, creates/replaces the root child if needed,
   records the child-to-record association, places the child opaque handle, and
   requests the child refresh.
4. `syncEditorModeState()` forwards to the current root child only when that
   child exists; missing root child is a data-empty condition, not mode state.

## 7. Side Effects

- Root child replacement when root record identity changes.

## 8. Constraints and Invariants

- Holds at most one root TreeItem.
- Does not push data into the root TreeItem.
- Does not manage expand/collapse or edit mode logic.

## 9. Non-Goals

- Does not manage recursive child trees.
- Does not apply indentation or labels.

## 10. Platform Implementation Notes

- Visual primitive: static root item holder container.
- Child removal/rematerialization uses parent-owned lifecycle/removal mechanics.
- Child handle placement is parent-owned placement of a direct child opaque
  handle.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/root_item_holder.top`
- Public node class: `RootItemHolderNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `RootItemHolderContentAccess`
  - Content-to-controller: `RootItemHolderControllerAccess`
- Companion artifact stems: none
