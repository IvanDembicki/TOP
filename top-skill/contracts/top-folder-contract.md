# Top Folder Contract

Defines the structure and requirements for the `top/` folder in a TOP project.

## Purpose of the `top/` folder

`top/` is the single source of truth for the project's architectural model.

Contains:
- Node tree descriptions (`specs/**/*.json`, plus an optional established root index such as `tree.json`)
- Optional external subtree spec files referenced by `props.source`
- Prompt files for each node (`prompts/**/*.md`)
- Migration workflow, status, plan, and handoff artifacts (`migration/**/*`)
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

## Canonical project layout

New TOP projects and new migration branches use this layout unless the repository
already has an explicit TOP convention recorded in `top/tree.json` or an equivalent
root index:

```text
top/
  specs/
    <branch-or-tree>.json
  prompts/
    <branch-or-tree>/**/*.md
  migration/
    <branch-id>/
      MIGRATION_WORKFLOW.json
      MIGRATION_PLAN.md
      GENERATOR_LEARNING_LEDGER.md
      reports/
        rejections/
    MIGRATION_STATUS.md
    MIGRATION_LOG.md
  assets/
  presentation/
  semantic/
  adaptations/<target>/
top_src/
  <branch-or-tree>/
```

`top/` is source truth. `top_src/` is the default source root for materialized
TOP implementation artifacts created during migration or generation.

New migration branch specs must be stored under `top/specs/`, for example:

```text
top/specs/settings-branch.json
```

Do not create ad hoc root-level branch specs such as `top/settings-branch.json`
for a new migration branch. A root-level `top/tree.json` may exist as an index or
aggregate tree, but branch specs belong under `top/specs/` unless an existing
project-local TOP convention explicitly says otherwise.

When a migration/modeling pass creates specs or prompts for implementation that
will be materialized later, it must also declare and prepare the implementation
source root:

- default root: `top_src/`;
- default branch root: `top_src/<branch-id>/`;
- branch specs record the root using `props.sourceRoot` at the branch or node
  level when it differs from the default;
- node `props.dir` values are resolved relative to the declared source root;
- implementation prompts' Expected Materialization sections must use artifact
  stems under the same source root;
- if no implementation files are generated yet, create the source root directory
  with `.gitkeep` or an equivalent project placeholder.

An analysis-only audit that creates no specs, prompts, or materialization plan
does not need a source root. A migration/modeling pass that writes prompts or
Expected Materialization for future code generation does.

## Migration control plane

Every migration-mode task that creates or changes project-local TOP artifacts
must maintain these files:

```text
top/migration/<branch-id>/MIGRATION_PLAN.md
top/migration/<branch-id>/MIGRATION_WORKFLOW.json
top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md
top/migration/<branch-id>/reports/**
top/migration/MIGRATION_STATUS.md
top/migration/MIGRATION_LOG.md
```

Before any migration artifact, generated source, adapter, route, integration, or
legacy source write is allowed, the migration must be running on a dedicated git
branch. The canonical branch name is:

```text
top-migration/<branch-id>
```

Migration Infrastructure Agent must inspect the current branch and git status,
create or switch to the dedicated branch, confirm the checked-out branch, and
write the first migration log entry with the git safety gate. The user's current
working branch must not receive migration writes. Remote push is forbidden
unless the user explicitly requests push. Local commits are allowed only when
requested or when a documented migration commit phase is active.

`top/migration/<branch-id>/MIGRATION_WORKFLOW.json` is the machine-readable
migration process tree for one branch. It must conform to the current `top-skill` schema
`top/schemas/migration-workflow.schema.json` and record:

- migration id, selected scope, branch id, and current phase;
- ordered phases with responsible agent, status, gates, outputs, and next phases;
- validation gates and their status;
- handoff rules;
- active, invalidated, or superseded migration decisions when they affect later work.

`top/migration/<branch-id>/MIGRATION_PLAN.md` is the explicit plan for one
branch migration effort. It must record:

- user-requested scope, if provided;
- selected migration scope and branch id;
- scope selection rationale when the user did not name the starting area;
- ordered phases and responsible agents;
- expected specs, prompts, source roots, adapters, tests, and validation gates;
- behavior preservation requirements;
- rollback and stop points;
- current phase status.

The branch workflow and branch plan must describe the same phase order and
current phase. If they disagree, validation treats the migration control plane
as stale.

`top/migration/MIGRATION_STATUS.md` records the current state of each branch and
validation result. It is shared status, not a plan and not a log. Updates must
preserve previous branch history.

`top/migration/MIGRATION_LOG.md` is shared, multi-branch, and append-only. Each
agent operating in migration mode must append an entry before handoff, and after
any persistent artifact change. Each entry must include:

- timestamp and `timestamp_source` (`real` or `placeholder`);
- agent name;
- migration phase, branch id, and migration id;
- files read;
- files created;
- files modified;
- files deleted;
- commands run;
- key decisions and why;
- accepted deviations;
- unable-to-verify items;
- potential canon risks or needs-later-validation notes;
- validation or self-check result;
- next agent, next action, or blocking condition.

The first log entry for a migration must also include:

```text
**Git safety gate:**
- initial_branch:
- migration_branch:
- branch_created:
- branch_checked_out:
- working_tree_status:
- remote_status:
- unrelated_uncommitted_changes:
- migration_writes_allowed:
- local_commit_policy:
- push_policy:
```

If a real timestamp is unavailable, write `timestamp_source: placeholder` and do
not invent identical fake forensic timestamps.

The log is for forensic replay. It must not be rewritten to make the migration
look cleaner after the fact. Corrections are new entries.

Failed validation must create a rejection ticket under the active branch reports,
for example:

```text
top/migration/<branch-id>/reports/rejections/<rejection-id>.md
```

The validator, not the generator, appends the rejection entry to
`top/migration/MIGRATION_LOG.md`. A rejection ticket must include rejection id,
validator agent, phase, attempt number, artifact under review, files checked,
canon rules checked, violation code, evidence, why the artifact is invalid,
required repair, forbidden repairs, and the return-to agent.

`top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md` is the branch-local
negative-constraint ledger for generators and repair agents. It records
rejected strategies and must be read before later generation or repair in that
branch. Repeating a rejected strategy without validator-approved justification
is a workflow violation.

Incremental validation checkpoints are public-record entries. Each micro-check,
meso-check, and macro-check must append a compact entry to
`top/migration/MIGRATION_LOG.md` or to a branch-local report referenced by the
log. Required fields are `checkpoint_id`, `checkpoint_type`, `phase`, `agent`,
`artifact`, `checks_performed`, `result`, failure evidence when applicable, and
`next_action`.

## Active migration workspace ownership

The active migration workspace is agent-owned. The legacy application remains
user-owned.

This ownership applies only within the confirmed dedicated migration git branch.
Before that branch is active, no migration writes are authorized.

Agents may create, modify, replace, and delete files required by the active
migration workflow inside branch-owned artifacts:

```text
top/specs/<branch-id>.json
top/prompts/<branch-id>/**
top/migration/<branch-id>/MIGRATION_PLAN.md
top/migration/<branch-id>/MIGRATION_WORKFLOW.json
top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md
top/migration/<branch-id>/reports/**
top/migration/<branch-id>/**
top/assets/**
top/semantic/**
top_src/<branch-id>/**
```

Shared artifacts are `top/migration/MIGRATION_LOG.md` and
`top/migration/MIGRATION_STATUS.md`. The log is append-only and multi-branch.
Shared status updates must preserve previous branch history. A new branch must
not overwrite another branch's plan, workflow, reports, prompts, spec, or
generated source. If a legacy project still uses flat
`top/migration/MIGRATION_PLAN.md` or `top/migration/MIGRATION_WORKFLOW.json`,
the agent must preserve prior branch information and explicitly log the
compatibility update.

This authority is scoped to the active branch and current
branch workflow/plan. It does not include unrelated legacy source files,
unrelated `top_src/` branches, another branch's `top/migration/<other-branch>/`
artifacts, package manifests or lock files, native iOS/Android files,
environment/secrets files, git push, or remote operations.

Legacy app files may be modified only for explicitly required thin adapter or
integration wiring. Such writes must be logged and validated as in-scope.


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
| `props.sourceRoot` | Project-relative source root for materialized TOP implementation artifacts. Defaults to `top_src` when absent. |
| `props.dir` | Source file directory relative to the declared source root. |
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
- Implementation source root (`top_src` by default, or the declared project root)
- Primary artifact stem, without a platform-specific extension
- Public node class (with `Node` suffix in the default naming convention)
- Controller role purity: public node/controller class/function is not a renderable platform artifact; renderable artifacts are content-side or adapter-side.
- Materialization policy (`one-file default`, `split`, `one-class-per-file`, or another explicit project/target policy)
- Base class or base role. If a concrete platform base class is named, it belongs to the target-specific materialization contract or Platform implementation notes.
- Internal contracts:
  - controller-to-content: named `IContentAccess`/equivalent contract, or explicit zero-contract
  - content-to-controller: named `IControllerAccess`/equivalent contract, or explicit zero-contract
- Companion artifact stems: `none` for one-file materialization, or a list of extensionless stems with each artifact's role

The artifact path/stem names the stable TOP implementation artifact, for example:

```text
top_src/pane/tree_item/tree_item.top
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
- Every new migration branch spec must live under `top/specs/` unless an established root index records a different project convention
- Every migration-mode task that creates or changes TOP artifacts must maintain
  `top/migration/<branch-id>/MIGRATION_WORKFLOW.json`,
  `top/migration/<branch-id>/MIGRATION_PLAN.md`,
  `top/migration/MIGRATION_STATUS.md`, and `top/migration/MIGRATION_LOG.md`
- Every `props.source` file referenced in JSON must exist on disk and describe the same node type
- Every `props.assetPath` file referenced in JSON must exist on disk
- Every file under `top/assets/` must have a corresponding asset node under the `Assets` branch
- Every `props.presentationPath` file referenced in JSON must exist on disk
- Every file under `top/presentation/` must have a corresponding presentation node under the `Presentation` branch
- Every prompt `sourcePath` must be an extensionless implementation artifact stem; target-specific extensions belong to generation/materialization rules, so validation checks for a materialized artifact must resolve the stem through the active target's extension rules, conceptually `sourcePath + ".*"`
- Every implementation/materialization prompt must declare the implementation source root and keep all artifact stems under that root
- Every migration/modeling pass that creates implementation prompts for future materialization must create or update the declared source root directory
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
