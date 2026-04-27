# TOP

TOP is a Tree-Oriented Programming workspace for structured AI systems.

This repository is the root navigation layer for the current TOP product line. It contains three active products that solve different parts of the same problem: keeping prompt-based and skill-based AI systems structured, reviewable, and evolvable.

## Product line

### 1. [`top-skill`](top-skill/)

The foundational TOP skill package.

Use this if you need:
- the core TOP skill model
- the base execution protocol
- onboarding into TOP concepts and structure
- the canonical reference layer for TOP-oriented skill design

Start here if you want to understand the TOP model itself.

### 2. [`top-prompt-cleaner`](top-prompt-cleaner/)

A product for cleaning, tightening, and restructuring prompts.

Use this if you need:
- prompt cleanup
- prompt normalization
- clearer instruction structure
- safer prompt editing before a prompt becomes a larger workflow

Start here if the problem is still mainly “this prompt is messy”.

### 3. [`top-skill-factory`](top-skill-factory/)

A governed skill-lifecycle product for converting, validating, comparing, updating, and rolling back AI skills.

Use this if you need:
- skill conversion from messy prompt workflows
- explicit contracts and validation gates
- compare / rollback / update flows
- structured artifacts instead of loose prompt text

Start here if the problem is no longer “a prompt”, but “a skill that now needs architecture and lifecycle control”.


## Repository structure

This root layer is intentionally thin.

It exists to:
- explain the product line
- route humans and AI agents to the correct product
- define cross-product contribution rules

Product-specific execution rules, validation, release metadata, and onboarding live inside each product directory.

## For agents

Read [`AGENTS.md`](AGENTS.md) for routing rules across the three products.

## For contributors

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before making cross-product or product-specific changes.

## License

See the license files inside the relevant product directories.
