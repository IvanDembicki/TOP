# Core invariants

Source of truth: `top/spec.json`. This file mirrors the spec invariants exactly.

1. ModeRouter activates exactly one mode.
2. SensitiveDataDetector runs before any transformation; blocking findings halt the pipeline.
3. ComplexityDetector runs before any transformation.
4. High complexity routes to FactoryEscalationController, not to a cleaning mode.
5. A prompt is a single-scope artifact; multi-step AI workflows are not in scope for cleaning.
6. OutputBuilder cannot invent goal, constraints, or output format not present in the original prompt.
7. A cleaned prompt must not silently remove user-stated constraints.
8. Validation must pass before the result is marked ready.
9. TargetLLMStyleMode changes style only, not semantics.
10. Diff is required when the prompt was modified.
11. Noise removal requires a traceable reason recorded in diff.
12. Conflict resolution must be explicit; silent choices are not allowed.
13. Escalation and cleaned output are mutually exclusive primary outputs.
14. A blocked result is honest; it is not a failure to be hidden.
15. ClarificationController blocks in strict mode when goal or output_format is absent and cannot be safely inferred.
16. A startup update check should run before active work begins when release metadata and a trusted comparison manifest are available.
