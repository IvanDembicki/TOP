# Code Generation

This document describes the rules for generating code artifacts from a TOP spec and project-local implementation prompts.

---

## 1. Base pipeline

The normative pipeline for the generative layer:

```text
tree model → node specs → project-local TOP artifacts → semantic interpretation → target adaptation → generated code → verification loop
```

Where:
- tree model defines the architecture;
- node specs fix the structure of specific nodes;
- implementation prompts specify platform-neutral semantic behavior and architecture;
- semantic interpretation produces Layer B meaning;
- target adaptation produces Layer C target-native decisions;
- code is a derived artifact.

---

## 2. What is required for code generation

For a node undergoing prompt-based generation, the following must be available:
- node spec;
- implementation prompt file;
- platform-neutral semantic interpretation output;
- target adaptation output for the active platform;
- target language/platform context;
- artifact placement rules;
- verification criteria.

The node spec must be architecturally complete.

If a node has content, the spec must record:
- the presence of a controller;
- the controller/content split;
- `props.contentType`.

---

## 3. Project-local artifacts

Spec and prompt files are project-local TOP artifacts.

They must:
- be stored inside the project;
- reside in `top/`;
- be linked to the corresponding tree or branch;
- not be stored inside the skill itself.

---


## 3.1. Semantic interpretation and target adaptation

Generation must not read source-platform primitives as implementation truth.

Before code generation:
- Semantic Interpreter Agent extracts Layer B: platform-neutral roles, intents, state, feedback, layout intent, constraints, and accessibility semantics.
- Target Adaptation Agent converts Layer B into Layer C: temporary target-native interaction, layout, primitive, and constraint decisions.

Generation may use target-specific primitives only from Layer C or from the active target's own conventions.
It must not copy source-platform constructs from prompts, platform notes, imported code, CSS, DOM, Flutter widgets, UIKit/Android classes, or framework APIs into another target.
## 4. Controller / Content split in generation

Every node always has a controller.

If a node has no content, generation may produce only a controller class.

If a node has content, generation must preserve the architectural split:
- a separate controller class;
- a separate concrete content class;
- concrete content is hidden behind the controller;
- the controller remains the sole external interface of the node.

### Canonical rule
Generated architecture must not mix the controller and concrete content into a single class where content exists.

### Public and internal protocol surfaces
Generated architecture must preserve the public node surface and two distinct internal access boundaries:
- `IControllerAccess` for content/view access to the controller via a narrow private contract;
- `IContentAccess` for controller access to content via a narrow private contract.

Content must not access the public node surface. Anything else is strictly prohibited.

### Opaque view handle for composition
Generated visual nodes may expose a general opaque view handle through `getView()` when parent-owned materialization requires it.

The parent may use this handle only for placement/composition:
- mount;
- unmount;
- insert;
- reorder;
- replace;
- passing the child view into the parent's own content boundary.

Generated code must not use a child view handle to attach event listeners, mutate styles/classes/attributes, query inside the child view, or use the child view's platform API as a behavior or communication channel. Any operation other than placement/composition must go through the child's public node surface or an explicit boundary owned by that child.

### Content responsibilities
Content creates and encapsulates the concrete implementation material.

Ordinary content may execute low-level platform commands that belong to its own concrete implementation:
- subscribe / unsubscribe on its own platform primitive;
- attach / detach local platform callbacks for its own primitive;
- show / hide / update its own implementation material when commanded through the content boundary;
- respond to platform events by translating them into narrow calls to `IControllerAccess`.

Ordinary content must not contain:
- architectural event interpretation;
- state transition decisions;
- tree navigation;
- structural/lifecycle decisions;
- calls to full controller methods;
- access to external implementation objects or integration handles;
- communication with anything except its own controller through `IControllerAccess`.

### Controller responsibilities for events and lifecycle
Semantic event interpretation, state changes, lifecycle decisions, and orchestration are the responsibility of the controller.
Low-level listener registration may be executed by content only for its own platform primitive and only as implementation material hidden behind the content boundary.
The controller interacts with content only through its explicitly defined external interface.
When a controller needs its own content to perform a visual/platform operation, generation must create a named command method on `IContentAccess` and call it as `this.content.<command>(...)`.
Generated controller code must not use the node's own render/view/native primitive, its platform API, or any equivalent exposed primitive handle for its own content. Detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()` — use the equivalent native/render primitive handle on other platforms.
The controller manages the content lifecycle and does not use the internal content implementation as a communication channel.
If a node has a separate content object, generation must not leave direct controller access to the concrete implementation bypassing the content boundary. Anything else is strictly prohibited.

### Requirements for internal access boundaries
Generation must create for nodes with a separate content only explicitly defined, narrow, and maximally strictly typed internal access boundaries: `IControllerAccess` and `IContentAccess`.
If a node has a separate content class/object, generation must materialize separate explicit access artifacts for both directions where the technology permits. Anything else is strictly prohibited.

Both directions must be accounted for:
- `IContentAccess` / controller-to-content: what the controller may command or request from its own content;
- `IControllerAccess` / content-to-controller: what content may report or request from its own controller.

If a direction has no permitted calls, generation must materialize or explicitly document a zero-contract for that direction according to the target technology. Silent omission is not valid.
Raw callbacks, anonymous objects, full controller references, or full concrete content references are not valid substitutes for a named internal contract where the technology can express one.

These boundaries/artifacts:
- are not the full controller or the full concrete content object;
- are not the external API of the node;
- must not contain parent/root links, host/container references, or integration handles;
- must not be used as a surrogate channel for accessing the outside world;
- must not be substituted by implicit or anonymous object shapes where the language allows materializing a typed boundary explicitly;
- if the content is a `view`, must not legalize direct access to child nodes, `children`, or `openedChild`. Child visual content must be requested only through explicitly described controller-provided endpoints.

Anything else is strictly prohibited.

### Materialization layout and declaration order
One semantic node may materialize as one file or multiple files. The target technology or project
convention may require one-class-per-file, separate contract files, or split controller/content files.

For one-file materialization, the order of appearance is:
1. public controller/node class;
2. internal access boundaries (`IContentAccess` and `IControllerAccess`, or explicit zero-contract declarations);
3. hidden content/view implementation.

For split materialization, the same outside-to-inside dependency direction must be preserved in
file structure and exports:
1. public controller/node artifact;
2. internal contract artifact(s);
3. hidden content/view artifact(s).

The implementation prompt's `Expected Materialization` section must declare whether the node uses
one-file default materialization or companion artifacts.

---


## 4.1. Strict method purpose in generated controllers

Generated controllers must not use runtime/lifecycle methods outside their semantic purpose. Anything else is strictly prohibited.

If a method such as `buildChildren()` is present in a generated controller, it is only permitted for runtime child construction.
Using it as a general controller init method is prohibited.

Placing the following inside `buildChildren()` is prohibited:
- creating content of the current node;
- listener wiring of the current node;
- initial visual/data sync of the current node;
- general initialization of the controller instance.

If runtime child construction is absent in a node, generation must not create `buildChildren()` in that class. Anything else is strictly prohibited.

## 5. `props.contentType` in generation

If a node has content and its type needs to be explicitly recorded in the spec, `props.contentType` is part of the generation contract.

Canonical values:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

Generation must account for:
- `view` — locally implemented content node;
- `component` — black-box content node;
- non-visual content must not be exposed externally as a public content object.

---

## 6. `props.dir` as a semantic branch anchor

The `props.dir` field is used not only as a technical path for generated code,
but also as a **semantic branch anchor**.

This means:
- `props.dir` fixes the directory anchor for a node or subtree;
- descendants inherit the effective dir path until a new local `props.dir` is set;
- the effective dir path must reflect the semantic branch structure of the project, not the accidental history of file moves.

### Canonical rule
The directory tree of code artifacts must be derived from the tree model through semantic branches and the effective `props.dir`.

---

## 7. Effective directory path

For each node, an **effective directory path** is computed:

1. if the node has a local `props.dir` — it is used as the anchor;
2. if there is no local `props.dir` — the effective dir of the nearest ancestor is used;
3. if no ancestor in the chain has `props.dir` — the path is determined by the root/project-level convention.

### Important
Not every node needs a separate folder.
A folder is created for a semantic branch, not for every leaf/control node.

Leaf/control nodes typically reside within the effective directory path of their branch.

---

## 8. Synchronization of code layout and prompt layout

`top/prompts/...` must mirror the same effective branch structure as the code artifacts.

That is:
- generated code layout and prompt layout must be consistent;
- the prompt file for a node must reside in a directory tree isomorphic to the effective branch structure;
- a difference between the code path and the prompt path is only acceptable at the root namespace level:
  - `src/...`
  - `top/prompts/...`

---

## 9. Semantic branch derivation before generation

Before code generation, it is necessary to:
- identify semantic branches;
- determine branch roots;
- identify nodes that do not need a separate subtree folder;
- compute the effective dir map;
- verify that the current artifact layout does not conflict with the target branch layout.

If the layout conflicts with the semantic tree, the target layout must be proposed first,
and only then is generation or regeneration performed.

---

## 10. What must be determined during generation

For each code-generated node, the following must be determined:
- the primary artifact stem and materialization policy;
- any companion artifact stems and roles;
- the effective dir path;
- the prompt file path;
- branch ownership;
- inheritance of `props.dir` if it is used;
- controller/content split if content exists;
- internal contracts in both directions if content exists;
- `props.contentType` if content exists and its type needs to be explicitly recorded.

If the layout is not obvious, the generation task is incomplete.

---

## 11. Output requirements for layout-aware generation

A good generation pipeline must be able to produce:
- semantic branch map;
- effective dir map;
- target code directory tree;
- target prompt directory tree;
- relocation map `old path → new path` if the project is being reorganized;
- required spec updates if `props.dir` needs to be added or corrected;
- required spec updates for `props.contentType` if it is missing from a node with content where the content type must be explicitly recorded.

---

## 12. Typical errors

Typical errors include:
- `props.dir` used only as an arbitrary path, not as a semantic anchor;
- code layout and prompt layout diverge in branch structure;
- a separate folder created for each node without a semantic reason;
- an entire subtree dumped into one folder despite clear semantic branches;
- AI generates code without checking the effective dir path;
- relocation performed without updating spec/prompt paths;
- generation mixes controller and concrete content;
- generation leaves controller code directly manipulating its own platform primitive instead of calling named `IContentAccess` commands;
- generation places hidden content/view declarations before the internal access boundary that stands between the controller and content;
- generation makes non-visual content publicly accessible;
- generation loses the distinction between `view` and `component`.

---

## 13. Verification implications

The verification loop must check not only behavior but also the architectural contract of generation:
- whether the controller/content split is maintained;
- whether a node with content has turned into a single mixed class;
- whether generated declaration order follows architectural depth: controller/node first, internal access boundary artifact(s) next, hidden content/view implementation last;
- whether the meaning of `props.contentType` is preserved;
- whether non-visual concrete content is exposed externally;
- whether the rule of a single external interface for a node is violated.

---

## 14. Mandatory post-generation validation

After generation/refactor, the AI must run `references/node-validation-rules.md`.

Code is not considered correct until the validation rules confirm that:
- the class of violation has been identified;
- the violation has been classified;
- a canonical refactor direction has been chosen;
- re-validation has been performed after the fix.

Successful compilation or local operability does not supersede this check. Anything else is strictly prohibited.

---

## 15. Related documents

For layout-aware generation, use together with this document:
- `references/artifact-layout-and-branch-derivation.md`
- `references/node-model.md`
- `references/tree-model.md`
- `references/source-of-truth-and-serialization.md`
- `prompts/derive-top-artifact-layout.md`
