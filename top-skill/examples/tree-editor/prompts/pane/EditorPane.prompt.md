---
sourcePath: src/pane/editor_pane.top
---

# EditorPane

## 1. Node Identity and Role

EditorPane is the main content area of the tree editor. It is a structurally
immutable container node and the direct parent of RootItemHolder.

## 2. Responsibility

- Materialize the pane's static content container.
- Serve as the structural parent for RootItemHolder.
- Expose the root tree record to RootItemHolder through an explicit pull method
  that delegates to TreeEditor.

## 3. Inputs and Events

- `getRootRecord()` - returns `parent.getRootRecord()` through the allowed
  parent/context contract.
- `requestRefresh()` - asks TreeEditor to refresh the branch after data/tree
  changes.

## 4. State Ownership

Owns no data state. It is an attachment and content host boundary.

## 5. Child Interaction Rules

- Has exactly one direct child: RootItemHolder.
- RootItemHolder constructor receives only EditorPane as parent/context.
- RootItemHolder pulls the root record through `getRootRecord()`; EditorPane does
  not push source data into RootItemHolder.

## 6. Lifecycle

1. Constructor creates the pane content boundary.
2. `buildChildren()` creates RootItemHolder and places its opaque handle through
   parent-owned materialization.
3. Refresh requests are routed to TreeEditor through the parent contract.

## 7. Side Effects

None beyond parent-owned placement of RootItemHolder's opaque handle.

## 8. Constraints and Invariants

- No post-construction data initialization method.
- No presentation commands into content.
- Structurally immutable after child materialization.

## 9. Non-Goals

- Does not own tree data.
- Does not manage expand/collapse or edit mode.

## 10. Platform Implementation Notes

- Visual primitive: static pane container.
- RootItemHolder's opaque handle is placed by EditorPane only as a direct child
  handle.

## 11. Expected Materialization

- Primary artifact stem: `src/pane/editor_pane.top`
- Public node class: `EditorPaneNode`
- Base class / base role: `DomNode`
- Materialization policy: one-file default
- Internal contracts:
  - Controller-to-content: `EditorPaneContentAccess`
  - Content-to-controller: `EditorPaneControllerAccess`
- Companion artifact stems: none
