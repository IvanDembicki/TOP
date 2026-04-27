# Quality control rules

Checks:
- ArtifactConsistencyValidator compares spec, prompts, validation files, schemas, and examples.
- TypeStrictnessValidator rejects weak contracts.
- ComplexityBudgetController checks node count, depth, signal count, and validation rule count.
- RuleVerifiabilityCheck ensures every validation rule can be checked.
- DryRunController runs at least one synthetic example when applicable.
- CoreInvariantGuard blocks violations of core TOP invariants.

Default thresholds:
- max_node_count_without_user_approval = 60
- max_tree_depth_without_user_approval = 6
- max_signal_types_without_user_approval = 12
- max_required_validation_files_without_rationale = 16
- max_payload_top_level_keys = 12
- max_payload_nesting_depth = 4

Verification requirements:
- every validation rule must name evidence source
- every validation rule must name check method
- every budget must define blocking vs warning threshold
- every dry run must declare scenario input, expected outcome, observed outcome, and diagnosis status

Blocking violations:
- Rule cannot be checked.
- Core invariant disabled.
- Artifacts contradict each other.
- Dry run fails without diagnosis.
- Dry run is presented as proof of runtime behavior.
- Hard budget exceeded without explicit approval.