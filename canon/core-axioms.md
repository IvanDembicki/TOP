# Core Axioms

## Human readability

The code must be written to be maximally understandable to a human reader.
Clarity and unambiguity take priority over brevity or conciseness.

All structural and naming decisions must support fast, reliable understanding of the code at scale, without requiring implicit knowledge or guesswork.

## Typing

- Object typing must be as strict, explicit, and complete as the technology reasonably permits.
- If an explicit type contract can be defined, it must be defined.
- Weak, implicit, partial, or shape-based typing is non-canonical unless stricter typing is not realistically achievable in the given technology.

## Naming

- Code must remain readable at scale (volumetrically readable).
- Names must be fully descriptive and unambiguous.
- An abbreviation is allowed only if it is immediately clear without explanation
  to any developer in the given domain.
- Any abbreviation that requires explanation or domain-external context is a violation.

## Behavioral state split (hidden switchable)

A node is a hidden switchable if it independently manages switching between fundamentally different representations or behaviors by accessing external architectural state.

Detection criterion — both conditions must hold simultaneously:

1. The node reads external architectural state (mode, lifecycle phase, openedChild, etc.)
2. And as a result changes at least one of:
   - the visual representation of its constituent elements
   - the available behavior (drag, add, delete, etc. — either present or absent)

The number of explicit child nodes is irrelevant. A hidden switchable may be a monolithic node whose internal elements and handlers change.

Not a violation:
- A node changes only model data (label text, color from data) — behavior is identical in both states.

Canonical refactoring: the node becomes an explicit switchable holder with child state nodes. Each state node fully owns its own representation and behavior. A state node does not read the external mode — it is itself the representation of that mode.

## Behavioral coherence

A node must not simultaneously own capabilities with mutually exclusive preconditions.

If capability A requires condition X, and capability B requires condition NOT-X — they belong to different state nodes.

Detection criterion:

Conflicting event handlers in a single node — handlers for opposite sides of a single transition:
- `mouseenter` / `mouseleave` — hover state
- `mouseover` / `mouseout` — hover state
- `pointerdown` / `pointerup` — press state
- analogous pairs with mutually exclusive preconditions

The presence of such pairs in a single node means the node contains hidden internal state that must be explicitly extracted into state nodes.

Not a violation:
- A single node registers both handlers to manage one continuous behavior (e.g. drag: `pointerdown` begins, `pointerup` ends a single action).

Canonical refactoring: extract NormalState and HoverState (or equivalents) as child state nodes. Each state node owns only those handlers that are active in its state.

## Typing fallback hierarchy

Typing priority:

1. strict nominal typing
2. explicit structural typing
3. documented weak typing

Rules:
- Moving to a weaker level is permitted only if the technology syntactically does not support a stricter level
- Convenience, verbosity, implementation speed, and local familiarity are not grounds for weakening
- `Realistic` means only technical impossibility of stricter typing, not its inconvenience
- If weak typing is used, it must be explicitly documented as a fallback, not as a norm
