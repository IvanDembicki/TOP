# Tree Editor — Real-World TOP Example

A complete real-world project built with TOP. Demonstrates full application of the paradigm across a non-trivial UI system.

## What this example covers

- Full spec tree (`top/tree_editor.json`) — complete node hierarchy for a tree editor application
- Switchable nodes — `ExpandCollapseHolder`, `EditToggleBtn`, `EditorModeHolder` with state nodes
- Dynamic collection — `ChildrenList` as a `DynamicCollectionViewNode`
- Library subtree — `pane.library.json` with reusable node definitions
- Presentation branch — `top/presentation/` with theme nodes and presentation artifacts
- Assets branch — `top/assets/demo-tree.json` as model-only data
- Full prompt coverage — implementation prompt for every generated node, organized by semantic position in the tree

## Structure

```
top/
  tree_editor.json          — root spec tree
  prompts/                  — implementation prompts, mirroring tree structure
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

To generate the implementation: provide `tree_editor.json` and the relevant prompt files to the generation pipeline.
To inspect a specific node: read its prompt file and its entry in `tree_editor.json`.

## How to start with this example (adoption path)

This example is the recommended starting point for teams evaluating TOP.

1. **Read the spec tree** — open `top/tree_editor.json`. See how the system is described as a tree of nodes with explicit responsibilities.
2. **Pick one node** — for example `EditToggleBtn` in the toolbar branch. Read its prompt: `top/prompts/toolbar/EditToggleBtn.prompt.md`.
3. **Ask the skill to generate it** — provide the spec entry and prompt to the generation pipeline. Review the result.
4. **Compare with your mental model** — notice how ownership, state, and boundaries are made explicit.
5. **Try a neighboring node** — expand to `EditorModeHolder` or `TreeItem` to see switchable and dynamic collection patterns.
6. **Decide on scope** — TOP works incrementally. One branch at a time is a valid adoption strategy.
