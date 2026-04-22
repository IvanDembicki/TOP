# DynamicCollectionViewNode

This document refines an existing skill rule: dynamic repeated visual composition is permitted only inside a dedicated container node.

---

## 1. Purpose

`DynamicCollectionViewNode` — a specialized visual contract for a node that owns a homogeneous dynamic child collection and builds its view by iterating over its direct child nodes.

Typical examples:
- news list;
- chat messages;
- menu items;
- rows;
- cards collection.

---

## 2. Base rule

An ordinary visual node does not iterate `children` to build UI.
Only explicitly declared named child-view endpoints provided by the controller through `IControllerAccess` are permitted for it.

Iteration over a child collection for view construction is permitted only inside a dedicated `DynamicCollectionViewNode`.

---

## 3. Structure rule

A dynamic collection must be extracted into a separate container node.

Correct:
- `Window` receives `Button1View`, `Button2View`, `Button3View`, and `NewsListContainerView`;
- `NewsListContainerNode` itself owns the `NewsItem` children and builds the repeated list from their views.

Incorrect:
- `WindowView` simultaneously works with static slots and directly iterates news items.

---

## 4. Access rule

Even in a `DynamicCollectionViewNode`, the view-part must not access child nodes directly.
It receives child visual content only through its controller.

The controller may provide:
- an ordered collection of direct child views;
- only for the collection that is explicitly described by the node's contract.

---

## 5. Homogeneity — definition

**Homogeneous collection** — a collection in which:
- all items share the same base node type (or one common supertype);
- each item is processed in the same way when building the view;
- no item requires special-casing or a named slot.

Example: all children are `TreeItemNode` → homogeneous.
Counter-example: children are `HeaderNode`, `SectionNode`, `FooterNode` → not homogeneous; these are named slots, not a collection boundary.

---

## 6. Constraints

`DynamicCollectionViewNode` permits iteration only over:
- direct children;
- a homogeneous collection boundary;
- a collection explicitly declared in the node's contract.

Forbidden:
- mixing static named slots and a dynamic child collection in a single ordinary visual contract;
- flattening descendants deeper than direct collection children;
- delivering the internal items of a dynamic collection to the parent node instead of the container view.

### One node — one collection boundary

A single `DynamicCollectionViewNode` declares exactly one collection boundary.

If a node has several dynamic groups of children — each group is extracted into a separate `DynamicCollectionViewNode`, and the parent is an ordinary visual node with named slots referencing those container nodes.

---

## 7. Controller access pattern

The controller provides the view-part with an ordered collection of direct child views through an explicit `IControllerAccess` endpoint.

Minimally sufficient contract:
- The controller iterates its own direct children.
- For each child it obtains `child.getView()` (through the controller, not directly from the view).
- It returns an ordered array/sequence of view-parts through the access endpoint.

The view-part receives the result as an opaque ordered sequence and places it in its own visual container.

The view-part must not know the type of items, the number of items in advance, or the details of their internal structure — only that it is an ordered sequence of renderable views.

---

## 8. Prompt requirements

If a node is a `DynamicCollectionViewNode`, the implementation prompt must explicitly describe:
- which child collection is the collection boundary;
- why items are homogeneous (common type);
- what order of elements is used (order of children in the tree);
- how the controller provides ordered child views to its view-part (through which `IControllerAccess` endpoint).
