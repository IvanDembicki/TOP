# Startup Update Check Template

Use this template in new skill or tool repositories when you want startup update checking to be part of the product contract from day one.

## What to copy

At minimum:

- `release-metadata.template.json` -> `release-metadata.json`
- the startup update rule into your shared rules or product policy layer
- a CLI or launcher command that exposes `check-updates`

## Minimum expected behavior

1. Read local `release-metadata.json`.
2. Optionally read a comparison manifest from a newer release package or trusted source.
3. Report one of:
   - `update_available`
   - `up_to_date`
   - `local_ahead`
   - `comparison_not_configured`
   - `mismatched_manifest`
4. Never auto-upgrade silently.

## Why this exists

The point is not auto-update magic.

The point is to make version freshness visible at startup, so teams do not keep working on stale skills or tools by accident.
