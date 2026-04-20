# Node Implementation Prompt

## Purpose

`Node Implementation Prompt` is the bridge between formal node description and
concrete code implementation.

It exists to preserve architectural continuity during AI-assisted generation.

## Position in the chain

The intended chain is:

- `spec tree`
- `node spec`
- `Node Implementation Prompt`
- `Semantic Interpretation` (Layer B)
- `Target Adaptation` (Layer C)
- `code artifact`

Code should not bypass the architectural layers above it.

## Why it matters

This layer makes it possible to:

- keep spec primary and code derivative;
- regenerate code after spec changes;
- keep implementation portable across stacks;
- validate output against architectural intent;
- avoid re-deriving architecture from code every time.

## Minimal contents

A `Node Implementation Prompt` should normally preserve:

- node identity and role;
- controller boundary;
- content boundary;
- allowed children or dependencies;
- state responsibilities;
- invariants and forbidden confusions;
- platform-neutral semantic intent;
- target adaptation boundary;
- target language or framework constraints;
- artifact output expectations.

## Platform-neutral behavior and platform notes

The behavioral part of a `Node Implementation Prompt` must be platform-neutral.
It describes node semantics, not a framework recipe.

Platform-specific material must be isolated in `Platform implementation notes`.
Those notes may explain why the current target requires a particular mechanism and may help
another target understand risks or edge cases. They are not portable implementation commands.
When generating for another technology, the AI must use them as context and choose the
native target-appropriate mechanism independently.

## Restriction

A `Node Implementation Prompt` must not silently expand architectural scope.
It may operationalize the node for implementation,
but must not invent new topology, ownership, or state logic on its own.
