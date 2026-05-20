# generate-top-node

agent: Generation Agent

input_contract:
- approved_top_model
- Behavior Preservation Plan when generating a migrated scope with legacy tests
- semantic_interpretation_output
- target_adaptation_output

output_contract:
- generated_artifact

rules:
- no architecture change
- generation is an executor activity: produce artifacts, mechanical checks,
  known risks, and an artifact manifest for validation; do not claim
  `TOP-clean`, `CORE-015 clean`, `canon compliant`, `validation passed`,
  `no violations`, `ready_for_manual_QA`, `ready_for_use`, or equivalent
  validation verdicts for generated artifacts (`WF-023`)
- in migration mode, read
  `top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md` before generating
  after a rejection and do not repeat a rejected strategy
- generate from Layer B semantic intent and Layer C target adaptation, not from source-platform primitives
- for migrated scopes, generate from normalized requirements in the Behavior Preservation Plan as well as Layer B and Layer C
- for migrated scopes, preserve the approved recursive decomposition. Do not
  collapse a modeled branch back into a single hub wrapper around the legacy
  screen/component/file.
- do not use `PanelDisplayStyle` or equivalent display-token getters as a
  substitute for generating modeled state nodes, modal/form/list nodes,
  capability branches, async process branches, or data ownership boundaries.
- isolate required hook/target bridge residuals as bridge components,
  connectors, black-box boundaries, data bridge nodes, or adapter residuals; do
  not place workflow logic, mutation body construction, routing decisions,
  alerts, store writes, or pending action execution into locally implemented
  content.
- runtime-created branches must follow the Runtime Branch Binding Pattern:
  entity context binding preferred, identity key binding when the branch resolves
  its context, typed DTO binding only when converted to owned data early.
- prefer the Library Object External Context Boundary pattern for
  runtime/library branches: attach branch-external access at the branch root
  where possible, including parent context, data tree, presentation/style tree,
  asset tree, permissions, runtime services, and connectors. Descendants should
  request narrow values/capabilities through the root or contracts derived from
  it. This is a recommended modeling pattern, not a hard invariant; document
  explicit exceptions in the prompt/spec/branch contract.
- do not invent behavior absent from the semantic layer
- do not lose, weaken, omit from prompts, or leave uncovered behavior proven by legacy tests
- generate or adapt TOP-compatible tests for each prompt requirement derived from legacy tests
- classify missing Behavior Preservation Plan as `WF-010` and test-covered behavior loss as `CORE-028`
- use `references/code-generation.md` section "Canonical Rich Typed TOP Node Pseudocode"
  as the best-practice reference for spec fragment -> rich typed
  pseudocode -> target-language derivation when generating runtime/library
  nodes or documenting canonical skeletons
- generate only into the approved implementation source root (`top_src/` by
  default); for new migration branches use `top_src/<branch-id>/` unless the
  approved model declares another root
- do not create TOP implementation artifacts in arbitrary legacy directories;
  only thin framework adapters may be written outside the source root when the
  integration contract declares them explicitly
- enforce Pull-Based Construction / Locality of Object Birth
- enforce Controller Role Purity
- generate context attachment, not data injection: TOP object construction
  attaches the object to its ownership context and does not fill it with values
- generate a runtime controller tree, not controller-shaped service/helper
  files. A controller without tree position is not a TOP controller.
- generated TOP controllers must extend the project runtime node base or
  implement the project runtime node interface. They must have or inherit
  parent/context or root/host context, child ownership, children access,
  lifecycle, child construction policy, disposal/cleanup, and materialized
  output access through their own content boundary when content exists.
- child construction must create child controllers/node objects, not child
  content, public wrapper components, render fragments, or target artifacts
  posing as child nodes.
- after each controller file, produce evidence for the
  `generated-controller-runtime-shape` micro-check; after each subtree, produce
  evidence for the `controller-tree-topology` meso-check
- static node constructors receive only parent/context as semantic input
- runtime-created branch roots may receive parent/context plus one canonical
  Runtime Branch Binding input: entity context reference, stable identity key,
  or typed immutable DTO fallback
- locally implemented content receives only the owning controller access
  contract as semantic input
- connectors and black-box boundaries receive only their explicit boundary
  interface as semantic input
- do not generate constructor arguments or public runtime inputs for data
  packets, flags, callbacks, config/options/props-like objects, stores,
  services, child views, presentation values, visibility values, style values,
  text values, runtime state, handlers, or arbitrary additional values
- do not generate setter-style post-construction injection such as
  apply-config, set-data, set-visible, update-text, set-style, set-callbacks,
  or target-equivalent calls into child nodes, locally implemented content,
  connectors, or black-box boundaries
- do not generate Node/Controller runtime inputs for semantic data, parent-derived facts, callbacks, services, stores, props/config/options, parameter bags, or runtime argument sets; use explicit pull access/update methods or modeled connector contracts instead
- do not generate the Node/Controller as a framework-rendered component, widget, composable, render/build function, platform UI lifecycle object, or equivalent target-renderable entity
- renderable target artifacts belong to Content or thin adapters, not to the controller
- Content constructor receives exactly one semantic value: the owning controller instance typed only as the narrow `IControllerAccess`/target-equivalent interface
- zero-contract content-to-controller access is an empty owner access interface implemented by the controller; do not generate `ControllerAccessZero` dummy objects
- controller stores and uses content through `IContentAccess`, not through the concrete Content class
- concrete locally implemented content is private to the owning controller.
  Do not import, instantiate, type against, downcast to, inspect, store, or call
  concrete content from parents, siblings, children, helpers, adapters, or
  generated callers.
- generate one controller and zero-or-one locally implemented content object per
  node. Additional modal/form/card/list/bridge/helper pieces must be modeled or
  classified as child nodes, state nodes, black-box components, bridge
  boundaries, reusable library nodes, or private target-local implementation
  detail inside that one content object.
- do not generate controller methods that return platform view fragments,
  content fragments, render/build trees, JSX/widget/composable fragments,
  style/layout fragments, animation objects, content-owned setter handles, or
  platform mutation handles.
- do not generate content-owned setter/mutation handles that cross the content
  boundary through controller fields, access contracts, helpers, adapters, or
  public APIs.
- controller receives/stores/uses its own Content instance typed through
  `IContentAccess`; do not generate decomposed content lifecycle/materialization bags,
  facade/adapters, platform primitive handles, or inline closure objects
- do not generate `IContentAccess` as a data/view-model/state/callback bag for Content; Content pulls controller-owned data through `IControllerAccess`
- do not type Content against the concrete controller, and do not import/downcast back to it
- do not generate semantic injection through constructor parameters, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, platform child views, child-output getter bundles, or prebuilt fragments
- if the target materializes Content through one public runtime input object/value, generate that input as a target-required envelope containing exactly one controller-typed value, for example `access={controllerAsIControllerAccess}` or `controller={controllerAsIControllerAccess}`; do not generate separate JSX props for access methods
- do not replace `IControllerAccess` with an externally assembled access bundle, adapter/facade, method bag, or inline closure object, even when it contains correctly named methods
- generate `IControllerAccess` methods as controller-boundary methods owned by the controller; they may delegate internally, but do not expose raw imported functions, external method references, service methods, store actions, or callbacks directly to Content as access methods
- for shared derived facts, do not generate either duplicate derivation in multiple controllers or parent-to-child runtime input tunneling; generate an explicit typed access/update boundary, named controller method, or modeled connector contract, or report the model as blocked
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles
- name child-output access methods by semantic branch/output, for example `getAccountIdentityView()`; do not require `Handle`/`ViewHandle`, do not use `slot`, and avoid generic `children`/`render`/`builder` names
- do not generate conditional selection logic inside locally implemented
  content. Locally implemented content must not decide, derive, branch, select,
  toggle, format, concatenate, hardcode, or compute which structure,
  class/style/token, text, icon, visibility, handler, child output, platform
  primitive, representation, output value, or capability should be used.
- generated locally implemented content may only materialize a structurally
  static content shape and apply already-resolved primitive/output values
  received through the owning controller access contract
- do not generate content-side output derivation from constants, runtime data,
  props, config, environment values, platform values, or assets. The owning
  controller resolves the final primitive/output value.
- do not generate `if`/`else`, `switch`/`case`, ternary selection, conditional
  rendering, conditional returns, multiple return branches, `&&`/`||`
  conditional selection, `match`/`when`/guard branches, or equivalent
  constructs inside locally implemented content when they participate in
  selection or derivation
- if a primitive value must be computed or selected, generate that derivation in
  the owning controller and expose the already-resolved primitive through
  controller access
- if structures, elements, handlers, visibility modes, representations, or
  capabilities vary, generate explicit child state nodes for the alternatives
- if selection logic belongs to an external, native, third-party, or
  self-contained implementation, wrap it as black-box component content behind a
  narrow explicit interface
- do not generate controller-to-content imperative presentation updates. The
  controller must not command, mutate, update, show, hide, configure, set
  class/style, apply state, or render-with into locally implemented content
- for presentation changes, generate controller state updates plus a
  node/runtime dirty or lifecycle/render refresh request; locally implemented
  content then pulls already-resolved primitive values through controller access
  during materialization or refresh
- presentation content reports semantic intent only. Controllers make decisions.
  Data controllers mutate their own private data content through internal
  storage boundaries when the relationship is architecturally allowed.
- do not generate presentation content that directly reads or mutates data
  content
