# Composite Systems (Tree-of-Trees)

A composite system is a system consisting of several relatively independent
trees that interact via `props.ref` or connectors.

The hallmark of a composite system is the presence of sufficiently independent parts
that make sense to describe and develop separately.
System size alone is not the criterion.

---

## Tree-of-trees

A tree-of-trees is a composite system in which each tree is described
by a separate file and connected to the parent tree as a subtree.

A child node may reference an external tree via `props.ref`:

```json
{
  "type": "MainApp",
  "children": [
    { "type": "Header" },
    { "type": "NewsFeedConnector", "props": { "ref": "modules/newsfeed/tree.json" } },
    { "type": "Footer" }
  ]
}
```

The tree referenced by `ref` is an independent artifact
with its own structure, its own state, and its own rules.

---

## Interaction between trees

An external tree is connected via `props.ref` on a node of the tree.

If the interfaces are compatible — `props.ref` is sufficient.
If transformation of calls, events, or data is needed — a connector node is used.

Direct access to nodes of another tree bypassing `props.ref` or a connector is forbidden.
Any other forms of interaction between trees are forbidden.

---

## Independence of trees during analysis

Each tree in a composite system is analyzed independently.

The materialization mode (spec-first / runtime-first) is determined
separately for each tree.
Different trees in the same system may use different modes —
this is not a contradiction.

---

## Ownership

Ownership of a subtree is determined by ownership of the file in which it is described.

The team or developer controlling the tree file
is the owner of that tree.

Ownership is not declared explicitly in the spec — it follows from file access rights.

---

## Violations

| Violation | Description |
|-----------|-------------|
| Direct access to nodes of another tree | accessing the internal structure of an external tree without going through `props.ref` or a connector |
| Interaction without `props.ref` and without a connector | any informal link between trees |
