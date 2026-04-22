# Forbidden Confusions

This file defines critical conceptual confusions that must never occur in TOP reasoning, modeling, generation, or validation.

## Core rule

If two concepts are explicitly separated in TOP, they must not be merged, blurred, or treated as interchangeable.

Any confusion listed below is considered a canonical violation.

---

## 1. Controller vs Content

- Controller owns behavior.
- Content is passive and has no architectural will.

Forbidden:
- assigning decision-making to content
- allowing content to manage lifecycle
- letting content control orchestration

### View encapsulation

Content exposes a view via `getView()`, which returns the most general view type possible.
The returned value is an opaque view handle for parent-owned materialization only.

- The node's view is private. Direct access to the view from outside is forbidden.
- The view-part builds only its own visual shell.
- If the view-part needs child visual content, it requests it only from its own controller via `IControllerAccess`.
- The controller itself retrieves `child.getView()` from the child node and returns the result to its own view-part.
- A parent may use a child view only as a placement/composition unit: mount, unmount, insert, reorder, replace, or pass into the parent's own content boundary.
- A regular visual node does not iterate `children` to build UI. Only explicitly declared named child-view endpoints are permitted.
- Dynamic repeated composition from an array of child nodes is only permitted inside a dedicated `DynamicCollectionViewNode`.

Forbidden:
- direct access from view/content to child nodes, `children`, or `openedChild`
- direct access to a child node's view bypassing `getView()`
- attaching event listeners to a child view obtained via `getView()`
- mutating styles/classes/attributes of a child view obtained via `getView()`
- querying inside a child view obtained via `getView()`
- using a child view's platform API as a behavior or communication channel
- self-mounting a child node into the parent view
- mixing static named slots and dynamic child collection in the same regular visual contract
- flattening dynamic descendants into the parent visual contract instead of a separate container node

---

## 2. Protocol vs Concrete Implementation

- Protocol defines allowed interaction.
- Implementation is hidden behind the protocol.

Forbidden:
- direct access to concrete implementation
- bypassing protocol for convenience
- exposing implementation details across boundaries

---

## 3. Canonical Architecture vs Working Code

- Canon defines valid structure.
- Working code only proves local functionality.

Forbidden:
- treating "it works" as "it is correct"
- accepting non-canonical structure because it compiles
- justifying violations by practicality

---

## 4. Lifecycle Ownership vs Local Convenience

- Lifecycle must be explicitly owned.
- Creation and destruction must be controlled.

Forbidden:
- hidden retention
- implicit lifecycle management
- leaving content alive "because it is easier"

---

## 5. Explicit Contract vs Implicit Access

- All boundaries must be explicit and typed.

Forbidden:
- implicit context objects
- shape-based access instead of contracts
- hidden coupling through shared state

---

## 6. Generation vs Architecture Design

- Modeling defines architecture.
- Generation implements it.

Forbidden:
- redesigning architecture during generation
- "fixing" structure implicitly in code
- introducing new ownership or boundaries at generation stage

---

## 7. Validation vs Commentary

- Validation is a strict pass/fail check.
- Commentary is descriptive.

Forbidden:
- replacing validation with opinions
- softening violations into suggestions
- skipping failed checks because the result looks reasonable

---

## 8. Repair vs Rewrite

- Repair is targeted correction.
- Rewrite is full replacement.

Forbidden:
- rewriting the entire structure without necessity
- destroying valid parts during repair
- masking inability to fix with full regeneration

---

## 9. Ambiguity Resolution vs Silent Assumption

- Ambiguity must be explicit.
- Assumptions must be declared.

Forbidden:
- silently choosing an interpretation
- hiding ambiguity behind conventions
- continuing pipeline with unresolved critical ambiguity

---

## 10. Typing vs Shape Approximation

- Typing must be explicit and strict where possible.

Forbidden:
- replacing explicit types with inferred shapes
- weakening contracts for convenience
- leaving boundaries untyped when typing is possible

---

## 11. Readability vs Brevity

- Code must be maximally understandable.

Forbidden:
- compressing names at the cost of clarity
- introducing non-obvious abbreviations
- prioritizing shortness over readability

---

## 12. Boundary vs Shortcut

- Boundaries must be respected.

Forbidden:
- bypassing content or protocol
- introducing backdoor access
- connecting components outside defined structure

---

## Final rule

If a decision or implementation relies on merging two separated concepts,
the result is non-canonical and must be rejected.

## Logic in content

- Content may only perform display-only logic.
- Display-only logic includes:
  - visibility toggles
  - styling decisions
  - formatting decisions
  - simple presentational branching that does not change behavior

- Logic in content is considered a violation if the branching:
  - makes behavioral decisions
  - changes orchestration
  - manages lifecycle
  - determines cross-boundary interaction
  - selects an architectural scenario based on state, props, or context

Forbidden:
- state-driven behaviour decisions inside content
- orchestration decisions inside content
- lifecycle decisions inside content
- protocol-routing decisions inside content

Clarification:
- `if` or `switch` by themselves are not a violation
- The violation is specifically behavioral or architectural decision logic inside content

---

## Self-validation vs external audit

Confusion: treating an agent's own assessment of its work as sufficient validation.

An agent cannot be the sole validator of its own output.
Confidence in a result is not the same as verified correctness.
An agent may be fully confident and still be wrong.

Self-reported completion must be confirmed by an independent step —
either another agent or a human reviewer.

Forbidden:
- accepting agent self-report as final validation
- treating high confidence as a substitute for audit
- skipping external audit because the result "looks correct"
---

## Semantic Layer vs Platform Implementation

Layer B describes meaning. Platform implementation describes one possible rendering or execution form.

Forbidden:
- treating DOM, CSS, Flutter widgets, UIKit/Android classes, framework APIs, or source event names as Layer B truth
- expanding semantic vocabulary with platform-specific primitive names
- preserving a source-platform mechanism when only its intent should be preserved

## Target Adaptation vs Source Truth

Layer C is derived and target-specific. It may guide generation for one target, but it is not the portable model.

Forbidden:
- treating Layer C as source truth
- copying Layer C decisions back into prompts, specs, or Layer B as portable requirements
- reusing one target adaptation as the adaptation for another target without a target-specific decision pass

## Semantic Interpretation vs Literal Translation

Semantic interpretation extracts intent. Literal translation copies implementation primitives.

Forbidden:
- renaming platform primitives without extracting user/system/interaction intent
- allowing generated code to define or rewrite Layer B semantics
- inventing behavior during adaptation that is absent from Layer B
