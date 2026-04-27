# Rollback audit

Source version:
- `v0.2-risky`

Target version:
- `v0.1-validated`

Why rollback was chosen:
- current routing language allowed detailed behavior to activate implicitly
- validated target preserved explicit user ownership of detail escalation

What was restored:
- explicit concise-default routing
- explicit-only detailed mode
- validation language protecting the default behavior boundary

Residual risks:
- none material inside this compact example