# Integration Checklist

## Discovery first

- [ ] Check whether the product already has `release-metadata.json`
- [ ] Check whether it already exposes a `check-updates` command or equivalent startup check
- [ ] Check whether validator coverage for release metadata already exists
- [ ] Check whether docs already describe startup update checking
- [ ] Classify the current state as: missing / partial / outdated / already current

## Replacement rule

- [ ] Do not layer a new startup update mechanism on top of an old one
- [ ] If an older or incompatible implementation exists, remove or replace it before installing the new pattern
- [ ] If only part of the pattern exists, keep compatible pieces and add only the missing parts
- [ ] After replacement, resync launchers, validator checks, and docs together

## Product contract

- [ ] Add `release-metadata.json` at repo root
- [ ] Add a shared rule that startup update checking is supported
- [ ] Add a validator check for release metadata presence and consistency
- [ ] Add a launcher or CLI command: `check-updates`

## Documentation

- [ ] Mention the startup update check in the root README
- [ ] Mention it in the quickstart or install flow
- [ ] Mention it in the publish checklist

## Behavior

- [ ] `check-updates` works with no comparison manifest and returns `comparison_not_configured`
- [ ] `check-updates --manifest <file>` compares versions deterministically
- [ ] The product never claims it auto-updates if it does not

## Validation

- [ ] Repo validator checks `release-metadata.json`
- [ ] Repo validator checks version consistency against the main spec or source-of-truth version
- [ ] Regression suite still passes after integration
