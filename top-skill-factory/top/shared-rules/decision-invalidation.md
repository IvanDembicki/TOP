# Decision invalidation and cleanup

New user requirements, new evidence, or resolved conflicts may invalidate previous decisions.

Invalidation is not deletion by default. Invalidated decisions should remain traceable unless the user explicitly requests hard cleanup.

Required process:

1. Detect conflict.
2. Resolve which requirement has authority.
3. Find affected decisions.
4. Mark old decisions as invalidated.
5. Record invalidation reason and invalidating authority.
6. Plan rebuild of affected artifacts.
7. Re-run validation.

Hard rule:

Do not simply add new requirements on top of old contradictory decisions.

Required trace fields:

- decision_id
- status
- status_reason
- invalidated_by or superseded_by when applicable
- affected_artifacts