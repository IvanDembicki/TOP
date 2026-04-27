# DryRunController

Responsibility: run synthetic scenarios against the generated skill definition.

Input:
- behavior_baseline
- generated_skill
- mode_result_examples

Output:
- dry_run_result

Primary objectives:
- test whether the artifact set behaves coherently under representative scenarios
- detect false-ready claims before delivery

What dry run means here:
- it does not execute a deployed runtime
- it replays representative synthetic scenarios against the generated artifacts, declared contracts, routing rules, and expected mode results
- it checks whether the produced skill definition would make the expected routing, clarification, validation, and output decisions

Process:
- choose at least one representative success-path scenario when the skill produces artifacts
- choose at least one failure or ambiguity scenario when the mode claims validation or clarification behavior
- compare expected decisions against observed decisions from the artifact set
- record contradictions, missing artifacts, or unbounded assumptions

Invalid output conditions:
- dry run has no explicit scenario inputs
- dry run has no expected outcomes
- dry run presents vague impressions instead of observed decision results
- dry run is used as proof of runtime correctness rather than bounded artifact-level evidence

Rules:
- dry run must produce diagnosis when it fails
- a dry run report without scenario inputs, expected outcomes, and observed outcomes is invalid
- dry run may support readiness, but it cannot be presented as proof of runtime correctness