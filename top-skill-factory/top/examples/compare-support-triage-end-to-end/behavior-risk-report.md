# Behavior Risk Report

The core risk is not formatting or structure. It is ownership.

- Variant A keeps the severe-versus-non-severe decision inside an explicit route.
- Variant B lets inferred urgency and VIP metadata silently shift the path.

That means Variant B is faster in some cases, but less predictable and harder to audit when escalation was triggered by model judgment rather than declared state.
