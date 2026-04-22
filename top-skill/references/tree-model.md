# Tree Model

The tree model describes a system as a hierarchy of nodes with strict parent-child relationships.

---

## 1. Core idea

The system is viewed as a tree, not as a graph or an arbitrary collection of objects.

Each node:
- has a controller;
- occupies a place in the tree;
- has parent-child relations;
- may have content;
- may participate in the state model;
- may own children;
- may materialize or delegate content.

### 1.1. Fixed node schema and `props`

The top-level schema node must remain minimal and stable.

This means:
- the tree model is not extended with new project-specific top-level node fields;
- additional node properties are stored in `props`;
- classification attributes in the spec, including content classification, are fixed via `props`.

---

## 2. Node and content

If a node has no content, it can be represented by a controller alone.

If a node has content, the node must be split into:
- controller
- content

Controller and content are two different classes.

The concrete content class is always hidden behind the controller.
The controller is the sole external interface of the node.

---

## 3. `props.contentType`

If a node has content and its type needs to be explicitly recorded in the spec, use `props.contentType` rather than a separate top-level `contentType` field.

Canonical values:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

### `view`
A locally implemented content node.

### `component`
A black-box content node.
It may follow its own internal rules, but for the tree model this node remains hidden content.

### `data`
A data-content node.

### `style`
A style-content node.

### `animation`
Animation content.

### `transition`
Transitional content/state representation.

### `asset`
Resource content.

### `other`
Fallback type.

---

## 4. External interface of a node

The outside world interacts only with the controller.

This means:
- concrete content does not leak outward;
- any events from content go to the controller first;
- direct access to non-visual content is prohibited;
- visual content may be exposed externally only as a general visual interface, if required for composition.

---

## 5. Parent-child structure

The tree model defines:
- structural parent-child relations;
- branch boundaries;
- child policy;
- state ownership;
- ownership of content composition.

Child nodes interact with the outside world through their controllers.

---

## 6. Tree and semantic branches

A tree may contain semantic branches.
They are used for:
- semantic decomposition of the system;
- artifact layout;
- branch-level ownership;
- identifying large subtrees.

Not every subtree must be a semantic branch.
A semantic branch is a meaningful block, not merely a technical nesting level.

---

## 7. Tree model and state

State is defined through tree configuration.

State holders, state nodes, mutable nodes, and single-child mutable nodes
must be analyzed independently of `props.contentType` as a means of storing content classification in the spec.

For example:
- state can be represented via `view`;
- a transition can have `props.contentType: transition`;
- an animation-state can have `props.contentType: animation`.

But the architectural ownership of state is always determined by the tree model and the controller hierarchy.

---

## 8. Tree model and external/black-box content

If a node uses `props.contentType: component`,
the internal life of the component does not need to be exposed in the tree model of that project.

For the TOP tree this content is treated as a black box.
But the node itself remains an ordinary node:
- with a controller;
- with a place in the tree;
- with child relations, if any;
- with access only through the controller.

---

## 9. What a spec tree must express

A good spec tree must be able to express:
- node type;
- semantic role;
- child policy;
- state role;
- `props`, including `contentType` if content exists and its type needs to be explicitly recorded, and `dir` if needed;
- prompt path, if the node is generated;
- branch structure.

---

## 10. Typical tree model violations

Violations include:
- absence of a controller as a mandatory part of the node;
- content present without a dedicated content class;
- absence of `props.contentType` on a node with content, when the content type must be explicitly recorded;
- direct external access to concrete content;
- mixing content semantics and controller semantics;
- graph-style relationships instead of tree structure;
- unclear child policy;
- substitution of tree semantics with visual placement.
