# Prompt: Design Node Prompt Pipeline

type: service prompt
agent: standalone — not part of the main pipeline
used on request outside task modes

input_contract:
- node_spec or a set of node specs

output_contract:
- pipeline_steps
- retry_policy
- escalation_policy

---

Use this prompt to design the full workflow:
node spec → implementation prompt → code → verification → refinement.

---

## What to do

For the given node or set of nodes, determine:

1. what inputs are needed for the implementation prompt;
2. where the project-local JSON spec is stored;
3. how the prompt file is formed in `prompts/` alongside the JSON spec;
4. how the `prompt` path is written into the node spec;
5. how `props.dir` is set for generated artifacts;
6. how code generation is triggered;
7. how reference behavior is determined;
8. how comparison is performed;
9. how the prompt is corrected;
10. what `maxAttempts` is;
11. what the escalation path looks like;
12. which artifacts are saved after each step.

---

## Expected output format

1. Artifact list
2. Pipeline steps
3. Decision points
4. Retry policy
5. Escalation policy
6. Risks
