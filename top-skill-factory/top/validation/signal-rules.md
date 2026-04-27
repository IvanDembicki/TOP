# Signal validation rules

Checks:
- Every signal has type, from, to, status, payload, and meta.
- Payload is structured.
- from/to nodes exist.
- No raw reasoning is passed.
- No uncontrolled previous context references are used.
- Payload size and nesting are bounded.
- Payload does not contain forbidden keys.

Blocking violations:
- Missing required signal fields.
- Raw free-form context passed as payload.
- Unknown source or target node.
- Payload exceeds defined size or depth budget.