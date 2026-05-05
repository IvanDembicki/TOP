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

For a migration scope with legacy tests, generation also requires a valid
Behavior Preservation Plan. The plan supplies normalized behavior requirements,
prompt update requirements, and TOP-compatible test coverage mapping.

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
- store branch specs under `top/specs/`;
- store implementation prompts under `top/prompts/`;
- be linked to the corresponding tree or branch;
- not be stored inside the skill itself.

Generated TOP implementation artifacts must be stored under the declared
implementation source root. The default root is `top_src/`; a new migration
branch defaults to `top_src/<branch-id>/`. Thin framework-boundary adapters may
remain in legacy framework paths only when the integration contract declares
them explicitly.

Generation must not invent a new source root such as `lib/top/<branch>` or
scatter TOP implementation artifacts into legacy source directories unless the
approved model declares that root and validation accepts it.

---


## 3.1. Semantic interpretation and target adaptation

Generation must not read source-platform primitives as implementation truth.

Before code generation:
- Semantic Interpreter Agent extracts Layer B: platform-neutral roles, intents, state, feedback, layout intent, constraints, and accessibility semantics.
- Target Adaptation Agent converts Layer B into Layer C: temporary target-native interaction, layout, primitive, and constraint decisions.

Generation may use target-specific primitives only from Layer C or from the active target's own conventions.
It must not copy source-platform constructs from prompts, platform notes, imported code, CSS, DOM, Flutter widgets, UIKit/Android classes, or framework APIs into another target.

## 3.1a. Behavior preservation during migration generation

Legacy tests are requirements evidence.

When generating or adapting a migrated scope, generation must preserve the
behavioral requirements proven by legacy tests. It must not treat old tests only
as files to keep passing.

Generation must:
- use normalized requirements from the Behavior Preservation Plan;
- ensure prompt update requirements from that plan are reflected before code is
  treated as final;
- preserve, adapt, replace, or generate tests that cover each preserved behavior
  requirement;
- classify discarded legacy tests with explicit behavior-level justification.

Generation that loses, weakens, omits from prompts, or fails to re-cover
test-covered behavior is invalid and reports `CORE-028`.
Generation that proceeds for a tested migration scope without a Behavior
Preservation Plan reports `WF-010`.

Generation must not repair ownership or derivation problems by adding semantic
runtime inputs to child Nodes/Controllers. Parent-derived values, state,
callbacks, services, stores, config/options/props-like objects, parameter bags,
or runtime argument sets passed into a child Node/Controller are `CORE-029`.

Generation must not repair `CORE-029` by making the child independently
re-derive the same shared or parent-owned fact from the same cross-cutting
source. That only restores the derivation duplication defect. Generated
structure must use an explicit typed access/update boundary, named controller
method, or modeled connector contract for shared derived facts; if the model
lacks that boundary, generation must report the block instead of inventing a
local workaround.

## 3.2. Pull-Based Construction / Locality of Object Birth

Generated code must construct every TOP object at the exact place where it
architecturally belongs in the tree.

Generated construction attaches objects to context; it does not inject the state
they will use. Objects are connected to context, not filled with data.

Generated node, locally implemented content, connector, and black-box boundary
constructors must receive only the narrow contextual reference required to place
the object inside its ownership boundary. They must not receive data packets,
flags, callbacks, config/options/props-like objects, stores, services, child
views, presentation values, visibility values, style values, text values,
runtime state, handlers, or arbitrary additional arguments.

Generated code must not configure child nodes, locally implemented content,
connectors, or black-box boundaries after construction through setter-style
data/config/state/presentation injection. If an object needs a value, generation
must expose that request through the appropriate access contract and let the
object pull the value after attachment.

Node constructors receive exactly one semantic argument: the parent reference.
For root materialization, `null` or `RootContext` is permitted only as a root
ownership/bootstrap marker. `RootContext` must not become a dependency injection
container.

Node/Controller target runtime entrypoints must not receive semantic data,
derived facts, callbacks, handlers, services, stores, child fragments,
config/options/props-like objects, parameter bags, runtime argument sets, or
arbitrary props.

Content constructors receive exactly one semantic argument: the owning
controller instance typed only through the narrow `IControllerAccess` or
target-equivalent interface. Content must be typed only against that narrow
access interface. If the content-to-controller
direction has no permitted methods, the zero-contract is an empty access
interface implemented by the owning controller; generation must not create a
separate dummy `ControllerAccessZero` object. Generated Content code must
not import, reference, inspect, store, or downcast to the concrete controller type.

Generated code must not pass data, callbacks, handlers, flags, state, stores,
services, child components, slots, prebuilt view fragments, platform child views,
child view handles, child-output getter bundles, view-model objects,
config/options/props-like objects, parameter bags, runtime argument sets, or
arbitrary props into Content constructors. It must also not move the same
semantic injection into any public runtime parameter, render/build parameter,
component/native/platform field, composition mechanism, or other
technology-specific entrypoint.

If the target materializes Content through one public runtime input object/value,
that input must carry exactly one value: the owning controller instance typed
only as the narrow content-to-controller owner access contract
(`IControllerAccess` or target-equivalent). A target-required technical envelope
is allowed only when it contains that single controller-typed value. It must not
become a general props/config/data/composition bag, a view-model/data carrier, a
method bag, an adapter/facade, or a merged `IContentAccess & IControllerAccess`
bundle.

Generated code must not treat an externally assembled access bundle as a valid
replacement for `IControllerAccess`. Even if that bundle contains correctly named
methods, it is invalid unless the runtime object is the owning controller
instance typed only as the narrow owner access interface.

Generated code must not decompose `IControllerAccess` members into separate
runtime props/parameters, JSX attributes, named function arguments, or object
literals assembled at a render/composition call site. This is `CORE-030`.

Generated `IControllerAccess` methods must be controller-boundary methods owned
by the controller. A controller-boundary method may delegate internally, but
generation must not expose a raw imported function, externally owned method
reference, service method, store action, or callback directly to Content as the
access method itself.

Content pulls from owner. Owner pulls from children when child output is required.
Children expose opaque handles.
Platform composition syntax may be used only as local materialization syntax; it
must not become the ownership model.

---

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

Generated controllers must be non-renderable controller artifacts. Generation
must not implement a TOP controller as a target framework renderable entity,
render/build function, route/screen component, widget/composable equivalent, or
platform UI lifecycle object.

If the target requires such an entity, generate it as Content or as a thin
framework-boundary adapter, not as the controller itself. The adapter may
instantiate, locate, or delegate to the TOP branch, but it must not accumulate
controller logic.

### Public and internal protocol surfaces
Generated architecture must preserve the public node surface and two distinct internal access boundaries:
- `IControllerAccess` for content access to the controller via a narrow private contract;
- `IContentAccess` for controller access to content via a narrow private contract.

Content must be constructed and stored against the narrow `IControllerAccess`
contract, not against the concrete controller class. The public constructor of
the concrete TOP Content receives exactly that one semantic argument.

The controller must receive, store, and use its own Content instance through
the narrow `IContentAccess` contract, not through the concrete Content
class. This protects the controller from accidentally depending on methods
exposed by a large platform component, native view, widget, or third-party object
wrapped inside content.

Generated code must not replace the Content instance typed as
`IContentAccess` with decomposed content lifecycle/materialization members, method bags,
facade/adapters, closure objects, platform primitives, or objects assembled
outside the controller/content construction boundary. This is `CORE-031`.

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

Locally implemented content must be structurally and decisionally static.
It may only materialize a structurally static content shape and apply
already-resolved primitive values received through its owning controller access
contract.

Generated locally implemented content must not contain conditional selection
logic. It must not decide, derive, branch, select, toggle, or compute which
structure, class/style/token, text, icon, visibility, handler, child output,
platform primitive, representation, or capability should be used.

Forbidden generated constructs inside locally implemented content include
`if`/`else`, `switch`/`case`, ternary selection, conditional rendering,
conditional return, multiple return branches, `&&`/`||` conditional selection,
`match`/`when`/guard branches, and target-equivalent constructs when they
participate in selection or derivation.

Generation repairs:
- primitive value derivation belongs in the owning controller and is exposed as
  an already-resolved value through controller access;
- structural, element, handler, visibility, representation, or capability
  alternatives become explicit child state nodes;
- external, native, third-party, or self-contained logic is wrapped as
  black-box component content with a narrow explicit interface.

Ordinary content may execute low-level platform commands that belong to its own concrete implementation:
- subscribe / unsubscribe on its own platform primitive;
- attach / detach local platform callbacks for its own primitive;
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
When a controller needs a presentation change, generation must update
controller-owned state and mark the node/content/runtime dirty or request
lifecycle/render refresh through the node/runtime mechanism. During
materialization or refresh, locally implemented content pulls already-resolved
primitive values through `IControllerAccess` and applies those values to its
static materialization.

Generation must not create controller-to-content presentation command methods
such as show/hide/update/apply-state/class/style/render-with commands on
`IContentAccess`.
Generated controller code must not use the node's own render/view/native primitive, its platform API, or any equivalent exposed primitive handle for its own content. Detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()` — use the equivalent native/render primitive handle on other platforms.
The controller manages the content lifecycle and does not use the internal content implementation as a communication channel.
If a node has a separate content object, generation must not leave direct controller access to the concrete implementation bypassing the content boundary. Anything else is strictly prohibited.

### Requirements for internal access boundaries
Generation must create for nodes with a separate content only explicitly defined, narrow, and maximally strictly typed internal access boundaries: `IControllerAccess` and `IContentAccess`.
If a node has a separate content class/object, generation must materialize separate explicit access artifacts for both directions where the technology permits. Anything else is strictly prohibited.

Both directions must be accounted for:
- `IContentAccess` / controller-to-content: lifecycle/materialization access,
  not presentation commands or mutation state;
- `IControllerAccess` / content-to-controller: what content may report or request from its own controller.

`IContentAccess` must not contain controller-owned data, state flags, view-model
values, callbacks, child-output handles, or data fields read by content. Content
gets those through `IControllerAccess` methods/accessors.

For locally implemented presentation content, `IContentAccess` is not a
presentation command channel. Generation must not add show/hide/set-text/
set-style/apply-state/render-with methods. For data content, a data node
controller may mutate its own private data content through an internal storage
boundary, but external objects still interact with the data node controller API
and presentation content must not directly access or mutate data content.

If a direction has no permitted calls, generation must materialize or explicitly document a zero-contract for that direction according to the target technology. Silent omission is not valid. For the content-to-controller direction, the zero-contract is an empty narrow access interface implemented by the owning controller and passed as `this` typed only as that interface. It is not a separate runtime access object. For the controller-to-content direction, if the target has no stable runtime content object for the controller to store, generation must explicitly document the zero direction in contracts or materialization notes instead of inventing a data bag or dummy runtime object.
Raw callbacks, handlers, anonymous objects, externally assembled access bundles, parameter bags, full controller references, full concrete controller types, full concrete content references, or public runtime inputs are not valid substitutes for a named internal contract where the technology can express one.

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
3. hidden Content implementation.

For split materialization, the same outside-to-inside dependency direction must be preserved in
file structure and exports:
1. public controller/node artifact;
2. internal contract artifact(s);
3. hidden Content artifact(s).

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
- `props.sourceRoot` fixes the implementation source root (`top_src/` by default);
- `props.dir` fixes the directory anchor for a node or subtree relative to that
  source root;
- descendants inherit the effective dir path until a new local `props.dir` is set;
- the effective dir path must reflect the semantic branch structure of the project, not the accidental history of file moves.

### Canonical rule
The directory tree of code artifacts must be derived from the tree model through
semantic branches, the implementation source root, and the effective `props.dir`.

---

## 7. Effective directory path

For each node, an **effective directory path** is computed:

1. determine the effective source root from `props.sourceRoot`, inherited
   `props.sourceRoot`, or the default `top_src/`;
2. if the node has a local `props.dir` — it is used as the anchor under that root;
3. if there is no local `props.dir` — the effective dir of the nearest ancestor is used;
4. if no ancestor in the chain has `props.dir` — the path is determined by the root/project-level convention.

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
- implementation source root and branch root;
- target prompt directory tree;
- relocation map `old path → new path` if the project is being reorganized;
- required spec updates if `props.dir` needs to be added or corrected;
- required spec updates for `props.contentType` if it is missing from a node with content where the content type must be explicitly recorded.

---

## 12. Typical errors

Typical errors include:
- new branch spec written as an ad hoc `top/<branch>.json` instead of
  `top/specs/<branch>.json`;
- implementation prompts created without a declared/prepared `top_src/<branch>/`
  source root;
- `props.dir` used only as an arbitrary path, not as a semantic anchor;
- code layout and prompt layout diverge in branch structure;
- a separate folder created for each node without a semantic reason;
- an entire subtree dumped into one folder despite clear semantic branches;
- AI generates code without checking the effective dir path;
- relocation performed without updating spec/prompt paths;
- generation mixes controller and concrete content;
- generation leaves controller code directly manipulating its own platform
  primitive or pushing presentation mutation through `IContentAccess` instead
  of using controller state, dirty/render refresh, and content pull of
  already-resolved values;
- generation passes semantic inputs into Content through extra constructor arguments, public runtime parameters, composition entrypoints, parameter bags, config/options/props-like objects, callbacks/handlers bundles, stores, services, child components, platform child views, child-output getter bundles, or prebuilt fragments;
- generation fills TOP objects with data/config/callback/state packets through
  constructor arguments or post-construction setter-style injection instead of
  attaching them to context and letting them pull through explicit contracts;
- generation types Content against the concrete controller or downcasts/imports back to that concrete type;
- generation places hidden Content declarations before the internal access boundary that stands between the controller and content;
- generation makes non-visual content publicly accessible;
- generation places conditional selection logic inside locally implemented
  content instead of moving primitive derivation to the controller, splitting
  alternatives into state nodes, or wrapping external logic as black-box
  component content;
- generation creates controller-to-content presentation commands or mutation
  commands instead of controller state update, dirty/render request, and content
  pull of already-resolved values;
- generation loses the distinction between `view` and `component`.

---

## 13. Verification implications

The verification loop must check not only behavior but also the architectural contract of generation:
- whether the controller/content split is maintained;
- whether a node with content has turned into a single mixed class;
- whether generated declaration order follows architectural depth: controller/node first, internal access boundary artifact(s) next, hidden Content implementation last;
- whether the meaning of `props.contentType` is preserved;
- whether non-visual concrete content is exposed externally;
- whether the rule of a single external interface for a node is violated;
- whether locally implemented content is structurally and decisionally static,
  with no conditional selection logic;
- whether controller-to-content flow is limited to lifecycle/materialization
  access and never pushes presentation state or imperative mutations into
  locally implemented content.
- whether TOP object construction is context attachment only, with no constructor
  data injection or setter-style post-construction data/config/state pushing.

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
