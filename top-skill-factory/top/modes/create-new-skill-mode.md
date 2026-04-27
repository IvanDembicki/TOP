# CreateNewSkillMode

Purpose: create a new TOP-based skill from a user goal.

Input:
- normalized_input
- discovery_result
- constraints

Output:
- new_skill_design
- node_contracts
- signal_definitions
- validation_rules
- output_artifacts

Primary objectives:
- turn the requested goal into a bounded TOP skill
- keep structure explicit from the first generated version
- prevent decorative completeness without operational value

Process:
- use normalized input and discovery result to define skill scope
- build the smallest sufficient tree through SkillDesignController
- materialize contracts, signals, and validation together rather than as unrelated fragments
- require clarification when missing information changes structure, behavior, or readiness
- validate the assembled artifact set before final decision

Boundaries:
- do not use legacy evidence in this mode
- do not silently add roadmap nodes for future convenience
- do not label draft artifacts as ready

Invalid output conditions:
- required prompts, schemas, validation files, modes, shared rules, examples, or README are missing or empty
- architecture is generated without explicit contracts and validation posture
- missing user-owned decisions are replaced with optimistic invention

Rules:
- ask clarification through UserInteractionController when the goal is underspecified
- run validation before marking the result ready
- generated structure must remain reviewable and proportionate to the request