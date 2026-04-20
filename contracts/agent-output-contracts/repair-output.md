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

details:
- applied_fixes
- preserved_structure
- remaining_issues

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