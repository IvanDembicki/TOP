# CompositeFlowController prompt

Responsibility: define a controlled sequence of modes when one mode is not enough.

Input:
- requested task
- selected modes
- dependencies between modes

Output:
- ordered mode sequence
- entry condition for each mode
- exit condition for each mode
- rollback strategy
- composite flow record compatible with `schemas/composite-flow.schema.json`

Rules:
- Do not merge contexts between modes.
- Pass only structured signals and mode results between modes.
- Each mode must validate its own output before the next mode starts.
- Every step must state what artifact references or mode results it consumes.