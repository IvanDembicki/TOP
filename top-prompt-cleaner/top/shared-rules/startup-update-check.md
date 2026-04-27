# Startup Update Check

Run a quick update check before active prompt-cleaning work begins.

## Rule

- Read local `release-metadata.json` at startup.
- If a trusted comparison manifest is available, compare versions and surface `update_available`, `up_to_date`, or `local_ahead` explicitly.
- If no comparison manifest is available, do not pretend the local copy is current; surface `comparison_not_configured` when update state matters.
- Do not auto-update silently.
- Do not block normal prompt-cleaning work just because no comparison manifest is available.

## Minimum behavior

1. Read local `release-metadata.json`.
2. If an external comparison manifest is provided, compare versions.
3. If a newer version exists, report it before normal work starts.
4. If no comparison source exists, report that startup update checking is supported but not configured.

## Non-goals

- No silent remote download.
- No fake certainty about update state.
- No readiness claim based on stale metadata alone.
