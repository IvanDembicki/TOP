# Failure handling

Process:
1. FailureClassifier classifies the failure.
2. ValidationFailureHandler routes the failure to the responsible designer/controller.
3. IterationBudgetController checks remaining attempts.
4. Affected artifacts are rebuilt.
5. Validation is re-run.

Default budgets:
- max_validation_repair_cycles = 3
- max_user_clarification_cycles = 2
- max_mode_retries = 2
- max_composite_flow_length_without_explicit_user_approval = 5

Hard fail:
- iteration budget exceeded
- failure cannot be classified
- core invariant violation cannot be resolved
- required user decision is missing
- ready output still contains blocking QC violations
- blocking blind spots remain unresolved

Hard fail output:
- diagnosis
- violations
- required user decisions
- partial artifacts if available