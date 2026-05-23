# Node Validation Rules

This file defines mandatory post-generation / post-refactor validation for node-level implementation.

Successful compilation, local operability, or passing partial framework checks do not imply architectural correctness.
A node implementation is not considered correct until the full cycle has been completed:
- load the current skill rules required by the active task;
- re-read the target artifacts being judged in the current validation pass;
- identify the class of violation;
- classify it as `confirmed`, `possible`, or `ambiguity`;
- choose the canonical correction direction;
- re-validate the result after the fix.

Anything else is strictly prohibited.

Prior session reads, previous generation context, memory of older skill versions,
or earlier inspections of target files are not validation evidence. If a
validation report lists a file as checked, that file must have been read during
the current validation pass.

---

## 1. Boundary validation

Required checks:
- if the node has a separate content, the controller does not bypass the content boundary through direct access to the concrete implementation;
- controller fields/references to content are typed as `IContentAccess` or the target-equivalent narrow contract, not as the concrete Content class where the technology permits that boundary;
- concrete locally implemented content is private to its owning controller:
  parents, siblings, children, adapters, helpers, generated callers, and other
  nodes do not import, instantiate, type against, downcast to, inspect, store,
  or call the concrete content class (`CORE-033`);
- no public node/controller artifact is a target-framework wrapper around
  concrete content, and no external/parent/adapter file can name concrete
  content or a wrapper around it (`CORE-036`);
- controller public APIs do not return platform view fragments, render/build
  trees, content fragments, style/layout fragments, JSX/widget/composable
  fragments, animation objects, content-owned setter handles, or mutation
  handles (`CORE-034`);
- content-owned setters/mutation handles are not captured by controllers,
  returned through controller APIs, passed through access contracts, or handed
  to parents/adapters/helpers (`CORE-035`);
- controller-to-content access through `IContentAccess` is limited to
  lifecycle/materialization access such as obtaining the root content primitive
  or participating in controlled lifecycle;
- controller does not imperatively command, mutate, update, show, hide,
  configure, set class/style, apply state, or render-with into locally
  implemented content;
- controller code does not use the node's own render/view/native primitive, its platform API, or an equivalent exposed primitive handle, except inside the implementation of `getView()` itself and parent-owned placement/composition code that treats a child view as an opaque handle (detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().removeEventListener`, `this.getView().setAttribute`, `this.getView().querySelector`, `content.getView()`);
- if a child view is obtained through `getView()`, it is used only as an opaque materialization handle for mount/unmount/insert/reorder/replace/placement through the parent's content boundary;
- the parent/controller does not attach event listeners to a child view, mutate its styles/classes/attributes, query inside it, or use its platform API as a behavior or communication channel;
- content does not gain access to the public node surface;
- content does not reach the outside world through surrogate channels;
- internal implementation details are not used as a communication channel.

Canonical correction direction:
- move interaction into an explicit external interface of the content;
- remove direct controller bypass;
- replace direct platform primitive access with controller state changes,
  dirty/render refresh through the node/runtime mechanism, and locally
  implemented content pulling already-resolved values through `IControllerAccess`;
- restrict `getView()` usage to parent-owned placement/composition only;
- close any surrogate channels.

---

## 2. Protocol artifact validation

Required checks:
- if the node has a separate content, there exists a separate explicit restricted-access artifact for content to access the controller;
- the artifact is narrow and whitelist-only;
- the artifact is explicitly typed where the language permits;
- the artifact is materialized as a separate named contract artifact, not as an anonymous object shape;
- the constructor/factory/method parameter receiving the artifact is explicitly typed where the language permits;
- the field/reference storing the artifact is explicitly typed where the language permits;
- if content access to the controller is permitted, the artifact is not an empty formal stub;
- if the artifact is empty, it explicitly signifies a complete prohibition of content access to the controller;
- if the content-to-controller artifact is a zero-contract, it is an empty narrow interface implemented by the owning controller, not a separate dummy runtime object;
- the artifact does not contain parent/root/host/container/integration handles.

Canonical correction direction:
- materialize a separate protocol artifact;
- remove extraneous fields;
- fix an explicit contract type;
- remove anonymous/untyped protocol parameters.

---


## 2a. Pull-Based Construction / Locality Validation

Required checks:
- every static Node constructor has exactly one semantic argument: its
  parent/context reference;
- every runtime-created branch root has at most parent/context plus one
  canonical Runtime Branch Binding input;
- every TOP object constructor attaches the object to context and does not inject
  data packets, flags, callbacks, config/options/props-like objects, stores,
  services, child views, presentation values, visibility values, style values,
  text values, runtime state, or handlers as additional arguments (`CORE-032`);
- child nodes, locally implemented content, connectors, and black-box boundaries
  are not configured after construction through setter-style data/config/state/
  presentation injection such as apply-config, set-data, set-visible,
  update-text, set-style, set-callbacks, or target-equivalent calls (`CORE-032`);
- a root constructor using `null` or `RootContext` treats it only as a root ownership/bootstrap marker, not as a dependency injection container;
- Node/Controller public runtime entrypoints do not receive semantic data,
  derived facts, callbacks, handlers, services, stores, child fragments,
  config/options/props-like objects, parameter bags, runtime argument sets, or
  arbitrary props;
- parent/root/external code does not repair duplication or ownership defects by
  pushing derived values into child Nodes/Controllers through target runtime
  input;
- child Nodes/Controllers do not repair parent-derived runtime input defects by
  independently re-deriving the same shared fact from the same cross-cutting
  source;
- every Content public constructor has exactly one semantic argument: the owning
  controller instance typed only through the narrow `IControllerAccess` or
  target-equivalent interface;
- Content constructor parameters, fields, and stored references are typed as the narrow access interface, not as the concrete controller class;
- content-to-controller zero-contracts are empty owner access interfaces implemented by the owning controller;
- Content does not import, reference, inspect, or downcast to the concrete controller type;
- Content does not receive data, callbacks, handlers, flags, state, stores, services, child components, slots, prebuilt view fragments, platform child views, child view handles, child-output getter bundles, view-model objects, config/options/props-like objects, parameter bags, runtime argument sets, or arbitrary props;
- the same semantic inputs are not moved into any public runtime parameter, render/build parameter, component/native/platform field, composition mechanism, or other technology-specific entrypoint;
- if the technology materializes Content through one public runtime input object/value, that input carries exactly one value: the owning controller instance typed only as the narrow content-to-controller owner access contract (`IControllerAccess` or target-equivalent), not a merged `IContentAccess & IControllerAccess` bundle or general props/config/data/composition bag;
- Content does not receive `IControllerAccess` members decomposed as separate runtime props/parameters, JSX attributes, named function arguments, method bags, facade/adapters, or object literals assembled at a render/composition call site (`CORE-030`);
- `IContentAccess` is not used as a view-model/data field carrier for content;
- no externally assembled access bundle replaces `IControllerAccess`, even when it contains correctly named methods;
- controller receives, stores, and uses its own Content instance typed only
  as `IContentAccess`/target-equivalent, not decomposed content
  lifecycle/materialization members, method bags, facade/adapters, closure
  objects, concrete Content types, platform primitives, or objects assembled
  outside the controller/content construction boundary (`CORE-031`);
- `IControllerAccess` methods are controller-boundary methods owned by the controller;
- `IControllerAccess` methods may delegate internally, but Content does not receive raw imported functions, externally owned method references, service methods, store actions, or callbacks as access methods;
- Content requests data/actions/permitted output handles from its owning controller through explicit access methods;
- the owning controller obtains child view handles from direct child controllers through public APIs;
- visual content does not construct, import, inspect, or directly own child nodes.

Canonical correction direction:
- move child construction to the owning parent controller at the child position in the tree;
- remove constructor data injection and setter-style post-construction pushes;
- replace pushed constructor/runtime inputs with explicit access methods on a narrow access interface;
- let the object pull values through its contextual contract after attachment;
- model pushed state/structural alternatives as explicit child state nodes;
- wrap external component configuration behind a black-box boundary with a
  narrow explicit interface;
- replace pushed Node/Controller runtime inputs with explicit pull access/update
  methods or modeled connector contracts; if no canonical channel exists, report
  the remaining violation instead of tunneling the value;
- do not accept repairs that merely swap Invariant 14 and `CORE-029`; shared
  derived facts require an explicit typed access/update boundary, named
  controller method, or modeled connector contract;
- type Content only against the access interface;
- remove downcasts/imports back to concrete controller types;
- classify legacy runtime parameters, parameter bags, config/options/props-like objects, and composition entrypoints as wrapped legacy until they are removed from the TOP-conformant path.

---

## 2b. Controller Role Purity Validation

Required checks:
- controller class/function/artifact is not a framework-rendered component or target-renderable entity;
- controller does not return render output, widget/render trees, platform views, layout fragments, style objects, animation objects, or content artifacts;
- controller does not receive props/config/options as framework component input or as a public runtime input receiver for content composition;
- controller does not use framework UI lifecycle APIs, hooks, callbacks, or equivalent target lifecycle mechanisms as its own controller lifecycle;
- controller does not construct platform primitives inline as a substitute for content;
- controller is not the artifact exported, registered, mounted, invoked, or executed as the screen/widget/view/composable/renderable object itself.

Non-exhaustive violation examples:
- a node/controller function invoked by a target runtime as a rendered component and returning render output;
- a controller object/class that implements the target's render/build/body method;
- a controller registered as a screen, view, widget, composable, route lifecycle object, or equivalent UI artifact;
- a controller receiving runtime props/config/options as framework component input.

Concrete examples are illustrative only. The rule is target-independent: any
target runtime mechanism that makes the controller itself the renderable/content
artifact is a controller role purity violation.

Canonical correction direction:
- split the artifact into a non-renderable Controller/Node object and a Content renderable artifact;
- add `IControllerAccess` and `IContentAccess` boundaries where content exists;
- move any controller-owned data exposed through `IContentAccess` into explicit `IControllerAccess` access methods;
- use a thin framework adapter only when the target runtime requires a renderable entrypoint;
- keep controller logic out of the adapter and renderable content artifact;
- expose only narrow access contracts and opaque handles.

---

## 2c. Runtime Controller Tree Validation

Required checks:
- TOP runtime is a tree of controllers, not a set of controller-shaped service
  files;
- every spec node has a corresponding controller artifact unless the model
  explicitly declares a non-runtime/source-only artifact;
- every generated TOP controller extends the project's canonical TOP node base
  class or implements the canonical TOP node runtime interface for the
  target/project;
- every non-root static controller has parent/context or inherited
  parent/context;
- every root controller has root/host context and runtime tree root mechanics;
- every controller has or inherits lifecycle, child ownership/registration,
  children access, and a declared child construction policy;
- every leaf controller has or inherits runtime node mechanics even when it has
  no children;
- every non-leaf controller constructs child controllers/node objects according
  to spec;
- no declared child is represented only as content, a public wrapper, a render
  fragment, or a target artifact posing as a child node;
- no controller-shaped service/helper/module is treated as a TOP node without
  runtime tree position (`CORE-037`).

Micro-check after each generated controller file:

```text
checkpoint: generated-controller-runtime-shape
artifact: controller file
checks:
- has/inherits runtime node base or interface;
- has parent/context or root context;
- has/inherits lifecycle;
- has declared child policy or explicit leaf declaration;
- creates child controllers if non-leaf;
- does not import foreign concrete content;
- does not expose concrete content;
result: PASS | REVIEW_REQUIRED | FAIL
```

Meso-check after generating a subtree:

```text
checkpoint: controller-tree-topology
checks:
- spec tree;
- generated folder tree;
- generated controller artifacts;
- child construction logic;
- prompt child rules;
```

The meso-check must verify that spec parent-child relations appear as
controller parent-child relations, no child is represented only as content, no
child node is missing a controller, no unmodeled generated controller exists
without explicit reason, and generated source paths mirror the spec tree.

After repair, validation restarts from the nearest complete validation gate
instead of checking only the edited line. Repair can close one violation while
introducing another.

Canonical correction direction:
- replace controller-shaped services with real node controllers that attach to
  parent/context or root context;
- add/inherit the project runtime node base/interface;
- move child creation into parent-owned child-controller construction;
- convert child content/wrapper/render fragments into child controllers,
  black-box content, or external target artifacts according to the model;
- rerun the controller runtime shape and controller-tree-topology checks after
  repair.

---

## 2d. Switchable and Downward Propagation Validation

Required checks:
- a node modeled as switchable has at least one state/candidate child;
- `openedChild` is non-null for every valid switchable holder;
- if no state is explicitly selected, the first state/candidate child is the
  default opened child;
- active-state operations/queries delegate to `openedChild` and do not use
  nullable opened-child fallback;
- no holder or external traversal loops over closed state siblings for active
  behavior;
- no external walker branches on node mode/status/state names, child policies,
  platform representation, or connector internals to steer active propagation;
- no external caller uses ask-then-handle or capability-preflight checks such
  as `canHandle`, `hasCapability`, `isInteractive`, `supportsEvent`, or
  `listensTo` to steer propagation through a node's internal descendants;
- runtime/library collection children are not treated as switchable children
  unless the branch explicitly models them as the switchable candidate set with
  one selected/opened child;
- downward queries/events enter through an approved propagation entrypoint and
  then propagate by node-owned local forwarding decisions;
- result-producing queries return a result or no-result from the receiving
  node; events/commands handle, delegate, stop, or no-op at the receiving node;
- no-op/no-result is placed at the highest owning node boundary that already
  knows the subtree has no relevant active behavior.

Canonical correction direction:
- establish explicit state/candidate children and a default opened child;
- replace nullable opened-child or null fallback logic with non-null state
  selection;
- move active behavior/no-result policy into the opened state child;
- move traversal decisions from global walkers into node/controller contracts;
- replace ask-then-handle preflight with tell-only handler/query invocation;
- move no-op/no-result policy into the receiving node instead of exposing child
  capability probing to callers;
- route external tree traversal through explicit connector/adapter boundaries;
- reclassify generic runtime/library collections as dynamic composition unless
  they are truly a switchable candidate set.

---

## 3. Content behavior validation

Required checks:
- content has no architectural will;
- content does not decide to attach/integrate/mount/remove/show/hide/destroy as an architectural or lifecycle action;
- one node has zero or one locally implemented content object. Extra
  modal/form/card/list/bridge/helper presentation objects are either private
  target-local implementation detail inside that content object or explicitly
  modeled/classified as child nodes, state nodes, black-box components, bridge
  boundaries, or reusable library nodes;
- locally implemented content contains no conditional selection logic of any
  kind;
- locally implemented content does not decide, derive, branch, select, toggle,
  format, concatenate, hardcode, or compute which structure, class/style/token,
  text, icon, visibility, handler, child output, platform primitive,
  representation, output value, or capability should be used;
- locally implemented content has no `if`/`else`, `switch`/`case`, ternary,
  conditional rendering, conditional return, multiple return branch, `&&`/`||`
  conditional selection, `match`/`when`/guard branch, or equivalent construct
  that participates in selection or derivation;
- locally implemented content materializes a structurally static content shape
  and applies only already-resolved primitive/output values received through its
  owning controller access contract;
- locally implemented content does not derive output values from constants,
  runtime data, props, config, environment values, platform values, assets, or
  other local sources;
- controller does not push presentation state or imperative mutation commands
  into locally implemented content;
- data-node controller domain methods such as `setAge(value)`,
  `updateName(value)`, or `replaceRecord(record)` are treated separately from
  presentation-content push. They are valid only when access is architectural,
  validation/business rules remain in the data controller, and mutation is
  limited to that controller's own private data content;
- external objects and presentation content do not mutate raw data content
  directly;
- controller changes its own state and marks the node/content/runtime dirty or
  requests lifecycle/render refresh through the node/runtime mechanism;
- content may execute low-level platform operations on its own implementation material, including subscribe/unsubscribe, disposal, local event handling, target-local mechanics, and applying already-resolved primitive values during materialization/refresh. These operations must not encode presentation decisions or receive controller-pushed presentation commands;
- content does not make lifecycle and structural decisions;
- content does not interpret its own events as system commands.

Canonical correction direction:
- move primitive value derivation or selection to the owning controller and let
  content request only the already-resolved value through controller access;
- move output formatting, concatenation, constant-based display values, and
  runtime/platform/environment-derived output values to the owning controller;
- split structural, element, handler, visibility, representation, or capability
  alternatives into explicit child state nodes;
- wrap external, native, third-party, or self-contained logic as black-box
  component content with a narrow explicit interface;
- replace controller-to-content presentation commands with controller state
  update, dirty/render request through node/runtime, and content pull of
  already-resolved values through `IControllerAccess`;
- leave in locally implemented content only static materialization,
  already-resolved primitive application, permitted platform-command execution,
  and event forwarding.

---

## 4. Controller behavior validation

Required checks:
- the controller remains the owner of node behavior;
- the controller manages lifecycle and orchestration;
- the controller does not use concrete implementation as a communication channel;
- the controller works with the implementation only through the content object and its external interface;
- the controller never performs visual/platform operations through inherited
  primitive fields, getters, or presentation commands pushed into content;
- a public/base-class primitive getter is not used as justification for controller access to the concrete implementation.

Canonical correction direction:
- move behavior ownership to the controller;
- move concrete implementation access behind lifecycle/materialization
  boundaries and use controller state plus dirty/render refresh for presentation
  changes.

---

## 5. Method semantics validation

Required checks:
- `buildChildren()` is used only for runtime child materialization;
- any analogous materialization/lifecycle methods have not been turned into an init bucket;
- method name does not mask a foreign semantic role.

Canonical correction direction:
- separate init/materialization/update/lifecycle responsibilities into their proper semantic methods;
- remove the method if its semantic role is absent.

---

## 6. Content lifecycle validation

Required checks:
- content is created on demand;
- content is destroyed when the node/branch becomes inactive, unless a retention pattern is explicitly declared;
- permanent content is absent by default.

Canonical correction direction:
- switch the lifecycle to create-on-demand / destroy-on-inactive;
- extract retention into a separate explicit pattern if it is genuinely needed.

---

## 7. Phase Separation Validation

Required checks:
- content materialization has a clear semantic boundary, whether implemented in a constructor, a dedicated method, or another target-native phase;
- child materialization has a clear semantic boundary, whether implemented in a constructor, a dedicated method, or another target-native phase;
- the constructor does not attach or mount this node's view into an external container;
- the constructor does not perform lifecycle activation/deactivation behavior that belongs to `onOpen()` / `onClose()` or equivalent;
- if the technology provides semantic lifecycle methods, each has one role and that role is not duplicated elsewhere.

Canonical correction direction:
- move content creation into the content materialization phase or method;
- move child materialization into the child materialization phase or method;
- move mount/attach logic to the parent's composition method.

---

## 8. Self-Mount Validation

Required checks:
- no child node calls `parent.content.mount()`, `parent.el.appendChild()`, or any equivalent on its own view from within itself;
- `onOpen()` does not attach the node's view into any external container;
- `onClose()` does not contain cross-boundary detach operations attributed to the parent's integration surface;
- no lifecycle hook performs self-insertion into a parent integration surface.

Canonical correction direction:
- move mount calls to the parent's `openChild()` or `buildChildren()`;
- child exposes `getView()`; mounting decision belongs to the parent.

---

## 9. Content Class Materialization Validation

Required checks:
- if the node has `contentType` in the spec, a separate content class exists in implementation;
- the content class is not a thin formal stub with actual platform logic remaining in the controller;
- the controller does not construct platform primitives inline as a substitute for the content layer;
- all platform-primitive construction is inside the content class, not in the controller.
- generated declarations follow architectural depth from outside to inside: controller/node first, internal access boundary artifact(s) next, Content implementation last.

Canonical correction direction:
- create a separate content class;
- move platform construction into it;
- controller accesses content through `IContentAccess`.
- reorder declarations so the access boundary stands between the controller and the hidden Content implementation.

---

## 10. Behavior Preservation Validation

Required checks for migrated nodes or branches:
- legacy tests, snapshots, fixtures, QA scripts, executable examples, and documented test cases covering the scope were inventoried;
- a Behavior Preservation Plan exists when behavior evidence exists;
- each extracted behavior expectation is normalized without legacy implementation details;
- each normalized requirement maps to node responsibility, state, method, event, lifecycle, prompt, and test coverage;
- each prompt requirement derived from legacy tests is covered by preserved, adapted, replaced, or newly generated TOP-compatible tests;
- discarded legacy tests have explicit behavior-level justification;
- no blocking behavior gaps remain.

Violation examples:
- generation updates code but leaves a legacy behavior expectation out of prompts;
- a legacy behavior test is deleted because it asserted old props, but its user-facing warning behavior is not re-covered;
- validation reports passing tests without mapping legacy test-covered behavior to TOP requirements;
- a tested migration scope reaches modeling or generation without Behavior Preservation Agent.

Canonical correction direction:
- run Behavior Preservation Agent;
- update prompts/specs/contracts with normalized requirements;
- preserve, adapt, replace, or generate TOP-compatible tests for each requirement;
- repair `CORE-028` by restoring behavior in TOP sources of truth and tests, not only in code.

---

## 10a. Migration Decomposition Validation

Required checks for migration branches:
- the migration scope root is not treated as a final TOP node boundary merely
  because it came from one screen, route, file, tab, section, or component;
- hidden objects, state holders, state alternatives, data ownership boundaries,
  runtime entities, async workflows, forms, modals, lists, list items, bridge
  boundaries, black-box components, and repeated structures are inventoried and
  classified;
- single-node migrations include explicit proof that no internal candidate
  should be a node, state node, data node, connector, black-box component, or
  library node;
- large `IControllerAccess`/target-equivalent surfaces, many display-style
  methods, many bridge hooks, many pending actions/mutations, and many unrelated
  modal/form/list/workflow responsibilities trigger giant-node review;
- `PanelDisplayStyle` or equivalent display-token methods are not hiding state
  alternatives, workflows, modal/form/list ownership, async process states,
  permission-gated capabilities, or data ownership boundaries;
- hook/target bridges inside locally implemented content are isolated and do
  not own orchestration, mutation construction, routing, alerts, pending action
  execution, or store writes;
- direct global store access is not labeled canonical TOP access unless modeled
  as a connector/data boundary; otherwise it is a migration residual with target
  repair and expiry;
- runtime/library branch descendants that directly reach ancestors, global
  stores, data trees, presentation/style trees, asset trees, services,
  permission sources, or connectors trigger `Library Object External Context Boundary review`.
  This is a recommended-pattern smell, not an automatic hard
  violation unless it also breaks a core access, injection, privacy, connector,
  or global-store rule;
- helper components, modals, forms, cards, rows, tiles, list items, banners,
  selectors, status panels, action panels, and repeated structures are
  classified as local details, nodes, state nodes, black boxes, or reusable
  library nodes.
- public wrappers around concrete content are rejected rather than treated as
  valid helper components (`CORE-036`);
- generated folder layout mirrors the approved TOP tree through the declared
  source root, effective `props.dir`, and prompt layout; semantic subtrees are
  not flattened into a wrapper folder without explicit materialization
  rationale (`CONV-010`);
- branch specs use canonical node shape (`type` or approved equivalent), not
  ad hoc `id`/`name` pseudo-spec trees that cannot regenerate canonical TOP
  nodes (`CONV-009`).

Violation codes:
- `WF-017` for missing or insufficient decomposition review;
- `WF-018` for accepted deviations without target repair/expiry/owner phase;
- `CORE-015` when locally implemented content owns orchestration or output
  derivation;
- `CORE-032` when dynamic branches receive scattered constructor data instead
  of following the Runtime Branch Binding Pattern.

Canonical correction direction:
- return to modeling when the fix changes tree structure;
- split hidden states/workflows/forms/modals/lists into explicit nodes or state
  branches;
- extract reusable repeated structures into library nodes when the role is
  stable and the interface remains narrow;
- isolate target hooks as bridge components, connectors, black-box boundaries,
  data bridge nodes, or adapter residuals;
- replace global store access with store connector, data node, data controller,
  adapter context, or a narrow access contract.

---

## 10b. Independent checkpoint validation

Required checks for migration and generation pipelines:
- infrastructure, scope/decomposition, model/spec, canon precheck, generation,
  post-generation validation, repair when needed, and final audit checkpoints
  are persisted as branch-scoped artifacts or append-only shared log entries
  before handoff;
- executor self-check output is treated as input evidence only;
- Validation Agent and Final Audit Agent re-read the current skill files and
  target artifacts in the current pass;
- validation is adversarial: it attempts to disprove conformance using canon,
  generated source, specs, prompts, contracts, logs, and branch layout.

Violation codes:
- `WF-020` for missing or stale checkpoints;
- `WF-021` for validation based on previous context or generator/repair claims
  instead of independent current-pass evidence.

---

## 11. Validation verdict and outcome

Required checks:
- confirmed core violations remain listed as core violations even when they are
  explicitly documented as migration waypoints;
- accepted deviations contain only TOP-canon-defined migration waypoints, not
  project-local reclassification of arbitrary core violations;
- an accepted migration deviation does not change validation status to `pass`;
- validation does not route to Final Audit while confirmed core violations or
  accepted core deviations remain.

Violation code:
- `WF-011` when validation or audit reports `pass`, `ready`, or `ready_for_use`
  while confirmed core violations or accepted core deviations remain.
- `WF-012` when a project prompt, migration status file, validation report,
  repair report, or final audit labels a confirmed core violation as
  accepted/temporary/deferred/waypoint without a TOP-canon-defined waypoint for
  that violation.

The result of a validation must always contain:
1. the identified class of problem;
2. confidence level (`confirmed` / `possible` / `ambiguity`);
3. canonical correction direction;
4. re-validation status after the fix.

If re-validation is absent, the work is not considered complete. Anything else is strictly prohibited.
