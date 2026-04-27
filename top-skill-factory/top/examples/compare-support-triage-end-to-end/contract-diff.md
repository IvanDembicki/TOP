# Contract Diff

## Variant A

- escalation requires declared severity state
- VIP status affects queue priority, not routing ownership

## Variant B

- escalation may occur on inferred urgency alone
- VIP status can force escalation path selection even when explicit classification is incomplete

## Practical effect

Variant B moves routing authority from explicit contract state to system inference.
