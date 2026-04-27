# Architecture validation rules

Checks:
- Single root exists.
- All modes are under Modes.
- ModeRouter exists.
- CompositeFlowController exists.
- CoreControllers exists.
- Leaf nodes do not control flow.
- User interaction is only through UserInteractionController.
- No uncontrolled global context is required for execution.
- Parent controllers own routing and switching.
- Mode handoff uses structured mode results or structured signals only.

Blocking violations:
- Missing root.
- Direct user interaction from a leaf node.
- Multiple active modes without CompositeFlowController.
- Missing validation path.
- Raw previous context used as a legal execution dependency between modes.