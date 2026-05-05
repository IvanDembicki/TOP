# top/

This folder is the self-governance layer for `top-skill`.

It exists so `top-skill` is governed by the same rules it applies to other
systems: explicit structure, artifact contracts, mode maturity, validation
rules, schemas, and traceability.

## Contents

- `spec.json` — skill execution model, root tree, invariants, and validation model
- `artifact-manifest.json` — readiness contracts for the skill package and
  migration project outputs
- `modes/mode-manifest.json` — supported mode maturity and routing boundaries
- `schemas/` — machine-readable schemas for structured project artifacts
- `shared-rules/` — cross-cutting rules for skill maintenance and evolution
- `validation/` — output and readiness validation rules
- `provenance.json` — evidence for where this governance layer came from

## Source-of-truth rules

- Required artifacts must not be empty placeholders.
- Structured workflow artifacts use JSON when a schema exists.
- Examples and previous outputs are evidence, not authority.
- When a schema and prose disagree, schema and validation rules win.
- A ready claim is invalid while required validation has not run.

