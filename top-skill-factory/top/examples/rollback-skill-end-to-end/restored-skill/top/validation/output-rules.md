# Output validation rules

Checks:
- concise mode remains the default path
- detailed mode is explicit-only
- rollback reason is preserved in rollback artifacts

Blocking violations:
- restored variant weakens the validated default-behavior boundary
- rollback target cannot be traced to validated evidence