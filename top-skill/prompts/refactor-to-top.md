# refactor-to-top

agent: Repair Agent

input_contract:
- existing_code
- violations

output_contract:
- repaired_artifact

rules:
- targeted fixes only
- for migration scopes, identify legacy tests, snapshots, fixtures, QA scripts, executable examples, and documented test cases that cover the scope
- require a Behavior Preservation Plan before modeling or generating replacements for a tested migration scope
- do not discard a legacy test until its behavioral meaning is extracted, normalized, mapped to TOP nodes/contracts/prompts, and re-covered or explicitly declared obsolete
- when replacing legacy composition, converge toward pull-based TOP construction
- classify runtime parameters, parameter bags, config/options/props-like objects, composition entrypoints, and callback/handler bundles as wrapped legacy unless removed from the TOP-conformant final path
- replace pushed Content/View inputs with narrow owner access methods
- detect framework/renderable artifacts that currently combine controller and content roles
- split them into non-renderable controller plus content/view or a thin adapter where the target runtime requires one
- classify unsplit renderable Node/Controller artifacts as `CORE-026`
- classify loss or weakening of test-covered behavior as `CORE-028`
- classify migration past tested legacy scope without a Behavior Preservation Plan as `WF-010`
- preserve valid internal platform/base constructor mechanics, but do not expose them as public TOP constructor inputs
