# Core invariants

1. A skill is a controlled TOP tree, not a free-form prompt.
2. Context is controlled node input, not a global text stream.
3. Leaf nodes do not control flow directly.
4. Parent controllers own routing and switching.
5. User interaction is allowed only through UserInteractionController.
6. Every forced user choice must include U = User-defined answer.
7. Legacy skill is evidence, not authority.
8. OutputAssembler cannot invent missing artifacts.
9. If validation fails, the skill is not ready.
10. Core TOP invariants cannot be disabled.
11. Conflicting old decisions must be explicitly invalidated.
12. Every important decision must have traceability.
13. Mode handoff must use structured mode results and structured signals, not uncontrolled previous context.
14. Required artifacts cannot be empty placeholders in a ready result.
15. A valid rule must have a known verification method.