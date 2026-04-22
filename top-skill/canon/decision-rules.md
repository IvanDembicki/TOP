# Decision Rules

## Repair attempt limit

- MAX_REPAIR_CYCLES = 3
- If blocking violations persist after 3 repair attempts, the pipeline must stop.
- After that, only escalation to re-modeling is permitted.
- Repeating repair without structural change after reaching the limit is forbidden.

## Tier integrity

- Tier must correspond to the actual scope of the task.
- Underclassifying Tier is considered a violation.
- If a task requires changing ownership, boundaries, lifecycle, or tree structure, it cannot be classified as Tier 1.
- Tier mismatch blocks the pipeline until explicit reclassification.
