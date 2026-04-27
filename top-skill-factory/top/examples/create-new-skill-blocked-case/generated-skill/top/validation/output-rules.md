# Output validation rules

Checks:
- `spec.json` exists
- `prompts/root.md` exists
- `prompts/mode-router.md` exists
- `modes/create-launch-plan-mode.md` exists
- `README.md` exists
- unresolved blocking blind spots prevent ready state

Blocking violations:
- any required artifact is missing
- ready output is emitted while blocking blind spots remain
- missing domain-specific launch meaning is replaced with guessed detail