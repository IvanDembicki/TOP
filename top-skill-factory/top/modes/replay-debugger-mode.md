# ReplayDebuggerMode

Maturity: planned / skeletal alpha.

Purpose: replay structured mode results, signals, and decision traces to diagnose where a skill build or update went wrong.

Input:
- decision_trace
- mode_results
- signal_log
- expected_behavior_baseline

Output:
- replay_report
- divergence_points
- repair_hints

Rules:
- Replay operates on structured artifacts, not on uncontrolled previous conversation text.
- Divergence must identify expected decision versus observed decision.
- If the available trace is incomplete, the report must say so explicitly instead of fabricating a replay.
