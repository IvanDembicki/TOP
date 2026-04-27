# Example: Dry run report

## Scenario

- mode: `CreateNewSkillMode`
- request: create a small two-mode skill with one validation rule

## Expected outcome

- `ModeRouter` selects `CreateNewSkillMode`
- `InputController` returns complete normalized input
- `SkillDesignController` produces a bounded tree
- validation remains in pass state if all required artifacts are present

## Observed outcome

- routing matched expectation
- contracts were present
- one required example artifact was missing
- final state remained `blocked`

## Diagnosis

Dry run succeeded in detecting an output completeness failure and prevented a false `ready` state.