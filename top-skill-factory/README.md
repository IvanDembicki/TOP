# TOP Skill Factory

TOP Skill Factory turns messy AI skills into structured, validated, versioned skill systems.

Short hook:

> Prompts were fine. Skills need architecture.

## Install and use

1. Copy this folder into your Claude-compatible skills directory.
2. Run a quick update check: `pwsh ./top-skill-factory.ps1 check-updates`.
3. Start your skill-enabled AI workflow environment.
4. Ask it to use `top-skill-factory` to create, convert, compare, update, or roll back a skill.
5. Expect structured artifacts rather than only prose.

Quick launcher options:

```powershell
pwsh ./top-skill-factory.ps1 check-updates
pwsh ./top-skill-factory.ps1 validate
pwsh ./top-skill-factory.ps1 demo --out .\tmp\demo-output
```

## What it is

TOP Skill Factory is a TOP-based meta-skill for:

- creating new skills
- converting legacy prompt-skills
- updating existing skills
- comparing competing variants
- rolling back to validated prior states
- governing skill evolution through contracts, signals, validation, and evidence

It is not a code runtime. It is a governance and lifecycle layer for skills.

## Status

This release is a **stable bounded skill package**.

It already has:

- explicit mode routing
- structured contracts
- structured signals
- validation and quality gates
- rollback and compare flows
- ready, draft, blocked, and failed outcome examples
- bounded CLI workflows with regression coverage

It does not claim:

- compiler-grade enforcement
- a finished autonomous runtime
- stable support for experimental or roadmap modes

## Stable release scope

The stable bounded workflow contract currently includes:

- `validate`
- `check-output`
- `demo`
- `create`
- `convert`
- `update`
- `compare`
- `rollback`

Experimental CLI surface:

- `merge`

Roadmap-only modes remain excluded from the stable contract.

## Artifact contracts

The repository now distinguishes between:

- `full_factory_contract`
- `stable_workflow_contract`
- `workflow_draft_contract`
- `minimal_demo_contract`

See [top/artifact-manifest.json](top/artifact-manifest.json).

Use them this way:

- `minimal_demo_contract` -> compact examples only
- `workflow_draft_contract` -> reviewable but non-final CLI outputs
- `stable_workflow_contract` -> bounded stable CLI outputs
- `full_factory_contract` -> full repository-level completeness

## Security posture

Legacy conversion now has explicit sensitive-import proof cases.

- API keys and private keys must block conversion
- PII and internal URLs must not silently leak into reusable output
- sensitive values must not be echoed verbatim in reports

See [top/examples/convert-sensitive-legacy-skill-blocked](top/examples/convert-sensitive-legacy-skill-blocked).

## Onboarding

- [SKILL.md](SKILL.md)
- [Quick start](onboarding/quickstart.md)
- [release-metadata.json](release-metadata.json)
- [Release criteria](RELEASE_CRITERIA.md)
- [Validation report](VALIDATION_REPORT.md)
- [Release notes](RELEASE_NOTES.md)
- [Mode maturity](onboarding/mode-maturity.md)
- [Publish checklist](onboarding/publish-checklist.md)
- [Demo script](onboarding/demo-script.md)

## Validation model

Validation in this release is still protocol-driven and partly LLM-governed, but the bounded CLI workflows, validator, and regression suite are now treated as release gates rather than demo conveniences.

## Current limitations

- this is still a bounded skill package, not a full autonomous runtime
- validator coverage is stronger, but still narrower than a general-purpose build system
- scenario coverage is good enough for stable bounded use, not proof of ecosystem-wide maturity
- experimental and roadmap modes remain intentionally outside the stable release contract

## Release check

Run `python scripts/release_check.py` for the full release gate pass.
