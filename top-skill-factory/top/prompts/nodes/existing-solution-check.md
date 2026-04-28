# ExistingSolutionCheck

Responsibility: determine whether an existing skill, tool, library, or approach already satisfies the requested goal before new design begins.

Input:
- normalized_input
- discovery_result

Output:
- existing_solution_check_result

Check result must include:
- mode_used (skip | quick | deep)
- decision (build | reuse | adapt | compose | reject | skipped)
- build_justification (required when decision is `build`)
- candidates (list of evaluated options, may be empty)
- composability_assessment (required when any candidate is partial)
- search_scope_used (internal_only | internal_and_external | user_declined_external | skipped)
- time_box_status (within | exceeded | not_applicable)

Primary objectives:
- prevent building what already exists
- prevent partial overlap going undetected
- surface composability opportunities before tree design begins
- force explicit justification when building from scratch

## Modes

**Skip**: user explicitly waived the check with awareness of the risk. Records decision as `skipped`. No search is performed.

**Quick Check (default)**: scan known internal inventory and immediately obvious external candidates. Time-boxed to 5–10 minutes of effort. Sufficient for most requests.

**Deep Check**: systematic scan of internal inventory and broader external landscape. Includes adjacent skills, libraries, and partial solutions. Time-boxed to 20–30 minutes. Use when the request overlaps with known active areas or when Quick Check surfaces ambiguous candidates.

## Search protocol

Internal search runs first and always:
- known skill inventory
- recently built or planned skills
- shared nodes or controllers that could be reused

If internal search does not resolve the decision, the user is asked whether to proceed with external search:
> "Internal search did not find a sufficient match. Shall I search externally (web, libraries, registries)?"

- User confirms → external search runs:
  - open-source libraries or tools
  - known AI skill marketplaces or registries
  - comparable implementations in adjacent domains
- User declines → decision is made based on internal results only; `search_scope_used` is recorded as `user_declined_external`

External search results are evidence, not authority. Internal artifacts take priority when capability is equivalent.

## Candidate evaluation matrix

For each candidate, produce one row:

| Candidate | Coverage | Gaps | TOP Compatible | Effort to Adapt | Composable | Recommended Action |
|-----------|----------|------|----------------|-----------------|------------|--------------------|

Coverage: percentage or qualitative estimate of how much of the goal the candidate addresses.
Gaps: what the candidate does not cover.
TOP Compatible: Yes / Partial / No / Unknown.
Effort to Adapt: Low / Medium / High / Prohibitive.
Composable: whether this candidate can serve as a building block for a larger solution.
Recommended Action: Reuse / Adapt / Compose / Skip.

## Decision outcomes

- **Reuse**: an existing solution satisfies the goal without modification. Build is blocked — present the existing solution instead.
- **Adapt**: an existing solution satisfies the goal with bounded modification. Tree design proceeds from the existing solution, not from scratch.
- **Compose**: multiple existing solutions can be combined to satisfy the goal. Tree design proceeds from the composition, not from scratch.
- **Build**: no sufficient existing solution found. Design proceeds from scratch. Build justification is mandatory.
- **Reject**: the goal should not be pursued regardless of available solutions (out of scope, redundant request, harmful pattern). Pipeline is blocked.
- **Skipped**: user explicitly skipped the check. Design proceeds. Risk acknowledged.

## Build justification (required when decision is `build`)

Must include:
- what was searched (internal inventory items reviewed, external candidates considered)
- why each candidate was insufficient (specific coverage gap or incompatibility)
- why composition is not viable
- explicit confirmation that building from scratch is the minimum viable path

Optimistic "nothing found" without documented search is not a valid build justification.

## Time-box rule

Quick Check: stop at 10 minutes. Record `time_box_status: exceeded` if the search consumed more time. Do not silently extend.
Deep Check: stop at 30 minutes. Escalate if the landscape is still unclear.

Process:
- determine mode from user instruction or default to Quick Check
- execute internal search
- if internal search does not resolve the decision: ask user whether to proceed with external search
- if user confirms: execute external search; if user declines: proceed with internal results only
- evaluate each candidate against the matrix
- determine decision
- record build justification if decision is `build`
- assess composability when any candidate is partial
- record time_box_status

Boundaries:
- do not begin tree design in this node
- do not perform SkillDiscovery work here
- do not treat familiarity with a domain as a substitute for an actual search
- do not record `build` without documented justification

Invalid output conditions:
- decision is `build` without a populated build_justification
- mode is not one of the three defined values
- candidates list is absent when decision is `reuse`, `adapt`, or `compose`
- composability_assessment is absent when any candidate is partial
- search was skipped without the Skip mode being active

Rules:
- internal search always runs first
- build justification must name specific candidates reviewed and specific gaps found
- time-box overruns must be recorded, not silently absorbed
- Reuse and Reject decisions block further design; all other decisions route to SkillDesignController
