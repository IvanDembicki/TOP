# SkillTreeDesigner

Responsibility: define the skill tree structure, node boundaries, and ownership segmentation for the generated or converted skill.

Input:
- discovery_result
- constraints
- normalized_input when available

Output:
- skill_tree_design

Primary objectives:
- choose the minimum viable tree that satisfies the user goal
- keep responsibilities isolated and reviewable
- avoid unnecessary depth, duplicate controllers, or decorative nodes
- reserve extension points only when they have a clear future role

Process:
- identify the root responsibility of the target skill
- separate mode routing from execution behavior
- decide which responsibilities require controllers, modes, validators, or designers
- keep sibling responsibilities non-overlapping unless a parent controller explicitly coordinates them
- stop tree growth when additional nodes do not remove real ambiguity or complexity

Boundaries:
- do not define detailed contracts that belong to NodeContractDesigner
- do not define signal payload schemas that belong to SignalDesigner
- do not define validation rules that belong to ValidationDesigner
- do not materialize roadmap placeholders unless a clear contract boundary exists

Invalid output conditions:
- one node mixes unrelated responsibilities that should be split
- multiple nodes own the same decision without explicit coordination
- tree depth grows without a concrete simplification benefit
- placeholder nodes are inserted only to make the tree look complete

Rules:
- choose the simplest tree that preserves explicit control
- prefer explicit parent-child authority over cross-branch coupling
- every non-leaf node must justify why orchestration is needed
- every leaf node must have a narrow and testable purpose