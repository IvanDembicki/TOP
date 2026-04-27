# RuntimeMonitorMode

Purpose: define how a generated skill should be observed after deployment or integration.

Maturity: planned / skeletal alpha.

Input:
- generated_skill
- monitoring_goal
- available_runtime_signals

Output:
- monitoring_plan
- runtime_risk_notes

Rules:
- Do not claim direct runtime enforcement if no runtime instrumentation exists.
- Distinguish between design-time validation evidence and post-deployment runtime evidence.
- If the target environment cannot provide runtime telemetry, return a bounded monitoring plan rather than fabricated monitoring detail.