---
sourcePath: src/pane/tree_item/children_list.top
---

# ChildrenList

## 1. Node Identity and Role

ChildrenList is a mutable container that holds the child TreeItem instances of a tree item. It is the logical child of ExpandedState, which has no visual content of its own. ExpandedState exposes the ChildrenList view through `getView()`, and the parent switcher places that view into ExpandCollapseHolder content.

ChildrenList follows a **destroy/activate content lifecycle**: its visual content is destroyed when the tree item collapses and re-created when it expands. The logical child nodes (TreeItems) are retained in the node tree across this cycle.

## 2. Responsibility

- Own and manage the visual container for child tree items.
- Expose `init(childrenData[])` to populate children from a data array (replace semantics).
- Expose `addItem(data)` to append a new child TreeItem.
- Expose `deactivate()` to destroy visual content while keeping logical children.
- Expose `activate()` to re-create visual content and re-attach all logical child views.

## 3. Inputs and Events

- `init(childrenData[])` — called by `TreeItem.reset()`. Removes all existing child TreeItems from the visual representation and from the logical tree, then creates and resets a new TreeItem for each data entry.
- `addItem(data)` — creates a new TreeItem via the library mechanism, calls `reset(data)` on it, and appends it to this list.
- `mountChildAt(item, index)` — inserts an existing TreeItem's view at a specific position; used during drag-and-drop reorder.
- `deactivate()` — destroys this node's current visual content. Logical children are retained.
- `activate()` — re-creates this node's visual content, then re-attaches all existing child TreeItem views to the new content.

## 4. State Ownership

- Manages the mutable ordered set of child TreeItem instances (as the logical children of this node).
- Owns no other state.
- **Source of truth policy**: one-way materialization only. Add, delete, and reorder operations modify the runtime node tree. The source data model is never written back.

## 5. Child Interaction Rules

- Creates child TreeItem instances from the project Library (`lib:pane.TreeItem`) via the library mechanism (`Library.create`).
- Calls `reset(data)` on each newly created TreeItem.
- Child TreeItem views are mounted through the node's content access boundary.
- On `init`: removes children with `child.detachView(); child.remove()` before creating new ones.
- On `activate`: re-mounts each existing child's view through the node's content access boundary.

## 6. Lifecycle

1. Constructor or `activate()`: creates the child-list content boundary with `setContent(...)`.
2. `init(data[])` is called during `TreeItem.reset()` to populate the list.
3. `deactivate()` is called by ExpandedState on collapse: destroys this node's visual content.
4. `activate()` is called by ExpandedState on expand if visual content is absent: re-creates the visual content and re-attaches child views.

## 7. Side Effects

- Creating a child TreeItem from `lib:pane.TreeItem` (via `addItem` or `init`) triggers `reset(data)`, which recursively initializes the entire subtree below that child.
- `deactivate()` removes this node's visual content from the materialized view.
- `activate()` re-creates this node's visual content so it can be returned by `getView()` and mounted by the parent switcher.

## 8. Constraints and Invariants

- Content is mounted within this node's own content area; this node does not attach its content directly to ancestor integration surfaces.
- Logical children must survive `deactivate()` / `activate()` cycles intact.
- `length` must accurately reflect the number of current logical child nodes.
- The platform content handle is absent after `deactivate()` and present after constructor materialization or `activate()`.

## 9. Non-Goals

- Does not manage expand/collapse visibility decisions (those are made by ExpandedState).
- Does not apply indentation (done by `TreeItem._refreshIndent()`).

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `children-list`.
- In the DOM implementation, visual content is represented by the node's `el`.
- `deactivate()`: calls `this.clearContent()` (base class method that destroys the content and nulls the reference).
- `activate()`: calls `this.setContent(new ChildrenListContent(...))`, then re-mounts each child's view via `this.content.mount(child.getView())`.
- Child TreeItem views are DOM elements returned by `child.getView()` and mounted through `this.content.mount(...)`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/tree_item/children_list.top`
- Public node class: `ChildrenListNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: ChildrenListContentAccess
  - Content-to-controller: ChildrenListControllerAccess with zero-contract implementation ChildrenListControllerAccessZero
- Companion artifact stems: none