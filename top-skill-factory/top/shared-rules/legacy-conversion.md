# Legacy conversion rules

Legacy skill conversion must treat the legacy skill as evidence, not as final authority.

The converter may use the legacy skill to infer:

- purpose
- target user
- input contract
- output contract
- process flow
- artifacts
- assumptions
- validation rules
- examples
- likely behavior baseline

The converter must escalate to the real user when:

- evidence is missing
- evidence conflicts
- the legacy skill gives ambiguous answers
- the legacy skill contradicts TOP core invariants
- a product or architectural decision is required
- the choice changes the public behavior of the converted skill

The converter must not preserve legacy drift as valid structure.

If behavior preservation is claimed, the converter must produce a behavior baseline and a conversion gap report.

The converter must also produce a blind-spot report whenever imported material leaves unanswered questions about:
- public behavior
- input/output contracts
- process flow
- failure behavior
- validation
- escalation conditions

The converter must produce a conversion report that records:
- available source artifacts
- major issues detected in the legacy skill
- preserved behavior
- structural changes introduced during conversion
- unresolved gaps or escalations
- final readiness or blocked rationale