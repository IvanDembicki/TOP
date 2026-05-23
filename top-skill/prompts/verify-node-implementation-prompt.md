# Prompt: Verify Node Implementation Prompt

agent: Validation Agent

input_contract:
- node_spec
- implementation_prompt
- regenerated_code
- current_attempt
- max_attempts

output_contract:
- decision (pass / refine-prompt / escalate)
- mismatch_list
- prompt_refinement_suggestions

rules:
- if current_attempt >= max_attempts and not stable → escalate
- pass requires full behavior coverage
- pass requires preserved legacy test-covered behavior to be represented in prompts and covered by TOP-compatible tests when the node belongs to a migration scope
- pass requires independent artifact evidence: artifacts reviewed, files
  inspected, canon rules checked, search/detection patterns used, and per-check
  evidence
- previous generator/repair reports are claims, not proof; executor
  self-validation claims are `WF-023`
- failed validation must create a structured rejection ticket and require a
  `top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md` update before repair

---

Use this prompt to verify that the implementation prompt stably produces a correct node implementation.

---

## Input data

Provide:
- node spec;
- implementation prompt;
- reference implementation or expected behavior;
- Behavior Preservation Plan when applicable;
- regenerated code;
- previous mismatch reports (if any);
- current attempt number;
- maxAttempts.

---

## What to do

### 1. Compare regenerated code against node requirements
Check:
- behavior coverage;
- behavior preservation coverage for legacy test-covered requirements;
- event handling;
- state ownership;
- state transitions;
- child interactions;
- invariants;
- forbidden behavior;
- compliance with `props.dir` and expected directory placement of generated files;
- compliance with `props.sourceRoot`, canonical `top_src/` source-root layout,
  and `top/specs/` branch spec placement;
- for migration scopes, confirmation that generated source preserves the
  approved decomposition and does not collapse into a single hub node or
  TOP-shaped wrapper around a legacy screen/component/file;
- for migration scopes, confirmation that `PanelDisplayStyle` or equivalent
  display-token getters do not hide state alternatives, modal/form/list
  ownership, async process branches, permission-gated capabilities, workflows,
  or data boundaries;
- confirmation that mode/status/phase flags, including owner-held fields on the
  same node, are not hiding switchable states when they change visual
  representation, behavior, hit targets, context actions, or capability
  availability;
- for migration scopes, confirmation that bridge residuals are isolated as
  bridge components, connectors, black-box boundaries, data bridge nodes, or
  adapter residuals, and do not make locally implemented content own
  orchestration;
- for migration scopes, confirmation that helper components, modals, forms,
  cards, rows, tiles, list items, banners, selectors, status panels, and action
  panels have been classified as local details, nodes, black boxes, or reusable
  library nodes;
- presence and correctness of an explicit restricted access artifact for content, if content exists;
- materialization of the artifact as a named contract type, not an anonymous object shape;
- explicit typing of the constructor/factory/method parameter receiving the artifact, if the language allows;
- explicit typing of the field/reference storing the artifact, if the language allows;
- absence of empty formal protocol objects where content access to controller is permitted;
- if the content-to-controller protocol artifact is empty, explicit confirmation that this is a zero-contract implemented by the owning controller and not a separate dummy runtime object;
- confirmation that controller fields/references to content are typed through `IContentAccess`, not through the concrete Content class where the technology permits;
- confirmation that TOP object constructors attach objects to context and do not
  inject data packets, flags, callbacks, config/options/props-like objects,
  stores, services, child views, presentation values, visibility values, style
  values, text values, runtime state, handlers, or arbitrary additional values;
- confirmation that static node constructors are parent/context-only, and that
  runtime-created branch roots, if present, use parent/context plus at most one
  canonical Runtime Branch Binding input: entity context reference, stable
  identity key, or typed immutable DTO fallback;
- confirmation that child nodes, locally implemented content, connectors, and
  black-box boundaries are not configured after construction through
  setter-style data/config/state/presentation injection (`CORE-032`);
- confirmation that the public node/controller artifact is not itself a renderable framework component, widget, composable, render/build function, platform UI lifecycle object, or equivalent target-renderable entity;
- confirmation that every generated TOP controller participates in the runtime
  controller tree: it extends the project runtime node base or implements the
  project runtime node interface, has parent/context or root/host context, has
  or inherits lifecycle, has child ownership/registration and children access,
  declares child policy or explicit leaf status, and maps to its spec tree
  position;
- confirmation that child construction creates child controllers/node objects,
  not child content, public wrappers, render fragments, or target artifacts
  posing as TOP children;
- confirmation that the `generated-controller-runtime-shape` micro-check and
  `controller-tree-topology` meso-check passed or are explicitly
  not_applicable;
- confirmation that documented renderable-controller waypoints remain reported as `CORE-026` and do not produce validation/final-audit pass;
- confirmation that render output is produced only by Content or adapter-side artifacts;
- confirmation that locally implemented content contains no conditional
  selection logic: no `if`/`else`, `switch`/`case`, ternary selection,
  conditional rendering, conditional return, multiple return branches,
  `&&`/`||` conditional selection, `match`/`when`/guard branches, or equivalent
  constructs that decide or derive structure, class/style/token, text, icon,
  visibility, handler, child output, platform primitive, representation, or
  capability;
- confirmation that locally implemented content materializes a structurally
  static content shape and applies only already-resolved primitive/output values
  received through the owning controller access contract;
- confirmation that locally implemented content does not format, concatenate,
  hardcode, or derive output values from constants, runtime data, props, config,
  environment values, platform values, assets, or other local sources;
- confirmation that locally implemented content does not derive presentation
  values such as text, class/style/token, icon, visibility, handler, child
  output, platform primitive, representation, or output value;
- confirmation that controller does not push show/hide/update/apply-state/
  class/style/render-with commands, presentation state, or imperative mutations
  into locally implemented content;
- confirmation that controller presentation changes use controller state update
  plus node/runtime dirty or lifecycle/render refresh, and that content pulls
  already-resolved primitive values through controller access during
  materialization or refresh;
- confirmation that child Nodes/Controllers do not receive semantic runtime input such as parent-derived values, state, callbacks, services, props/config/options, parameter bags, or runtime argument sets (`CORE-029`);
- confirmation that shared derived fact repairs do not swap `CORE-029` and Invariant 14: no parent-derived runtime input, no duplicate child derivation from the same cross-cutting source, and an explicit typed access/update boundary or connector if the fact is shared;
- confirmation that any public runtime input object/value used to materialize Content carries exactly one value: the owning controller instance typed only as `IControllerAccess`/target-equivalent, optionally inside a target-required technical envelope;
- confirmation that Content does not receive decomposed `IControllerAccess` members as separate props/parameters/JSX attributes, method bags, facade/adapters, or inline object literals (`CORE-030`);
- confirmation that Controller does not receive decomposed `IContentAccess` members as method bags, facade/adapters, concrete Content types, platform primitives, or inline object literals (`CORE-031`);
- confirmation that `IContentAccess` is not used as a data/view-model/state/callback bag for Content;
- confirmation that `IControllerAccess` methods exposed to Content are controller-boundary methods owned by the controller, not raw imported functions, external method references, service methods, store actions, or callbacks;
- absence of controller bypass to concrete implementation;
- absence of cases where a public/base-class primitive getter is used to justify controller access to concrete implementation;
- absence of controller-side platform primitive access for anything other than implementing `getView()` or parent-owned placement/composition of an opaque child view (detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()`);
- compliance with `references/node-validation-rules.md`;
- preservation of Layer B semantic intent;
- confirmation that behavior extracted from migrated tests is represented in the implementation prompt;
- confirmation that each prompt requirement derived from legacy tests has preserved, adapted, replaced, or newly generated TOP-compatible test coverage;
- confirmation that discarded legacy tests have explicit behavior-level justifications;
- absence of source-platform leakage in a non-source target;
- adherence to Layer C target adaptation decisions.

### 2. Identify mismatches
Categorize them as:
- missing behavior;
- missing preserved test-covered behavior;
- wrong state ownership;
- structural mismatch;
- missing child interaction;
- platform-specific leakage;
- missing prompt representation for a migrated behavior requirement;
- missing TOP-compatible test coverage for a prompt requirement;
- invalid pass with remaining accepted core deviation (`WF-011`);
- ad hoc accepted-deviation label for a core violation with no TOP-canon-defined
  waypoint (`WF-012`);
- Node/Controller semantic runtime input (`CORE-029`);
- decomposed owner access input into Content (`CORE-030`);
- decomposed content access input into Controller (`CORE-031`);
- context data injection into TOP objects (`CORE-032`);
- missing migration decomposition review / giant-node wrapper (`WF-017`);
- undisciplined accepted deviation (`WF-018`);
- locally implemented content conditional selection logic (`CORE-015`);
- locally implemented content output derivation (`CORE-015`);
- controller-to-content presentation command or mutation push into locally
  implemented content (`CORE-015`);
- controller-shaped service/helper/module that does not participate in the
  runtime controller tree (`CORE-037`);
- invalid shared derived fact repair that swaps `CORE-029` with Invariant 14 or Invariant 14 with `CORE-029`;
- instability / ambiguity in prompt;
- artifact placement mismatch.

### 3. Determine whether the prompt can be fixed
If yes:
- propose precise changes to the implementation prompt.
If no:
- explain why the prompt remains unstable.

### 4. Make a decision
Output one of the statuses:
- `pass`
- `refine-prompt`
- `escalate`

### 5. Account for the attempt limit
If `currentAttempt >= maxAttempts` and stability has not been reached,
you must output `escalate`.

---

## Expected output format

1. Coverage summary
2. Mismatch list
3. Prompt refinement suggestions
4. Canonical fix direction
5. Re-validation status
6. Decision
7. Escalation note if needed
