# Behavior risk report

## Variant A

Risk level: lower

Reason:
- detailed behavior is explicitly user-triggered
- default concise behavior is protected by both routing and validation language

## Variant B

Risk level: higher

Reason:
- the phrase "when more detail seems useful" allows the router to change behavior implicitly
- concise default behavior is no longer guaranteed by contract or validation

## Comparison judgment

The difference is not cosmetic.
It changes who owns the decision to leave the concise path: the user in Variant A, the system in Variant B.