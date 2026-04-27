# FrontendStyleMode — DEPRECATED

> **This mode has been renamed to `TargetLLMStyleMode`.**
>
> The name "FrontendStyle" was misleading — it implied HTML/UI styling, but the mode adapts LLM prompt conventions, not frontend formatting.
>
> **Use `top/modes/target_llm_style.md` instead.**
>
> All behavior, rules, and profiles from this file have been migrated to `target_llm_style.md` and `top/model-profiles/`.

## Migration

| Old reference | New reference |
|---|---|
| `FrontendStyleMode` | `TargetLLMStyleMode` |
| `FrontendStyleAdapter` | `TargetLLMStyleMode` (mode handles adaptation directly via model profiles) |
| `modes/frontend_style.md` | `modes/target_llm_style.md` |
| `prompts/frontend_adapter.md` | Model profiles in `top/model-profiles/` |

## Why renamed

The name "FrontendStyle" was identified in external review as a false signal — readers assumed it modified HTML or UI output, not LLM prompt structure. The new name `TargetLLMStyle` is unambiguous about the scope: it adapts prompts to the target language model's formatting conventions.
