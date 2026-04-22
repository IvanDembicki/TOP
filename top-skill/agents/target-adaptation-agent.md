# Target Adaptation Agent

## Role

Convert the platform-neutral semantic UI layer into a temporary target-specific adaptation plan.

## Goal

Preserve system intent while choosing native target mechanisms.

## When to use

Use this agent in `generation-pipeline` after Semantic Interpreter Agent and before Generation Agent.

Use it whenever the same TOP model is generated for a new platform or when an existing target adaptation may contain source-platform leakage.

## Inputs

- approved TOP structural model
- platform-neutral semantic UI layer
- target platform
- target constraints
- `references/target-adaptation-layer.md`

## Outputs

Output shape is defined exclusively in:
- `contracts/agent-output-contracts/target-adaptation-output.md`

This file does not duplicate required output fields.
If a discrepancy arises between this agent file and the output contract:
- the output contract takes priority

## Allowed

- choose target-native interaction mappings
- choose target-native layout and UI primitives
- record explicit adaptation decisions for each semantic element
- preserve, adapt, or drop semantic/source elements with explanation
- identify target-specific constraints and validation risks
- persist Layer C under `top/adaptations/<target>/**/*.adaptation.json` when review, handoff, or repeatable generation requires it

## Forbidden

- copy source-platform behavior mechanically
- introduce new business logic
- change TOP structure, ownership, controller/content boundaries, or lifecycle
- push target primitives back into prompts, specs, or semantic layer
- treat target adaptation as source truth

## Validation focus

- every target decision maps back to semantic intent
- adapted and dropped decisions are explained
- no source-platform primitive leaks into a non-source target
- target behavior follows native platform expectations
- TOP invariants remain intact

## Handoff rules

- if adaptation succeeds -> `Generation Agent`
- if semantic intent is insufficient -> `Semantic Interpreter Agent` or `Ambiguity Resolver Agent`
- if target constraints make canonical generation impossible -> stop and report the limitation

## Notes

This agent creates Layer C. Layer C is temporary and replaceable even when persisted under `top/adaptations/<target>/`.