# TargetLLMStyleMode

## Purpose

Adapt the cleaned prompt's formatting, structure, and phrasing to the conventions of the specified target LLM. This mode changes **style only** — it does not change the semantic goal, constraints, or output format.

Replaces the deprecated `FrontendStyleMode`. See `docs/migration/frontend_style.md` for migration note.

## Input

- `structured_prompt` — output from StructureExtractor (goal, constraints, output_format, noise_candidates)
- `target_style` — one of `"claude"`, `"gpt"`, `"default"` (required; absent → treat as `"default"`)
- `target_model` — optional string, e.g. `"o1"`, `"claude-opus-4"` (enables sub-profile logic)
- `complexity_level` — from ComplexityDetector; must be `"low"` or `"medium"`

## Output

- `cleaned_prompt` — restyled prompt string
- `diff` — object matching `diff.schema.json`
- `profile_used` — one of `"claude"`, `"gpt"`, `"generic"`

## Activation condition

ModeRouter sets `mode = "target_llm_style"` when:
1. The user explicitly requests style adaptation for a target LLM, OR
2. `structured_prompt.style` is set to a non-default value (`"claude"` or `"gpt"`), OR
3. The input prompt contains strong model-specific idioms (XML tags → Claude, numbered system message → GPT).

## Primary objectives

1. Apply the model profile for the specified `target_style` (from `top/model-profiles/`).
2. Fix anti-patterns listed in the applicable profile.
3. Preserve all semantic content: goal, constraints, output format, domain vocabulary.
4. Produce a diff showing every rewritten phrase and its reason.

## Process

1. Resolve `target_style` → load the corresponding model profile.
   - `"claude"` → `top/model-profiles/claude.md`
   - `"gpt"` → `top/model-profiles/gpt.md`
   - `"default"` or unknown → `top/model-profiles/generic.md`
2. Check for `target_model` sub-profile (e.g., o1/o3 in GPT profile).
3. Apply anti-pattern fixes from the profile table.
4. Apply structural recommendations (role framing, system/user split, XML wrappers) as described in the profile.
5. Run ValidationController — pass required, style change only, no semantic drift.
6. Build diff with `rewritten_phrases`, `removed_noise`, `warnings`.

## Boundaries

- Do NOT resolve blocking contradictions — surface them in `diff.unresolved_conflicts`.
- Do NOT invent constraints, output format, or goal not present in the input.
- Do NOT apply GPT formatting conventions to a Claude-targeted prompt, or vice versa.
- Do NOT restructure the logical flow of the prompt (reordering sections) unless the profile explicitly requires it (e.g., GPT: move role to system message).
- Style changes only. If a change would alter meaning, do not make it.

## Invalid output conditions

- `diff` absent or empty when the prompt was modified.
- `cleaned_prompt` identical to input when at least one anti-pattern was present.
- Semantic content changed (goal, constraint, output format altered).
- `profile_used` absent or mismatched with `target_style`.
