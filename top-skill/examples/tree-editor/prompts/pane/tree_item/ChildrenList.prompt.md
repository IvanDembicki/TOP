---
sourcePath: src/pane/tree_item/children_list.top
---

# ChildrenList

## 1. Node Identity and Role

ChildrenList is a mutable collection node holding TreeItem child instances for
the currently expanded TreeItem. It attaches child TreeItems to the tree and
exposes their records through a context contract.

## 2. Responsibility

- Pull child records from the owning TreeItem through the parent/context chain.
- Maintain an ordered set of child TreeItem controllers.
- Create child TreeItems from `lib:pane.TreeItem` with only this ChildrenList as
  parent/context.
- Maintain a private child-to-record association map.
- Expose `getRecordForTreeItem(child)` to direct TreeItem children.
- Support architecturally allowed add/remove/reorder domain methods for child
  records.
- Destroy/recreate presentation content on collapse/expand while retaining
  logical child controllers when policy allows.

## 3. Inputs and Events

- `refresh()` - pulls current child records, reconciles the child controller set,
  updates child-to-record associations, places direct child opaque handles, and
  requests child refresh.
- `syncEditorModeState()` - forwards explicit editor-mode structural
  synchronization to each currently owned child TreeItem.
- `addChildRecord(record)` - data-controller/domain method called by the owning
  TreeItem when add-child is allowed.
- `removeChild(child)` - removes an existing child and its associated record.
- `moveChild(child, targetIndex)` - reorders an existing child and its associated
  record.
- `activate()` / `deactivate()` - content lifecycle methods for expanded/collapsed
  materialization.

## 4. State Ownership

Owns the ordered child controller set and child-to-record associations for this
collection. The source child records are obtained from the owning TreeItem.

## 5. Child Interaction Rules

- Child TreeItem constructors receive only this ChildrenList as parent/context.
- ChildrenList never calls any post-construction data setter on a child.
- Child TreeItems pull their record through `getRecordForTreeItem(child)`.
- Child opaque handles are placed by ChildrenList only as direct child handles.

## 6. Lifecycle

1. Constructor creates content if the collection is active.
2. `refresh()` reconciles child controllers against current child records.
3. `syncEditorModeState()` forwards to current child TreeItems.
4. `deactivate()` destroys presentation content only; logical children and
   associations remain according to the declared retention policy.
5. `activate()` recreates content and places existing direct child opaque
   handles.

## 7. Side Effects

- Child controller creation/removal/reorder inside this collection.
- Presentation content destruction/recreation on collapse/expand.

## 8. Constraints and Invariants

- No child data is injected through constructors, props, config, or setters.
- `length` reflects current logical child controller count.
- Presentation content is not the data source.

## 9. Non-Goals

- Does not own expand/collapse state.
- Does not apply indentation or labels.

## 10. Platform Implementation Notes

- Visual primitive: static children list container.
- Parent-owned placement may mount each direct child opaque handle.
- `activate()` and `deactivate()` are lifecycle/materialization operations, not
  presentation state pushes.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/children_list.top`
- Public node class: `ChildrenListNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `ChildrenListContentAccess`
  - Content-to-controller: `ChildrenListControllerAccess`
- Companion artifact stems: none
