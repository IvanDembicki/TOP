# Output validation rules

Checks:
- `spec.json` exists
- `prompts/root.md` exists
- `prompts/mode-router.md` exists
- `modes/create-plan-mode.md` exists
- `README.md` exists

Blocking violations:
- any required artifact is missing
- ready output is emitted without the required artifact set