# Pattern Recognition Rules

A catalog of architectural patterns that must be recognized during analysis.

Each pattern describes: detection signals, architectural problem, canonical refactoring.

## Analysis protocol

Analysis is performed in two independent passes:

**Pass 1 — Code analysis**
Check each node for signals from groups A–G.

**Pass 2 — Spec analysis**
For each node that has a spec/prompt: read the description and verify — does the spec describe N distinct states of the node? If yes — verify that the code implements N explicit state children.

Both passes are mandatory. The absence of code signals (pass 1) does not exempt from spec analysis (pass 2). Platform mechanisms (CSS, system events) hide code signals but do not eliminate the architectural problem.

---

## Universal hidden-state signals

The following signals indicate that a node contains hidden state — regardless of the specific pattern.

### Group A — Visibility and style manipulation

- `el.style.display = 'none' / 'block'` — conditional hiding based on mode (not model data)
- `classList.add/remove/toggle` with names reflecting state (`active`, `hover`, `pressed`, `edit-mode`)
- `el.style.opacity`, `el.style.visibility`, `el.style.pointerEvents` — conditionally toggled
- `el.hidden = condition`

Important: if a style is set from model data (color from `data.color`) — this is not a violation. A violation is when a style reflects the mode or internal state of the node itself.

### Group B — Dynamic DOM manipulation

- `appendChild` / `removeChild` / `insertBefore` called inside `refresh()` — structure changes conditionally
- platform visual primitives created inside `refresh()` instead of the content materialization phase
- A node has two DOM elements with overlapping visual roles (`_viewEl` and `_editEl`, two sets of buttons)

### Group C — Internal state flags

- Field `_isHovered`, `_isPressed`, `_isExpanded`, `_isActive`, `_currentState` — the node tracks its own visual state
- Pattern `_listenersAdded = false` with a check before `addEventListener` — conditional handler registration
- Any boolean/enum field that changes rendering or behavior, not model data

### Group D — Dynamic handler registration

- `addEventListener` / `removeEventListener` called in `refresh()` — not during initialization
- One handler registered with different functions depending on mode
- Handlers for opposite sides of a state transition in the same node (see Pattern #2)

### Group E — Behavior-altering attributes

- `el.draggable = condition` — toggled in `refresh()`
- `el.disabled = condition`
- `input.readOnly = condition`

These are not model data. If they are toggled based on mode — this is hidden behavioral state.

### Group F — Structural branching in refresh()

- `if/else` in `refresh()` where branches change not data but visibility, structure, or available actions
- Different child nodes active in different branches

### Group G — Delegation to state objects (State pattern)

- Node stores a field `_state`, `_currentState`, `_strategy` — a reference to an object managing behavior or rendering
- Node delegates rendering, content materialization, or event handling to the state object
- Node switches the state object in `refresh()` or in response to events: `this._state = new HoverState(this)`
- State classes implement a common interface (render, activate, deactivate, etc.)

The State pattern does not eliminate the problem — it encapsulates it. Behavioral ownership remains hidden inside the node, lifecycle is implicit.

In TOP terms: if a node needs the State pattern — this is a signal that a switchable holder is needed with explicit state nodes as tree children, not objects inside a single node.

### Group H — Multiple states described in spec

A node has two or more mutually exclusive visual representations or sets of available actions, conditioned by any external context — regardless of the nature of that context or the mechanism for detecting it.

This signal does not require the presence of code indicators (groups A–G). It is detected through the node's spec/prompt.

Signal: the spec or prompt describes N distinct states of the node (normal/hover, normal/pressed, view/edit, expanded/collapsed, etc.).

Violation: the code does not implement these states as explicit state nodes — instead uses a platform mechanism (CSS, system events, animations) that is invisible to the code analyzer.

Important: the absence of code signals (groups A–G) does not mean the absence of a violation. The platform mechanism hides the problem but does not eliminate it.

### Combination rule

One signal — reason to be alert. Two or more signals simultaneously — high probability of a hidden switchable. The more groups affected, the higher the probability of a violation.

---

## Switching vs. dynamic composition

Before applying Pattern #1, verify which mechanism is architecturally correct.

A **hidden switchable** is a violation only when switching is the right choice.
If child nodes appear and disappear based on data or external configuration — that is
dynamic composition (add/remove), not switching. Applying the switchable refactoring
to a dynamic composition case is itself an architectural error.

See `rules/decision-trees.md` — **Decision tree: switching vs. dynamic composition**.

---

## Pattern #1 — Hidden switchable

### Definition

A node that independently manages switching between fundamentally different representations or behaviors by referencing external architectural state.

A hidden switchable may be monolithic — it may have no explicit child state nodes. It is recognized not by its child structure, but by the fact that it reads external mode and then changes its own state.

### Detection signals

Both conditions must hold simultaneously:

1. The node reads external architectural state:
   - `isEditMode`, `openedChild`, lifecycle phase, operating mode, etc.

2. And as a result changes at least one of:
   - visual representation of constituent elements (show/hide, swap, structural change)
   - available behavior (drag enabled/disabled, event handlers registered/removed, interactive elements appear/disappear)

### Not a violation

- The node only updates model data (label text, counter, color from data)
- Node behavior is the same in both states — only styling changes

### Architectural problem

- Hidden behavioral ownership: unclear who is responsible for drag, add, delete
- Hidden lifecycle: behavior activation/deactivation occurs implicitly through `refresh()`
- Violation of the principle: each node must have a clearly bounded role

### Canonical refactoring

The node becomes an explicit switchable holder. A separate state node is created for each mode.

```
Before (violation):
  TreeItemRowNode
    content materialization / refresh() → reads isEditMode
    → shows/hides DragHandle, AddBtn, DeleteBtn
    → enables/disables draggable and drag listeners

After (canonical):
  TreeItemRowNode  ← switchable holder
    ├─ TreeItemRowViewStateNode
    │    ├─ ToggleBtnNode
    │    └─ NodeLabelNode
    │    (drag is architecturally absent — not disabled, but non-existent)
    └─ TreeItemRowEditStateNode
         ├─ DragHandleNode
         ├─ ToggleBtnNode
         ├─ NodeLabelNode
         ├─ AddBtnNode
         └─ DeleteBtnNode
         (el.draggable = true, drag listeners registered here)
```

### State node rules

- ViewState is open by default
- EditState is activated via `onBranchOpen()` — not via `isEditMode`
- Each state node mounts its DOM on activation, unmounts on deactivation
- A state node **does not read** external mode — it **is** the representation of that mode
- Functionality absent in ViewState is not hidden — it architecturally does not exist in that state

### Agent chain for refactoring

```
Domain Structuring Agent
  → identify N states, extract holder, describe responsibility of each state node

TOP Modeling Agent
  → model holder + state nodes in the spec tree

Canon Precheck Agent
  → verify that state nodes do not read external mode
  → verify that holder does not duplicate an external mode holder

Generation Agent
  → implement

Validation Agent
  → verify: no state node accesses isEditMode or equivalent
```

---

## Pattern #2 — Behavioral coherence violation (contradicting handlers)

### Definition

A node that registers event handlers for opposite sides of the same state transition — thereby containing hidden internal state that should be represented by explicit state nodes.

### Detection signals

The node registers a pair of mutually exclusive handlers:

- `mouseenter` + `mouseleave` — cursor presence/absence
- `mouseover` + `mouseout` — same
- `pointerdown` + `pointerup` — press/release (if they manage different visual states)
- similar pairs with mutually exclusive preconditions

### Not a violation

- One node registers `pointerdown` + `pointerup` as the start and end of a single continuous action (drag): both handlers are active in the same node state.
- Handlers do not change visual representation or manage behavior — they only pass data upward.

### Architectural problem

- The node contains a hidden hover state (or press state): different visual representation depending on cursor position
- This violates the behavioral coherence principle: capability A (normal view) implies NOT-hover, capability B (hover view) implies hover — they are mutually exclusive

### Canonical refactoring

```
Before (violation):
  SomeNode
    content materialization →
      el.addEventListener('mouseenter', () => { this.el.classList.add('hover') })
      el.addEventListener('mouseleave', () => { this.el.classList.remove('hover') })

After (canonical):
  SomeNode  ← switchable holder
    ├─ SomeNormalStateNode
    │    (appearance without hover)
    └─ SomeHoverStateNode
         (appearance with hover)
         (activated via onBranchOpen on hover)
```

Real example: `TreeItemRowEditStateNode` has normal and hover sub-states.

### Agent chain for refactoring

```
Domain Structuring Agent
  → identify: which states are hidden inside the node (normal/hover, normal/pressed, etc.)
  → extract holder, describe responsibility of each state node

TOP Modeling Agent
  → model holder + state nodes

Canon Precheck Agent
  → verify that state nodes do not register mutually exclusive handlers

Generation Agent
  → implement

Validation Agent
  → verify absence of mouseenter/mouseleave pairs in the same node (except exceptions)
```
