---
sourcePath: src/pane/root_item_holder.top
---

# RootItemHolder

## 1. Node Identity and Role

RootItemHolder is a mutable container holding exactly one root TreeItem instance. It is the entry point for tree data initialization and the direct parent of the root TreeItem in the node tree.

## 2. Responsibility

- Expose `init(sourceData)` to populate the tree from data.
- Use replace semantics in `init`: remove the existing root TreeItem from both the materialized view and the logical tree before creating the new one, so repeated calls are safe.
- Create the root TreeItem from the project Library (`lib:pane.TreeItem`) via the library mechanism and call `reset(data)` on it.

## 3. Inputs and Events

- `init(sourceData)` — called by EditorPane, which is in turn called by TreeEditor during `mount()`. Clears any existing root TreeItem, then creates a new TreeItem and calls `reset(sourceData)` on it.

## 4. State Ownership

Owns no state beyond being the logical parent of the root TreeItem.

## 5. Child Interaction Rules

- After `init`, holds exactly one child: the root TreeItem.
- Creates TreeItem instances from the project Library (`lib:pane.TreeItem`) via the library mechanism (`Library.create`).
- Calls `reset(data)` on the created TreeItem.
- On `init`, removes existing children from the materialized view and then removes their nodes from the logical tree before creating the new root.

## 6. Lifecycle

1. Constructor: no root item is created.
2. Constructor: creates the holder content boundary with `setContent(...)`.
3. On `init(sourceData)`: clears existing children (removing their views and logical nodes), creates a new root TreeItem from `lib:pane.TreeItem` via the library mechanism, places its view through the holder content boundary, calls `reset(sourceData)`.
4. The root TreeItem's view is placed into RootItemHolder's content area through content access.

## 7. Side Effects

- On `init`: replaces the materialized root item view.

## 8. Constraints and Invariants

- Must hold exactly one TreeItem after `init` completes.
- Must not manage expand/collapse or edit mode logic.
- Replace semantics: after `init`, no stale children remain in the node tree.

## 9. Non-Goals

- Does not manage child trees recursively (that is done by ChildrenList inside each TreeItem).
- Does not apply indentation.
- Does not react to mode changes.

## 10. Platform Implementation Notes

- Visual element: `div` with CSS class `root-item-holder`.
- Child removal: `child.getView()?.remove(); child.remove()` for each existing child.
- New root item view: `this.content.mount(item.getView())`.
- Extends `DomNode`.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/root_item_holder.top`
- Public node class: `RootItemHolderNode`
- Base class / base role: `DomNode`

- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: RootItemHolderContentAccess
  - Content-to-controller: RootItemHolderControllerAccess with zero-contract implementation RootItemHolderControllerAccessZero
- Companion artifact stems: none