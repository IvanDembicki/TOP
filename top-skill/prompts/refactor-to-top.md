# refactor-to-top

agent: Repair Agent

input_contract:
- existing_code
- violations

output_contract:
- repaired_artifact

rules:
- targeted fixes only
- when replacing legacy composition, converge toward pull-based TOP construction
- classify runtime parameters, parameter bags, config/options/props-like objects, composition entrypoints, and callback/handler bundles as wrapped legacy unless removed from the TOP-conformant final path
- replace pushed Content/View inputs with narrow owner access methods
- detect framework/renderable artifacts that currently combine controller and content roles
- split them into non-renderable controller plus content/view or a thin adapter where the target runtime requires one
- classify unsplit renderable Node/Controller artifacts as `CORE-026`
- preserve valid internal platform/base constructor mechanics, but do not expose them as public TOP constructor inputs
