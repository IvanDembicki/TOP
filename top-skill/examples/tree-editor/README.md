# Tree Editor - Real-World TOP Example

A complete real-world project built with TOP. Demonstrates the current
canonical form across a non-trivial editor system.

## Canon status

This example is intended to be canonical for top-skill 1.1.18 and later.

The example follows:
- context attachment, not data injection;
- locally implemented content with static materialization;
- presentation content pulling already-resolved values through controller access;
- content reporting semantic intent to controllers;
- controller-owned decisions and runtime dirty/refresh requests;
- dynamic tree data represented through owner/context contracts, not
  constructor data packets or post-construction value packets.

## What this example covers

- Full spec tree (`tree_editor.json`) - complete node hierarchy for a tree editor application
- Switchable nodes - `ExpandCollapseHolder`, `EditToggleBtn`, `EditorModeHolder` with state nodes
- Dynamic collection - `ChildrenList` as a mutable collection node
- Library subtree - `pane.library.json` with reusable node definitions
- Presentation branch - `presentation/` with theme nodes and presentation artifacts
- Assets branch - `assets/demo-tree.json` as model-only data
- Full prompt coverage - implementation prompt for every generated node, organized by semantic position in the tree

## Structure

```text
tree_editor.json
prompts/
  TreeEditor.prompt.md
  pane/
  toolbar/
  presentation/
libraries/
  pane.library.json
assets/
  demo-tree.json
presentation/
  tree-editor.presentation.json
```

## How to use

This folder contains the spec and prompts only. Code is a generated artifact.

To generate the implementation: provide `tree_editor.json` and the relevant
prompt files to the generation pipeline. To inspect a specific node: read its
prompt file and its entry in `tree_editor.json`.

## How to start with this example

This example is the recommended starting point for teams evaluating TOP.

1. Read the spec tree - open `tree_editor.json`. See how the system is described as a tree of nodes with explicit responsibilities.
2. Pick one node - for example `EditToggleBtn` in the toolbar branch. Read its prompt: `prompts/toolbar/EditToggleBtn.prompt.md`.
3. Ask the skill to generate it - provide the spec entry and prompt to the generation pipeline. Review the result.
4. Compare with your mental model - notice how ownership, state, and boundaries are made explicit.
5. Try a neighboring node - expand to `EditorModeHolder` or `TreeItem` to see switchable and dynamic collection patterns.
6. Decide on scope - TOP works incrementally. One branch at a time is a valid adoption strategy.

## Context attachment audit

Tree item data is not pushed into child node constructors and is not applied
through post-construction setter methods. Runtime item nodes attach to their
parent/context only. The owning parent records which source record belongs to
which child and exposes that record through a narrow parent/context contract.

Presentation nodes such as `NodeLabel`, `NodeIcon`, row states, and action
controls do not receive text/icon/style/visibility values through constructors or
setter methods. Their locally implemented content pulls already-resolved
primitive values from the owning controller access contract during
materialization or refresh.

Content reports user intent, for example toggle, add, delete, hover, and drag
requests. Controllers interpret those requests, update controller/data state, and
request refresh through the node/runtime mechanism.

## Pull-based construction audit

Prompt wording that describes placing child views refers to parent-owned
materialization of direct child opaque handles, not to slots, runtime props,
external child injection, or prebuilt fragment passing.

During generation, locally implemented content constructors receive exactly one
narrow typed owner access interface implemented by the owning controller. Empty
zero-contracts are empty owner access interfaces, not separate dummy access
objects. Child nodes are constructed by their owning parent controllers at their
tree positions.
