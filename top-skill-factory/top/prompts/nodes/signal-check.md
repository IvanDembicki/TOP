# SignalCheck

Responsibility: verify that defined signals are structured, bounded, and semantically consistent.

Input:
- signal_definitions
- schema_artifacts when present

Output:
- signal_check_report

Primary objectives:
- prevent signal drift and ambiguous handoff
- enforce bounded payload design

Process:
- inspect each signal for sender, receiver, purpose, and payload
- identify overlaps, vague naming, or illegal payload content
- verify that signals support actual routing or validation decisions

Invalid output conditions:
- raw context transfer is allowed through signal payload
- signal variants overlap so heavily that routing depends on guesswork

Rules:
- signals must be intentionally typed, not conversationally improvised
- every signal should exist because a concrete decision needs it