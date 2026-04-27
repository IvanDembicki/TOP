# QualityControlController prompt

Responsibility: check consistency, type strictness, complexity budget, rule verifiability, dry run, and core invariants.

Children:
- ArtifactConsistencyValidator
- TypeStrictnessValidator
- ComplexityBudgetController
- RuleVerifiabilityCheck
- DryRunController
- CoreInvariantGuard

Rules:
- A structurally valid skill can still fail semantic or execution validation.
- Rules that cannot be checked must be rejected or rewritten.
- CoreInvariantGuard has authority over legacy evidence and user override.
- Quality control must use measurable thresholds, not only general warnings.