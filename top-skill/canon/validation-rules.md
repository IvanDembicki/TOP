# Validation Rules

Result is invalid until all validation checks pass.
Compilation success is not architectural success.
Local functionality does not override TOP rules.

## Boundary validation
- No direct access to concrete implementation.
- No bypass around content.
- All interaction through allowed protocols.

## Protocol validation
- If a node has a separate content object, explicit internal access boundaries must exist: `IContentAccess` and `IControllerAccess`.
- Internal access boundaries must be explicit, typed, and hidden from the external world as far as the technology allows.
- Public node surface and internal access boundaries must not be mixed.
- Controller fields/references to content must be typed as `IContentAccess` or an equivalent narrow contract, not as the concrete content class.
- `IContentAccess` is controller-to-content only. It must not contain view-model values, state flags, callbacks, child-output handles, or data fields that content reads from the controller.
- Content requests controller-owned data, state, actions, and child/output handles only through `IControllerAccess`.
- No real interaction outside allowed protocol boundaries.


## Construction and locality validation
- Every TOP object is constructed at its architectural position in the tree.
- TOP construction attaches objects to context; it does not inject the state
  they will use.
- A TOP object constructor receives only the narrow contextual reference required
  to place that object inside its ownership boundary. Data packets, flags,
  callbacks, config/options/props-like objects, stores, services, child views,
  presentation values, visibility values, style values, text values, runtime
  state, and arbitrary additional arguments are `CORE-032`.
- Post-construction data/config/state/presentation pushing into child nodes,
  locally implemented content, connectors, or black-box boundaries through
  setter-style calls is `CORE-032`.
- Node constructors receive only the parent reference as their semantic argument; root `null`/`RootContext` is allowed only as a root ownership/bootstrap marker, not as dependency injection.
- Node/Controller public runtime entrypoints must not receive semantic data,
  derived facts, callbacks, handlers, services, stores, child fragments,
  config/options/props-like objects, parameter bags, runtime argument sets, or
  arbitrary props. Passing a parent-derived value into a child Node/Controller
  through target runtime input is `CORE-029`.
- Content constructors receive exactly one semantic argument: the owning controller instance typed only through the narrow `IControllerAccess`/target-equivalent interface.
- Content is not typed against, imported as, downcast to, or stored as the concrete controller class.
- Empty content-to-controller zero-contracts are narrow access interfaces implemented by the owning controller, not separate dummy runtime objects.
- No data, callbacks, handlers, flags, state, stores, services, child components, slots, prebuilt fragments, child view handles, child-output getter bundles, view-model objects, config/options/props-like objects, parameter bags, runtime argument sets, or arbitrary props are pushed into Content through constructors or any public runtime/composition entrypoint.
- Content pulls from owner; owner pulls from children when child output is required; children expose opaque handles.
- TOP spec props are declarative metadata, not runtime inputs.
- If a technology materializes Content through one public runtime input object/value, that input carries exactly one value: the owning controller instance typed only as the narrow content-to-controller owner access contract (`IControllerAccess` or target-equivalent), not a merged `IContentAccess & IControllerAccess` bundle or a general props/config/data/composition bag.
- Content does not receive `IControllerAccess` members decomposed as separate runtime props/parameters, JSX attributes, named function arguments, or an ad hoc object literal assembled at the render/composition call site. Decomposed owner access input is `CORE-030`.
- The owner access runtime value is the owning controller itself typed through the narrow interface. It is not an adapter/facade object, externally assembled method bag, or inline closure bundle. If a target cannot pass controller identity at all, this is a non-final target adapter constraint and must be validated as a deviation, not as canonical TOP.
- Controller receives, stores, and uses its own Content instance typed only as `IContentAccess`/target-equivalent. Controller does not receive decomposed content lifecycle/materialization members, method bags, facade/adapters, closure objects, concrete Content types, platform primitives, or objects assembled outside the controller/content construction boundary as substitutes for `IContentAccess`. Decomposed content access input is `CORE-031`.
- `IControllerAccess` methods are controller-boundary methods owned by the controller; raw imported functions, externally owned method references, service methods, store actions, or callbacks are not exposed directly to Content as access methods.

Canonical repair for context data injection:
- remove additional constructor arguments;
- add the missing value/request to the appropriate access contract;
- let the object pull the value through that contract;
- split pushed state/structural alternatives into explicit child state nodes;
- wrap external component configuration behind a black-box boundary with a
  narrow explicit interface;
- route service/store/global dependency access through the owning context,
  parent, or controller contract.

## Shared derived fact repair validation
- A repair must not replace derivation duplication with parent-to-child runtime input tunneling.
- A repair must not replace Node/Controller semantic runtime input (`CORE-029`) with independent duplicate derivation of the same fact from the same cross-cutting source.
- Shared or parent-owned derived facts must move through an explicit typed access/update boundary, named controller method, or modeled connector contract after the child exists at its tree position.
- If that boundary is not present in the current model, validation must keep the repair blocked or incomplete; it must not accept a local workaround that merely swaps `CORE-029` and Invariant 14.

## Validation freshness

- Validation/review must load the current skill rules required for the active task.
- Validation/review must re-read target artifacts in the current pass.
- Prior session reads, old skill memory, previous generation context, or earlier file inspections are not validation evidence.
- If a report lists a file as checked without reading it in the current pass, validation is incomplete.

## Content validation
- Content has no architectural will.
- Content does not manage lifecycle.
- Content does not know or use the full public node surface directly; it interacts with the controller only through `IControllerAccess`.
- Locally implemented content must contain no conditional selection logic. It
  must not decide, derive, branch, select, toggle, or compute which structure,
  class/style/token, text, icon, visibility, handler, child output, platform
  primitive, representation, or capability should be used.
- Locally implemented content may only materialize a structurally static content
  shape and apply already-resolved primitive values received through its owning
  controller access contract.
- Controller must not imperatively command, mutate, update, show, hide,
  configure, or push presentation state into locally implemented content.
- Controller-to-content access through `IContentAccess` is lifecycle and
  materialization access only, such as obtaining the root content primitive or
  participating in controlled lifecycle. It is not a presentation command
  channel.
- For locally implemented presentation content, `IContentAccess` must not expose
  show/hide, set-visible, set-text, set-style, set-class, apply-state,
  render-with, update-from-state, or equivalent imperative presentation
  commands.
- For data content, validation must not misclassify a data node controller
  domain method such as `setAge(value)`, `updateName(value)`, or
  `replaceRecord(record)` as a presentation-content push when access to that
  data controller is architecturally valid. The data controller may mutate its
  own private data content internally through `IContentAccess` or an equivalent
  storage boundary. External direct data-content mutation and presentation
  content direct access to data content remain violations.
- Any `if`/`else`, `switch`/`case`, ternary operator, conditional rendering,
  conditional return, multiple return branch, `&&`/`||` conditional selection,
  `match`/`when`/guard branch, or equivalent conditional construct inside
  locally implemented content is a hard `CORE-015` validation error when it
  participates in selection or derivation.
- Content may execute low-level platform commands on its own implementation material, including subscribe/unsubscribe and analogous operations, but it must not interpret those operations as architectural decisions or use them as an external communication channel.

## Semantic event/request validation
- Locally implemented content reports semantic intent to its owning controller
  through methods such as `requestAgeChange(value)`, `onAgeInputCommitted(value)`,
  `requestToggleMode()`, or `requestSubmit()`.
- Locally implemented content must not decide where the data goes or mutate data
  models directly.
- A controller may call another controller's typed public/domain method only
  when the relationship is architecturally allowed: direct parent, direct/static
  child controller through public contract, guaranteed typed ancestor, connector
  boundary, or explicitly declared data-tree reference.
- If the current controller is not the owner of the decision, it raises or
  passes a semantic event upward instead of directly mutating an unrelated node.

## Controller validation
- Controller owns behavior, lifecycle, orchestration, branching.
- Controller remains a controller-only artifact.
- Controller is not itself a view, component, widget, composable, render function, route/screen component, framework lifecycle UI object, or public runtime input receiver for content composition.
- Controller does not return render output, render trees, platform views, layout fragments, style objects, animation objects, or content artifacts.
- Controller is not mounted, registered, invoked, or executed by the target runtime as the renderable UI/content entity.
- Target UI lifecycle APIs, hooks, callbacks, or equivalent lifecycle mechanisms must not become the controller lifecycle.
- Controller does not use render primitives as communication channel.

## Lifecycle validation
- Content is created on demand.
- Content is destroyed on deactivate/close by default.
- No hidden retention.

## Method semantics validation
- Methods are used strictly by intended semantics.
- No semantic overloading (e.g. init bucket).

## Typing validation
- All boundaries explicitly typed.
- No implicit context objects.
- No weak typing where strict is possible.

Operational checklist: `rules/typing-checklist.md`.
Behavioral analysis and typing analysis are independent passes. The absence of behavioral violations does not imply the absence of typing violations.

## Semantic preservation validation
- Layer B must preserve original user intent, system intent, interaction intent, feedback intent, state model, layout intent, constraints, and accessibility semantics where applicable.
- Platform-specific source artifacts must be removed from Layer B or quarantined as evidence, not preserved as meaning.
- Semantic vocabulary may be extended only with platform-independent meaning.

## Behavior preservation validation for migration
- Legacy tests are requirements evidence.
- A migrated scope with legacy tests, snapshots, fixtures, QA scripts, executable examples, or documented test cases must have a Behavior Preservation Plan before validation can pass.
- Each legacy behavior expectation must be extracted or discarded with explicit behavior-level justification.
- Each normalized requirement must be mapped to TOP nodes, contracts, state, events, lifecycle, and prompt update requirements.
- Each prompt requirement derived from legacy tests must be covered by preserved, adapted, replaced, or newly generated TOP-compatible tests.
- A legacy test may be discarded only if its behavior is declared obsolete by explicit decision or re-covered through a normalized TOP requirement.
- Missing Behavior Preservation Agent execution is `WF-010`.
- Lost, weakened, unmapped, unprompted, or uncovered test-covered behavior is `CORE-028`.

## Validation verdict rule
- `overall_status` must be `fail` when any confirmed core violation remains.
- A documented migration waypoint or accepted core deviation remains in
  `core_violations`; documentation explains the state but does not convert the
  result into `pass`.
- Validation must not route to Final Audit while confirmed core violations or
  accepted core deviations remain.
- Reporting `pass`, `ready`, or `ready_for_use` with remaining core violations
  is `WF-011`.

## Source-platform leakage validation
- DOM, CSS, Flutter widgets, UIKit/Android classes, framework APIs, and source-specific event APIs must not appear in Layer B.
- A non-source target adaptation must not copy source-platform primitives unless the same primitive is native and justified for that target.
- Generated target artifacts must trace target decisions to Layer B semantics, not to source-platform notes.

## Target adaptation validation
- Layer C must explicitly mark each semantic element as preserved, adapted, or dropped with reasons for adapted/dropped decisions.
- Target adaptation must use native target expectations and must not introduce new business logic.
- Target adaptation must not alter TOP ownership, lifecycle, controller/content boundaries, or structural invariants.

## TOP artifact layout validation
- New migration branch specs must be stored under `top/specs/` unless an
  established project-local TOP index explicitly declares another convention.
- Implementation prompts must live under `top/prompts/` and mirror the semantic
  branch position.
- Migration status and tracking artifacts must live under `top/migration/`.
- If specs or prompts declare future implementation materialization, the branch
  must declare and prepare an implementation source root. The default for new
  migration branches is `top_src/<branch-id>/`.
- Empty source roots created before generation must contain `.gitkeep` or an
  equivalent placeholder so the materialization path is visible to later agents.
- Expected Materialization artifact stems, `props.sourceRoot`, and `props.dir`
  must resolve under the same source root.
- A migration/modeling result that creates specs/prompts but no implementation
  must report an honest phase status such as analysis-only, modeled, or
  materialization-pending. It must not report validated or complete.
- Noncanonical spec placement is `CONV-007`.
- Missing or inconsistent implementation source root is `CONV-008`.
- A migration/materialization handoff without canonical paths, source root, and
  honest phase status is `WF-013`.
- A migration-mode task that creates or changes TOP artifacts without
  `top/migration/MIGRATION_PLAN.md` is `WF-014`.
- A migration-mode handoff or artifact change without an appended
  `top/migration/MIGRATION_LOG.md` entry is `WF-015`.
- A migration-mode task that creates or changes TOP artifacts without current
  `top/migration/MIGRATION_WORKFLOW.json`, or with workflow JSON that disagrees
  with plan/status/log, is `WF-016`.

## Migration workflow/plan/log validation
- `MIGRATION_WORKFLOW.json` must exist before migration scope analysis,
  modeling, generation, repair, validation, or final audit proceeds.
- The workflow JSON must parse and record current scope, branch id, current
  phase, phases, responsible agents, gates, handoffs, and next phases.
- `MIGRATION_PLAN.md` must exist before migration scope analysis, modeling,
  generation, repair, validation, or final audit proceeds.
- The plan must record current scope, branch id, phases, responsible agents,
  planned artifacts, validation gates, behavior preservation routing, and
  rollback/stop points.
- Workflow JSON and plan must agree on selected scope, branch id, phase order,
  responsible agents, gates, and current phase.
- If the user specified a starting scope, the plan must preserve that scope or
  explicitly block with reasons.
- If the user did not specify a starting scope, the plan must record the
  selection rationale.
- `MIGRATION_LOG.md` must exist and contain append-only entries for each
  migration-mode handoff and persistent artifact change.
- Each log entry must name timestamp, agent, phase, files read/changed,
  decisions, validation/self-check result, and next stage.

## Canon rule
Only canonical patterns are allowed. Everything else is a violation.

## Hidden switchable check

Violation signal (both conditions must hold simultaneously):

1. The node accesses external architectural state (isEditMode, openedChild, lifecycle phase, etc.)
2. And as a result changes:
   - the visual representation of its constituent elements (show/hide, swap)
   - or the available behavior (drag, event handlers, interactive buttons)

Not a violation:
- `refresh()` changes only model data (text, label, icon from data model) — see the formal `refresh()` contract in `references/tree-node-contracts.md §5`
- Node behavior is identical in both states

Classification: `core_violation`
Reason: hidden ownership of behavior, hidden lifecycle

The node is a candidate for switchable refactoring. See `rules/pattern-recognition.md` — Pattern #1.

## Behavioral coherence check

Violation signal:

A node registers handlers for opposite sides of a single state transition:
- `mouseenter` + `mouseleave` (or `mouseover` + `mouseout`) — hover
- `pointerdown` + `pointerup` — press
- analogous mutually exclusive pairs

Exception: if the handler pair manages a single continuous action (drag start / drag end) — not a violation.

Classification: `core_violation`
Reason: hidden internal state; the node contains behavior that must be split across state nodes.

The node is a candidate for switchable refactoring. See `rules/pattern-recognition.md` — Pattern #2.

## Structural correspondence check

Prompt paths and code paths must reflect the same semantic position of the node in the tree.
If a node belongs to a particular semantic branch, its prompt and its implementation must be located in the corresponding subdirectories of their respective roots.

Definition: `references/artifact-layout-and-branch-derivation.md` — Structural Correspondence Rule.

Classification: `skill_convention_violation`

## Logic in content check

- Locally implemented content conditional selection logic is a hard validation
  error (`CORE-015`).
- There is no presentational exception. Visibility toggles, styling decisions,
  formatting decisions, text/icon selection, handler selection, conditional
  child output, conditional platform primitive selection, and structural
  selection are controller/tree decisions, not content decisions.
- Low-level platform-command execution inside content is permitted only when it
  is limited to the content's own implementation material, contains no
  selection/derivation decision, and forwards semantic events only through
  `IControllerAccess`.
- If locally implemented content needs an already-resolved primitive, it must
  request that primitive through the owning controller access contract.
- Controller must update its own state and mark the node/content/runtime dirty
  or request lifecycle/render refresh through the node/runtime mechanism. It
  must not push show/hide/update/apply-state/class/style/render-with commands
  into locally implemented content.
- If locally implemented content needs alternative structures, elements,
  handlers, visibility modes, representations, or capabilities, the alternatives
  must be modeled as explicit child state nodes.
- External, native, third-party, or self-contained logic may be wrapped only as
  black-box component content with a narrow explicit interface.
