# ModeRouter

Purpose: select the correct output depth for the plan-builder skill.

Rules:
- use `CreatePlanMode` by default
- use `CreateDetailedChecklistMode` only when the user explicitly asks for a detailed checklist
- do not route ambiguous requests into the detailed mode by assumption