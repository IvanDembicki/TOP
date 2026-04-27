# Contract validation rules

Checks:
- Every node has responsibility.
- Every executable node has input and output contract.
- Node responsibilities do not overlap without an explicit parent controller.
- Designers may modify only their own artifact.
- Outputs are structured and schema-compatible.
- Required schemas define concrete fields, not only generic placeholders.
- Import, conversion, and update flows explicitly account for blind-spot detection when source material is incomplete.
- `ConvertLegacySkillMode` defines a conversion report as an explicit output artifact.`r`n- Legacy import and conversion flows define a sensitive-data pass before reusable artifacts are emitted.

Blocking violations:
- Undefined input.
- Undefined output.
- Generic untyped fields such as data, content, result, or context without schema.
- Node doing another node's responsibility.
- Mode or node artifact exists but is empty.
- Conversion flow claims improvement or preservation without a conversion report artifact.`r`n- Legacy import reaches ready without a declared sensitivity scan or redaction policy.
