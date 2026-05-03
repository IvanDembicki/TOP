# Startup update check and runtime hydration

## Runtime freshness policy

The packaged `SKILL.md` is the bootstrap and fallback entrypoint — not the full source of truth.

On every invocation, the agent must hydrate from the installed skill filesystem directory before applying any skill content. See `SKILL.md` § Runtime hydration for the mandatory steps.

The hydration sequence is:
1. Read `hydration-manifest.json` from the skill base directory.
2. Read all `always` tier files.
3. Read the task-specific or `full` tier files as required.

If the skill base directory is not provided by the host environment, or direct file reading is unavailable, the agent must report that runtime freshness cannot be verified. It must not silently proceed as if the packaged content is current.

## Version check rule

After hydrating, perform the version check:

- Compare `skill.json` version with `release-metadata.json` version.
- If a trusted comparison manifest from a newer snapshot or release package is available, compare versions against it.
- If a newer version exists, surface that fact before continuing.
- If no comparison manifest is available, state that version comparison is not configured in the current task.

## Important

- Do not auto-upgrade silently.
- Do not pretend that the local package is up to date if no comparison source exists.
- Do not block all work when comparison or hydration is unavailable; make the status explicit and proceed with the user's acknowledgement.
- Hydration failure is not silent. It must always be reported.
