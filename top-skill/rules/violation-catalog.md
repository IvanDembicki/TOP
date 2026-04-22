# Violation Catalog

This file defines canonical violation codes for all known TOP violations.

All validation, audit, and repair output must reference these codes.
Consistent codes enable stable cross-session reporting and precise repair targeting.

---

## Core violations — CORE-xxx

Affect architectural correctness. Always block finalization.

| Code | Name | Description |
|------|------|-------------|
| CORE-001 | Controller/Content boundary violation | Controller accesses content platform primitive directly (e.g. `this.el`, `this.getView().classList`, `content.getView()`). Must use named `IContentAccess` methods only. |
| CORE-002 | Content encapsulation violation | Content object or its platform primitive exposed as public interface outside the node. |
| CORE-003 | Hidden switchable | Node reads external architectural state (mode, lifecycle phase, openedChild) and changes visual representation or available behavior as a result. Must be refactored into explicit switchable. |
| CORE-004 | Behavioral coherence violation | Node registers handlers for mutually exclusive states (mouseenter/mouseleave, pointerdown/pointerup) without a single continuous action justification. Must be split into state nodes. |
| CORE-005 | Lifecycle violation | Content not destroyed on deactivate/close without an explicit retention pattern. Hidden retention is forbidden. |
| CORE-006 | Method semantics violation | `buildChildren()` used as general init method, or any lifecycle method used for a purpose outside its defined semantics. |
| CORE-007 | Non-tree relationship | Implicit cross-link between non-adjacent nodes bypassing the tree structure. Must be expressed through a connector or explicit contract. |
| CORE-008 | Missing internal access boundary | Node has separate content but `IContentAccess` or `IControllerAccess` is absent or anonymous. Both directions must be explicit, typed, and named. |
| CORE-009 | Child node encapsulation violation | Public getter or method returns a child node reference directly. External code must not hold a reference to a non-direct child. |
| CORE-010 | Phase separation violation | Constructor used as undifferentiated initialization bucket mixing content materialization, child materialization, activation, and refresh. |
| CORE-011 | Parent-owned materialization violation | Child self-mounts or self-attaches its view into the parent integration surface from within its own lifecycle methods. |
| CORE-012 | Content materialization violation | `props.contentType` is declared in spec but no separate content class exists, or a thin stub exists while platform logic remains in the controller. |
| CORE-013 | Declaration order violation | In a one-file node implementation, content/view class declared before the access boundary artifact that mediates access to it. |
| CORE-014 | View access violation | `getView()` called on a node by any caller other than its direct parent. |
| CORE-015 | Logic in content violation | Behavioral or architectural decision logic inside content — orchestration, lifecycle decisions, protocol routing, or state-driven behavior selection. |
| CORE-016 | Semantic layer platform leakage | Layer B contains platform primitives, source-framework APIs, CSS/DOM/widget terms as truth, or copies source implementation details instead of semantic intent. |
| CORE-017 | Target adaptation semantic drift | Layer C or generated target artifacts change business/system meaning, introduce new behavior, or adapt source primitives without preserving semantic intent. |

---

## Skill convention violations — CONV-xxx

Violations of skill-specific conventions. Do not automatically classify as CORE.

| Code | Name | Description |
|------|------|-------------|
| CONV-001 | Naming convention mismatch | Node, file, or class name does not follow the naming rules defined in `rules/naming-conventions.md`. |
| CONV-002 | File layout mismatch | Generated artifact not placed in the directory specified by `props.dir` or the structural correspondence rule. |
| CONV-003 | Structural Correspondence Rule violation | Prompt path does not reflect the same semantic position in the tree as the corresponding code path. See `references/artifact-layout-and-branch-derivation.md`. |
| CONV-004 | Missing prompt file | A code-generated node has no implementation prompt file in `top/prompts/`. |
| CONV-005 | Spec storage violation | Spec tree not stored as `.json` inside `top/`. |
| CONV-006 | Missing props.contentType | Node has content and its type must be explicitly recorded, but `props.contentType` is absent from the spec. |

---

## Workflow gaps — WF-xxx

Violations of the execution process. Affect pipeline validity, not TOP Core itself.

| Code | Name | Description |
|------|------|-------------|
| WF-001 | Missed pipeline stage | A required stage for the active `task_mode` was skipped. |
| WF-002 | Missing output contract field | Agent output is missing a required field defined in the corresponding output contract. |
| WF-003 | Unresolved ambiguity passed through | Critical ambiguity was not resolved before the pipeline continued past the point where it was required. |
| WF-004 | Invalid Tier classification | Declared Tier does not match the actual scope of the task. Underclassification is a violation. |
| WF-005 | Invalid task_mode routing | Task was routed through the wrong mode pipeline. |
| WF-006 | Spec/code drift not checked | Changes to `src/`, generated artifacts, JSON specs, or prompts were made without running a drift check. |
| WF-007 | Repair cycle limit exceeded | `MAX_REPAIR_CYCLES = 3` reached without convergence and without escalation to re-modeling. |
| WF-008 | Missing semantic interpretation stage | Generation pipeline reached target adaptation or generation without a valid Semantic Interpreter output. |
| WF-009 | Missing target adaptation stage | Generation pipeline reached Generation without a valid Target Adaptation output for the active target. |

---

## Usage

Validation Agent and Final Audit Agent must reference violation codes in all output.

Format: `[CODE] Short description of the specific instance.`

Example: `[CORE-003] TreeItem reads isEditMode from parent and hides/shows drag handle based on it.`
