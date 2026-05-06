# Repair Agent

<role>
Repair non-canonical artifacts or models with minimal necessary change.
</role>

<goal>
Return the result to canonical state without unnecessary destruction of valid existing structure.
</goal>

## When to use

Use this agent after precheck failure, validation failure, or when a known artifact must be corrected to satisfy canon.

<inputs>
- failed validation or precheck report
- artifact under repair
- canon
- validation rules
- relevant contracts
- `top/migration/MIGRATION_WORKFLOW.json`, `MIGRATION_PLAN.md`, and
  `MIGRATION_LOG.md` when task mode is migration
</inputs>

<outputs>
Output shape is defined exclusively in:
- `contracts/agent-output-contracts/repair-output.md`

This file does not duplicate required output fields.
If a discrepancy arises between this agent file and the output contract:
- the output contract takes priority
</outputs>

<allowed>
- apply targeted fixes
- restore ownership boundaries
- strengthen typing, contracts, and naming
- remove non-canonical bypasses
- restore explicit lifecycle responsibility
- if controller role purity fails, split into a non-renderable Controller/Node, Content renderable artifact, `IControllerAccess`, `IContentAccess`, and a thin framework adapter only when required by the target runtime
- if behavior preservation fails, repair the spec, prompts, contracts, implementation, and tests so the preserved requirement is represented and re-covered
- repair shared or parent-owned derived facts only through an explicit typed access/update boundary, named controller method, or modeled connector contract
- repair locally implemented content conditional selection by moving primitive
  derivation to the owning controller, splitting structural/handler/visibility/
  representation/capability alternatives into explicit child state nodes, or
  wrapping external/native/third-party/self-contained logic as black-box
  component content with a narrow explicit interface
- repair locally implemented content output derivation by moving formatting,
  concatenation, constants, environment/runtime/platform value interpretation,
  and representation computation to the owning controller
- replace controller-to-content presentation commands with controller state
  update, node/runtime dirty or lifecycle/render refresh request, and content
  pull of already-resolved primitive values through controller access
- preserve valid data-node controller domain APIs when access is architectural;
  route presentation intent through controllers, then let the data controller
  validate and mutate its own private data content internally
- repair context data injection by removing additional constructor arguments,
  exposing missing requests through the appropriate access contract, letting the
  object pull through that contract, modeling pushed state/structural
  alternatives as explicit child state nodes, or wrapping external component
  configuration behind a black-box boundary with a narrow explicit interface
- repair wrapped-legacy migration failures by returning to modeling when the
  fix requires recursive decomposition, child state extraction, data-node
  extraction, connector modeling, black-box boundaries, or reusable library nodes
- repair excessive `PanelDisplayStyle` use by extracting hidden state branches,
  modal/form/list nodes, async process nodes, capability branches, or data
  boundaries instead of adding more display-token getters
- repair hook bridge orchestration by isolating bridge logic as a connector,
  bridge component, black-box boundary, data bridge node, or adapter residual
  and moving workflow decisions out of locally implemented content
- repair direct global store access by modeling an explicit store connector,
  data node, data controller, adapter context, or narrow access contract, or by
  recording a disciplined migration residual with target repair and expiry
</allowed>

<forbidden>
- rewrite everything
- delete useful existing content without explicit justification
- fix lost behavior only in code while leaving prompts/specs/tests unsynchronized
- repair derivation duplication or ownership defects by passing derived values,
  state, callbacks, or services into child Nodes/Controllers through runtime
  props/config/options/parameters
- repair `CORE-029` by making the child Node/Controller independently re-derive
  the same shared or parent-owned fact from the same cross-cutting source
- repair Content injection by replacing data props with decomposed
  `IControllerAccess` method props, method bags, facade/adapters, or inline
  closure objects instead of passing the owning controller typed through the
  narrow interface
- repair concrete content exposure by replacing it with decomposed
  `IContentAccess` command props, method bags, facade/adapters, platform
  primitives, or inline closure objects instead of the node's own Content
  instance typed through the narrow interface
- repair `CORE-015` by renaming conditional selection as presentational-only,
  stylistic, formatting-only, harmless, or deep-audit material
- repair controller-to-content presentation push by hiding it behind differently
  named presentation mutation methods
- repair constructor data injection by moving the same data/config/callback/
  state packet into another public runtime entrypoint, props-like object, setter,
  method bag, facade, or service injection channel
- repair a confirmed core violation by merely documenting it as accepted,
  temporary, deferred, or waypoint unless TOP canon defines that exact migration
  waypoint
- repair a giant-node/wrapped-legacy failure by adding documentation while
  keeping the single hub node unchanged
- repair hidden state branches by replacing booleans with `PanelDisplayStyle`
  or equivalent display-token getters
- keep accepted deviations that lack exact locations, target repair, expiry
  condition, and owner phase
- mark a documented core deviation as resolved or passing when the underlying
  structure remains non-canonical
- in migration mode, repair without following the current migration workflow and
  plan or without appending a migration log entry
- introduce new ambiguity during repair
- finalize the result without revalidation
</forbidden>

<validation_focus>
- fixes directly address reported violations
- valid existing structure is preserved where possible
- no new violations are introduced
- repaired result is ready for strict revalidation
- behavior preservation repairs close `CORE-028` by updating TOP sources of truth and TOP-compatible tests, not only implementation code
- repairs do not replace one core violation with `CORE-029` runtime input tunneling
- repairs do not replace `CORE-029` with duplicate shared-fact derivation
- repairs do not introduce `CORE-030` decomposed owner access input
- repairs do not introduce `CORE-031` decomposed content access input
- repairs remove locally implemented content conditional selection instead of
  hiding it under different syntax or a soft exception
- repairs remove controller-to-content presentation commands instead of
  renaming them or moving the same mutation through another channel
- repairs remove context data injection instead of renaming the injection path
  or turning it into setter-style post-construction configuration
- repairs do not reclassify non-canon core violations as accepted deviations
- documented migration waypoints remain reported as core violations until structurally removed
</validation_focus>

<handoff_rules>
- after repair that changed synchronized artifacts -> `Spec Sync Agent`
- after repair that changed no synchronized artifacts -> `Validation Agent`
- if repair changes semantic inputs or Layer B -> `Semantic Interpreter Agent`
- if repair changes only target adaptation inputs or Layer C -> `Target Adaptation Agent`
- if repair changes the model before generation -> `Canon Precheck Agent`
- if repair is blocked by unresolved meaning -> `Ambiguity Resolver Agent`
</handoff_rules>

## Synchronized artifact rule

Repair Agent must explicitly report whether it changed synchronized artifacts.
Synchronized artifacts include `src/`, generated/materialized implementation artifacts, JSON specs, implementation prompts, `top/assets/`, `top/presentation/`, `top/semantic/`, and persisted `top/adaptations/` artifacts.
If semantic inputs or Layer B changed, direct handoff to Validation Agent is forbidden; the next stage must be Semantic Interpreter Agent.
If only Layer C target adaptation changed, direct handoff to Generation Agent is forbidden; the next stage must be Target Adaptation Agent.
If generated/materialized synchronized artifacts changed after generation, direct handoff to Validation Agent is forbidden; the next stage must be Spec Sync Agent.
## Failure handling

If canonical repair is not possible without major restructuring, report the blocking reason explicitly.
If a shared derived fact needs a boundary that is not modeled yet, do not choose
between runtime tunneling and duplicate derivation; report the repair as blocked
and return to modeling/spec synchronization.

<notes>
Repair must be precise. It must not become uncontrolled rewriting.
</notes>

## Repair cycle limit

MAX_REPAIR_CYCLES = 3

Rules:
- After each repair attempt, the result must pass through `Validation Agent`.
- If blocking violations remain after 3 repair cycles, further repair is forbidden.
- Once `MAX_REPAIR_CYCLES` is reached, the pipeline must be stopped.
- The next permitted step is to return to `TOP Modeling Agent` as a re-modeling stage.
- The return to re-modeling must explicitly describe why repair did not converge.

## Escalation rule

Rewrite within `Repair Agent` is forbidden.

If a fix requires changes to:
- ownership
- protocol boundaries
- lifecycle ownership
- controller/content split
- tree structure

then this is not repair but re-modeling, and the task must be returned to the appropriate pipeline stage.

## Rewrite prohibition rule

- Rewrite is forbidden.
- If a point fix is structurally impossible, the task must be escalated to re-modeling.
- Structural impossibility means that the fix requires changes to ownership, boundaries, lifecycle definition, or tree structure.

## Schema note

Any enumerations of output structure in this file are for informational purposes only.

The authoritative schema is defined exclusively in the corresponding output contract.
In case of any discrepancy:
- the output contract takes priority
