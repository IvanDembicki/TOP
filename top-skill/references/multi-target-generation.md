# Multi-Target Generation Workflow

## Purpose

Multi-target generation allows one TOP structural model and one platform-neutral semantic layer to produce multiple target implementations without rewriting prompts for each platform.

The workflow preserves intent first and adapts implementation second.

## Source truth and derived artifacts

Authoritative inputs:

- Layer A: TOP structural truth (`top/*.json`, external branch specs, prompts, assets, presentation, and other project-local TOP source artifacts).
- Layer B: platform-neutral semantic UI layer stored under `top/semantic/**/*.semantic.json`.

Derived outputs:

- Layer C: target adaptation artifacts, normally stored under `top/adaptations/<target>/**/*.adaptation.json` when persistence is needed for review, handoff, or repeatable generation.
- Generated target code and target-native resources.

Layer C and generated code are not source truth. They may be deleted and recreated from Layer A, Layer B, and target constraints.

## Per-target loop

For each target platform:

1. Read the approved TOP structural truth.
2. Read or produce the approved Layer B semantic artifact.
3. Run Target Adaptation Agent for the target.
4. Store the target adaptation output if persistence is needed.
5. Run Generation Agent for that target.
6. Run Spec Sync Agent if synchronized artifacts changed.
7. Run Validation Agent with target-specific checks and shared TOP invariants.
8. Run Final Audit Agent only after validation passes.

The Semantic Interpreter Agent does not run once per target unless Layer A, prompts, or semantic inputs changed.
Target Adaptation Agent runs separately for each target.
Generation Agent runs separately for each target.

## Orchestrator responsibility

For a multi-target request, Orchestrator Agent must create an explicit target matrix:

- target platform;
- semantic layer source;
- target adaptation artifact path;
- generated artifact scope;
- validation status;
- unresolved target-specific risks.

One target passing validation does not imply that another target passed.
Each target requires its own adaptation, generation, and validation result.

## Repair routing

If validation fails:

- semantic preservation failure or Layer B source-platform leakage -> repair semantic inputs, then return to Semantic Interpreter Agent;
- target coherence failure or invalid Layer C decision -> repair adaptation inputs/constraints, then return to Target Adaptation Agent for that target;
- generated implementation failure without semantic/adaptation change -> Repair Agent, then Spec Sync Agent if synchronized artifacts changed, then Validation Agent;
- structural TOP violation -> return to Canon Precheck Agent or TOP Modeling Agent depending on scope.

## Rule

Prompts are not rewritten for each platform.
Platform notes may provide evidence, but target-specific behavior is produced through Target Adaptation Agent, not by copying source-platform primitives.