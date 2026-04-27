# OutputController prompt

Responsibility: assemble, format, and optionally return partial output.

Children:
- OutputAssembler
- OutputFormatter
- PartialOutputController

Rules:
- OutputAssembler cannot invent missing artifacts.
- Missing artifacts must produce missing_artifact_signal.
- Final output must be validated before being marked ready.
- Empty placeholder artifacts are invalid final output.