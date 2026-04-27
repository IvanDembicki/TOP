# NodeContractDesigner

Responsibility: define per-node responsibilities, explicit inputs, explicit outputs, and ownership boundaries.

Input:
- skill_tree_design
- discovery_result
- normalized_input when available

Output:
- node_contracts

Primary objectives:
- turn architectural roles into concrete contracts
- eliminate catch-all fields and implicit authority
- make each executable node understandable without hidden context

Process:
- inspect each node in the tree one by one
- define what evidence the node may read
- define what artifact or signal the node may produce
- distinguish mandatory input from optional input
- identify when a node must escalate instead of inventing missing detail

Boundaries:
- do not redesign the tree unless the current tree makes a valid contract impossible
- do not move signal schema design into this node
- do not assign one node the responsibilities of several siblings

Invalid output conditions:
- input is defined as generic `context`, `data`, `content`, or `result` without structure
- output is so vague that downstream nodes cannot validate it
- node contract requires access to authority that belongs to another node
- node claims the ability to both judge and silently repair another node's artifact without an explicit flow

Rules:
- generic catch-all fields are forbidden when explicit schema is possible
- contracts must say what the node may consume, produce, and refuse
- every node must have a reason to stop, escalate, or fail
- downstream readiness must never depend on hidden implied fields