# Core Axioms

## Human readability

The code must be written to be maximally understandable to a human reader.
Clarity and unambiguity take priority over brevity or conciseness.

All structural and naming decisions must support fast, reliable understanding of the code at scale, without requiring implicit knowledge or guesswork.

## Pipeline power separation

The executor produces artifacts. The validator produces verdicts. The log
records both. The canon governs all.

No agent may validate its own output. Generation, repair, modeling, migration,
and implementation agents may report generated files, assumptions, mechanical
checks, type checks, known issues, and an artifact manifest submitted for
validation. They must not claim `TOP-clean`, `CORE-015 clean`, `canon
compliant`, `validation passed`, `no violations`, `ready_for_manual_QA`,
`ready_for_use`, or `final_status: pass` for their own artifacts.

Validation, canon precheck, and final audit must operate from a clean,
adversarial context: current top-skill canon/rules, current artifacts under
review, relevant specs/prompts/contracts, and migration log chronology only.
Previous agent reports are claims, not proof. A pass verdict without artifact
evidence is invalid.

Failed validation creates a structured rejection and a repair obligation.
Rejected strategies are recorded in the branch-local
`top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md` and become negative
constraints for later generation or repair attempts.

Detailed branch definitions and evidence rules live in
`canon/agent-power-separation.md`. Rejection, ledger, and incremental
validation rules live in `canon/validation-rejection-protocol.md`.

## Typing

- Object typing must be as strict, explicit, and complete as the technology reasonably permits.
- If an explicit type contract can be defined, it must be defined.
- Weak, implicit, partial, or shape-based typing is non-canonical unless stricter typing is not realistically achievable in the given technology.

## Naming

- Code must remain readable at scale (volumetrically readable).
- Names must be fully descriptive and unambiguous.
- An abbreviation is allowed only if it is immediately clear without explanation
  to any developer in the given domain.
- Any abbreviation that requires explanation or domain-external context is a violation.

## Behavioral state split (hidden switchable)

A node is a hidden switchable if it independently manages switching between fundamentally different representations or behaviors by accessing external architectural state.

Detection criterion — both conditions must hold simultaneously:

1. The node reads external architectural state (mode, lifecycle phase, openedChild, etc.)
2. And as a result changes at least one of:
   - the visual representation of its constituent elements
   - the available behavior (drag, add, delete, etc. — either present or absent)

The number of explicit child nodes is irrelevant. A hidden switchable may be a monolithic node whose internal elements and handlers change.

Not a violation:
- A controller changes only already-resolved model data exposed through a narrow
  access contract while node behavior is identical in both states. Locally
  implemented content still may not derive or select label text, color, style,
  visibility, structure, handlers, or representation by itself.

Canonical refactoring: the node becomes an explicit switchable holder with child state nodes. Each state node fully owns its own representation and behavior. A state node does not read the external mode — it is itself the representation of that mode.

## Locally implemented content static materialization

Locally implemented content is static implementation material, not a decision
layer. Locally implemented content must not derive output values.

It must not contain conditional selection logic of any kind and must not derive
output values. It must not decide, derive, branch, select, toggle, format,
concatenate, hardcode, or compute which structure, class/style/token, text,
icon, visibility, handler, child output, platform primitive, representation,
output value, or capability should be used.

Locally implemented content may only materialize a structurally static content
shape and apply already-resolved primitive values received through its owning
controller access contract.

Even simple formatting or concatenation belongs to the owning controller. The
controller resolves the final primitive/output value; locally implemented
content only asks for that value and applies it.

Controller must not push presentation state or imperative mutation commands into
locally implemented content. Presentation changes flow as controller state
updates plus node/runtime dirty or lifecycle/render refresh, followed by content
pulling already-resolved primitive values through controller access.

This preserves deterministic materialization, cacheability, pre-rendering,
portability, and verifiability. If content contains selection logic, it becomes
a hidden decision engine and breaks the TOP boundary between controller/tree
decision ownership and content materialization.

## Absolute content privacy

Concrete locally implemented content is private implementation material of its
own node. It is not a public dependency, not a sibling dependency, not a parent
API, and not an integration surface for arbitrary code.

Only the owning controller may create, store, and use its own concrete content,
and even that controller must store and use it only through the narrow
`IContentAccess`/target-equivalent boundary. Other nodes, parents, siblings,
helpers, adapters, and generated callers must not import, instantiate, type
against, downcast to, inspect, store, or call concrete content classes.

A node may expose public controller-level values or opaque placement handles
where canon permits. It must not expose concrete content or content-owned
platform primitives as a route around controller ownership.

If external code can name a node's concrete content class, encapsulation is
already broken. The runtime TOP tree is a tree of controllers, not content
objects and not public target-framework wrappers around content.

A public node artifact must not be a target-framework wrapper around private
content. Target-specific example only; not a canonical model term: a React-like
component that merely renders a private content class is not a TOP controller.
It is a public wrapper around concrete content (`CORE-036`).

## Runtime controller tree

TOP runtime is a tree of controllers.

A TOP controller is not just a file with methods. It is the public runtime
object of a TOP node. A controller without tree position is not a TOP
controller.

Canonical formula: A controller without tree position is not a TOP controller.

Every generated TOP node controller must either extend the project's canonical
TOP node base class or implement the canonical TOP node runtime interface for
the active target/project. The exact names are project-specific, but the roles
are canonical: parent/context reference, child ownership/registration, children
access, lifecycle, child construction policy, refresh/invalidate/update
lifecycle when applicable, disposal/cleanup lifecycle, and materialized output
access through the node's own content boundary when content exists.

A root controller may have no ordinary parent, but it must still be a runtime
tree root with root/host context, child ownership, lifecycle, branch identity,
integration boundary, and materialized output access when it has content.

A leaf controller may have no children, but it must still attach to
parent/context, have or inherit lifecycle, correspond to the spec/prompt, and
own its private content boundary when it has content.

TOP generation must produce a controller tree, not a set of controller-shaped
service files. A controller-shaped service/helper/module with no runtime tree
position is not a TOP node (`CORE-037`).

## One controller, zero-or-one content

A TOP node has exactly one controller. It may have zero or one locally
implemented content object owned by that controller.

Multiple presentation objects, fragments, modal helper components, bridge
components, widgets, or platform primitives inside one node are not extra
content objects by default. They are candidate child nodes, state nodes,
black-box components, bridge boundaries, or reusable library nodes until the
model proves that they are only target-local implementation detail hidden inside
the one private content object.

Splitting a large legacy screen into many local helper components without TOP
classification is not decomposition. It is a wrapped-legacy risk.

## Controller is not a renderer

A controller must not return platform view fragments, content fragments,
render/build trees, style/layout fragments, JSX/widget/composable fragments,
animation objects, or content-owned mutation handles as a controller API.

Parent-owned placement may use an opaque child output handle only where the
child controller's public API explicitly exposes that handle and only for
placement/composition. The returned value must not expose concrete content,
platform internals, setters, callback registration, or a mutation surface.

## Content-owned setters do not cross the boundary

Locally implemented content may have private local mechanics, but content-owned
setter/mutation handles must not be stored by, returned to, or passed through
controllers, parents, adapters, helpers, or other nodes.

If presentation must change, the controller changes controller-owned state and
requests dirty/render/lifecycle refresh through the node/runtime mechanism.
During materialization or refresh, locally implemented content pulls the
already-resolved values through `IControllerAccess` and applies them to its
static structure.

## Context attachment, not data injection

TOP objects are context-bound, not parameter-bound.

Construction attaches an object to its ownership context. It does not fill that
object with the data, flags, callbacks, configuration, presentation values,
runtime state, services, stores, child views, or handlers it will use.

A TOP object constructor may receive only the narrow contextual reference needed
to place it inside the tree or boundary:
- a static node receives its parent/context reference;
- a runtime-created branch root may receive parent/context plus one canonical
  Runtime Branch Binding input: entity context reference, stable identity key,
  or typed immutable DTO fallback;
- locally implemented content receives its owning controller access contract;
- a connector or black-box boundary receives its explicit boundary interface.

Runtime Branch Binding is not a general constructor argument escape hatch. It
must not carry scattered data, props/config/callback bags, mutable raw model
objects, presentation values, services/stores, or arbitrary runtime state.

After attachment, the object requests required information through that
contract. The owner remains responsible for exposing the contract, but it does
not push changing state or presentation decisions into the object through
constructor arguments or post-construction setters.

This preserves tree locality, predictable regeneration, cacheability,
pre-rendering, and a single narrow validation path for data flow.

## Presentation content and data content

The no-push presentation rule applies to locally implemented presentation,
rendering, and materialization content.

Presentation content reports intent. Controllers make decisions. Data
controllers mutate data. Presentation content later pulls resolved values.

Correct presentation flow:
1. user input in locally implemented content is reported as a semantic
   event/request to the owning controller;
2. the controller validates, interprets, and either updates its own state, calls
   an architecturally allowed data-node controller API, or raises the semantic
   event upward;
3. affected controllers or data controllers update;
4. the node/runtime marks dirty or requests refresh;
5. presentation content pulls already-resolved primitive values again.

Data content is different. A data node controller may expose domain methods such
as `setAge(value)`, `updateName(value)`, or `replaceRecord(record)` when the
relationship is architecturally allowed. Inside that same data node, the data
controller may mutate its own private data content through `IContentAccess` or
an equivalent internal storage boundary. Validation and business rules remain in
the data controller, not in raw data content.

External objects must not mutate data content directly. Presentation content
must not directly access or mutate data content.

## Migration decomposition axiom

Migration is architectural extraction, not wrapping.

A legacy screen, route, file, tab, section, or component names the analysis
scope. It does not prove that the result is one TOP node.

Migration must discover hidden objects, state holders, state alternatives,
runtime entities, async processes, forms, modals, lists, list items, data
owners, connectors, bridge boundaries, black-box components, and repeated
structures. The result must be an explicit tree of responsibilities.

A node with a giant controller access surface, many display-style methods, many
bridge hooks, many pending actions/mutations, or multiple independent
modal/form/list/workflow responsibilities is not "complete" by having a large
contract. It is a decomposition-risk signal until proven otherwise.

Node atomicity is required. A node must be small, simple, and single-purpose
enough to regenerate and validate in isolation. A screen section, modal, form,
list item, card, state branch, bridge, or workflow fragment is a node candidate
until the model proves otherwise.

Folder structure must mirror the approved TOP tree. Child nodes normally live
in child folders under the parent folder. A flat branch folder that mixes all
node files is a layout/topology smell unless the model explicitly records a
target/materialization exception.

`PanelDisplayStyle` is not a substitute for node decomposition. It may represent
an already-resolved display value for a stable structural section, but it must
not conceal state alternatives, lifecycle-bearing branches, independent
workflows, forms, modals, permission-gated capabilities, or data ownership
boundaries.

Migration must pass through short, persistent checkpoints. The recommended
minimum checkpoints are infrastructure, scope/decomposition, model/spec,
precheck, generation, post-generation validation, repair if needed, and final
audit. Each checkpoint must persist branch-scoped artifacts and append the
shared migration log before handoff. A later agent must be able to resume from
the artifacts without trusting previous chat context.

Validate the smallest meaningful artifact as soon as it exists. Micro-checks
catch single-artifact risks, meso-checks validate related artifact groups, and
macro-checks validate full phases. Do not build on unvalidated architecture.

Execution and verification must remain independent. The agent that generated or
repaired a branch may perform a self-check, but final validation must re-read
the current skill and target artifacts and must judge adversarially against the
canon, not against the generator's explanation.

The canonical retry limits are:
- `max_repair_attempts_per_validation_gate: 3`;
- `max_same_violation_repeats: 2`.

If either limit is exceeded, the workflow is blocked until human review or a
top-skill rule update resolves the repeated failure.

## Behavioral coherence

A node must not simultaneously own capabilities with mutually exclusive preconditions.

If capability A requires condition X, and capability B requires condition NOT-X — they belong to different state nodes.

Detection criterion:

Conflicting event handlers in a single node — handlers for opposite sides of a single transition:
- `mouseenter` / `mouseleave` — hover state
- `mouseover` / `mouseout` — hover state
- `pointerdown` / `pointerup` — press state
- analogous pairs with mutually exclusive preconditions

The presence of such pairs in a single node means the node contains hidden internal state that must be explicitly extracted into state nodes.

Not a violation:
- A single node registers both handlers to manage one continuous behavior (e.g. drag: `pointerdown` begins, `pointerup` ends a single action).

Canonical refactoring: extract NormalState and HoverState (or equivalents) as child state nodes. Each state node owns only those handlers that are active in its state.

## Typing fallback hierarchy

Typing priority:

1. strict nominal typing
2. explicit structural typing
3. documented weak typing

Rules:
- Moving to a weaker level is permitted only if the technology syntactically does not support a stricter level
- Convenience, verbosity, implementation speed, and local familiarity are not grounds for weakening
- `Realistic` means only technical impossibility of stricter typing, not its inconvenience
- If weak typing is used, it must be explicitly documented as a fallback, not as a norm
