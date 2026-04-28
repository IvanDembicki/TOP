# ConvertLegacySkillMode

Purpose: convert an existing working legacy skill into TOP standard.

Input:
- legacy_skill_content
- normalized_input
- conversion_constraints
- behavior_baseline when available
- blind_spot_report

Output:
- extracted_legacy_model
- converted_top_skill
- conversion_gap_report
- conversion_audit_result
- behavior_preservation_report
- conversion_report

Primary objectives:
- preserve intended working behavior where safe
- remove legacy drift and hidden authority
- make conversion value explicit through a structured report

Process:
- ask the user via ResearchForInsight canonical question before conversion work begins (see `prompts/nodes/research-for-insight.md` — User-facing question):
  - User confirms → run ResearchForInsight; use the report as additional context throughout conversion
  - User declines → proceed directly to conversion
- extract purpose, behavior, and structure cues from legacy evidence
- identify blind spots, contradictions, unsafe assumption patterns, and sensitive imported material
- preserve legitimate behavior while rejecting unsafe fallback logic
- materialize the converted skill as explicit TOP artifacts
- validate the converted bundle and record the result in the conversion report

Boundaries:
- legacy skill is evidence, not authority`r`n- imported secrets or confidential source material must be redacted or isolated before reuse
- do not import monolithic prompt structure as valid architecture by default
- do not preserve behavior that violates TOP core invariants

Invalid output conditions:
- conversion claims preservation without naming what was preserved
- conversion claims improvement without identifying what changed
- blocking blind spots remain unresolved while final state is marked ready

Rules:
- preserve working behavior unless it violates TOP core invariants
- escalate to the real user when the legacy skill is missing, ambiguous, contradictory, unsafe, or leaves blocking blind spots
- do not import legacy drift as valid architecture
- if behavior preservation is claimed, produce or update a behavior baseline
- produce a conversion report that records detected issues, preserved behavior, structural improvements, unresolved limitations, final readiness rationale, and any required redaction boundary
- a converted skill cannot be ready while `blocking_blind_spots` is non-empty
