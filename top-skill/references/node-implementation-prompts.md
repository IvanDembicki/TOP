# Node Implementation Prompts

This document describes a separate layer of implementation artifacts in TOP.

---

## What is a Node Implementation Prompt

A Node Implementation Prompt is a separate file associated with a single node
that describes the implementation of the node at a level higher than specific code syntax.

It must define:
- the node's purpose;
- responsibility boundaries;
- observable behavior;
- event handling;
- state ownership;
- state transitions;
- child interaction;
- constraints;
- invariants;
- expected outcomes;
- non-goals.

---

## Why it is needed

Goals:
- portability across technologies;
- code regeneration from the same semantics source;
- reduced dependence on framework-specific implementation;
- improved controllability of AI generation;
- the ability to run a verification loop.

---

## Where prompt files are stored

A Node Implementation Prompt is a project-local artifact.

It must:
- be stored inside the project's root `top/` directory;
- be placed in the `prompts/` directory alongside the JSON tree description or branch description;
- use the module hierarchy inside `top/` for modular projects.

Examples:

```text
top/
  tree.json
  prompts/
    TreeItem.prompt.md
```

```text
top/
  root.json
  modules/
    editor/
      tree.json
      prompts/
        TreeItem.prompt.md
```

---

## Required properties

An implementation prompt must be:
- node-scoped;
- a separate file;
- a project-local artifact;
- language-agnostic in behavioral sections;
- linked to the spec via the `prompt` field;
- kept up to date when the node changes.

---

## Recommended prompt structure

1. Node identity and role
2. Responsibility
3. Inputs and events
4. State ownership and transitions
5. Child interaction rules
6. Rendering / materialization expectations
7. Side effects
8. Constraints and invariants
9. Non-goals
10. Platform implementation notes
11. Expected Materialization

Sections 1-9 are behavioral sections and must remain platform-neutral.
Technology-specific details belong only in `Platform implementation notes`.

Platform implementation notes:
- describe target-specific implementation concerns for the current platform;
- may be used by another target technology as explanatory context;
- must not be treated as portable behavior requirements;
- must not be copied mechanically across technologies.

---

## Relationship with the node spec and generated files

The node spec must:
- reference the prompt via `prompt`;
- specify `props.dir` as needed for placement of generated class files.
  If `dir` is already set on an ancestor node, it is inherited by descendants by default.

Thus:
- `prompt` defines where the project-local semantics source resides inside `top/`;
- `props.dir` defines where generated implementation artifacts should be placed.
- `sourcePath` in prompt frontmatter binds the prompt to an extensionless primary implementation artifact stem.
  The stem is stable across target technologies; concrete file extensions are target-specific materialization details.

An implementation prompt describes one semantic node, not necessarily one physical file.
If the target or project convention materializes a node into multiple artifacts, the prompt
must declare the materialization layout:
- primary artifact stem;
- public node/controller class;
- materialization policy;
- internal access contracts in both directions;
- companion artifact stems and roles.

For nodes with separate content, both internal directions must be represented in the expected
materialization: controller-to-content (`IContentAccess`) and content-to-controller
(`IControllerAccess`). If either direction has no permitted calls, this must be declared as
an explicit zero-contract rather than silently omitted.

---

## What the prompt must not do

An implementation prompt must not:
- mix multiple semantic nodes in a single description;
- duplicate the entire project instead of node-specific semantics;
- strictly require specific syntax without necessity;
- place platform-specific implementation details in behavioral sections;
- require another platform to copy the current platform's implementation mechanism;
- substitute for the tree model;
- hide state ownership;
- be the only place where the tree structure appears.

The tree model remains the primary architectural model.
The prompt describes the implementation of an already defined node.
