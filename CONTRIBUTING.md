# Contributing to TOP

This repository is a workspace for multiple TOP-based products.

It is not a single-product repository. Before making changes, identify which product you are actually changing.

## Product model

The current active products are:
- [`top-skill/`](top-skill/)
- [`top-prompt-cleaner/`](top-prompt-cleaner/)
- [`top-skill-factory/`](top-skill-factory/)

Each product owns its own:
- README and onboarding
- release metadata
- validation surface
- examples
- release criteria
- product-specific contracts and rules

## Before making changes

1. Determine the target product.
2. Read that product's local `README.md` and `SKILL.md`.
3. Read that product's release metadata and release criteria if they exist.
4. Use that product's local validator, test scripts, and release checks.

Do not treat the root docs as a substitute for product-local documentation.

## Product-specific changes

If a change affects only one product:
- make the change inside that product directory
- update that product's docs and metadata as needed
- run that product's validator and test or release-check scripts
- keep the change local unless a shared convention is intentionally being updated

## Cross-product changes

If a change affects more than one product:
- define the shared convention explicitly
- inspect each affected product before editing
- update all affected products in the same pass when practical
- keep wording, status models, and release semantics aligned where the convention is shared
- do not force artificial uniformity where products intentionally differ

Examples of valid cross-product changes:
- root navigation layer updates
- shared startup update check conventions
- shared provenance conventions
- shared release metadata patterns

## Release and validation discipline

For every product, prefer the local release surface over assumptions.

That usually means checking some combination of:
- `release-metadata.json`
- `RELEASE_CRITERIA.md`
- `VALIDATION_REPORT.md`
- local validator scripts
- local regression or sensitive-case tests

A product is ready when its own release gates pass, not because another product in this repository is already stable.

## Root docs

The root files:
- [`README.md`](README.md)
- [`AGENTS.md`](AGENTS.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)

should stay focused on:
- repository navigation
- product routing
- cross-product contribution rules

Do not overload root docs with product-specific execution detail that belongs inside a product folder.

## Commit discipline

Prefer commit messages that make the scope obvious.

Examples:
- `docs(root): rewrite product-line navigation`
- `docs(factory): align release report wording`
- `feat(cleaner): add update check support`
- `fix(skill): sync release metadata`
- `chore(shared): align provenance convention across products`