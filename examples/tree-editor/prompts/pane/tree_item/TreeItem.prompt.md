---
sourcePath: src/pane/tree_item/tree_item.top
---

# TreeItem

## 1. Node Identity and Role

TreeItem is the core library template node representing a single item in the tree. It is instantiated by RootItemHolder (for the root item) and by ChildrenList (for all other items). Each TreeItem contains two immutable structural children: TreeItemRow (the row visual switcher) and ExpandCollapseHolder (the expand/collapse state machine).

## 2. Responsibility

- Hold the item's data object.
- Expose `reset(data)` to populate the item from data: stores data, sets row indentation and label, initializes the children list, and calls `notifyToggle()`.
- Capture the guaranteed ancestor TreeEditor once during construction and use that stored reference for editor-level coordination.
- Compute `treeLevel` (depth: number of ancestor TreeItem nodes) and `isRoot` (whether parent is not a ChildrenList).
- Delegate expand/collapse to ExpandCollapseHolder via `_toggle()`.
- Handle add-child and delete-self actions via `_onAddClick()` and `_onDeleteClick()`.
- Expose `notifyToggle()` so descendants can request a re-evaluation of the expand/collapse icon state.
- Handle drag-and-drop events at the item level.
- Apply and clear the dragging visual marker through its content boundary.
- Expose `_refreshIndent()` to recursively update indentation after a drag-and-drop reorder.

## 3. Inputs and Events

- `reset(data)` — called after creation; populates the item and its subtree from data.
- `_toggle()` — called by NodeIcon on click; delegates to `expandCollapseHolder.toggle()`.
- `notifyToggle()` — called when the children list or expanded state changes; updates the row's toggle icon state through ExpandCollapseHolder (`childrenCount` and `isChildrenListActive`).
- `_onAddClick()` — called by AddBtn; creates a new `{type: 'NewNode', children: []}` child, expands if collapsed, calls `notifyToggle()` and `refreshAll()` on TreeEditor.
- `_onDeleteClick()` — called by DeleteBtn; removes this item's materialized view and node from the tree, then calls `notifyToggle()` on the parent TreeItem (if any).
- Drag events on own view: drag start, drag end, drag over, drag leave, drop.
- Drag start and drag end update the item's own dragging marker only through a named content command.

## 4. State Ownership

- **data** — the raw data object for this item. Owned by TreeItem.
- Expand/collapse state is owned by ExpandCollapseHolder, not by TreeItem.
- Editor mode state is owned by EditorModeHolder, not by TreeItem.
- Source of truth policy: one-way materialization only. Add, delete, and drag-and-drop operations modify the runtime node tree; the source data model is never updated back.

## 5. Child Interaction Rules

- Accesses `row` (TreeItemRow) via private field `_row`.
- Accesses `expandCollapseHolder` via private field `_expandCollapseHolder`.
- Accesses `childrenList` by delegating through `_expandCollapseHolder.childrenList`.
- Accesses the guaranteed TreeEditor ancestor through the stored `_editor` reference captured during construction.
- To locate the parent TreeItem from inside a ChildrenList, uses upward type-based lookup — direct parent traversal does not yield TreeItem because ChildrenList's logical parent is ExpandedState.
- Does not use hardcoded index chains or fixed-depth `.parent` assumptions.

## 6. Lifecycle

1. Constructor: captures the guaranteed TreeEditor ancestor via `findUpByType(TreeEditorNode)` and stores it in `_editor`; if absent, construction fails because the library deployment contract is broken.
2. Constructor: initializes item-owned runtime state only.
3. Constructor: creates the item content boundary with `setContent(...)`.
4. `buildChildren()`: creates TreeItemRow and ExpandCollapseHolder as children and places their views through the item content boundary.
5. `reset(data)` is called after construction; it configures the row and recursively initializes the subtree.
6. Drag-and-drop may relocate the item's materialized view and node at runtime; `_refreshIndent()` is called afterward.

## 7. Side Effects

- `_onAddClick()`: creates a new child data object `{type: 'NewNode', children: []}`, expands if collapsed, triggers `refreshAll()` on TreeEditor.
- `_onDeleteClick()`: uses the stored TreeEditor reference, removes own materialized view and node from the tree, notifies parent TreeItem to update its toggle icon, and triggers `refreshAll()` on TreeEditor.
- Drag-and-drop: moves own materialized view and node to a new position in a ChildrenList; calls `_refreshIndent()` recursively on self and all descendants; notifies both old and new parent TreeItems via `notifyToggle()`.

## 8. Constraints and Invariants

- `isRoot` is true if and only if the direct parent node is not a ChildrenList instance.
- Must not store expand/collapse state as a boolean flag.
- Must not store edit mode state.
- Drag-and-drop must block dropping an item onto itself or any of its descendants.
- `_refreshIndent()` must update indentation based on tree level for self and recurse into all children via ChildrenList.
- Controller code must not mutate the item's visual primitive directly to represent dragging; it must call a named content command.
- TreeEditor access is guaranteed by the typed deployment chain in this project; it is captured once in the constructor and reused. Parent TreeItem lookup remains nullable because the root item has no parent TreeItem and runtime reordering can change the nearest parent.

## 9. Non-Goals

- Does not apply the editor-level visual edit-mode marker (done by state nodes).
- Does not directly show/hide any child view (done by sub-state nodes).
- Does not serialize or write back to the source data model.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `tree-item`.
- Dragging marker: content command toggles CSS class `dragging` on the item element.
- `treeLevel`: count ancestor nodes of type TreeItem by walking `.parent` upward.
- Row indentation: `row.setPaddingLeft(treeLevel * 20)`.
- Drag API: HTML5 draggable + DataTransfer; `effectAllowed = 'move'`.
- Drop position detection: compare `event.clientY` with the midpoint of the row element's bounding rect to determine above/below.
- CSS classes for drop target: `drop-top` and `drop-bottom` on the row element.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/tree_item.top`
- Public node class: `TreeItemNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: TreeItemContentAccess
  - Content-to-controller: TreeItemControllerAccess with zero-contract implementation TreeItemControllerAccessZero
- Companion artifact stems: none