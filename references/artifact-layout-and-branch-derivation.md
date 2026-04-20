# Artifact Layout and Branch Derivation

This document describes how the directory structure for code artifacts and `top/prompts`
is derived from the tree model.

---

## 1. Why layout derivation is needed

The project file structure must not be:
- arbitrary;
- historically broken;
- flat when there are clearly defined branches;
- different for code and prompts without a reason.

Directory structure must be derived from the TOP tree through semantic branches.

---

## 2. What is a semantic branch

A **semantic branch** is a subtree that:
- has a distinct responsibility;
- reads as a self-contained semantic unit;
- naturally becomes a separate folder in both code layout and prompt layout.

A semantic branch is not just any subtree.
A separate folder is not needed for every node.

---

## 3. Characteristics of a semantic branch

A subtree is typically a semantic branch if it has at least several of the following:
- a distinct responsibility;
- a distinct content region;
- an independent state region;
- a mutable container boundary;
- a composite boundary;
- a module-like role;
- it appears in multiple places in the tree as a self-contained structure;
- a distinct branch owner, identifiable from the model.

---

## 4. What typically does not need its own folder

A separate folder is typically not needed for:
- leaf nodes;
- small control nodes;
- tiny helper nodes;
- nodes without their own semantic subtree;
- simple visual atoms inside an already existing branch.

Such nodes typically reside in the effective directory path of their semantic branch.

---

## 5. Branch roots

For layout derivation, **branch roots** must be identified.

A branch root:
- is a semantic anchor subtree;
- may have its own `props.dir`;
- defines the effective directory path for descendants if they do not open a new semantic branch.

---

## 6. `props.dir` and effective layout

`props.dir` defines the directory anchor.

Computation rule:
1. local `props.dir` of the node;
2. otherwise, the inherited effective dir of the nearest ancestor;
3. otherwise, the root/project-level default.

### Canonical rule
The effective dir path must correspond to the semantic branch structure,
not merely to the current file locations.

---

## 7. Code layout and prompt layout

Two parallel structures must be built:
- code artifact layout;
- prompt artifact layout.

They must be isomorphic in terms of branches.

Example:
```text
src/
  pane/
    tree_item/
      tree_item.ux.js

top/
  prompts/
    pane/
      tree_item/
        TreeItem.prompt.md
```

The root namespace differs, but the semantic branch structure is the same.

### Structural Correspondence Rule

What matters is not the root directory — it is that spec, prompt, and code share
the same semantic coordinate system.

Prompt paths and code paths must reflect the same semantic position of the node
in the tree. Root directories may differ depending on the technology stack
(`src/`, `lib/`, `top/prompts/`, etc.), but the internal structure must be consistent.
If a node belongs to a particular semantic branch of the tree, its prompt and its
class must be located in the corresponding subdirectories of their respective roots.

This ensures:
- navigation across the project is predictable;
- a node in the tree can always be located in both its prompt and its implementation
  without guessing;
- AI can reliably map a tree node to its prompt and code artifact;
- the source structure groups files by meaning, not by accident.

Forbidden:
- placing a prompt file at a path that does not correspond to the node's semantic
  position in the tree;
- having code and prompt layouts that are structurally inconsistent with each other.

---

## 8. What the AI must do during derivation

The AI must:
1. reconstruct the tree model;
2. identify semantic branches;
3. determine branch roots;
4. compute the effective dir path per node;
5. identify nodes that do not need a separate folder;
6. build the target code directory tree;
7. build the target prompt directory tree;
8. produce a relocation map `old path → new path`;
9. produce required spec updates for `props.dir` and prompt paths.

---

## 9. Derivation result format

The result must contain:
- semantic branch map;
- branch root list;
- effective dir map;
- target code directory tree;
- target prompt directory tree;
- relocation map;
- required spec updates;
- ambiguities and assumptions.

---

## 10. When a layout is considered good

A good layout:
- reflects semantic branches;
- does not create unnecessary nesting;
- does not mix independent branches in one folder;
- does not separate code and prompts into different semantic layouts;
- is explainable from the tree model;
- is stable for future generation/regeneration.

---

## 11. Typical mistakes

- one folder contains multiple independent semantic branches;
- prompts are flat while code is nested, or vice versa;
- a separate folder is created for every leaf node;
- `props.dir` is insufficient to reconstruct the layout;
- a relocation map is absent despite a re-layout being recommended.

---

## 12. Related documents

Use together with:
- `references/code-generation.md`
- `references/node-model.md`
- `references/analysis-rules.md`
- `prompts/derive-top-artifact-layout.md`
