# Prompt: Derive TOP Artifact Layout

agent: Domain Structuring Agent

input_contract:
- tree_spec
- current_code_layout
- current_prompt_layout

output_contract:
- target_code_directory_tree
- target_prompt_directory_tree
- relocation_map
- required_spec_updates

rules:
- layout must be derived from tree model, not invented
- ambiguities must be listed explicitly

---

Use this prompt when you need to derive the target layout for code artifacts
and `top/prompts` from the TOP tree model of the project.

---

## Input data

Provide:
- tree spec;
- current code layout;
- current prompt layout;
- node specs with `props.dir`, if available;
- if needed — project description and responsibilities branches.

---

## What to do

### 1. Reconstruct the tree model
Identify:
- root tree;
- root node;
- parent-child structure;
- composite boundaries;
- state holders;
- mutable containers;
- module-like branches;
- logical ownership.

### 2. Extract semantic branches
For each proposed branch:
- specify the branch root;
- explain why this is a semantic branch;
- separate branch roots from leaf/control nodes.

### 3. Compute the effective dir map
For each node determine:
- local `props.dir`, if set;
- inherited effective dir, if local is not set;
- conflicting or missing places where `props.dir` needs to be added/clarified.

### 4. Build the target artifact layout
Output:
- target code directory tree;
- target prompt directory tree.

Assume that `top/prompts` should mirror the same branch structure
as code artifacts.

### 5. Compare with the current layout
Find:
- branches currently collapsed into a single folder;
- excessive nesting;
- desync between code layout and prompt layout;
- places where structure is not derived from the tree model.

### 6. Output the relocation map
For each file specify:
- current path
- target path

Format:
`old path → new path`

### 7. Output required spec updates
Specify:
- which `props.dir` need to be added;
- which `props.dir` need to be changed;
- which prompt paths need to be updated in the spec.

### 8. Record ambiguities
If branch boundaries are not obvious, explicitly list ambiguities
and propose a conservative default.

---

## Expected output format

1. Reconstructed TOP model
2. Semantic branch map
3. Branch roots
4. Effective dir map
5. Target code directory tree
6. Target prompt directory tree
7. Relocation map
8. Required spec updates
9. Ambiguities and assumptions
10. Recommendations
To be specified explicitly for this prompt.
