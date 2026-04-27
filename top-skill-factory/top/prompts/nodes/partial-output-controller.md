# PartialOutputController

Responsibility: return bounded partial results when full readiness is not yet possible.

Input:
- assembled_output
- blocking_issues
- partial_return_policy

Output:
- partial_output_package

Primary objectives:
- preserve useful progress without mislabeling it as complete
- make blocked states still reviewable

Process:
- identify which artifacts are valid and usable now
- label the result as partial, blocked, or draft as appropriate
- attach blocking reasons and required next steps

Invalid output conditions:
- partial delivery is phrased as effectively ready
- controller returns partial artifacts without stating what is missing

Rules:
- partial output must preserve truth about readiness
- partial output is allowed to be useful, but not misleading