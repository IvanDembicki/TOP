# Spec Sync Rules

Rules for detecting and classifying discrepancies between code and the `top/` folder.

## Sources of truth

- **`top/` JSON specs** — the source of truth for the architectural tree, node roles, props, declared external subtrees, assets, and presentation artifacts.
- **Implementation prompts** — the source of truth for node behavior, lifecycle, child interaction rules, constraints, invariants, and expected materialization.
- **Generated/materialized code** — the target-platform materialization that must conform to the current spec and prompts.

If there is a discrepancy, classify it as drift first. Do not assume automatically that code wins or that `top/` wins. The correction direction depends on the active task mode:
- in `generation-pipeline`, update generated/materialized artifacts from the approved `top/` model and prompts, then sync any legitimately discovered materialization details back into prompts;
- after manual code repair or migration, update `top/` only when the code change represents an approved architectural/materialization change;
- in `spec-change`, verify or update code against the changed spec according to `references/spec-change-verification.md`.

## Discrepancy classification

### missing_in_spec
A node exists in code but is absent from `top/tree_editor.json` or has no prompt file.

Indicators:
- A class in `src/` has no corresponding entry in JSON
- A JSON entry exists, but the `prompt` file does not
- A JSON entry uses `props.source`, but the external spec file does not exist

### orphan_in_spec
A node is described in `top/` but does not exist in code.

Indicators:
- JSON contains an entry with a `type` for which no class exists in `src/`
- A prompt file exists, but the corresponding class has been deleted or renamed

### role_mismatch
The architectural role of the node in code does not match the description in JSON or prompt.

Indicators:
- Node declared with one base role in prompt, but extends or materializes a different base role in code
- Node described as a leaf, but in code is a holder (has state children)
- `doc` in JSON describes an outdated responsibility

### structural_mismatch
The child node structure in code does not match `children` in JSON.

Indicators:
- Code materializes child nodes at a child materialization point not listed in JSON `children`
- JSON `children` lists nodes that are not materialized by code and are not explained by an explicit materialization policy such as deferred, source/model, generation-support, target-compiled, externally provided, model-only, or another project/target policy
- Order of children in JSON does not match the static materialization order where order is meaningful

### stale_prompt
The prompt describes behavior that is no longer implemented.

Indicators:
- Prompt mentions a method that does not exist in the class
- Prompt describes a visibility condition that has changed
- Prompt references `isEditMode`, but the class no longer reads it
- Prompt describes a delegation that has moved to another node

### broken_reference
The prompt contains incorrect technical references.

Indicators:
- Incorrect class name, artifact stem, materialization policy, internal contract, or companion artifact reference in "Expected Materialization"
- Incorrect file path
- Reference to a non-existent base class

### noncanonical_top_layout
Project-local TOP artifacts were created outside the canonical layout.

Indicators:
- A new migration branch spec exists as an ad hoc root-level file such as
  `top/settings-branch.json` instead of `top/specs/settings-branch.json`
- Implementation prompts exist without a matching branch spec under `top/specs/`
- Migration status exists outside `top/migration/` without an established
  project-local convention

### missing_source_root
Specs or prompts declare implementation materialization, but the implementation
source root is missing, undeclared, or inconsistent.

Indicators:
- Expected Materialization sections name artifact stems, but no
  `props.sourceRoot`, default `top_src/`, or project-approved source root is
  recorded
- A migration/modeling pass creates implementation prompts but does not create
  `top_src/<branch-id>/` or an equivalent declared root
- `props.dir` paths and prompt artifact stems resolve to different source roots

### missing_migration_control_plane
A migration-mode task lacks required plan/status/log artifacts or the log was
not updated for a handoff/change.

Indicators:
- `top/migration/MIGRATION_PLAN.md` is missing or does not mention the current scope
- `top/migration/MIGRATION_WORKFLOW.json` is missing, invalid JSON, or does not
  mention the current scope and phase
- `top/migration/MIGRATION_LOG.md` is missing
- artifact changes occurred without a new log entry
- old log entries were rewritten instead of appending corrections

### platform_leak
The prompt contains platform-dependent elements in behavioral sections.

Indicators:
- HTML tags, CSS properties, DOM API in sections 1–9
- Specific language/runtime methods outside "Platform implementation notes"
- Violation of rules from `rules/prompt-writing-rules.md`

## Severity

| Class | Severity | Reason |
|---|---|---|
| missing_in_spec | HIGH | spec is incomplete, regeneration will produce an incomplete result |
| orphan_in_spec | MEDIUM | spec contains garbage, may mislead the agent |
| role_mismatch | HIGH | regeneration from prompt will produce incorrect architecture |
| structural_mismatch | HIGH | tree in spec does not match the real tree |
| stale_prompt | HIGH | regeneration from prompt will produce outdated behavior |
| broken_reference | MEDIUM | generation may create a file with incorrect name/path |
| noncanonical_top_layout | HIGH | future agents may not hydrate, validate, or regenerate the branch consistently |
| missing_source_root | HIGH | generation has no canonical place to materialize TOP implementation artifacts |
| missing_migration_control_plane | HIGH | migration cannot be replayed or diagnosed and downstream agents lack a reliable plan |
| platform_leak | MEDIUM | prompt is not portable, but may be functionally accurate |

## Application protocol

Spec Audit Agent applies these rules when traversing the project.
Spec Sync Agent applies these rules to determine what needs to be updated.

When `role_mismatch` or `structural_mismatch` is detected, resolving the drift is mandatory before running the next Generation Agent. The resolution may update JSON, prompts, code, or protocol artifacts depending on the approved correction direction.

## Mandatory drift check after any artifact change

After **any** change in `src/`, generated artifacts, JSON specs, implementation prompts, `top/assets/`, `top/presentation/`, `top/semantic/`, or persisted `top/adaptations/` artifacts — regardless of task mode, reason for the change, or scope — the agent must verify whether spec, prompts, project-local TOP artifacts, semantic/adaptation artifacts, and materialized implementation still agree.

This check is mandatory even if the code compiles, tests pass, or the visible behavior appears correct.

The agent must compare:

1. Static children materialized in code:
   - target-specific child materialization methods such as `buildChildren()` when they exist;
   - constructor-time child materialization and direct child constructors receiving the current node as parent;
   - `setInitialChild(...)`, `openChild(...)`, or equivalent switchable/single-child materialization points;
   - ordered static child creation sequence.

2. Dynamic/library children materialized in code:
   - `Library.create(...)`;
   - mutable containers that create runtime child instances;
   - single-child mutable replacement points.

3. The JSON spec:
   - new migration branch specs must be under `top/specs/`, unless an existing
     project-local TOP convention is recorded in a root index;
   - every static child created in code must appear in JSON `children` or in an external subtree resolved through `props.source`;
   - every `props.source` file must exist, be resolved relative to the project `top/` directory, and describe the same node type as the node that references it;
   - every file under `top/assets/` must be described by a node under the model-only `Assets` branch using `props.assetPath`;
   - every `props.assetPath` file must exist and be resolved relative to the project `top/` directory;
   - every file under `top/presentation/` must be described by a node under a `Presentation` branch or another explicitly named presentation branch using `props.presentationPath`;
   - every persisted Layer B file under `top/semantic/` must match semantic source inputs and contain no source-platform leakage;
   - every persisted Layer C file under `top/adaptations/<target>/` must name the target and trace decisions to Layer B;
   - every `props.presentationPath` file must exist and be resolved relative to the project `top/` directory;
   - every JSON child must correspond to code, unless it is explicitly marked as `props.lib` or is described by an explicit materialization policy such as source/model, generation-support, target-optional runtime, target-compiled, externally provided, model-only, or deferred/runtime creation;
   - child order must match static creation order unless the spec explicitly defines a different ordering rule;
   - every referenced prompt file must exist.

4. The node prompts:
   - child interaction rules must match the actual child topology;
   - lifecycle descriptions must match the actual creation/open/close/mount behavior;
   - Expected Materialization must declare the implementation source root and
     artifact stems under that root;
   - `doc` strings must not describe removed or moved responsibilities.

5. The implementation source root:
   - if implementation prompts or Expected Materialization exist, the declared
     source root must exist on disk;
   - for new migration branches, the default is `top_src/<branch-id>/`;
   - if the root is intentionally empty before generation, it must contain
     `.gitkeep` or an equivalent placeholder;
   - generated TOP implementation artifacts must be under that root unless they
     are thin framework adapters explicitly declared by an integration contract.

6. The migration control plane:
   - `top/migration/MIGRATION_WORKFLOW.json`, `MIGRATION_PLAN.md`,
     `MIGRATION_STATUS.md`, and `MIGRATION_LOG.md` must exist for
     migration-mode artifact changes;
   - the workflow JSON must name the current migration scope, branch id,
     current phase, responsible agents, gates, and next phases;
   - the plan must name the active scope, branch id, agent work packages, planned
     artifacts, validation gates, and rollback/stop points;
   - the log must contain entries for each migration-mode handoff and persistent
     artifact change.

If code creates a new child node and the node is absent from JSON, classify it as both `missing_in_spec` and `structural_mismatch`.

If JSON lists a child that code no longer creates, classify it as `orphan_in_spec` or `structural_mismatch`, depending on whether the implementation was removed or moved to a different creation policy.

If topology changed intentionally, updating the relevant JSON spec and prompt files is mandatory before the task can be considered complete.

No generation, repair, refactor, or manual code change may be finalized while code ↔ spec topology drift remains unresolved.
