---
sourcePath: src/pane/tree_item/tree_item.top
---

# TreeItem

## 1. Node Identity and Role

TreeItem is the reusable library template node representing one item in the
tree. It attaches to either RootItemHolder or ChildrenList and pulls its record
through that parent/context contract.

## 2. Responsibility

- Pull the current item record from its owning parent/context.
- Derive already-resolved primitive values for its own presentation subtree:
  label text, depth/indent token, root token, child-count token, icon token,
  drag token, and drop-hint token.
- Own item-level drag/drop coordination and add/delete/toggle requests.
- Own two immutable structural children: TreeItemRow and ExpandCollapseHolder.
- Expose read methods used by descendant controllers, for example
  `getLabelText()`, `getIndentToken()`, `getIconToken()`, `canDrag()`,
  `canDelete()`, and `getChildRecords()`.

## 3. Inputs and Events

- `refresh()` - pulls the record through the parent/context contract and
  refreshes its child controllers. It does not receive a data argument.
- `requestToggle()` - called by NodeIcon controller after content reports toggle
  intent.
- `requestAddChild()` - called by AddBtn controller.
- `requestDeleteSelf()` - called by DeleteBtn controller.
- `requestDragStart(eventInfo)`, `requestDragEnd(eventInfo)`,
  `requestDragOver(eventInfo)`, `requestDragLeave(eventInfo)`,
  `requestDrop(eventInfo)` - semantic drag/drop requests from row state
  controllers.
- `requestSubtreeRefresh()` - asks TreeEditor to refresh affected presentation.

## 4. State Ownership

- TreeItem owns item-level runtime interaction state such as drag/drop hint.
- The source record is owned by the parent/context data association and is pulled
  on demand.
- Expand/collapse state is owned by ExpandCollapseHolder.
- Editor mode state is owned by EditorModeHolder.

## 5. Child Interaction Rules

- TreeItemRow and ExpandCollapseHolder constructors receive only TreeItem as
  parent/context.
- TreeItem exposes resolved values through typed controller/domain methods.
- Descendant controllers pull data from TreeItem or from their direct parent
  chain; TreeItem does not push setter-style updates into descendants.
- ChildrenList obtains child records by pulling `getChildRecords()` from the
  owning TreeItem through its parent/context chain.

## 6. Lifecycle

1. Constructor captures the guaranteed TreeEditor ancestor through approved typed
   ancestor access.
2. Constructor creates item content typed through `IContentAccess`.
3. `buildChildren()` creates TreeItemRow and ExpandCollapseHolder and places
   their opaque handles through parent-owned materialization.
4. `refresh()` pulls the current item record, resolves primitive values, and
   requests child refresh.

## 7. Side Effects

- `requestAddChild()` asks the owning ChildrenList or RootItemHolder data
  context to add a new record where architecturally allowed, then requests
  refresh.
- `requestDeleteSelf()` asks the owning collection context to remove this item
  where allowed, then requests refresh.
- Drag/drop requests update TreeItem-owned drag/drop state and may ask an
  allowed collection context to reorder child records.

## 8. Constraints and Invariants

- No post-construction data setter exists.
- No child receives item data through constructor arguments, props, config, or
  setter methods.
- TreeEditor access is through the guaranteed typed ancestor chain.
- TreeItem does not mutate its presentation content to apply dragging or drop
  hints; content pulls resolved tokens during refresh.

## 9. Non-Goals

- Does not serialize source data externally.
- Does not own editor mode or expand/collapse state.

## 10. Platform Implementation Notes

- Visual primitive: static tree item container.
- Drag/drop platform events are content-local event sources that become semantic
  requests to the TreeItem controller.
- Label, indentation, icon, drag, and drop-hint values are resolved controller
  values pulled by descendant presentation content.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item.top`
- Public node class: `TreeItemNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `TreeItemContentAccess`
  - Content-to-controller: `TreeItemControllerAccess`
- Companion artifact stems: none
