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

---

## Important rules

- One prompt — one node.
- Prompt must be a project-local artifact.
- Prompt must reside in `prompts/` alongside the JSON tree/branch spec.
- Do not duplicate the entire project.
- Do not substitute the tree structure.
- Do not place platform-specific implementation details in behavioral sections.
- Do not make platform notes portable requirements.
- Do not require another platform to copy the current platform's mechanism mechanically.
- Keep `Expected Materialization` separate from platform notes: it declares artifact stems,
  public classes/roles, internal contracts, materialization policy, and companion artifact
  stems, while concrete target extensions remain target-specific materialization details.
- Explicitly state the owner state.
- If the node has a separate content, the implementation prompt must require explicit internal access boundaries `IControllerAccess` and `IContentAccess`, materialized as explicitly as the technology allows. If either direction has no permitted calls, the prompt must declare an explicit zero-contract for that direction.
- These access artifacts must be narrow and strongly typed where the language permits. They must be materialized as named contract artifacts or other explicitly designated typed boundaries, and the constructor/factory/method parameter accepting such an artifact must have an explicit contract type. Anonymous/untyped parameters such as `constructor(facing)` without an explicit contract type are not allowed if the language can express it.
- If the node has a separate content, the controller must not work with the concrete implementation bypassing the content object and its external interface. A public/base-class primitive getter does not legalize such a bypass.
- If the controller needs a visual/platform operation on its own content, the prompt must require a named `IContentAccess` command method. Generated controller code must not use the node's own render/view/native primitive, its platform API, or an equivalent exposed primitive handle for direct platform primitive access. Detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()` — use the equivalent native/render primitive handle on other platforms.
- The prompt must require generated declarations/materialization to follow architectural depth from outside to inside: controller/node first, internal access boundary artifact(s) next, hidden content/view implementation last. In a one-file implementation this means `Controller/Node` -> `IContentAccess` + `IControllerAccess` (or explicit zero-contracts) -> `Content/View`. In split-file or one-class-per-file targets, the same dependency direction must be preserved across files and the companion artifact stems must be declared in Expected Materialization.
- The prompt must include mandatory post-generation validation based on `references/node-validation-rules.md`.

To be specified explicitly for this prompt.
