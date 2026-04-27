# Startup Update Check

Every product built on this stack should perform a quick update check before active work begins.

## Rule

- Check the local skill or product version against a trusted release metadata source if one is available.
- Surface `update_available`, `up_to_date`, or `comparison_not_configured` explicitly.
- Do not auto-upgrade silently.
- Do not block normal work when no comparison manifest is available.

## Minimum behavior

1. Read local `release-metadata.json`.
2. If an external comparison manifest is provided, compare versions.
3. If a newer version exists, report it before normal work starts.
4. If no comparison source exists, report that startup update checking is supported but not configured.

## Non-goals

- No silent remote download.
- No fake certainty about update state.
- No readiness claim based on stale release metadata.
