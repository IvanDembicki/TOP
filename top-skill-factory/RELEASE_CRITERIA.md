# Release Criteria

A release may be presented as a stable bounded skill package only if all of the following are true:

1. Validator passes.
2. CLI regression suite passes.
3. Sensitive-data regression suite passes.
4. All stable modes have at least one example.
5. Stable CLI commands are limited to `validate`, `check-output`, `demo`, `create`, `convert`, `update`, `compare`, and `rollback`.
6. `merge` remains explicitly experimental.
7. Planned or skeletal modes are excluded from the stable contract.
8. No broken local markdown links remain in release docs.
9. Version numbers are synchronized across release metadata, spec, and release docs.
10. Security proof artifacts exist for blocked sensitive import.
11. Demo output validates.
12. No stable release claim relies on `minimal_demo_contract`.
