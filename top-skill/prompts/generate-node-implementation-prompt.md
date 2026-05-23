# Prompt: Generate Node Implementation Prompt

agent: Generation Agent

input_contract:
- node_spec
- tree_role
- state_model
- child_nodes
- expected_behavior
- semantic_layer_requirements
- target_adaptation_boundary

output_contract:
- implementation_prompt_file
- prompt_path_in_spec

rules:
- one prompt per node
- prompt must be project-local artifact
- behavioral prompt sections must be platform-neutral
- behavioral prompt sections are Layer B inputs and must not contain source-platform primitives as truth
- platform-specific details must be isolated in `Platform implementation notes`

---

Use this prompt to create the implementation prompt for a specific node.

---

## Input data

Provide:
- node spec;
- the role of the node in the tree;
- state model;
- child nodes;
- expected behavior;
- constraints;
- path to the project-local JSON spec;
- target technology context (only as additional context, not as the primary source of semantics).

---

## What to do

Generate a separate implementation prompt file for one node.
Its behavioral sections must be platform-neutral.

The implementation prompt must contain:

1. Node identity and role
2. Responsibility
3. Inputs and events
4. State ownership
5. Child interaction rules
6. Lifecycle
7. Side effects
8. Constraints and invariants
9. Non-goals
10. Platform implementation notes
11. Expected Materialization

Sections 1-9 must describe platform-neutral behavior and architecture.
Section 10 may contain technology-specific implementation notes for the current target.
Those notes may inform another technology about implementation pressures and edge cases,
but must not be copied mechanically. A generator for another platform must make an
independent target-appropriate implementation decision.
Section 11 must declare the expected materialization contract without hardcoding a concrete
platform extension in platform-neutral TOP fronts.

Also specify:
- where this prompt should be stored in the project;
- what `prompt` path should be written into the node spec;
- whether the path follows the convention `prompts/` alongside the JSON spec.
- the implementation source root (`top_src/` by default) and the primary
  artifact stem under that root.

---

## Important rules

- One prompt — one node.
- Prompt must be a project-local artifact.
- Prompt must reside in `prompts/` alongside the JSON tree/branch spec.
- New branch specs must reside under `top/specs/`; do not create ad hoc
  root-level branch specs in `top/`.
- Expected Materialization must name the implementation source root. For new
  migration branches the default is `top_src/<branch-id>/`.
- Do not duplicate the entire project.
- Do not substitute the tree structure.
- Do not place platform-specific implementation details in behavioral sections.
- Do not make platform notes portable requirements.
- Do not require another platform to copy the current platform's mechanism mechanically.
- Keep `Expected Materialization` separate from platform notes: it declares artifact stems,
  public classes/roles, internal contracts, materialization policy, and companion artifact
  stems, while concrete target extensions remain target-specific materialization details.
- Explicitly state the owner state.
- The prompt must require controller role purity: the public node/controller artifact is non-renderable and must not be the target framework view/component/widget/composable/render function, platform UI lifecycle object, or equivalent content-side artifact.
- The prompt must state whether target framework renderable artifacts belong to Content or to a thin adapter. They must not be declared as the controller.
- If the node has a separate content, the implementation prompt must require explicit internal access boundaries `IControllerAccess` and `IContentAccess`, materialized as explicitly as the technology allows. If content-to-controller has no permitted calls, the prompt must declare an empty `IControllerAccess` zero-contract implemented by the owning controller; do not request a separate dummy zero-access object. If controller-to-content has no permitted calls, the prompt must still declare an empty `IContentAccess` zero-contract where the technology can express it, or explicitly document the zero direction when the target has no stable runtime content object for the controller to store.
- The prompt must require the controller to store and use content through `IContentAccess`, not through the concrete Content class.
- The prompt must state that `IContentAccess` is not a data/view-model/state/callback bag for Content. Controller-owned data and actions used by Content belong behind `IControllerAccess` methods/accessors.
- These access artifacts must be narrow and strongly typed where the language permits. They must be materialized as named contract artifacts or other explicitly designated typed boundaries, and the constructor/factory/method parameter accepting such an artifact must have an explicit contract type. Anonymous/untyped parameters such as `constructor(facing)` without an explicit contract type are not allowed if the language can express it.
- Construction must attach TOP objects to context, not inject data. Static nodes receive only parent/context, locally implemented content receives only owning controller access, and connectors or black-box boundaries receive only their explicit boundary interface. Runtime-created branch roots may receive parent/context plus one canonical Runtime Branch Binding input: entity context reference, stable identity key, or typed immutable DTO fallback. Do not pass data packets, flags, callbacks, config/options/props-like objects, stores, services, child views, presentation values, visibility values, style values, text values, runtime state, handlers, scattered entity fields, or arbitrary extra values through constructors, runtime entrypoints, or setter-style post-construction configuration.
- Switchable holders must have at least one state/candidate child and a non-null
  `openedChild`. If no state is explicitly selected, use the first
  state/candidate child as the default opened child. Active-state
  operations/queries delegate to `openedChild`; do not generate nullable
  opened-child fallback, loops over closed state siblings, or mode/status
  branches for active behavior.
- Downward query/event propagation must be node-owned after an approved
  entrypoint. Generate node/controller methods that decide locally whether to
  answer, return no-result, stop, delegate to active/selected children, or use a
  connector/adapter boundary. Do not generate an external/global walker that
  inspects node modes, closed siblings, child policies, platform representation,
  or external-tree internals to steer propagation.
- If the node has a separate content, the controller must not work with the concrete implementation bypassing the content object and its external interface. A public/base-class primitive getter does not legalize such a bypass.
- If the controller needs a presentation change, the prompt must require
  controller-owned state plus node/runtime dirty or lifecycle/render refresh.
  Locally implemented content must then pull already-resolved primitive/output
  values through controller access during materialization or refresh. Do not require
  named `IContentAccess` presentation command methods. Generated controller code
  must not use the node's own render/view/native primitive, its platform API, or
  an equivalent exposed primitive handle for direct platform primitive access.
  Detection examples for DOM-like targets: `this.el`,
  `this.getView().classList`, `this.getView().style`,
  `this.getView().addEventListener`, `this.getView().setAttribute`,
  `querySelector`, `content.getView()` — use the equivalent native/render
  primitive handle on other platforms.
- The prompt must prohibit locally implemented content from deriving output
  values. Text formatting, concatenation, hardcoded display values,
  style/class/token selection, icon selection, visibility selection, handler
  selection, and output computation from constants, runtime data, props,
  config, environment values, platform values, or assets belong to the owning
  controller.
- The prompt must require generated declarations/materialization to follow architectural depth from outside to inside: controller/node first, internal access boundary artifact(s) next, hidden Content implementation last. In a one-file implementation this means `Controller/Node` -> `IContentAccess` + `IControllerAccess` (or explicit zero-contracts) -> `Content`. In split-file or one-class-per-file targets, the same dependency direction must be preserved across files and the companion artifact stems must be declared in Expected Materialization.
- The prompt must include mandatory post-generation validation based on `references/node-validation-rules.md`.

To be specified explicitly for this prompt.
