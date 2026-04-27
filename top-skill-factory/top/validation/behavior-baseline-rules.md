# Behavior baseline rules

A behavior baseline is required when a mode claims preserved external behavior.

Checks:
- baseline_id exists
- scenario_inputs are explicit
- expected_outputs are explicit
- acceptance_assertions are explicit
- baseline is referenced by compare, replay, refactor, split, merge, or conversion reports when behavior preservation is claimed

Blocking violations:
- behavior preservation claimed without baseline or equivalent replay evidence
- acceptance assertions missing