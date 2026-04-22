# Top Folder Contract

Defines the structure and requirements for the `top/` folder in a TOP project.

## Purpose of the `top/` folder

`top/` is the single source of truth for the project's architectural model.

Contains:
- Node tree description (`*.json`)
- Optional external subtree spec files referenced by `props.source`
- Prompt files for each node (`prompts/**/*.md`)
- Optional project-local source assets (`assets/**/*`) used by prompts, examples, fixtures, or demo data
- Optional project-local presentation artifacts (`presentation/**/*`) used as source styling/theme/materialization input
- Platform-neutral semantic artifacts (`semantic/**/*.semantic.json`) produced by Semantic Interpreter Agent
- Optional target adaptation artifacts (`adaptations/<target>/**/*.adaptation.json`) produced by Target Adaptation Agent for review, handoff, or repeatable generation

`top/` must accurately reflect the current code implementation.
If generated code depends on project-local demo data, fixtures, schema examples, or other
non-code source material, that material must be stored under `top/assets/` and referenced
explicitly. Do not hide canonical demo/source data as an unexplained literal inside generated
application code.
Every file under `top/assets/` must be described in the JSON tree under a model-only
`Assets` branch.
Every file under `top/presentation/` must be described in the JSON tree under a
`Presentation` branch with an explicit presentation materialization policy. Presentation artifacts are source descriptions that generators
interpret into an internal presentation model and then materialize for the target platform;
they are not copied or linked verbatim into generated code. Canonical files under
`top/presentation/` use a project/platform-neutral TOP presentation format. Imported styling
systems are converted into that format before they become canonical TOP presentation
artifacts.


## Semantic and adaptation artifact storage

Layer B semantic artifacts are stored under:

```text
top/semantic/**/*.semantic.json
```

These files are platform-neutral semantic source truth for generation. They must describe roles, intents, state models, feedback intent, layout intent, constraints, and accessibility semantics without target primitives.

Layer C target adaptation artifacts may be stored under:

```text
top/adaptations/<target>/**/*.adaptation.json
```

These files are derived handoff artifacts for a concrete target. They are not source truth and must not be copied back into prompts, specs, or Layer B as portable requirements.
## JSON schema for a node

Each node in `top/tree_editor.json` (or equivalent file) must have:

```json
{
  "type": "<NodeTypeName>",
  "doc": "<single line: node role>",
  "prompt": "<path to prompt file relative to top/>",
  "props": { ... },
  "children": [ ... ]
}
```

### Required fields

| Field | Requirement |
|---|---|
| `type` | Node type name without the `Node` suffix. Example: `TreeItemRow` |
| `doc` | Single line. Describes the role. Platform-neutral. |
| `prompt` | Required for nodes that are expected to generate or materialize implementation artifacts. May be omitted for source/model, generation-support, pending, externally provided, target-compiled, model-only, or other explicitly declared non-implementation policies. When present, the file must exist. |

### Optional fields

| Field | Purpose |
|---|---|
| `props.dir` | Source file directory relative to `src/` |
| `props.contentType` | Content type (`view`, `data`, etc.) |
| `props.lib` | `true` if the node is a library node |
| `props.source` | Path to an external spec file for this node, relative to `top/` |
| `props.assetRoot` | Asset root directory for an `Assets` branch, relative to `top/` |
| `props.assetPath` | Path to a concrete project-local asset file, relative to `top/` |
| `props.presentationRoot` | Presentation root directory for a `Presentation` branch, relative to `top/` |
| `props.presentationPath` | Path to a concrete presentation source artifact, relative to `top/` |
| `props.format` | Asset format when useful (`json`, `svg`, `png`, etc.) |
| `props.materializationPolicy` | Optional open project/target policy describing whether the node or branch is expected as runtime nodes, source/model input, generation support, target-compiled artifacts, externally provided infrastructure, model-only data, or another explicit policy. |
| `children` | Array of child nodes. Absent for leaf nodes. |

## Prompt file naming

Rule: `<NodeTypeName>.prompt.md`

The prompt path must reflect the node's position in the tree:
- Toolbar nodes → `prompts/toolbar/`
- Pane nodes → `prompts/pane/`
- Nested nodes → `prompts/pane/tree_item/`

## Required prompt sections

Each prompt file must contain sections in the following order:

1. Node identity and role
2. Responsibility
3. Inputs and events
4. State ownership
5. Child interaction rules
6. Lifecycle
7. Side effects
8. Constraints and invariants
9. Non-goals
10. Platform implementation notes *(optional)*
11. Expected Materialization

Sections 1-9 are behavioral sections and must be platform-neutral.
Semantic UI requirements:
- Behavioral prompt sections and JSON `doc` fields are Layer B inputs and must describe meaning, not source-platform primitives.
- Platform implementation notes may contain target-specific evidence, but that evidence is not source truth and must be passed through Semantic Interpreter before cross-target generation.
- Target-specific adaptation decisions belong to Target Adaptation output or generated target artifacts, not to platform-neutral TOP fronts.
Platform-specific implementation details are permitted only in "Platform implementation notes".
Those notes may inform another target technology about implementation pressures, edge cases,
or risks, but they are not portable behavior requirements and must not be copied mechanically
when generating for another platform.

For a prompt that describes an implementation/materialized node, the "Expected Materialization" section must contain:
- Primary artifact stem, without a platform-specific extension
- Public node class (with `Node` suffix in the default naming convention)
- Materialization policy (`one-file default`, `split`, `one-class-per-file`, or another explicit project/target policy)
- Base class or base role. If a concrete platform base class is named, it belongs to the target-specific materialization contract or Platform implementation notes.
- Internal contracts:
  - controller-to-content: named `IContentAccess`/equivalent contract, or explicit zero-contract
  - content-to-controller: named `IControllerAccess`/equivalent contract, or explicit zero-contract
- Companion artifact stems: `none` for one-file materialization, or a list of extensionless stems with each artifact's role

The artifact path/stem names the stable TOP implementation artifact, for example:

```text
src/pane/tree_item/tree_item.top
```

Concrete generated files add the target-platform extension during materialization:

```text
src/pane/tree_item/tree_item.top.*
```

Prompt metadata and "Expected Materialization" sections must not hardcode a concrete
language extension when they are part of platform-neutral TOP fronts.

One implementation prompt describes one semantic node. It does not imply that the
node must be materialized as one physical file or one class. If the target technology
or project convention uses one-class-per-file, split controller/content files, or
separate contract files, the prompt must declare the companion artifact stems and
their roles explicitly.

## Code ↔ spec correspondence

| In code | In JSON |
|---|---|
| Class name `TreeItemRowNode` | `"type": "TreeItemRow"` |
| child materialization points create N children | `children` contains N entries in the same order, unless an explicit external/deferred/model-only policy applies |
| logical node base class or role | prompt/base role: logical node |
| visual/content node base class or role | prompt/base role: visual/content node |

## Invariants

- Every prompt file referenced in JSON must exist on disk
- Every `props.source` file referenced in JSON must exist on disk and describe the same node type
- Every `props.assetPath` file referenced in JSON must exist on disk
- Every file under `top/assets/` must have a corresponding asset node under the `Assets` branch
- Every `props.presentationPath` file referenced in JSON must exist on disk
- Every file under `top/presentation/` must have a corresponding presentation node under the `Presentation` branch
- Every prompt `sourcePath` must be an extensionless implementation artifact stem; target-specific extensions belong to generation/materialization rules, so validation checks for a materialized artifact must resolve the stem through the active target's extension rules, conceptually `sourcePath + ".*"`
- Every prompt's Expected Materialization must account for the public node artifact, internal access contracts, and any companion artifacts required by the target/project materialization policy
- Every node materialized through child materialization points must have a corresponding entry in JSON `children`, an external subtree loaded through `props.source`, or an explicit materialization policy that explains deferred, source/model, target-compiled, externally provided, model-only, or other non-runtime materialization
- `doc` in JSON must not contain platform-dependent elements
- Behavioral prompt sections must not contain platform-dependent implementation details
- Every persisted Layer B artifact under `top/semantic/` must match the Semantic Interpretation Output Contract or a project-local schema derived from it
- Layer B semantic descriptions must not contain DOM/CSS/widgets/framework primitives as truth
- Layer C target adaptation artifacts under `top/adaptations/` must name their target platform explicitly
- Layer C target adaptation artifacts must not be treated as source truth
- A JSON branch that is not materialized as runtime nodes is valid when its materialization policy explicitly says so; it is drift only when the declared policy or surrounding prompts/docs imply runtime materialization.
- The prompt must not contradict the code

## Violations

Violation classification is defined in `rules/spec-sync-rules.md`.
