# ModeRouter

Responsibility: select the active mode based on the normalized input and complexity signal.

Input:
- normalized_input (from InputController)
- complexity_signal (from ComplexityDetector)

Output:
- selected_mode
- routing_reason
- target_style_source (when TargetLLMStyleMode is selected): "stated" | "detected" | "default"

Primary objectives:
- route to exactly one mode
- trigger escalation instead of routing when complexity is high

Process:
- check complexity_signal first; if high, route to FactoryEscalationController, not a mode
- if target_style is explicitly declared in normalized_input → select TargetLLMStyleMode; set target_style_source: "stated"
- if target_style is not declared but strong model-specific idioms are detected (e.g. Claude XML tags, GPT system-block pattern) → select TargetLLMStyleMode; set target_style_source: "detected"
- if user requests strict validation, or the prompt has clearly missing required fields, select StrictMode
- otherwise select QuickCleanMode as default

Auto-detection signals for TargetLLMStyleMode:
- Claude: `<context>`, `<task>`, `<instructions>` XML blocks present
- GPT: "System:" or "User:" labels present; explicit system/user message split
- If signals are ambiguous, do NOT auto-select TargetLLMStyleMode — default to QuickCleanMode

Boundaries:
- do not execute the selected mode
- do not select multiple modes simultaneously
- do not treat complexity as a style preference

Invalid output conditions:
- mode selected despite high complexity signal
- TargetLLMStyleMode selected without target_style_source being set
- routing_reason is absent

Rules:
- activate exactly one mode or trigger escalation
- QuickCleanMode is the default when no stronger signal is present
- routing_reason must name the signal that determined the choice
- target_style_source must be emitted whenever TargetLLMStyleMode is selected
