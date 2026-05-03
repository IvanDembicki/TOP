---
name: top-skill
description: Skill for designing, generating, and validating systems built with Tree-Oriented Programming (TOP). Use when working with TOP architecture, node trees, spec generation, multi-platform code generation, or architectural validation.
---

# TOP Skill

**Version:** 1.1.6
**Last updated:** 2026-05-03 01:06 -07:00
**Invocation:** `/top`

> **Rule for AI:** whenever any top-skill file is modified, update the date and time in this field to the current values.

This skill is intended for tasks where a system **is explicitly treated or must be treated as a tree of nodes** in terms of **Tree-Oriented Programming (TOP)**.

Within the TOP product line, this is the foundational architecture skill. Use `top-prompt-cleaner` for single-prompt cleanup and `top-skill-factory` for governed skill lifecycle work.

---

## Runtime hydration (mandatory on every invocation)

The packaged `SKILL.md` is the bootstrap and fallback entrypoint — not the full source of truth.

On every invocation, before applying or citing any TOP canon, validation rules, references, prompts, or agent instructions:

1. Identify the skill base directory exposed by the host environment.
2. Read `hydration-manifest.json` from that directory using the available filesystem read capability and an absolute path.
3. Read all files listed in the `always` tier of the manifest.
4. Determine the active task type and read the corresponding `task` tier. For validation, maintenance, or release tasks, read the `full` tier instead.

**If hydration fails:** If the host environment does not expose a skill base directory, or direct file reading is unavailable, report that runtime freshness cannot be verified and continue with the packaged fallback only if the user accepts that risk.

The hydrated filesystem state is the preferred source of truth after hydration succeeds. The packaged content is the fallback only.

---

## Mandatory AI preload context

Before producing any explanation, critique, trade-off analysis, simplification proposal, or architectural conclusion about top-skill, AI must first read:

- `AI_PRELOAD_CONTEXT.md`

This file is mandatory preload context.
It exists to prevent generic but incorrect criticism that ignores the AI-first workflow, prompt/code reproducibility model, node locality, explicit interface fences, portability goals, and validator evolution model.

If `AI_PRELOAD_CONTEXT.md` was not read first, any high-level evaluation of top-skill is considered incomplete.

When modifying top-skill itself, AI must also read:

- `rules/skill-maintenance-rules.md`

This file is mandatory for changes to top-skill canon, rules, references, prompts, agents, examples, validation wording, or release metadata.

The required preload order for any first serious analysis is:
1. `AI_PRELOAD_CONTEXT.md`
2. `overview.md`
3. `QUICKSTART_FOR_AI.md`
4. `agents/index.md` and the mode-specific path
5. canon, references, and prompts as required by the task

For top-skill maintenance tasks, read `rules/skill-maintenance-rules.md` before proposing or applying changes.

---

Use it when the task involves at least one of the following topics:
- tree model;
- node hierarchy;
- state ownership through tree structure;
- spec tree;
- node specs;
- controller/content split;
- `props.contentType`;
- switchable nodes;
- dynamic switchable nodes;
- single-child mutable nodes;
- mutable child policy;
- logical parent;
- render attachment target;
- source of truth;
- spec-first / runtime-first mode;
- implementation prompt for a node;
- pipeline `spec → prompt → code → verification`.

This skill is not intended for architectural tasks in general.
It is specifically for cases where the requirement is to:
- design a system in TOP terms;
- analyze a project through the TOP model;
- build or verify TOP artifacts;
- use a prompt-based workflow on top of TOP node specs.

---

## TOP positioning

TOP must not be interpreted as a framework, runtime library,
prompt engineering technique, or merely an agent orchestration layer.

TOP is the architectural paradigm itself.
The skill, contracts, and pipeline are only the execution/guidance layer for working with it through AI.

For AI-oriented workflows, the sufficient operational unit is the pair:
- `spec + prompt`

This means that formal node structure and implementation intent must remain
sufficient for regeneration, verification, and controlled evolution,
and code must not become the sole source of truth.

TOP relies on locality of context:
a node must be maximally analyzable and generatable in local context,
relying on explicit structural contracts rather than hidden global graph knowledge.

The practical goal of this strictness is complexity control.
Without strict structural constraints, the number of significant cross-dependencies
tends to grow faster than the number of components, pushing the system toward `O(n²)`-like behavior.
TOP aims to limit this growth through typed tree discipline and bring the system toward `O(n)`-like scalability.

AI is permitted to derive, generate, regenerate, and verify within the defined model,
but must not silently invent architecture, ownership rules, or hidden graph logic in place of it.

---

## Anthem of Tree-Oriented Programming

https://youtu.be/NS0rwed0gjE

---

## License

MIT — free to use, modify, and distribute, including in commercial projects.

---

## When to use this skill

Use this skill when the task belongs to at least one of the two modes below.

### Mode 1. Architectural layer

Use the skill for:
- designing a system in TOP terms;
- analyzing existing architecture through the TOP model;
- finding architectural violations;
- decomposing composite nodes;
- determining state ownership;
- building a spec tree;
- designing the controller/content split;
- determining `props.contentType`;
- refactor-to-TOP tasks;
- explaining architecture in TOP terms.

Implementation prompts may be absent in this mode.

Primary focus:
- tree model;
- node hierarchy;
- controller/content separation;
- `props.contentType`;
- strict method semantics for runtime/lifecycle methods;
- state model;
- module boundaries;
- classification by four axes;
- logical ownership;
- source-of-truth policy.

### Mode 2. Generative layer

Use the skill for:
- preparing node specs for code generation;
- creating project-local implementation prompt files;
- building the pipeline `spec → prompt → code → verification`;
- verifying the robustness of implementation prompts;
- refining implementation prompts;
- preparing a migration path between technologies.

In this mode, the implementation prompt layer is mandatory for nodes
that are intended to be generated or regenerated through a prompt-based workflow.

---

## When NOT to use this skill

Do not use this skill if the task:
- is a routine local bugfix with no discussion of tree model, controller/content split, state ownership, or source of truth;
- is a general question about Flutter, React, TypeScript, a UI framework, or language syntax without TOP context;
- is a purely algorithmic or data-structure task outside TOP;
- concerns only code style, naming, formatting, or linting;
- describes a plain component hierarchy without semantic TOP-tree;
- requires only code generation but with no node specs, TOP artifacts, or TOP terminology.

---

## Out of scope / near-miss cases

The following tasks may appear similar but do not by themselves imply that this skill is needed:

- a plain project file hierarchy;
- a state machine without a tree model;
- a plain UI component tree without TOP semantics;
- a plain JSON schema without a node model;
- plain prompt engineering without TOP node specs;
- a plain code generation pipeline without TOP artifacts;
- a general discussion about "architecture" where nodes, branches, ownership, states, or tree decomposition are not involved.

If TOP is not explicitly present but the task is very close in meaning, the skill may be used only if the task is first interpreted through the TOP model.

---

## Activation cues

Strong signals for activating the skill:
- "TOP"
- "Tree-Oriented Programming"
- "tree model"
- "spec tree"
- "node spec"
- "controller/content split"
- "props.contentType"
- "view vs component"
- "state holder"
- "state node"
- "dynamic switchable"
- "single-child mutable"
- "childrenType"
- "logical parent"
- "render attachment"
- "source of truth"
- "spec-first"
- "runtime-first"
- "implementation prompt for node"
- "project-local TOP artifacts"
- "refactor to TOP"

---

## Core ideas

1. The system is described as a tree, not a graph.
2. State is defined through tree structure.
3. Composite nodes are decomposed into semantic child nodes.
4. State belongs to the owner node, not necessarily to the control element.
5. Code is not the sole source of truth.
6. For prompt-based generation, a separate implementation prompt layer is introduced between node spec and code.
6a. Implementation prompts must keep behavioral sections platform-neutral. Platform-specific details belong only in `Platform implementation notes`; these notes may inform another target technology, but must not be copied mechanically across platforms.
7. Logical ownership and render placement must not be mixed.
8. Runtime mutation requires an explicit source-of-truth policy.
9. Every node always has a controller.
10. If a node has content, the content must be separated from the controller and hidden behind it.
11. The controller is the sole external interface of the node.
12. Between controller and content only explicitly defined closed protocol boundaries operate. The internal implementation of either side is not a communication channel. Any other approach is strictly forbidden.
12a. Pull-Based Construction / Locality of Object Birth is foundational: a TOP object is constructed at the exact place where it architecturally belongs in the tree. A node constructor receives exactly one semantic argument: its parent reference. For a root node, the parent may be `null` or a special `RootContext`, but `RootContext` is only a root ownership/bootstrap marker. It must not become a generic dependency injection container and must not pass application data, callbacks, services, stores, child instances, view fragments, or arbitrary props into the tree. A parent node/controller owns its direct children and constructs them at their tree positions. Objects are not assembled outside the tree and pushed inward.
12b. A Content/View constructor receives exactly one semantic argument: a narrow typed access interface implemented by its owning node/controller. The constructor must not receive the concrete node/controller as its concrete class type. The runtime object must be the owning controller instance typed only through the narrow access interface. If Content/View has no permitted calls to the controller, this is an empty zero-contract access interface implemented by the owning controller; a separate dummy `ControllerAccessZero` object is not a valid substitute. Content/View must not receive additional data, callbacks, handlers, flags, state, stores, services, child components, slots, prebuilt view fragments, platform child views, child view handles, child-output getter bundles, view-model objects, config/options/props-like objects, parameter bags, runtime argument sets, or arbitrary props. This rule is technology-independent: moving the same semantic input into any public runtime parameter, render/build parameter, component/native/platform field, composition mechanism, or other technology-specific entrypoint is still the same violation. If a technology materializes Content through one public runtime input object/value, that input must be exactly the narrow owner access contract and nothing else. It is not a general props/config/data/composition bag. Any other approach is push-based composition and is strictly forbidden.
12c. Content pulls from owner; owner pulls from children when child output is architecturally required; children expose opaque handles. If content needs data, actions, state, or visual child output, it requests them from its owning controller through the narrow access interface. The owning controller obtains direct child handles from direct child controllers through their public APIs and returns only opaque placement handles to its own content. The content may place returned opaque handles, but must not construct, import, inspect, downcast, or own child nodes/controllers. Child-output access method names on the narrow owner access interface must identify the semantic child branch/output, for example `getAccountIdentityView()`, `getOrganizationsAccessView()`, `getAppPreferencesView()`, or `getDebugAdminToolsView()`. Do not require artificial suffixes such as `Handle` or `ViewHandle`; do not require `Section` unless the branch is actually modeled as a section; do not use `slot` terminology. Generic `children`, `slot`, `render`, or framework-composition names are not valid TOP access names.
12d. Controller Role Purity is foundational: a TOP controller must remain only a controller. It may contain orchestration, coordination, lifecycle, state-transition, validation, routing, async-flow, child-management, and domain decision logic when that logic belongs to the node responsibility. It must not become, extend, implement, replace, or be materialized as content, view, component, renderable artifact, render/build function, layout/style/animation/content artifact, platform UI lifecycle object, or public runtime input receiver for content composition. A controller may own and coordinate content through `IContentAccess` and may expose opaque output handles where canon allows parent-owned placement, but the controller itself must not participate in the platform rendering lifecycle. Controller complexity may be a design smell; controller role leakage is a structural violation.
13. If a node has a separate content class/object, the public node surface of the node/controller faces outward, while two separate access protocols operate internally: `IContentAccess` for the controller's access to content and `IControllerAccess` for content access to the controller. The controller must store and use content through `IContentAccess`, not through the concrete content class. The public node surface is not required to be materialized as a separate protocol artifact. Mixing the public node surface with internal access protocols, exposing the concrete content surface to the controller, or substituting direct access for these directions is strictly forbidden.
14. Content has no architectural will and does not gain access to the public node surface. Content may execute low-level platform commands that belong to its own concrete implementation, including subscribe, unsubscribe, show, hide, and response to platform events. Any semantic event, state change request, lifecycle decision, structural decision, or orchestration request must go to the controller only through `IControllerAccess`. Content must not use these platform commands as a surrogate external interaction channel. Any other approach is strictly forbidden.
15. If a node has a separate content class/object, `IContentAccess` and `IControllerAccess` must be explicit, narrow, and typed as strictly as the language permits. Their typing must be materialized in the code as separate named contract artifacts or other explicitly designated typed protocol boundaries allowed by the technology, and as explicitly typed boundaries in signatures, fields, and references where these access artifacts are passed or stored. `IContentAccess` is especially required when content wraps a large platform component, widget, native view, or third-party object: the controller may use only the small allowed surface, even if the concrete content object exposes many public methods. An implicit, anonymous, shape-only parameter/object, externally assembled access bundle, parameter bag, props-like object, config/options object, callbacks/handlers bundle, child-output getter bundle, full concrete content type, full concrete controller type, or dummy zero-access object is not a valid materialization of a protocol. Methods exposed through `IControllerAccess` must be controller-boundary methods owned by the controller. A controller-boundary method may delegate internally to utilities, services, stores, or platform APIs, but Content must not receive a raw imported function, externally owned method reference, service method, store action, or callback as the access method itself. These internal access protocols must be hidden from the outside world to the extent the technology allows. The public node surface is not considered one of these internal access protocols. Any other approach is strictly forbidden.
16. Content interacts with its owning controller only through `IControllerAccess`. If content is visual and needs child visual output, that output may only be requested through explicitly declared `IControllerAccess` endpoints. An ordinary visual node works only with explicitly declared named child-view endpoints. Iterating over `children` for repeated rendering is permitted only inside a separate `DynamicCollectionViewNode` explicitly described by the node contract. Any other approach is strictly forbidden.
17. Content lifecycle is controlled by the controller: a runtime content instance is created only when actually needed and destroyed when the node/branch becomes inactive, unless a special retention pattern is explicitly defined. Any other approach is strictly forbidden by default.
18. The top-level schema node must remain minimal and stable.
19. Additional, project-specific, and descriptive node properties are placed in `props`, not added as new top-level fields.
20. If a node has content and its type needs to be explicitly recorded in the spec, use `props.contentType`, not a top-level `contentType`.
21. Runtime/lifecycle methods must preserve strict purpose. A method intended for building child nodes cannot be used as a general init method for the controller. Any other approach is strictly forbidden.
22. A platform primitive owned by content may execute commands — subscribe, unsubscribe, show, hide, respond to platform events, and perform analogous low-level platform operations. It must not make architectural decisions, interpret events as system commands, or choose lifecycle/structure/orchestration outcomes. Execution is permitted; decision-making is forbidden.
23. A visual node may expose a general opaque view handle through `getView()` when this is required for parent-owned materialization. The parent may use this handle only as a materialization unit: mount, unmount, insert, reorder, replace, or make it available to the parent's own Content/View only through the declared owner access boundary or through an explicitly permitted parent-owned placement command. This must not become constructor injection, runtime-prop injection, slot injection, or any other push-based composition channel. The parent must not inspect the handle, attach event listeners to it, mutate its styles/classes/attributes, query inside it, or use its platform API as a behavior or communication channel. Any operation other than placement/composition must go through the child's public node surface or an explicit boundary owned by that child.
24. A controller must not access its own content platform primitive directly. Platform operations on the node's own visual/content implementation must be executed only through explicitly named `this.content.<command>(...)` methods defined by `IContentAccess`. Direct controller usage of the node's own render/view/native primitive, its platform API, or any equivalent exposed primitive handle is a confirmed content-boundary violation, except inside the implementation of `getView()` itself and parent-owned placement/composition code that handles a child view as an opaque handle. Detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()` — these are platform-specific illustrations, not canonical model terms.
25. In generated node implementation materialization, declaration/file organization must follow architectural depth from outside to inside. The controller/node class is declared or exposed first because it is the external surface of the node. Internal access boundary artifacts used between controller and content are declared next: `IContentAccess` for controller-to-content access and `IControllerAccess` for content-to-controller access. Only after these boundary artifacts may the hidden content/view implementation be declared or exposed. For a one-file node implementation the canonical order is: `Controller/Node` -> `IContentAccess` + `IControllerAccess` (or explicit zero-contract declaration where one direction is intentionally empty) -> `Content/View`. If a technology or project convention requires one-class-per-file or otherwise splits a node implementation across multiple files, this is allowed, but the same outside-to-inside dependency direction must be preserved in file structure and exports.
26. A lib subtree does not automatically break upward guaranteed access. `findUpByType()` through a lib deployment remains permitted when the full parent chain to the target ancestor is explicitly typed and architecturally guaranteed. If the deployment context is untyped, variable, external, or otherwise not guaranteed, the dependency must be provided through a connector, typed contract, interface, or equivalent boundary artifact.
27. Implementation prompts bind to generated implementation artifacts by an extensionless primary artifact stem in `sourcePath`, for example `src/pane/tree_item/tree_item.top`. The `.top` segment is the stable TOP artifact marker. Concrete platform extensions such as `.js`, `.ts`, `.tsx`, `.swift`, or `.dart` are target-specific materialization details and must not be hardcoded in platform-neutral TOP fronts.
28. One implementation prompt describes one semantic node, not necessarily one physical file or one class. The prompt's `Expected Materialization` section must declare the primary artifact stem, public node class, materialization policy, internal contracts, and companion artifact stems if the node is split across multiple files. Companion artifacts are allowed when required by target technology, project convention, one-class-per-file rules, or clarity of controller/content/contract separation.
29. If a node has separate content, both internal directions must be accounted for in materialization: controller-to-content (`IContentAccess`) and content-to-controller (`IControllerAccess`). If content-to-controller has no permitted calls, the prompt and generated materialization must declare an empty `IControllerAccess` zero-contract implemented by the owning controller; Content/View is still constructed as `new Content(this)` with `this` typed only as that access interface. If controller-to-content has no permitted calls, an empty `IContentAccess` zero-contract must still hide the concrete content class from the controller where the technology can express that boundary. Passing raw callbacks, anonymous objects, dummy zero-access objects, or the full concrete controller/content object is not a valid substitute where the technology can materialize a named typed contract.
30. Validation and review must be fresh. The validator/reviewer must load the current skill files required by the active task and must re-read the target artifacts being judged in the current validation pass. Prior session reads, previous generation context, memory of older skill versions, or earlier inspections of target files are not valid evidence. If a report lists a file as checked, it must have been read for that pass. Anything else is a workflow gap and the validation is incomplete.

Normative chain for the generative layer:

```text
tree model → node specs → project-local TOP artifacts → generated code → verification loop
```

---

## Fixed node schema and `props`

The top-level schema node must remain minimal and stable.

This means:
- new project-specific node properties are not added as separate top-level fields;
- node spec extension happens through `props`;
- `props` is the primary extension point for descriptive, classification, and project-local metadata.

TOP spec props are declarative metadata in the TOP specification. They are not runtime parameters, component fields, platform fields, render/build parameters, or any other technology-specific input channel. Fields such as `props.source`, `props.dir`, and `props.contentType` describe the model; they do not authorize props-based composition or external assembly.


### `props.materializationPolicy`

For an executable application, the top-level application root is normally materialized as the runtime composition root. During incremental migration or staged generation, a project may explicitly mark that root as pending, delegated, externally provided, or otherwise not yet materialized; the policy must make that status verifiable.

Child branches of the application root do not all have to be materialized in the same way.

A branch may be materialized as runtime nodes, used as source/model input, used during generation, compiled into target-specific artifacts, provided by external infrastructure, or handled by another explicitly described project/target policy.

The list of materialization policies is open. The following examples are common policies, not a closed taxonomy:
- runtime branch;
- source/model branch;
- generation-support branch;
- runtime-library-reference branch;
- target-optional runtime branch;
- target-compiled branch;
- externally provided branch;
- model-only branch.

`Library`, `Assets`, and `Presentation` are examples of branches that often use different policies from the main executable feature branch. They are not special hardcoded exceptions and are not the only possible branches of the application root.

Projects may record this policy in `props.materializationPolicy` or an equivalent project-local `props` field. The selected policy must be explicit enough for verification: an agent must be able to decide whether the branch is expected to appear as runtime nodes, as generated target artifacts, as source/model artifacts, or as another declared form.

If a branch is present in JSON but not materialized as runtime nodes, this is not drift by itself. It becomes drift only when the declared materialization policy says it should be runtime-materialized, or when no policy exists and the surrounding docs/prompts imply runtime materialization.
### `props.contentType`
For a node with content, the content type is recorded in `props.contentType` when necessary, not in a separate top-level `contentType` field.

Canonical values:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

---

## What is the controller/content split

### Controller
The controller always exists.

It:
- is the external interface of the node;
- receives events from content;
- manages state and runtime behavior;
- orchestrates propagation and re-rendering;
- exposes only the permitted abstract interface of the node to the outside.

### Content
If a node has content, it must be extracted into a separate concrete content class.

Exactly one concrete content class is permitted per node.

Concrete content:
- is hidden;
- is not the external interface of the node;
- interacts with the outside world only through the controller.

### `view`
Locally implemented content of this node.

### `component`
Black-box content of this node.
May operate by its own internal rules, but remains hidden behind the node controller from the outside world.

---

## Where project artifacts are stored

### Root directory for TOP artifacts

All project TOP artifacts must be stored in a separate directory:

```text
top/
```

This directory is located at the root of the project and contains:
- JSON tree descriptions;
- project-local prompt files;
- optional project-local source assets under `top/assets/`;
- optional project-local presentation source artifacts under `top/presentation/`;
- module-level TOP artifacts when needed.

`top/` is the model and implementation prompts layer.
Application code and generated code artifacts may be stored outside `top/`
in the technology directories of the project.

### JSON tree descriptions

Spec tree files must be stored as `.json` files inside the `top/` directory.

### Project-local source assets

If prompts, examples, fixtures, or demo runtime data depend on non-code source material,
store that material under `top/assets/` and reference it explicitly. Generated code must not
hide canonical demo/source data as unexplained hardcoded literals when that data is part of
the TOP project description.
All files under `top/assets/` must also be described in the project JSON tree under a
model-only `Assets` branch. Asset nodes use `props.assetPath` for the concrete file path
relative to `top/`; use `props.contentType` and `props.format` when the asset role or format
must be explicit.

### Project-local presentation artifacts

If prompts, examples, themes, style references, design tokens, or user styling inputs depend
on non-code presentation source material, store that material under `top/presentation/` and
describe it in the project JSON tree under a `Presentation` branch or another explicitly named
presentation branch.

Presentation nodes use `props.presentationPath` for the concrete file path relative to `top/`.
Use `props.contentType: "presentation"`, `props.format`, and `props.role` when the artifact
role or format must be explicit.

Presentation artifacts must use a project/platform-neutral TOP presentation format. They are
source descriptions for generation or runtime interpretation. A generator/AI must interpret
them into a platform-neutral presentation model and then materialize the target implementation
according to the branch materialization policy.

When importing an existing project, convert the source project's styling system into the TOP
presentation format first. For example, imported web styles or imported native theme/style
objects are analyzed and represented as TOP presentation tokens, roles, states, and rules.
After import, generation works from the TOP presentation model, not from the original
platform source.

When the `Presentation` branch is materialized as runtime nodes, it follows the same TOP/Q-oriented
rules as other runtime subtrees: controller/content separation, typed internal contracts,
lifecycle rules, and explicit child topology. When it is compiled into target-specific artifacts,
provided externally, or handled as source/model input, that policy must be explicit and feature
branches must still obtain presentation through the declared target-appropriate boundary rather
than by directly reading `top/presentation` files or traversing Presentation internals.

### Where prompt files are stored

Implementation prompt files are stored **inside the project**, not in the skill.

They must:
- be located inside the `top/` directory;
- sit alongside the JSON description of the corresponding tree or branch;
- be stored in a `prompts/` folder;
- be project-local artifacts;
- be referenced from the node spec via the `prompt` field.

### Prompt portability rule

Behavioral sections of an implementation prompt must describe platform-neutral node semantics:
responsibility, inputs/events, state ownership, lifecycle, child interaction, side effects,
constraints, invariants, and non-goals.

Technology-specific details must be isolated in `Platform implementation notes`.
These notes are explanatory context for the current platform. A generator targeting another
technology may use them to understand implementation pressures, edge cases, and likely pitfalls,
but must make an independent target-appropriate decision. It must not create a mechanical copy
of React, DOM, SwiftUI, Flutter, or any other platform-specific mechanism unless that mechanism
is explicitly required by the target platform.

### Where generated class files are stored

Generated class files must be placed in directories
that mirror the tree or branch organization structure of the project.

For this purpose, the node spec `props` uses the field:

```json
{
  "props": {
    "dir": "editor/tree-items"
  }
}
```

`props.dir` specifies the relative directory path for the generated artifacts of this node.

If `dir` is set on a parent node, this path is inherited by all descendants until overridden.
There is no need to repeat the same `dir` in child nodes.

Important:
- `top/` stores the model and prompts;
- `props.dir` controls the placement of generated code artifacts;
- generated code is not required to be stored inside `top/`.

---

## Reading order

Always read in the following order:

1. `overview.md`
2. `glossary.md`
3. `references/paradigm-definition.md`
4. `references/paradigm.md`
5. `references/core-principles.md`
6. `references/architecture-rules.md`
7. `references/tree-model.md`
8. `references/three-trees.md`
9. `references/node-model-definition.md`
10. `references/node-model.md`
11. `references/runtime-model.md`
12. `references/analysis-rules.md`
13. `references/node-validation-rules.md`

If the task relates to the generative layer, additionally read:

1. `references/code-generation.md`
2. `references/node-implementation-prompt.md`
3. `references/node-implementation-prompts.md`
4. `references/prompt-verification-loop.md`

If the task involves deeper analysis of mutable/runtime-heavy systems,
additionally read as needed:

1. `references/logical-vs-materialized-structure.md`
2. `references/state-holder-api.md`
3. `references/tree-node-contracts.md`
4. `references/dynamic-collection-view-node.md`
5. `references/source-of-truth-and-serialization.md`
6. `references/core-vs-skill-conventions.md`
7. `references/pattern-cards.md`
8. `references/anti-patterns.md`
9. `references/artifact-layout-and-branch-derivation.md`

---

## Using prompts

### Architectural prompts

Use these prompts for the architectural layer:

- `prompts/generate-top-node.md`
- `prompts/generate-top-tree.md`
- `prompts/analyze-top-project.md`
- `prompts/refactor-to-top.md`
- `prompts/explain-top-architecture.md`
- `prompts/derive-top-artifact-layout.md`

### Generative prompts

Use these prompts for the implementation prompt layer and code generation pipeline:

- `prompts/generate-node-implementation-prompt.md`
- `prompts/verify-node-implementation-prompt.md`
- `prompts/design-node-prompt-pipeline.md`

---

## Workflows

Mode-specific execution steps are defined in `rules/task-modes.md`.

- `modeling-refactor` — architectural workflow steps
- `generation-pipeline` — generative workflow steps

---

## What must always be checked

### For the architectural layer
- graph-like violations
- hardcoded navigation chains
- mixed mutable / immutable children
- mixed switchable / non-switchable children
- dynamic switchable nodes without explicit candidate-set, selection, source-of-truth, and active-child removal policy
- incorrect state ownership
- monolithic composite nodes
- missing semantic decomposition
- confusion between logical ownership and render placement
- missing source-of-truth policy in mutable/runtime-heavy branches
- every node has a controller
- controller/content split for nodes with content
- `props.contentType` present for nodes with content where the content type must be explicitly recorded
- correct distinction between `view` and `component`

### For the generative layer
- every code-generated node has a `prompt`
- prompt is a project-local artifact
- prompt is stored inside `top/` in a `prompts/` folder alongside the corresponding JSON spec or branch spec
- spec uses `.json` inside `top/`
- `props.dir` is set for the node where needed
- prompt and code do not diverge
- code and JSON spec topology do not diverge: every child materialized through any child materialization point is represented in JSON `children` or an external subtree resolved through `props.source`; every JSON child is materialized in code or explicitly marked as `props.lib`, a model-only branch, or a deferred/runtime creation policy; and child order is verified where order is meaningful
- after any change to `src/`, generated artifacts, JSON specs, prompts, `top/assets/`, `top/presentation/`, `top/semantic/`, or persisted `top/adaptations/`, run a drift check before finalizing the task
- after any repair that changes synchronized artifacts, route through Spec Sync Agent before Validation; direct Repair -> Validation is allowed only when the repair changed no synchronized artifact or only updated analysis/metadata outside the TOP artifact chain
- verification loop is bounded by attempt count
- escalation path is explicitly defined
- lifecycle semantics are not lost during regeneration
- render attachment model is recorded where it is non-trivial
- source-of-truth policy is recorded where the node participates in mutable runtime behavior
- controller/content split is maintained in generated architecture
- non-visual content does not leak outward as a public content object

---

## What constitutes a good result

A good result for the architectural layer:
- a correct tree model exists;
- no basic architectural violations;
- composite nodes are decomposed;
- owner state is correctly identified;
- logical ownership is separated from render placement;
- source of truth is defined for mutable/runtime-heavy parts;
- controller/content split is described correctly;
- `props.contentType` is defined for nodes with content where the content type must be explicitly recorded.

A good result for the generative layer:
- node spec is correct;
- prompt is stored in `top/`;
- generated code is placed predictably;
- verification loop is stable;
- prompt remains the source of truth for node implementation;
- behavioral prompt sections remain platform-neutral, while technology-specific details are isolated in `Platform implementation notes`;
- generated architecture does not mix controller and concrete content.

---

## Important constraints

- Do not mix the four classification axes.
- Do not substitute switchable / dynamic switchable / mutable / single-child mutable patterns for one another.
- Do not assume control owner state automatically.
- Do not mix logical ownership and render placement.
- Do not leave runtime mutation without a source-of-truth policy.
- Do not assemble TOP objects outside their architectural position and push them inward through constructor parameters, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, prebuilt fragments, platform child views, child-output getter bundles, or child view handles.
- Do not type a Content/View against the concrete controller class. The public constructor of concrete TOP Content/View receives exactly one semantic argument: a narrow typed access interface implemented by the owning controller. Internal platform/base constructor mechanics inside the Content/View implementation are allowed only when they do not become an external injection channel.
- Do not create separate dummy zero-access objects for Content/View constructors. A zero-contract is an empty narrow access interface implemented by the owning controller; Content/View is constructed with the owning controller instance typed only as that interface.
- Do not store or use concrete content/view classes from the controller when a separate content boundary exists. The controller must hold content through `IContentAccess`, which exposes only the allowed commands and opaque placement output.
- Do not treat TOP spec `props` as runtime inputs. Spec props are declarative metadata, not a composition mechanism.

- Do not use `buildChildren()` as a general init method for the controller. If runtime child construction is absent, `buildChildren()` must not exist in the class. Any other approach is strictly forbidden.
- Do not store project-local implementation prompts inside the skill.
- Do not place platform-specific implementation details in behavioral prompt sections. Put them only in `Platform implementation notes`.
- Do not mechanically transfer `Platform implementation notes` from one technology to another; use them as context and choose the target-appropriate implementation independently.
- Spec tree descriptions must be stored as `.json` inside `top/`.
- Do not make the verification loop infinite.
- Do not fix only the code while leaving the prompt outdated.
- Do not merge controller and concrete content into one class where content exists.
- Do not treat the public node surface as a mandatory separate protocol artifact: the node/controller itself may serve as the public external surface of the node if the technology and architecture do not require separate materialization.
- If a node has content, explicit internal access boundaries `IContentAccess` and `IControllerAccess` must exist, materialized as explicitly and strictly as the technology allows.
- If a node has content, the controller has no right to work directly with the concrete implementation bypassing the content object and its external interface. A public/base-class primitive getter does not legitimize such a bypass.
- A general opaque view handle returned by `getView()` is permitted when required for parent-owned materialization. The handle may be used only for placement/composition: mount, unmount, insert, reorder, replace, or passing into the parent's own content boundary. The controller must not inspect it, attach event listeners to it, mutate its styles/classes/attributes, query inside it, or use its platform API as a behavior or communication channel. The concrete platform primitive owned by content must not become part of `IContentAccess` except as this opaque view handle for placement/composition.
- A controller must perform operations on its own content only through named `this.content.<command>(...)` methods. Direct usage of the node's own render/view/native primitive, its platform API, or an equivalent exposed primitive handle in controller code is a confirmed violation. Detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()` — these are platform-specific illustrations, not canonical model terms.
- Generated node implementation declarations must be ordered from outside to inside: controller/node first, internal access boundary artifact(s) next, hidden content/view implementation last. Do not put the content/view class before the access boundary that stands between controller and content.
- A lib subtree does not automatically break guaranteed upward access. Direct `findUpByType()` through a lib deployment is permitted when the deployment chain is explicitly typed and the target ancestor is architecturally guaranteed; otherwise use a connector or typed contract.
- After generation/refactor, node validation rules must be run without fail, and re-validation performed after each fix.
- Do not expose concrete non-visual content externally.

---

## Execution model

This skill operates as a staged agent pipeline.

Primary workflow is defined in:

- `agents/index.md`

All tasks must follow the defined pipeline and may not skip required stages.

Agents must operate strictly within their roles and follow:

- `canon/core-axioms.md`
- `canon/validation-rules.md`
- `contracts/*`

Pipeline execution is mandatory.
Result is invalid if:
- required stages are skipped
- validation is not performed
- canonical rules are violated


## Decision discipline

Decision and ambiguity handling must follow:

- `rules/decision-trees.md`
- `rules/ambiguity-resolution-rules.md`

No stage may resolve ambiguity implicitly or skip mandatory decision gates.


## Platform-neutral semantic generation

Generation must preserve intent, not source-platform primitives.

TOP uses three layers:

1. **Layer A — TOP Structural Truth**: nodes, controllers, content, states, relationships, lifecycle, invariants.
2. **Layer B — Platform-Neutral Semantic UI Layer**: element purpose, user intent, system intent, interaction intent, feedback intent, layout intent, state model, constraints, and accessibility semantics.
3. **Layer C — Target Adaptation Layer**: temporary target-native mapping of Layer B to target primitives, interactions, layout, and constraints.

Layer A and Layer B are source truth. Persisted Layer B artifacts live under `top/semantic/**/*.semantic.json`. Layer C is derived, target-specific, temporary, and replaceable; when persisted for handoff or review, it lives under `top/adaptations/<target>/**/*.adaptation.json`.

Platform artifacts such as DOM, CSS, Flutter widgets, UIKit/Android classes, framework APIs, and source-platform event names must not become Layer B truth. They may be used only as source evidence for Semantic Interpreter or as current-target notes.

In `generation-pipeline`, the required target path is:

`Canon Precheck -> Semantic Interpreter -> Target Adaptation -> Generation -> Spec Sync -> Validation -> Final Audit`

Target adaptation must record whether each semantic element is preserved, adapted, or dropped. Adapted and dropped decisions require reasons. Business logic must never be introduced during adaptation.
## Official task modes

The execution model must use the official task modes:

- `analysis-only`
- `modeling-refactor`
- `generation-pipeline`
- `spec-change`

Detailed rules are defined in:
- `rules/task-modes.md`

A single universal pipeline does not apply to all tasks automatically.

Generation is mandatory only for `generation-pipeline`.
Analysis-only and modeling-refactor tasks remain valid without a Generation stage if their own mode pipeline has been completed in full.

## Learning / onboarding entrypoint

A separate onboarding layer is available for a user's first introduction to TOP:

- `onboarding/README.md`
- `onboarding/top-learning-agent.md`

This layer does not replace the main skill pipeline.
It is used only for introductory explanation and subsequent Q&A on the basic ideas of TOP.

## Minimum viable read paths

A shortened mandatory read path is used for frequent tasks.

See:
- `QUICKSTART_MIN_READS.md`

A full pre-read of all operational files is not required for every minor task.

For validation, review, migration repair, or any task that judges architectural
correctness, the shortened read path is not enough by itself. The agent must
load the current canon, validation rules, violation catalog, review/typing
checklists, and the references directly named by those rules for the artifact
under review. It must also re-read the target artifacts in the current pass.
Older session reads or remembered rules do not count as validation evidence.

## Schema-first contracts

Contracts have schema-first status.

This means:
- required output fields are defined only in `contracts/agent-output-contracts/*`
- agent files are not an alternative source of output schema
- orchestration and handoff validation must rely on contract files

## Recommended orchestration fields

The following fields should be used consistently across relevant contracts where applicable:

- `task_mode`
- `proposed_tier`
- `effective_tier`
- `allowed_next_stage`
- `block_reason`

This improves schema consistency and orchestration reliability.
