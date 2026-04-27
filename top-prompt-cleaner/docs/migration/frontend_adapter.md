# FrontendStyleAdapter — DEPRECATED

> **This prompt has been superseded by `TargetLLMStyleMode` and the model profiles in `top/model-profiles/`.**
>
> The name "FrontendStyleAdapter" implied HTML/UI styling. The actual function is LLM prompt convention adaptation.

## Migration

| Old | New |
|---|---|
| `prompts/frontend_adapter.md` | `modes/target_llm_style.md` + `model-profiles/claude.md` / `gpt.md` / `generic.md` |
| `style_adapted_prompt` input signal | handled internally by `TargetLLMStyleMode` |

All logic from this file has been migrated to `modes/target_llm_style.md`.
