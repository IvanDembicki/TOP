# Orchestration Run

workflowId: top-skill-2-llm-smoke
runId: 2026-05-13-live-smoke
mode: maintenance
profile: llm-smoke
adapterKind: llm-api

This package was scaffolded by `scripts/create_orchestration_run.py`.

Initial status:

- executionIsolationLevel: protocol-defined
- verificationEvidenceLevel: none
- deliveryStatus: not-certified

Do not report this run as runner-enforced, hard-check-verified, or delivery
complete until the runner, judicial validation, hard checks, and delivery
certification artifacts provide that evidence.

LLM smoke execution:

```text
$env:TOP_LLM_API_KEY = "<secret>"
$env:TOP_LLM_MODEL = "<model>"
python -B scripts/top_protocol_runner.py runner/runner-workflow.json --root top/orchestration/top-skill-2-llm-smoke/2026-05-13-live-smoke --execute-passes --execute-hard-checks --accept-external-runner-evidence --report-out runner/runner-report.json
```

This run can prove runner-enforced isolation only after the LLM API adapter
writes model invocation evidence for each required pass.
