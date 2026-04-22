# Semantic Interpretation Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
artifact:
semantic_layer:
constraint_classification:
platform_artifact_removal:
ambiguities:
validation_signals:
next_step:

## Required fields

goal:
- extract platform-neutral semantic UI layer

context:
- source_specs
- source_prompts
- source_platform_evidence
- structural_scope

artifact:
- semantic_artifact_path
- semantic_artifact_format
- semantic_artifact_persisted

semantic_layer:
- semantic_elements
- semantic_roles
- user_intents
- system_intents
- interaction_intents
- state_models
- feedback_intents
- layout_intents
- accessibility_semantics

constraint_classification:
- essential_constraints
- adaptive_constraints
- optional_constraints
- source_artifact_constraints

platform_artifact_removal:
- removed_or_quarantined_artifacts
- artifact_source_locations
- semantic_replacements

ambiguities:
- unresolved_semantic_ambiguities
- required_clarifications

validation_signals:
- source_platform_leakage_present
- semantic_intent_preserved
- target_adaptation_ready
- structural_change_required

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- Layer B must not contain target primitives, platform APIs, framework classes, CSS properties/selectors, native widget names, or source-specific event APIs.
- `semantic_artifact_path` must point under `top/semantic/` when `semantic_artifact_persisted` is true.
- Source artifacts may be listed only as removed/quarantined evidence, not as semantic truth.
- Semantic vocabulary is open, but every term must represent platform-independent meaning.
- `target_adaptation_ready` must be `false` if semantic intent is ambiguous.
- Free text outside the required structure is prohibited.

## Semantic validity rule

- Empty values, placeholder values, and formal stubs are invalid.
- A result is invalid if it merely renames platform primitives without extracting intent.