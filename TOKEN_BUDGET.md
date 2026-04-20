# Token Budget

Token estimates for planning work with the skill.

Coefficient: ~1.3 tokens per word (English text).
All figures are approximate guidelines, not guaranteed values.

---

## Budget by reading layer

### Mandatory minimum (SKILL.md + canon + agents/index)

| File | ~words | ~tokens |
|---|---|---|
| `AI_PRELOAD_CONTEXT.md` | 900 | 1 170 |
| `SKILL.md` | 2 800 | 3 640 |
| `canon/core-axioms.md` | 500 | 650 |
| `canon/validation-rules.md` | 520 | 675 |
| `canon/forbidden-confusions.md` | 850 | 1 105 |
| `agents/index.md` | 1 150 | 1 495 |
| **Total** | **6 720** | **~8 735** |

### Mandatory minimum — canon (supplement)

| File | ~words | ~tokens |
|---|---|---|
| `canon/controller-content-rules.md` | 210 | 275 |
| `canon/forbidden-interpretations.md` | 276 | 360 |
| `canon/architectural-invariants.md` | 300 | 390 |
| **Total (supplement)** | **786** | **~1 025** |

### Base read path (13 mandatory reference files)

| File | ~words | ~tokens |
|---|---|---|
| `overview.md` | 1 000 | 1 300 |
| `glossary.md` | 1 600 | 2 080 |
| `references/paradigm-definition.md` | 435 | 565 |
| `references/paradigm.md` | 1 300 | 1 690 |
| `references/core-principles.md` | 800 | 1 040 |
| `references/architecture-rules.md` | 1 400 | 1 820 |
| `references/tree-model.md` | 650 | 845 |
| `references/three-trees.md` | 270 | 350 |
| `references/node-model-definition.md` | 234 | 305 |
| `references/node-model.md` | 2 200 | 2 860 |
| `references/runtime-model.md` | 1 200 | 1 560 |
| `references/analysis-rules.md` | 1 450 | 1 885 |
| `references/node-validation-rules.md` | 550 | 715 |
| **Total** | **13 089** | **~17 015** |

### Generative layer (in addition to base)

| File | ~words | ~tokens |
|---|---|---|
| `references/code-generation.md` | 1 360 | 1 770 |
| `references/node-implementation-prompt.md` | 179 | 235 |
| `references/node-implementation-prompts.md` | 370 | 480 |
| `references/prompt-verification-loop.md` | 440 | 570 |
| **Total** | **2 349** | **~3 055** |


### Semantic generation layer (in addition to generative layer)

| File | ~words | ~tokens |
|---|---|---|
| `references/semantic-ui-layer.md` | 520 | 675 |
| `references/target-adaptation-layer.md` | 360 | 470 |
| `references/multi-target-generation.md` | 430 | 560 |
| `agents/semantic-interpreter-agent.md` | 250 | 325 |
| `agents/target-adaptation-agent.md` | 245 | 320 |
| `contracts/agent-output-contracts/semantic-interpretation-output.md` | 240 | 310 |
| `contracts/agent-output-contracts/target-adaptation-output.md` | 245 | 320 |
| **Total** | **2 290** | **~2 980** |

### Runtime/mutable analysis (additionally, as needed)

| File | ~words | ~tokens |
|---|---|---|
| `references/logical-vs-materialized-structure.md` | 750 | 975 |
| `references/state-holder-api.md` | 910 | 1 183 |
| `references/tree-node-contracts.md` | 685 | 890 |
| `references/dynamic-collection-view-node.md` | 495 | 645 |
| `references/source-of-truth-and-serialization.md` | 840 | 1 092 |
| `references/core-vs-skill-conventions.md` | 825 | 1 073 |
| `references/pattern-cards.md` | 1 090 | 1 417 |
| `references/anti-patterns.md` | 1 430 | 1 859 |
| `references/artifact-layout-and-branch-derivation.md` | 575 | 748 |
| **Total** | **7 600** | **~9 882** |

### Validation and workflow (as needed)

| File | ~words | ~tokens |
|---|---|---|
| `rules/violation-catalog.md` | 500 | 650 |
| `rules/violation-classification.md` | 220 | 285 |
| `agents/spec-change-verification-agent.md` | 300 | 390 |
| `contracts/agent-output-contracts/spec-change-verification-output.md` | 200 | 260 |
| **Total** | **1 220** | **~1 585** |

### Additional reference files (as needed)

| File | ~words | ~tokens |
|---|---|---|
| `references/branch-state-model.md` | 610 | 793 |
| `references/spec-change-verification.md` | 476 | 619 |
| `references/data-model-tree.md` | 369 | 480 |
| `references/event-model.md` | 433 | 563 |
| `references/history-undo.md` | 291 | 378 |
| `references/tree-materialization-modes.md` | 947 | 1 231 |
| **Total** | **3 126** | **~4 064** |

---

## Total budget by mode

| Mode | What is read | ~tokens |
|---|---|---|
| `analysis-only` (minimum) | Mandatory minimum | ~8 300 |
| `analysis-only` (full) | Minimum + base read path | ~25 300 |
| `modeling-refactor` | Base read path + agents | ~22 000 |
| `generation-pipeline` | Base + generative layer + semantic generation layer | ~23 000 |
| `spec-change` | Minimum + spec-change-verification | ~8 900 |
| Full skill (all files) | Everything | ~59 000 |

---

## Recommended minimum context

| Task | Minimum context |
|---|---|
| Quick analysis / validation | 32K tokens |
| Generation pipeline | 64K tokens |
| Deep analysis with all references | 128K tokens |

---

## Load priority under limited context

If context is limited, load in the following order:

1. `SKILL.md` — always mandatory
2. `canon/core-axioms.md` + `canon/validation-rules.md` — always mandatory
3. `agents/index.md` — mandatory for pipeline
4. Base read path (13 files) — when possible
5. Mode-specific files from `QUICKSTART_MIN_READS.md`
6. Remaining reference files — as required by the task

A full pre-read of all documents is not required for every task.
Load only what is needed for the specific mode and task.
