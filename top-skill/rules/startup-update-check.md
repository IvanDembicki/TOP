# Startup update check

Before serious work begins, AI should quickly check whether the local `top-skill` package may be outdated.

## Rule

- Read local `release-metadata.json`.
- If a trusted comparison manifest from a newer snapshot or release package is available, compare versions.
- If a newer version exists, surface that fact before continuing.
- If no comparison manifest is available, state that update checking is supported but not configured in the current task.

## Important

- Do not auto-upgrade silently.
- Do not pretend that the local package is up to date if no comparison source exists.
- Do not block all work when comparison is unavailable; just make the status explicit.
