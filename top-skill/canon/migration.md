# TOP Migration

Rules for migrating existing code into TOP structure incrementally.

These rules apply specifically to migration phases. They complement — and do not
replace — the universal TOP canon (`canon/architectural-invariants.md`,
`canon/controller-content-rules.md`, `references/architecture-rules.md`).

---

## Mg-0. Migration discovers hidden architecture

Migration modeling is not wrapping existing code into TOP-shaped files.

The primary goal of migration modeling is to discover the hidden object/state
architecture inside the legacy implementation and re-express it as an explicit
TOP tree.

Migration means discovering and externalizing hidden structure. It does not mean
wrapping legacy code.

The migration agent must identify hidden candidates including:
- domain objects;
- UI/presentation objects;
- data objects and data ownership boundaries;
- state holders and state alternatives;
- runtime entities;
- async processes and workflow fragments;
- forms, modals, lists, list items, cards, rows, tiles, banners, selectors,
  status panels, and action panels;
- repeated structures and reusable patterns;
- external integration boundaries;
- black-box components;
- hook/target bridge boundaries.

For each discovered candidate, the agent must classify it as one of:
- TOP node;
- child state node;
- data node;
- runtime/lib node;
- connector;
- black-box component;
- reusable library node;
- local implementation detail.

Migration is successful only when the legacy structure is re-modeled as an
explicit TOP tree, not when the old component is wrapped behind one large
controller/content pair.

## Mg-0a. Scope is not node boundary

A user-named migration scope is an analysis root, not a final node boundary.

When the user says "migrate Account section", "migrate Settings section",
"migrate screen X", "migrate route Y", or "migrate component Z", the named
thing defines the migration scope root. It does not define the final TOP node
count.

Single route, single screen, single file, or single framework component does
not imply single TOP node. Legacy file boundaries are evidence, not TOP node
boundaries. Screen boundaries are host/context boundaries, not necessarily node
boundaries.

The agent must create a candidate root branch for the scope and then recursively
decompose the internal structure.

## Mg-0b. Recursive decomposition is mandatory

Migration modeling must be recursive.

The agent must inspect the legacy implementation and split hidden
responsibilities into child nodes, child state nodes, data nodes, connectors,
black-box boundaries, and reusable library nodes until each remaining node has:
- one clear responsibility;
- a small and role-focused controller access surface;
- no hidden state alternatives;
- no independent async workflow hidden inside locally implemented content;
- no internal forms, modals, list items, cards, or rows that deserve separate
  ownership;
- no data ownership boundary hidden inside a presentation node;
- no large bridge cluster inside locally implemented content;
- no repeated helper component pattern that should become a reusable node.

The recursion stops only when each node can be understood and regenerated in
isolation.

Before approving a single-node migration, the agent must prove all of the
following:
1. no independent state holders exist inside the scope;
2. no lifecycle-bearing sub-objects exist;
3. no repeated runtime entities exist;
4. no independent async processes exist;
5. no forms or modals with their own behavior exist;
6. no lists or list items should be runtime/lib nodes;
7. no data ownership boundaries are hidden inside the visual scope;
8. no reusable repeated structures exist;
9. the controller access surface remains small and role-focused.

If this proof cannot be made, a single-node model must not pass precheck.

## Mg-0c. Giant node detection

A large node is a migration smell. It is not automatically a core violation, but
it is a mandatory decomposition review trigger.

Trigger decomposition review when a modeled or generated node has any of:
- a very large `IControllerAccess`/target-equivalent surface;
- many `PanelDisplayStyle` or equivalent display-value access methods;
- many state fields;
- many pending actions or pending mutations;
- many bridge hooks or target-framework bridge points;
- many unrelated public action methods;
- many modal, form, list, card, or row responsibilities;
- many sections with independent behavior;
- too many unrelated display value getters;
- a role that cannot be explained in one short sentence.

A giant node must not be accepted merely because it came from one screen, route,
file, tab, or framework component.

If the agent keeps the candidate as one node, the output must provide an
explicit decomposition justification explaining why internal candidates are not
nodes, state nodes, data nodes, connectors, black-box components, or library
nodes. Without that proof, validation reports `WF-017`.

## Mg-0d. PanelDisplayStyle is not decomposition

`PanelDisplayStyle` or equivalent display-token access is not a substitute for
node decomposition.

It is allowed only for stable structural sections whose existence is constant
and whose visibility/display is an already-resolved presentation value.

It must not hide:
- state alternatives;
- lifecycle-bearing branches;
- different capabilities;
- independent workflows;
- async process states;
- forms with independent validation or save lifecycle;
- modal states;
- permission-gated capability branches;
- data ownership boundaries.

If a section has its own responsibility, lifecycle, actions, async flow, or
state transition semantics, it must be modeled as a node or state branch
candidate, not merely hidden with `PanelDisplayStyle`.

Validation must flag excessive `PanelDisplayStyle` use as a possible hidden
state tree and require decomposition evidence.

## Mg-0e. Reusable structure and library extraction

Migration modeling has two axes:

1. Vertical decomposition: scope -> child responsibilities -> states ->
   substates.
2. Horizontal extraction: repeated structures -> reusable library nodes or
   black-box components.

Repeated legacy structures are candidates for reusable TOP library nodes.

A modal, card, row, tile, list item, selector, banner, form, status panel,
action panel, or workflow fragment is not automatically a helper component. It
is a candidate node, state node, runtime/lib node, reusable library node,
black-box component, or local implementation detail until classified.

A candidate should become a library node when:
- the same structural pattern appears more than once;
- it has a stable semantic role;
- it can be parameterized through a narrow contract;
- it has its own content, lifecycle, or events;
- duplicating it would create repeated prompt/code logic.

Do not extract a library node when:
- similarity is only visual but behavior is different;
- the abstraction would require a wide props/config object;
- extraction would create a generic god-component;
- the repeated part has no stable responsibility.

If helper components remain, the migration output must explain why each retained
helper is not a TOP node, black-box component, or library node.

## Mg-0f. Hook bridge residuals are not content orchestration

React hooks or other target-framework hooks inside locally implemented content
may be accepted only as forced bridge residuals.

A hook bridge inside locally implemented content must not turn content into an
orchestration layer.

If hooks are required by the target framework, classify them as one of:
- bridge component;
- connector;
- black-box boundary;
- data bridge node;
- adapter residual.

The content must not own workflow logic, mutation construction, routing
decisions, alert/business decisions, store writes, pending action execution, or
business orchestration.

If a content file contains multiple hooks plus effect workflows, pending action
execution, mutation body construction, router calls, alert calls, or store
writes, validation must flag a possible orchestration-in-content violation and
require isolation as a bridge/connector/black-box/data node.

## Mg-0g. Global store access is residual, not canonical access

Direct access to global stores from a controller must not be called
architecturally correct by default.

It may be accepted only as a migration residual when it is:
- documented;
- isolated;
- justified by legacy constraints;
- assigned a target repair direction;
- given an expiry condition.

Preferred repairs are explicit store connectors, data nodes, data controllers,
adapter context, or narrow access contracts.

Validation must distinguish temporary residual access from canonical TOP access.

## Mg-0h. Accepted deviation discipline

Accepted deviations are not a place to hide core violations.

Every accepted deviation must include:
- deviation name;
- exact files/locations affected;
- why it is accepted temporarily;
- why it is not blocking this phase;
- target repair direction;
- expiry condition;
- phase where it must be removed or re-evaluated;
- whether it is allowed in canonical target architecture or only in migration
  mode.

If any accepted deviation lacks target repair and expiry condition, validation
must not produce a clean final pass.

## Mg-0i. Runtime Branch Binding Pattern

Runtime-created branches may receive binding input only to attach them to an
entity context, not to fill them with scattered data.

This pattern is the only exception to the static-node constructor rule. Static
TOP nodes receive only their parent/context reference. Runtime-created branch
roots may receive parent/context plus one canonical binding input:

Preferred binding:
1. Entity Context Binding — the runtime branch root receives a narrow entity
   context reference: data-node controller, entity access interface, or model
   controller.

Allowed binding:
2. Identity Key Binding — the runtime branch root receives a stable identity key
   only when the branch is responsible for resolving or loading its entity
   context.

Allowed but weaker:
3. Typed DTO Binding — the runtime branch root receives a typed immutable DTO
   only when no entity context exists yet. The DTO must be converted into owned
   data content/model as early as possible.

Forbidden:
- scattered constructor data;
- props/config/callback bags;
- mutable raw model objects;
- presentation values;
- services/stores passed directly as arbitrary arguments.

A runtime branch must not be filled with scattered data. It must be bound to an
entity context, or to an input that deterministically creates one.

Allowed examples:
- `new StaticChildNode(parent)`
- `new RuntimeItemNode(parent, entityAccess)`
- `new RuntimeItemNode(parent, stableEntityId)`
- `new RuntimeItemNode(parent, typedImmutableDto)`

Forbidden examples:
- `new RuntimeItemNode(parent, id, name, status, callbacks, config)`
- `new ChildNode(parent, props)`
- `child.setData(...)`
- `child.applyConfig(...)`

Repair replaces scattered data arguments with an entity context reference when
available, uses a scalar identity only when the runtime branch owns
resolution/loading, uses a typed immutable DTO only as a fallback, converts DTOs
into owned data content/model early, and exposes required values through narrow
contracts.

## Intermediate migration states

A migrated branch may exist in a defined intermediate state. These states describe
migration depth, not architecture quality.

### partially-restructured

The controller/content boundary is clean and explicitly typed. The integration
layer beneath it remains wrapped legacy — the controller delegates to existing
services, queries, or subscriptions that have not yet been migrated to a TOP
integration layer.

Content has no dependency on integration-layer types. The TOP boundary holds;
the integration layer migration is deferred.

This is a valid hybrid state, not a structural violation. partially-restructured
is a migration waypoint, not a target state. See `references/hybrid-systems.md`
— the wrapped legacy integration layer is the non-TOP part; the controller/content
split is the TOP part.

### renderable-controller waypoint

During migration from renderable-artifact-centered code, a branch may temporarily
retain a source renderable artifact in the Node/Controller position only when it
is explicitly declared as a known migration deviation.

This is not TOP-conformant structure. It remains a `CORE-026` controller role
purity violation until the branch is split into:
- a non-renderable Controller/Node orchestration boundary;
- Content or an explicit thin adapter for renderable target materialization;
- explicit `IControllerAccess` and `IContentAccess` accounting.

This waypoint is useful for tracking staged repair work. It must not be reported
as validated TOP architecture, must not produce Validation `PASS` or Final Audit
`PASS`, and must not be used as a generation target. The deviation remains listed
under `core_violations` until the renderable/controller split is actually
performed.

### no ad hoc accepted deviations

Only migration waypoints explicitly defined by TOP canon may appear in
`accepted_deviations`. A project prompt, migration status file, validation report,
or repair report must not convert an arbitrary core violation into an accepted
deviation by documenting it as "known", "temporary", "accepted", "deferred", or
"planned".

Documentation may track an unresolved violation, but tracking is not repair and
does not make the violation an accepted deviation. In particular, `CORE-029`
semantic runtime input has no standalone accepted-deviation waypoint. It remains
blocking until structurally repaired or returned to modeling as a blocked
migration issue.

---

## Mg-1. Partially-restructured must be explicitly declared

A branch may be declared `partially-restructured` explicitly. This is a precise
description of current migration depth, not a defect.

Validation against this state checks only what the state claims:
- Does the controller/content boundary hold?
- Does content have no structural dependency on integration-layer types?

Validation does not require the integration layer itself to be migrated.
It does not waive universal canon violations such as controller role purity,
push-based construction, semantic runtime injection, or access-direction collapse.

---

## Mg-1a. Migration artifact layout must be canonical

A migration pass that creates persistent TOP artifacts must use the canonical
project layout:

- branch specs under `top/specs/`;
- implementation prompts under `top/prompts/`;
- migration status and tracking under `top/migration/`;
- materialized TOP implementation artifacts under a declared implementation
  source root, `top_src/<branch-id>/` by default.

Creating `top/<branch-id>.json` as a new branch spec is not canonical unless the
repository already has an explicit TOP root index or project-local convention
that records that layout. New migration branches default to
`top/specs/<branch-id>.json`.

If the pass writes implementation prompts, Expected Materialization, or a
generation next step, it must prepare the source root before stopping. If no
code is generated yet, the empty root is recorded with `.gitkeep` or an
equivalent placeholder.

The phase status must be honest:

- an analysis/modeling pass may report `analysis-only`, `modeled`, or
  `materialization-pending`;
- it must not report migration complete, validated, or ready when no
  materialized implementation and validation pass exist;
- generation may start only after specs, prompts, and source-root layout agree.

---

## Mg-1b. Migration workflow tree, plan, and action log are mandatory

Migration is a controlled workflow, not a single agent improvisation.

### Mandatory dedicated git branch

Every TOP migration must run on a dedicated git branch. The migration branch is
a safety boundary around the active migration workspace. Migration agents must
not create or modify migration artifacts, generated files, adapters, route
files, legacy integration files, or project source files on the user's current
working branch.

Before any migration write, Migration Infrastructure Agent must inspect git
status, detect the current branch, create or switch to a deterministic dedicated
migration branch, confirm that the checked-out branch is correct, and append the
git safety gate entry to `top/migration/MIGRATION_LOG.md`.

Recommended branch name:

```text
top-migration/<branch-id>
```

If the branch already exists, the agent must inspect it and continue only when
it belongs to the same migration. If branch ownership is ambiguous, unrelated
work is present, or unrelated uncommitted changes would be mixed with migration
output, the agent must stop and report the blocking condition.

Default git operation policy:
- create/switch dedicated branch: mandatory before migration writes;
- local commit: allowed only when explicitly requested by the user or when the
  workflow has reached a documented local-commit phase;
- remote push: forbidden unless the user explicitly requests push.

The active migration workspace is agent-owned only after the dedicated migration
branch is active and confirmed.

Every migration-mode task that creates or changes project-local TOP artifacts
must maintain:

```text
top/migration/<branch-id>/MIGRATION_WORKFLOW.json
top/migration/<branch-id>/MIGRATION_PLAN.md
top/migration/<branch-id>/reports/**
top/migration/MIGRATION_STATUS.md
top/migration/MIGRATION_LOG.md
```

`top/migration/<branch-id>/MIGRATION_WORKFLOW.json` is the machine-readable
process tree for the current branch migration. It records phases, responsible
agents, current phase, gates, handoff rules, and decision trace entries. It
must be updated before a new phase starts and after any phase changes status.

`top/migration/<branch-id>/MIGRATION_PLAN.md` is required before scope analysis,
modeling, generation, or repair proceeds. It records:

- the user-requested starting scope, if present;
- the selected migration scope and branch id;
- scope selection rationale when the user did not name a starting point;
- ordered phases and responsible agents;
- expected specs, prompts, source roots, adapters, tests, and validation gates;
- behavior preservation routing;
- rollback and stop points.

The branch workflow and branch plan must agree on selected scope, branch id,
phase order, responsible agents, and current phase. Markdown explains; JSON
controls routing and validation.

`top/migration/MIGRATION_LOG.md` is shared, multi-branch, and append-only. Each
agent operating in migration mode must append a log entry before handoff and
after any persistent artifact change. The entry records:
- git safety gate results for the first entry of the migration;
- phase;
- branch id;
- migration id;
- files read;
- files created;
- files modified;
- files deleted;
- commands run;
- key decisions;
- accepted deviations;
- unable-to-verify items;
- potential canon risks or needs-later-validation notes;
- self-check result;
- next agent or next action.

If a real timestamp is unavailable, do not fake it. Write
`timestamp_source: placeholder`. Identical fake timestamps must not be presented
as forensic timestamps.

The first migration log entry must include:

```text
**Git safety gate:**
- initial_branch:
- migration_branch:
- branch_created:
- branch_checked_out:
- working_tree_status:
- remote_status:
- unrelated_uncommitted_changes:
- migration_writes_allowed:
- local_commit_policy:
- push_policy:
```

The log is forensic evidence. Agents must not rewrite old entries to hide a bad
decision. Corrections are appended as new entries.

`top/migration/MIGRATION_STATUS.md` is shared branch status. It may be updated
only by preserving previous branch history and adding or updating the current
branch entry; it must not be rewritten as if only one active branch exists.

If these files are missing, stale, contradictory, or not updated for a migration
handoff, the migration is incomplete even if generated code exists.

### Mandatory short checkpoints

Migration work must move through short persistent checkpoints:

1. infrastructure prepared;
2. scope and recursive decomposition completed;
3. model/spec and prompts written;
4. canon precheck completed;
5. generation completed;
6. post-generation source validation completed;
7. repair completed when needed;
8. final audit completed.

Each checkpoint must update branch-scoped control artifacts and append the
shared `top/migration/MIGRATION_LOG.md` before handoff. A later agent must be
able to resume from repository artifacts alone. Chat memory, previous agent
claims, and generator self-check text are not migration state.

Validation and final audit must be independent and adversarial. The verifier
must re-read the current skill rules and target artifacts in its own pass. A
generation or repair self-check is evidence to inspect, not a substitute for
validation.

## Mg-1c. Active migration workspace ownership

The active migration workspace is agent-owned. The legacy application remains
user-owned.

During migration, agents may create, modify, replace, and delete files required
by the active branch migration workflow inside branch-owned artifacts:

```text
top/specs/<branch-id>.json
top/prompts/<branch-id>/**
top/migration/<branch-id>/MIGRATION_PLAN.md
top/migration/<branch-id>/MIGRATION_WORKFLOW.json
top/migration/<branch-id>/reports/**
top/migration/<branch-id>/**
top/assets/**
top/semantic/**
top_src/<branch-id>/**
```

Shared migration artifacts are not branch-owned:

```text
top/migration/MIGRATION_LOG.md
top/migration/MIGRATION_STATUS.md
```

`MIGRATION_LOG.md` is append-only and multi-branch. Shared status files may be
updated only without erasing previous branch history. A new branch must not
overwrite another branch's plan, workflow, reports, prompts, spec, or generated
source. If a legacy project still uses flat `top/migration/MIGRATION_PLAN.md` or
`top/migration/MIGRATION_WORKFLOW.json`, the agent must preserve prior branch
information and explicitly log the compatibility update.

They do not need user confirmation for each file write inside the active
migration workspace when the write follows the current migration plan/workflow
and is recorded in the migration log.

This authority does not include:
- unrelated legacy source files;
- unrelated `top_src/` branches;
- unrelated migration branches;
- another branch's `top/migration/<other-branch>/` artifacts;
- package manifests or lock files;
- native iOS/Android files;
- environment or secrets files;
- git push or remote operations.

Legacy app files may be modified only for explicitly required thin adapters or
integration wiring, and those changes must be logged.

Validation must verify that active branch writes stayed inside the branch-owned
workspace, shared artifacts preserved previous branch history, `MIGRATION_LOG.md`
was appended rather than rewritten, unrelated `top_src/<other-branch>` and
`top/migration/<other-branch>` files were not changed, and writes outside the
active migration workspace are either explicitly allowed adapter/integration
changes or scope violations.

Validation must also verify that migration writes happened only after the
dedicated branch was created or selected, the migration branch matches
`top-migration/<branch-id>` or a documented deterministic project equivalent,
the first migration log entry contains the git safety gate, no remote push was
performed without explicit user request, and any local commit was requested or
was part of a documented commit phase.

---

## Mg-2. External contract must be preserved

The public interface of the migrated branch must not change as a result of
migration.

Callers, parent connectors, and framework-boundary files must not require changes
to accommodate the migration. If they must change, that change is a separate
explicit decision — not a side effect of the migration.

---

## Mg-3. Residual responsibilities must be explicitly justified

When responsibilities remain in the root controller after child branch
decomposition, each residual responsibility must be explicitly justified.

Accepted justifications:
- the responsibility is genuinely cross-cutting: consumed by two or more child
  branches and cannot be cleanly owned by any single child;
- the responsibility is tied to a framework-level constraint that requires it in
  the root controller (routing context configuration, session-level lifecycle
  setup, etc.);
- the responsibility coordinates a flow that spans multiple child branches and
  requires a single orchestration point.

A responsibility that meets none of these criteria is a candidate for extraction
into a child branch.

Residual justifications must be recorded in the migration spec or implementation
prompt, not left implicit.

---

## Mg-3a. Legacy composition is wrapped legacy, not TOP end state

During migration, existing runtime parameters, parameter bags, config/options/props-like
objects, slots, render/build parameters, callback/handler bundles, service bags,
stores, prebuilt child components, and platform child views
may be retained only as explicitly declared wrapped legacy or adapter mechanics.

They are not TOP-conformant final structure.

The target migration direction is pull-based construction:
- a static Node constructor receives only its parent/context reference;
- a runtime-created branch root may receive parent/context plus one canonical
  Runtime Branch Binding input;
- a Content constructor receives exactly one semantic value: the owning controller
  instance typed only through `IControllerAccess`/target-equivalent;
- Content is not typed against the concrete controller;
- Node/Controller artifacts are non-renderable orchestration boundaries, not preserved source framework renderable artifacts;
- parent Nodes/Controllers construct direct children at their tree positions;
- Content asks its owner for data, actions, and permitted output handles;
- the owner asks direct child controllers for opaque public handles.

A migration plan that merely moves legacy constructor injection into public
runtime parameters, parameter bags, config/options/props-like objects,
composition entrypoints, or render/build callbacks has not reached
TOP architecture. It has only changed the platform syntax of the same push-based
composition.

Derived facts, owner state, and cross-cutting values must not be tunneled into
child Nodes/Controllers through target runtime input. A repair that removes
duplicate derivation by passing the derived value into a child Node/Controller
through props/config/options/parameters has only replaced the original violation
with `CORE-029`.

The opposite repair is also invalid. A repair that removes `CORE-029` by making
the child independently re-derive the same parent-owned or shared fact from the
same cross-cutting source has only restored the Invariant 14 violation. Migration
repair must introduce or use an explicit typed access/update boundary, named
controller method, or modeled connector contract. If no such boundary exists in
the current model, the migration remains blocked or in a declared waypoint; the
agent must not invent a props-based or duplicate-derivation workaround.

Declaring the resulting `CORE-029` as an accepted deviation is not a repair
unless TOP canon defines a specific waypoint for that violation. For shared
derived facts, no such waypoint exists. The correct next stage is structural
repair or re-modeling of the missing access/update boundary.

---

## Mg-4. Content boundary isolation check

Before declaring a migration slice implemented, verify:

1. Content has no direct structural dependency on integration-layer types (API
   response shapes, external service types, database record types).
2. All integration-derived data displayed by content has been transformed into
   typed view-model fields at the controller level.
3. Content obtains view-model values only through the content-to-controller owner
   access contract (`IControllerAccess` or target-equivalent), using explicit
   methods or accessors owned by the controller.
4. `IContentAccess` is not used as a view-model/data carrier or presentation
   command channel. It contains only controller-to-content
   lifecycle/materialization access, or it is explicitly declared as a
   zero-contract when that direction has no permitted lifecycle/materialization
   calls.

If any of these checks fail, the migration is incomplete regardless of whether the
content is visually correct at runtime.

---

## Mg-5. Legacy tests are requirements evidence

Legacy tests covering the migrated scope must be treated as executable evidence
of expected behavior, not merely as verification files.

Do not migrate tests as files. Migrate the behavioral requirements proven by
those tests.

Implementation-specific assertions may be discarded only after their behavioral
meaning is:
- extracted from the legacy test;
- normalized into a platform-neutral requirement;
- mapped to TOP nodes, contracts, state, events, or lifecycle responsibilities;
- reflected in the relevant spec and implementation prompts;
- re-covered by preserved, adapted, replaced, or newly generated TOP-compatible
  tests, or explicitly declared obsolete by an approved behavior-level decision.

Migration is incomplete until behavior preserved by legacy tests is represented
in TOP prompts and covered by TOP-compatible tests.

Validation must fail if:
- a migration scope has tests but no Behavior Preservation Plan was produced;
- a legacy behavior expectation has no mapped TOP requirement;
- a mapped requirement has no prompt representation;
- a prompt requirement has no TOP-compatible test coverage;
- a legacy test was discarded without justification;
- behavior gaps remain unresolved.
