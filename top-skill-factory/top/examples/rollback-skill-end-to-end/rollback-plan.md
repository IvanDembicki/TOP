# Rollback plan

1. Confirm that `v0.1-validated` exists in version history.
2. Confirm that the target version is validated.
3. Restore the validated router and root behavior documents.
4. Restore the validated mode and validation artifacts.
5. Preserve rollback reason and audit evidence.
6. Mark the restored bundle as ready only if restored artifacts match the validated target boundary.