# Validation Rules

Result is invalid until all validation checks pass.
Compilation success is not architectural success.
Local functionality does not override TOP rules.

## Boundary validation
- No direct access to concrete implementation.
- No bypass around content.
- All interaction through allowed protocols.

## Protocol validation
- If a node has a separate content object, explicit internal access boundaries must exist: `IContentAccess` and `IControllerAccess`.
- Internal access boundaries must be explicit, typed, and hidden from the external world as far as the technology allows.
- Public node surface and internal access boundaries must not be mixed.
- No real interaction outside allowed protocol boundaries.

## Content validation
- Content has no architectural will.
- Content does not manage lifecycle.
- Content does not know or use the full public node surface directly; it interacts with the controller only through `IControllerAccess`.
- Content may execute low-level platform commands on its own implementation material, including subscribe/unsubscribe and analogous operations, but it must not interpret those operations as architectural decisions or use them as an external communication channel.

## Controller validation
- Controller owns behavior, lifecycle, orchestration, branching.
- Controller does not use render primitives as communication channel.

## Lifecycle validation
- Content is created on demand.
- Content is destroyed on deactivate/close by default.
- No hidden retention.

## Method semantics validation
- Methods are used strictly by intended semantics.
- No semantic overloading (e.g. init bucket).

## Typing validation
- All boundaries explicitly typed.
- No implicit context objects.
- No weak typing where strict is possible.

Operational checklist: `rules/typing-checklist.md`.
Behavioral analysis and typing analysis are independent passes. The absence of behavioral violations does not imply the absence of typing violations.

## Semantic preservation validation
- Layer B must preserve original user intent, system intent, interaction intent, feedback intent, state model, layout intent, constraints, and accessibility semantics where applicable.
- Platform-specific source artifacts must be removed from Layer B or quarantined as evidence, not preserved as meaning.
- Semantic vocabulary may be extended only with platform-independent meaning.

## Source-platform leakage validation
- DOM, CSS, Flutter widgets, UIKit/Android classes, framework APIs, and source-specific event APIs must not appear in Layer B.
- A non-source target adaptation must not copy source-platform primitives unless the same primitive is native and justified for that target.
- Generated target artifacts must trace target decisions to Layer B semantics, not to source-platform notes.

## Target adaptation validation
- Layer C must explicitly mark each semantic element as preserved, adapted, or dropped with reasons for adapted/dropped decisions.
- Target adaptation must use native target expectations and must not introduce new business logic.
- Target adaptation must not alter TOP ownership, lifecycle, controller/content boundaries, or structural invariants.
## Canon rule
Only canonical patterns are allowed. Everything else is a violation.

## Hidden switchable check

Violation signal (both conditions must hold simultaneously):

1. The node accesses external architectural state (isEditMode, openedChild, lifecycle phase, etc.)
2. And as a result changes:
   - the visual representation of its constituent elements (show/hide, swap)
   - or the available behavior (drag, event handlers, interactive buttons)

Not a violation:
- `refresh()` changes only model data (text, label, icon from data model) — see the formal `refresh()` contract in `references/tree-node-contracts.md §5`
- Node behavior is identical in both states

Classification: `core_violation`
Reason: hidden ownership of behavior, hidden lifecycle

The node is a candidate for switchable refactoring. See `rules/pattern-recognition.md` — Pattern #1.

## Behavioral coherence check

Violation signal:

A node registers handlers for opposite sides of a single state transition:
- `mouseenter` + `mouseleave` (or `mouseover` + `mouseout`) — hover
- `pointerdown` + `pointerup` — press
- analogous mutually exclusive pairs

Exception: if the handler pair manages a single continuous action (drag start / drag end) — not a violation.

Classification: `core_violation`
Reason: hidden internal state; the node contains behavior that must be split across state nodes.

The node is a candidate for switchable refactoring. See `rules/pattern-recognition.md` — Pattern #2.

## Structural correspondence check

Prompt paths and code paths must reflect the same semantic position of the node in the tree.
If a node belongs to a particular semantic branch, its prompt and its implementation must be located in the corresponding subdirectories of their respective roots.

Definition: `references/artifact-layout-and-branch-derivation.md` — Structural Correspondence Rule.

Classification: `skill_convention_violation`

## Logic in content check

- Display-only logic inside content is permitted.
- Low-level platform-command execution inside content is permitted when it is limited to the content's own implementation material and forwards semantic events only through `IControllerAccess`.
- Behavioural or architectural decision logic inside content is considered a violation.
- If a conditional branch inside content affects ownership, lifecycle, orchestration, or protocol interaction, it is a violation.
