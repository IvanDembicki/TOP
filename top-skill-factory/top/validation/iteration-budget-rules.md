# Iteration budget rules

Default limits:
- validation/repair cycles: 3
- clarification cycles: 2
- mode retries: 2
- unresolved blocking ambiguities after clarification: 1

Rules:
- Budget exhaustion must be visible in output.
- Budget exhaustion must route to blocked or failed, never to ready.
- A mode may not silently restart itself after budget exhaustion.