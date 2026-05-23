# Pattern Recognition Rules

A catalog of architectural patterns that must be recognized during analysis.

Each pattern describes: detection signals, architectural problem, canonical refactoring.

## Analysis protocol

Analysis is performed in two independent passes:

**Pass 1 — Code analysis**
Check each node for signals from groups A–G.

**Pass 2 — Spec analysis**
For each node that has a spec/prompt: read the description and verify — does the spec describe N distinct states of the node? If yes — verify that the code implements N explicit state children.

Both passes are mandatory. The absence of code signals (pass 1) does not exempt from spec analysis (pass 2). Platform mechanisms (CSS, system events) hide code signals but do not eliminate the architectural problem.

---

## Universal hidden-state signals

The following signals indicate that a node contains hidden state — regardless of the specific pattern.

Platform-specific examples in this section are examples for semantic review
only. They must not be copied into platform-neutral quick validation scripts.
Quick validation scripts must detect only language/syntax-level conditional
constructs and must remain independent of DOM, React, Flutter, Compose, SwiftUI,
Android, iOS, or any other target framework.

### Group A — Locally implemented content conditional selection

Inside a locally implemented content boundary, any language-level conditional
construct is a candidate `CORE-015` signal when it participates in selecting or
deriving structure, class/style/token, text, icon, visibility, handler, child
output, platform primitive, representation, or capability.

Output derivation inside locally implemented content is also a candidate
`CORE-015` signal even when no branch is present. Content-side formatting,
string concatenation, hardcoded display values, style/class/token selection,
icon selection, visibility value construction, handler choice, or representation
computation means content is deriving output instead of applying an
already-resolved primitive from controller access.

Platform-neutral construct signals:
- `if` / `else`
- `switch` / `case`
- ternary or conditional-expression syntax
- conditional return or multiple return branches
- boolean short-circuit selection such as `&&` or `||`
- `match` / `when` / guard branches
- equivalent language constructs that choose between alternatives

The prefilter does not make the final architectural verdict by itself. It
reports candidates for Validation Agent review. Validation confirms `CORE-015`
when the construct participates in content-local selection or derivation.

Canonical repair:
- primitive value derivation moves to the owning controller and is requested as
  an already-resolved primitive through controller access;
- output formatting, concatenation, constants, runtime/environment/platform
  values, and asset-derived display values move to the owning controller;
- structural, visibility, handler, representation, or capability alternatives
  become explicit child state nodes;
- external, native, third-party, or self-contained logic is wrapped as
  black-box component content with a narrow explicit interface.

### Group A2 — Context data injection

TOP construction attaches objects to context; it does not inject the state they
will use. Platform-neutral recognition should look for constructor signatures,
factory calls, or runtime entrypoints for known TOP object roles that receive
more than the allowed context argument.

Candidate signals:
- constructors for static nodes with arguments beyond parent/context;
- constructors for runtime-created branch roots with more than parent/context
  plus one canonical Runtime Branch Binding input;
- runtime branch constructors whose extra input is a props/config/callback bag,
  scattered entity fields, mutable raw model object, service/store object,
  presentation value, or arbitrary runtime state;
- constructors for locally implemented content with arguments beyond the owning
  controller access contract;
- constructors or factories for connectors or black-box boundaries with data,
  config/options/props-like objects, callbacks, handlers, flags, stores,
  services, state, text, visibility, style, presentation values, child views, or
  platform primitives as additional inputs;
- post-construction setter-style injection into child/content objects, such as
  apply-config, set-data, set-visible, update-text, set-style, set-callbacks, or
  equivalent calls.

The prefilter reports these as possible `CORE-032` candidates for Validation
Agent review. It must not make the final semantic verdict by itself.

Do not classify an architecturally allowed data node controller domain method
such as `setAge(value)`, `updateName(value)`, or `replaceRecord(record)` as a
controller-to-presentation-content push. The violation is direct mutation of raw
data content from outside the owning data controller, constructor data
injection, or setter-style packet pushing into child/content objects.

Canonical repair:
- remove additional constructor arguments;
- for runtime-created branches, replace scattered data arguments with an entity
  context reference, stable identity key, or typed immutable DTO fallback;
- expose the missing value/request through the appropriate access contract;
- let the object pull the value through that contract after attachment;
- model pushed state or structural alternatives as explicit child state nodes;
- wrap external component configuration behind a black-box boundary with a
  narrow explicit interface;
- route service/store/global dependency access through the owning context,
  parent, or controller contract.

### Group A3 — Migration wrapper and giant-node signals

During migration, a user-named screen, route, tab, component, section, or file
is a scope root, not a final node boundary.

Candidate `WF-017` signals:
- phrases such as "single-node architecture", "single hub node", "no separate
  data child nodes", or "all hooks inline";
- a very large `IControllerAccess`/target-equivalent method set;
- many `PanelDisplayStyle` or equivalent display-token methods;
- many pending actions, pending mutations, or bridge callbacks in one node;
- many modal/form/list/card/row/tile/helper components left local without
  classification;
- target hook clusters in locally implemented content combined with effect
  workflows, mutation construction, routing, alerts, store writes, or pending
  action execution;
- direct global store access labeled architecturally correct instead of
  residual/connector/data-boundary access.

The canonical question is: what hidden tree is inside this legacy scope?

Validation confirms `WF-017` when the migration output lacks recursive
decomposition evidence, single-node proof, reusable-pattern analysis,
PanelDisplayStyle justification, hook bridge residual classification, or helper
component classification.

### Group A3a — Library object external context boundary signals

Library Object External Context Boundary is a strong recommended modeling
pattern, not a hard invariant.

Review signals:
- a descendant inside a runtime/library branch directly reaches an ancestor,
  global store, data tree, presentation/style tree, asset tree, service,
  permission source, or connector;
- external access is attached to multiple internal descendants instead of the
  library object root;
- branch prompts/specs do not state whether the external dependency belongs to
  the branch-root contract, an explicit connector, or an approved exception;
- a runtime/library branch root is treated only as a data holder and not as the
  external context boundary for services, assets, presentation/style context,
  permissions, and other external trees.

Review questions:
- is the external dependency part of the explicit library object root contract?
- should the root obtain this access and expose a narrower resolved
  contract/value/capability to the descendant?
- is external context leaking into the branch through accidental direct
  dependencies?

### Group A4 — Concrete content privacy and fragment-output signals

Concrete locally implemented content is private to the owning controller.

Candidate `CORE-033` signals:
- files outside the owning controller import a `*Content` class;
- files outside the owning controller instantiate `new *Content(...)`;
- controller fields or public APIs are typed as concrete content instead of
  `IContentAccess`/target-equivalent;
- adapters, helpers, parents, siblings, or children downcast to, store, inspect,
  or call concrete content.

Candidate `CORE-034` signals:
- controller public methods return platform view fragments, render/build trees,
  JSX/widget/composable fragments, content fragments, style/layout fragments,
  animation objects, content-owned setters, or platform mutation handles;
- methods named like `get*View`, `render*`, `build*Content`, or `get*Fragment`
  return inspectable platform/content implementation rather than an opaque
  placement-only handle allowed by canon.

Candidate `CORE-035` signals:
- content-owned setters/mutation handles are stored in controller fields;
- content passes setter handles through `IControllerAccess`/`IContentAccess`;
- helpers/adapters capture content setters for later controller-driven updates;
- callback registration is used as a hidden controller-to-content presentation
  command channel.

Canonical repair:
- keep concrete content imports/instantiation inside the owning controller only;
- store the content as `IContentAccess`;
- expose controller-level values or opaque placement handles only where canon
  permits;
- remove crossed setter handles and use controller state, dirty/render/lifecycle
  refresh, and content pull of already-resolved values.

### Group A5 — Spec shape and generated layout signals

Candidate `CONV-009` signals:
- project TOP specs model nodes through ad hoc `id`/`name` fields without a
  canonical `type` or project-approved equivalent;
- generated prompt/code cannot identify node kind, parent/child topology, or
  content classification from the spec shape.

Candidate `CONV-010` signals:
- generated implementation files flatten a semantic subtree into one folder
  without explicit materialization rationale;
- prompt paths and code paths do not mirror the same semantic branch structure;
- `props.dir`, `props.sourceRoot`, and Expected Materialization disagree.

Quick validation may report these as hard errors for unambiguous spec files or
as agent review candidates when project conventions are unclear.

### Group A6 — Missing checkpoint / non-independent validation signals

Candidate `WF-020` signals:
- migration outputs hand off without branch-scoped infrastructure,
  decomposition, model/spec, precheck, generation, post-generation validation,
  repair, or final-audit checkpoint artifacts;
- shared `MIGRATION_LOG.md` lacks an append-only entry for a persistent artifact
  change or handoff.

Candidate `WF-021` signals:
- validation cites generator memory, previous chat context, or self-check text
  as proof without current-pass file reads;
- final audit trusts type-check or generator output without adversarially
  re-reading generated source, specs, prompts, contracts, and logs.

### Group A6b — Validation control and rejection protocol signals

Candidate `WF-023` signals:
- generation, repair, modeling, migration, or implementation reports use
  verdict phrases such as `TOP-clean`, `CORE-015 clean`, `canon compliant`,
  `validation passed`, `no violations`, `ready_for_manual_QA`,
  `ready_for_use`, or `final_status: pass` for their own artifacts.

Candidate `WF-024` signals:
- validation treats previous agent reports, migration log commentary, or chat
  history as proof instead of re-reading current artifacts.

Candidate `WF-025` signals:
- PASS without artifacts reviewed, files inspected, canon rules checked,
  detection/search patterns, artifact types, or per-check evidence.

Candidate `WF-026` signals:
- Final Audit accepts validation without auditing validation evidence, file
  lists, current-artifact inspection, and rejection closure.

Candidate `WF-027` signals:
- failed validation without a rejection ticket or appended validator log entry.

Candidate `WF-028` signals:
- generation/repair after rejection without reading or updating
  `top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md`.

Candidate `WF-029` signals:
- a later generation/repair repeats a strategy already rejected in the generator
  learning ledger.

Candidate `WF-030` signals:
- more than `max_repair_attempts_per_validation_gate: 3` repair attempts at one
  gate;
- more than `max_same_violation_repeats: 2` repeats of the same violation.

Candidate `WF-031` signals:
- a generation, repair, migration, or spec-sync pass also writes validation or
  final-audit claims and declares delivery `complete`;
- delivery `complete` appears without a separate judicial pass id, validation
  report reference, judicial handoff artifact reference, or final audit report
  reference;
- delivery `complete` appears without `executionIsolationLevel:
  runner-enforced` and `verificationEvidenceLevel: hard-check-verified`;
- protocol-only execution claims `runner-enforced`;
- schema validation or hard-check output is treated as proof of role isolation;
- a required hard-check gate is `fail` or `not_verified`;
- `GENERATION_OUTPUT.md` claims delivery completion rather than generation
  completion;
- public-record summaries upgrade `blocked`, `partial`, `fail`, or
  `not_verified` judicial findings to complete.

Incremental validation signals:
- a large generation or migration phase proceeds without micro-check entries
  for newly created specs, prompts, generated node files, folders, or rejection
  tickets;
- related artifact groups are handed off without a meso-check for topology,
  boundaries, layout, or prompt/spec consistency;
- a full phase reaches final audit without a macro-check for the phase.

### Group A7 — Migration git branch safety signals

Candidate `WF-022` signals:
- migration artifacts or generated source were created while the repository was
  still on the user's current branch;
- branch name is missing, ambiguous, or does not match
  `top-migration/<branch-id>` or a documented deterministic equivalent;
- the first `MIGRATION_LOG.md` entry lacks the git safety gate;
- the log does not record initial branch, migration branch, branch creation or
  checkout result, working tree status, remote status, unrelated uncommitted
  changes, write permission, local commit policy, and push policy;
- unrelated uncommitted changes were mixed with migration output;
- remote push occurred without explicit user request;
- a local commit occurred without explicit request or a documented commit phase.

Canonical repair is not to continue writing. Stop, preserve user work, ask for
commit/stash/branch clarification when needed, switch/create the dedicated
migration branch, append the git safety gate, then resume migration writes.

### Group A7b — Required post-generation delivery gate signals

Blocking validation candidates:
- Content Child Import Violation: parent `*Content` artifacts import,
  instantiate, render, or type against child concrete content classes instead of
  requesting child materialized outputs through controller access.
- Prompt-Code Contract Drift: prompts/specs require child-output methods such
  as `getAccountIdentityView(): MaterializedOutput`, but implementation
  materializes a different architectural contract such as
  `getAccountIdentityAccess()` without an approved prompt/spec update.
- Node Global Store Access Violation: `*Node` or controller artifacts directly
  import or call React hooks, Zustand/global stores, `useAppStore`,
  route/navigation hooks, UI framework hooks, runtime singleton state, or
  target hook APIs instead of explicit bridge/runtime/data boundaries.
- Bridge Callback Injection Violation: TOP nodes/controllers receive raw
  callback functions from route/framework layers instead of a narrow bridge or
  runtime context boundary.
- Self-Audited Pass Report Warning: the same pass generated/repaired artifacts,
  wrote validation/final audit, and declared completion without independent
  judicial evidence.

These patterns are validation-gate candidates. Quick scripts may surface them,
but the Validation Agent must inspect actual files, prompts, and specs before
issuing the final architectural verdict.

### Group A8 — Public wrapper, node atomicity, and spec/layout signals

Candidate `CORE-036` signals:
- a public node/controller artifact is just a target-framework wrapper around
  concrete locally implemented content;
- external/parent/adapter code can name a concrete content class or wrapper to
  reach content.

Candidate node atomicity signals:
- one node owns several unrelated workflows, modal systems, form systems, list
  item families, bridge clusters, or state sections;
- a screen section is dismissed as "just part of the screen" without node
  candidacy analysis.

Candidate folder/tree layout signals:
- generated node files for a semantic subtree are flattened into one branch
  folder without explicit materialization rationale;
- child nodes do not have child folders under the parent folder when the target
  materialization policy would allow it.

Candidate strict TOP spec shape signals:
- node-like objects use generic `type` values such as `Node`, `Component`,
  `View`, or `Controller` while real identity appears only in `id`/`name`;
- node-like objects omit canonical `type`, `doc`, `prompt`, `props`, or
  `children` without a project-approved equivalent.

### Group A9 — Runtime controller tree shape signals

TOP generation must produce a controller tree, not controller-shaped service
files.

Candidate `CORE-037` signals:
- a class/function/module is named or treated as a controller but does not
  extend the project runtime node base or implement the project runtime node
  interface;
- a non-root static controller has no parent/context relation;
- a root controller has no root/host context or runtime tree root mechanics;
- a controller has no child ownership/registration, children access, lifecycle,
  disposal/cleanup, or declared child policy;
- a non-leaf spec node's generated controller does not construct child
  controllers;
- a declared child is represented only as content, public wrapper, render
  fragment, or target artifact;
- a controller file is only a collection of functions, hooks, helpers, or
  service calls with no relationship to spec tree position;
- generated folder topology and child construction do not mirror the spec tree.

Canonical repair:
- make the artifact a real runtime node controller by extending/inheriting the
  project runtime node base or implementing the project node interface;
- attach static nodes to parent/context and root nodes to root/host context;
- add/inherit lifecycle, child ownership, children access, and child policy;
- construct child controllers at their tree positions;
- reclassify service/helper logic as connector, data controller, black-box
  boundary, or private implementation detail when it is not a TOP node.

Required checkpoints:
- micro-check `generated-controller-runtime-shape` after each generated
  controller file;
- meso-check `controller-tree-topology` after each generated subtree.

### Group B — Visibility and style manipulation

- `el.style.display = 'none' / 'block'` — conditional hiding based on mode (not model data)
- `classList.add/remove/toggle` with names reflecting state (`active`, `hover`, `pressed`, `edit-mode`)
- `el.style.opacity`, `el.style.visibility`, `el.style.pointerEvents` — conditionally toggled
- `el.hidden = condition`

Important: inside locally implemented content, style/class/token selection is
not permitted even when it looks presentational. The owning controller must
provide already-resolved primitive values, or the alternatives must become
explicit child state nodes.

### Group C — Dynamic DOM manipulation

- `appendChild` / `removeChild` / `insertBefore` called inside `refresh()` — structure changes conditionally
- platform visual primitives created inside `refresh()` instead of the content materialization phase
- A node has two DOM elements with overlapping visual roles (`_viewEl` and `_editEl`, two sets of buttons)

### Group D — Internal state flags

- Field `_isHovered`, `_isPressed`, `_isExpanded`, `_isActive`, `_currentState` — the node tracks its own visual state
- Field `mode`, `status`, `phase`, `_mode`, `_status`, `_activeMode`,
  `_displayMode`, or equivalent — the node tracks an owner-held architectural
  state that can select representation, behavior, hit targets, context actions,
  or capabilities
- Pattern `_listenersAdded = false` with a check before `addEventListener` — conditional handler registration
- Any boolean/enum field that changes rendering or behavior, not model data

### Group E — Dynamic handler registration

- `addEventListener` / `removeEventListener` called in `refresh()` — not during initialization
- One handler registered with different functions depending on mode
- Handlers for opposite sides of a state transition in the same node (see Pattern #2)

### Group F — Behavior-altering attributes

- `el.draggable = condition` — toggled in `refresh()`
- `el.disabled = condition`
- `input.readOnly = condition`

These are not model data. If they are toggled based on mode, status, phase, or
another architectural state — this is hidden behavioral state.

### Group G — Structural branching in refresh()

- `if/else` in `refresh()` where branches change not data but visibility, structure, or available actions
- Different child nodes active in different branches

### Group H — Delegation to state objects (State pattern)

- Node stores a field `_state`, `_currentState`, `_strategy` — a reference to an object managing behavior or rendering
- Node delegates rendering, content materialization, or event handling to the state object
- Node switches the state object in `refresh()` or in response to events: `this._state = new HoverState(this)`
- State classes implement a common interface (render, activate, deactivate, etc.)

The State pattern does not eliminate the problem — it encapsulates it. Behavioral ownership remains hidden inside the node, lifecycle is implicit.

In TOP terms: if a node needs the State pattern — this is a signal that a switchable holder is needed with explicit state nodes as tree children, not objects inside a single node.

### Group I — Multiple states described in spec

A node has two or more mutually exclusive visual representations or sets of
available actions, conditioned by any architectural mode/status/context —
including owner-held state inside the same node. The storage location of the
mode does not matter; what matters is whether the state selects representation,
behavior, hit targets, context actions, or capabilities.

This signal does not require the presence of code indicators (groups A–G). It is detected through the node's spec/prompt.

Signal: the spec or prompt describes N distinct states of the node (normal/hover, normal/pressed, view/edit, expanded/collapsed, etc.).

Violation: the code does not implement these states as explicit state nodes — instead uses a platform mechanism (CSS, system events, animations) that is invisible to the code analyzer.

Important: the absence of code signals (groups A–G) does not mean the absence of a violation. The platform mechanism hides the problem but does not eliminate it.

### Combination rule

One signal — reason to be alert. Two or more signals simultaneously — high probability of a hidden switchable. The more groups affected, the higher the probability of a violation.

---

## Switching vs. dynamic composition

Before applying Pattern #1, verify which mechanism is architecturally correct.

A **hidden switchable** is a violation only when switching is the right choice.
If child nodes appear and disappear based on data or external configuration — that is
dynamic composition (add/remove), not switching. Applying the switchable refactoring
to a dynamic composition case is itself an architectural error.

See `rules/decision-trees.md` — **Decision tree: switching vs. dynamic composition**.

---

## Pattern #1 — Hidden switchable

### Definition

A node that independently manages switching between fundamentally different
representations, behaviors, hit targets, context actions, or capabilities by
referencing architectural state.

A hidden switchable may be monolithic — it may have no explicit child state
nodes. It is recognized not by its child structure, but by the fact that it
reads mode/status/phase/openedChild state, including owner-held state inside the
same node, and then changes its own representation or behavior.

### Detection signals

Both conditions must hold simultaneously:

1. The node reads architectural state:
   - `isEditMode`, `mode`, `status`, `openedChild`, lifecycle phase,
     operating mode, owner-held mode flag, etc.

2. And as a result changes at least one of:
   - visual representation of constituent elements (show/hide, swap, structural change)
   - available behavior (drag enabled/disabled, event handlers registered/removed, interactive elements appear/disappear)
   - hit-test surface or interactive target set
   - context actions or capability availability

### Not a violation

- The controller only updates already-resolved model data exposed through a
  narrow access contract and node behavior is identical in both states.

Inside locally implemented content, text/color/style/visibility/handler or
representation selection is still not allowed. The content may apply the
already-resolved primitive value, but it must not select or derive that value.

### Architectural problem

- Hidden behavioral ownership: unclear who is responsible for drag, add, delete
- Hidden lifecycle: behavior activation/deactivation occurs implicitly through `refresh()`
- Violation of the principle: each node must have a clearly bounded role

### Canonical refactoring

The node becomes an explicit switchable holder. A separate state node is created for each mode.

```
Before (violation):
  TreeItemRowNode
    content materialization / refresh() → reads isEditMode
    → shows/hides DragHandle, AddBtn, DeleteBtn
    → enables/disables draggable and drag listeners

After (canonical):
  TreeItemRowNode  ← switchable holder
    ├─ TreeItemRowViewStateNode
    │    ├─ ToggleBtnNode
    │    └─ NodeLabelNode
    │    (drag is architecturally absent — not disabled, but non-existent)
    └─ TreeItemRowEditStateNode
         ├─ DragHandleNode
         ├─ ToggleBtnNode
         ├─ NodeLabelNode
         ├─ AddBtnNode
         └─ DeleteBtnNode
         (el.draggable = true, drag listeners registered here)
```

### State node rules

- ViewState is open by default
- EditState is activated via `onBranchOpen()` — not via `isEditMode`
- Each state node mounts its DOM on activation, unmounts on deactivation
- A state node **does not read** the mode/status it represents — it **is** the representation of that mode/status
- Functionality absent in ViewState is not hidden — it architecturally does not exist in that state

### Active-state operation/query delegation

When a switchable holder exposes an operation or query that belongs to the
current active state, it forwards to `openedChild` only.

Canonical form:

```text
getActiveTarget(input):
  return openedChild.getActiveTarget(input)
```

The operation name is illustrative. The same rule applies to hit-test, target
lookup, event routing, active command availability, active capability checks,
and active output requests.

State children own their answer. A non-interactive or unavailable state returns
`null` or the project's equivalent no-result value. An edit state and a display
state may expose different targets or capabilities through their own
implementations. The holder does not encode those differences.

Anti-patterns:
- the holder treats missing/null `openedChild` as normal active behavior;
- the holder uses nullable opened-child fallback instead of ensuring a selected
  opened child;
- the holder loops over all state children and asks closed siblings for active
  behavior;
- external traversal inspects holder `mode`/`status` or state siblings to decide
  current-state behavior;
- leaf nodes carry mode guards while the holder still walks closed branches.

Closed state siblings may remain in the tree for persistence, caching, or future
switching, but they are not part of the active behavior, pointer, context-action,
or capability surface until opened.

This is primarily a state-replacement correctness rule. Performance is a
secondary benefit.

### Node-owned downward query/event propagation

When a query or event travels downward, it enters through an approved
propagation entrypoint and then becomes node-owned propagation.

The entrypoint may be a tree root, branch root, interaction-layer node,
viewport/canvas node, connector boundary, or another declared subroot. It does
not have to be the whole application root.

After entry, each node decides locally whether to answer, return no-result,
stop, delegate to `openedChild`, delegate to selected children, or delegate
through a connector/adapter. The external caller or traversal mechanism must not
inspect internal modes, closed state siblings, child policies, platform
representation, or external-tree internals to steer propagation.

Candidate violations:
- a global walker branches on `mode`, `status`, state child names, or
  unavailable/edit/display concepts outside the node;
- a traversal mechanism loops through closed switchable state siblings for an
  active behavior query;
- external code directly traverses a connected external tree instead of calling
  the node's explicit connector/adapter boundary;
- the traversal mechanism decides which nodes are "view" or "interactive"
  through out-of-band knowledge instead of asking node contracts.
- ask-then-handle traversal such as `if child.canHandle(event)
  child.handle(event)`;
- capability preflight probes such as `hasCapability`, `isInteractive`,
  `supportsEvent`, `listensTo`, `hasPointerMove`, `canHover`, or equivalent
  names used by external traversal to decide which descendant receives an
  operation/query;
- code that treats a no-op/no-result from one node as permission for the caller
  to inspect the node's children or try closed/internal branches itself.

Canonical repair:
- introduce an approved propagation entrypoint;
- move traversal policy into node/controller methods;
- let switchable holders delegate active-state behavior to non-null
  `openedChild`;
- let connector nodes translate and forward through explicit adapters;
- make no-result a node response, not an external traversal assumption.
- replace ask-then-handle preflight with tell-only propagation: call the node's
  declared handler/query and let that node return result/no-result, no-op, stop,
  or delegate deeper;
- move no-op/no-result policy to the highest owning node boundary that already
  knows the subtree has no relevant active behavior.

Capability/reporting methods are not automatically forbidden. They become a
`CORE-039` candidate when they are used by an external caller as a preflight
gate to steer propagation through another node's internal subtree.

### Agent chain for refactoring

```
Domain Structuring Agent
  → identify N states, extract holder, describe responsibility of each state node

TOP Modeling Agent
  → model holder + state nodes in the spec tree

Canon Precheck Agent
  → verify that state nodes do not read the mode/status they represent
  → verify that holder does not duplicate another mode/status source of truth

Generation Agent
  → implement

Validation Agent
  → verify: no state node accesses isEditMode or equivalent
```

---

## Pattern #2 — Behavioral coherence violation (contradicting handlers)

### Definition

A node that registers event handlers for opposite sides of the same state transition — thereby containing hidden internal state that should be represented by explicit state nodes.

### Detection signals

The node registers a pair of mutually exclusive handlers:

- `mouseenter` + `mouseleave` — cursor presence/absence
- `mouseover` + `mouseout` — same
- `pointerdown` + `pointerup` — press/release (if they manage different visual states)
- similar pairs with mutually exclusive preconditions

### Not a violation

- One node registers `pointerdown` + `pointerup` as the start and end of a single continuous action (drag): both handlers are active in the same node state.
- Handlers do not change visual representation or manage behavior — they only pass data upward.

### Architectural problem

- The node contains a hidden hover state (or press state): different visual representation depending on cursor position
- This violates the behavioral coherence principle: capability A (normal view) implies NOT-hover, capability B (hover view) implies hover — they are mutually exclusive

### Canonical refactoring

```
Before (violation):
  SomeNode
    content materialization →
      el.addEventListener('mouseenter', () => { this.el.classList.add('hover') })
      el.addEventListener('mouseleave', () => { this.el.classList.remove('hover') })

After (canonical):
  SomeNode  ← switchable holder
    ├─ SomeNormalStateNode
    │    (appearance without hover)
    └─ SomeHoverStateNode
         (appearance with hover)
         (activated via onBranchOpen on hover)
```

Real example: `TreeItemRowEditStateNode` has normal and hover sub-states.

### Agent chain for refactoring

```
Domain Structuring Agent
  → identify: which states are hidden inside the node (normal/hover, normal/pressed, etc.)
  → extract holder, describe responsibility of each state node

TOP Modeling Agent
  → model holder + state nodes

Canon Precheck Agent
  → verify that state nodes do not register mutually exclusive handlers

Generation Agent
  → implement

Validation Agent
  → verify absence of mouseenter/mouseleave pairs in the same node (except exceptions)
```
