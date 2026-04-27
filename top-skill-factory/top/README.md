# top/

This folder is the source-of-truth bundle for `TOP Skill Factory`.

It contains the artifacts that define how the skill is structured, how it routes work, how it validates output, and how it demonstrates behavior.

## Contents

- `artifact-manifest.json`
  - declares artifact contracts for full-ready and minimal-demo-ready bundles
- `spec.json`
  - declares the root tree, invariants, validation model, and mode maturity
- `prompts/`
  - controller and node prompts that define bounded responsibilities
- `modes/`
  - mode-level prompts such as create, convert, update, compare, and rollback
- `schemas/`
  - JSON Schemas for signals, decisions, clarification requests, rollback records, and other structured artifacts
- `validation/`
  - contract, architecture, quality, and output rules
- `shared-rules/`
  - cross-cutting rules such as invalidation and legacy conversion policy
- `examples/`
  - bounded evidence bundles that demonstrate ready, draft, and blocked outcomes

## Source-of-truth rules

- Required artifacts inside this folder must not be empty placeholders.
- Structured artifacts must use explicit JSON files instead of free-form text when a schema exists.
- Examples are evidence, not authority. They demonstrate expected behavior, but they do not override `spec.json`, validation rules, or invariants.
- When a schema and an example disagree, the schema and validation rules win.

## Expected usage

Reviewers and downstream AI agents should read:

1. `spec.json`
2. the relevant mode prompt
3. `artifact-manifest.json`
4. the referenced controller and node prompts
5. the matching schemas
6. the related validation rules
7. one or more example bundles

This order keeps interpretation grounded in source artifacts instead of inferred intent.

