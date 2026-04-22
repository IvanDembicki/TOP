# Target Adaptation Output Contract

## Required structure

All sections are required. The absence of any section makes the output invalid.

goal:
context:
artifact:
adaptation_plan:
adaptation_decisions:
target_constraints:
validation_signals:
generation_handoff:
next_step:

## Required fields

goal:
- adapt semantic UI layer to target platform

context:
- semantic_layer_source
- target_platform
- target_constraints
- structural_scope

artifact:
- adaptation_artifact_path
- adaptation_artifact_format
- adaptation_artifact_persisted

adaptation_plan:
- target_interaction_mapping
- target_layout_mapping
- target_ui_primitives
- target_accessibility_mapping
- target_feedback_mapping

adaptation_decisions:
- preserved_elements
- adapted_elements
- dropped_elements
- decision_reasons

target_constraints:
- native_platform_constraints
- unsupported_semantics
- required_target_workarounds

validation_signals:
- semantic_intent_preserved
- source_platform_leakage_present
- target_coherence_risk
- business_logic_added
- top_invariants_preserved

generation_handoff:
- target_specific_generation_notes
- forbidden_source_artifacts
- required_validation_checks

next_step:
- recommended_agent
- allowed_next_stage

## Rules

- `adaptation_artifact_path` must point under `top/adaptations/<target>/` when `adaptation_artifact_persisted` is true.
- `business_logic_added` must be `false` for a valid adaptation.
- `source_platform_leakage_present` must be `false` for a valid adaptation.
- Every adapted or dropped element must have a reason.
- Target-specific primitives are allowed only in this Layer C output and generated target artifacts, never in Layer B.
- `allowed_next_stage` must be `Generation Agent` for a valid generation-pipeline adaptation.
- Free text outside the required structure is prohibited.

## Semantic validity rule

- Empty values, placeholder values, and formal stubs are invalid.
- A result is invalid if it copies source-platform primitives instead of making target-native decisions.