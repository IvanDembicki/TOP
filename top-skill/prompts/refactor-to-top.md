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
- for migration/modeling artifacts, use canonical layout: branch specs under
  `top/specs/`, prompts under `top/prompts/`, status under `top/migration/`,
  and implementation artifacts under the declared source root (`top_src/<branch-id>/`
  by default)
- if implementation prompts or Expected Materialization are created before code
  generation, create the source root with `.gitkeep` or an equivalent placeholder
- classify runtime parameters, parameter bags, config/options/props-like objects, composition entrypoints, and callback/handler bundles as wrapped legacy unless removed from the TOP-conformant final path
- replace pushed Content inputs with narrow owner access methods
- Content must receive only the owning controller instance typed as
  `IControllerAccess`/target-equivalent; do not decompose access methods into
  separate props or inline method bags (`CORE-030`)
- detect framework/renderable artifacts that currently combine controller and content roles
- split them into non-renderable controller plus Content or a thin adapter where the target runtime requires one
- classify unsplit renderable Node/Controller artifacts as `CORE-026`
- classify loss or weakening of test-covered behavior as `CORE-028`
- classify parent-derived values, state, callbacks, or services pushed into child
  Nodes/Controllers through runtime props/config/options/parameters as `CORE-029`
- do not repair `CORE-029` by making the child independently re-derive the same
  shared fact from the same source; this only restores Invariant 14
- do not repair Invariant 14 by passing the derived fact through child
  Node/Controller runtime input; this only creates `CORE-029`
- use an explicit typed access/update boundary, named controller method, or
  modeled connector contract for shared derived facts; if none exists, report the
  repair as blocked
- do not "repair" a confirmed core violation by documenting it as accepted,
  temporary, deferred, or waypoint unless TOP canon defines that exact waypoint;
  otherwise report `WF-012`
- classify migration past tested legacy scope without a Behavior Preservation Plan as `WF-010`
- do not mark documented `CORE-026` or other accepted core deviations as validation pass; classify that verdict error as `WF-011`
- preserve valid internal platform/base constructor mechanics, but do not expose them as public TOP constructor inputs
