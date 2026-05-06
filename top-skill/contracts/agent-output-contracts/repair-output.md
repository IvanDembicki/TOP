# Repair Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
result:
details:
validation_signals:
next_step:

## Required fields

goal:
- fix violations

context:
- input_artifact
- relevant_validation_report

result:
- repaired_artifact
- violations_addressed
- behavior_violations_addressed
- migration_log_entry

details:
- applied_fixes
- behavior_preservation_fixes
- preserved_structure
- remaining_issues
- re_modeling_required
- accepted_deviation_updates

validation_signals:
- new_violations_introduced
- revalidation_required
- synchronized_artifacts_changed
- changed_synchronized_artifacts

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- Only targeted fixes are permitted
- Unnecessary rewrites are prohibited
- For non-migration repairs, `behavior_violations_addressed` and `behavior_preservation_fixes` must be explicitly `not_applicable`
- For non-migration repairs, `migration_log_entry` must be explicitly `not_applicable`
- For migration repairs that change artifacts or hand off to another stage,
  `migration_log_entry` must identify the appended `top/migration/MIGRATION_LOG.md`
  entry and any `top/migration/MIGRATION_WORKFLOW.json` phase/status update
  entry
- Repair output must report if a fix leaves a documented core deviation in place; such a deviation is not resolved
- Repair output must report `CORE-029` if the repair introduced semantic runtime input into a Node/Controller
- Repair output must report an invalid repair if it replaces `CORE-029` with duplicate derivation of the same shared fact, or replaces Invariant 14 with Node/Controller runtime input tunneling
- Repair output must report `CORE-030` if the repair replaces Content data
  injection with decomposed `IControllerAccess` method props, method bags,
  facade/adapters, or inline closure objects instead of the owning controller
  typed through the narrow interface
- Repair output must report `CORE-031` if the repair replaces concrete content
  exposure with decomposed `IContentAccess` lifecycle/materialization members, method bags,
  facade/adapters, platform primitives, or inline closure objects instead of the
  node's own Content instance typed through the narrow interface
- Repair output must report `CORE-032` if the repair leaves or introduces
  constructor data injection or setter-style post-construction data/config/
  state/presentation pushing into TOP objects instead of context attachment and
  pull-through contracts
- Repair output must report `WF-017` when a reported wrapped-legacy or
  giant-node failure cannot be fixed without returning to recursive modeling.
- Repair output must report `WF-018` when accepted deviations remain without
  target repair direction and expiry condition.
- If a shared derived fact cannot be repaired without a new typed access/update boundary, named controller method, or modeled connector contract, repair output must mark the repair blocked instead of proposing a local workaround
- Repair output must not treat documentation of a core violation as repair. A
  core violation may be listed in `accepted_deviations` only when TOP canon
  defines a specific migration waypoint for that violation; otherwise labeling it
  accepted/temporary/deferred/waypoint is `WF-012`
- Free text outside the required structure is prohibited

## Semantic validity rule

- All required fields must contain semantically valid content.
- Empty values, placeholder values, formal stubs, and contentless responses are considered invalid.
- Formally filling the structure without real content is not permitted.

## Next-stage rule

`next_step.allowed_next_stage` must be selected by priority:
- `Ambiguity Resolver Agent` if repair is blocked by unresolved meaning;
- `Canon Precheck Agent` if the repair changed the model before generation;
- `Semantic Interpreter Agent` if the repair changed semantic inputs or Layer B;
- `Target Adaptation Agent` if the repair changed only target adaptation inputs or Layer C;
- `Spec Sync Agent` if generated/materialized synchronized artifacts changed after generation;
- `Validation Agent` only if no synchronized artifact, semantic artifact, adaptation artifact, or model artifact changed.

Synchronized artifacts are `src/`, generated/materialized implementation artifacts, JSON specs, implementation prompts, `top/assets/`, `top/presentation/`, `top/semantic/`, and persisted `top/adaptations/` artifacts.
