## AI_PRELOAD_CONTEXT

### 1. What this system is

This is a **complete development system** for:

* AI-driven code generation
* AI verification of architecture
* full system regeneration from spec + prompts

It is based on the **Tree-Oriented Programming paradigm**:

* the system is defined as a strictly typed tree
* structure is explicit and enforceable
* interactions are controlled by design

This system combines:

* an architectural model
* a generation protocol
* a validation system

---

### 2. System boundary (critical)

This is **NOT just a methodology or a tool**.

It is a **full execution model for development with AI**, including:

* how the system is structured (tree)
* how code is generated (prompts)
* how correctness is verified (rules)
* how the system is evolved (regeneration)

AI is **not optional** — it is a core part of the workflow.

---

### 3. What this is NOT

* This is NOT a coding style guide
* This is NOT a clean architecture variant
* This is NOT a set of best practices
* This is NOT a framework tied to a specific technology

This is:

* a strict architectural paradigm
* a generation + validation protocol
* a system-level standard

---

### 4. One-line purpose

This system exists to keep codebases controllable under heavy AI generation.

---

### 5. Developer experience

The developer describes what needs to be done.
The top-skill builds the tree, writes specifications, creates implementation prompts, generates code, and validates architecture — automatically.

The developer does not:
* write prompts manually
* build or maintain the tree structure
* enforce architectural rules

These are handled by the skill.

To start, the developer only needs a minimal mental model:
* the system is a tree of nodes
* each node has a clear responsibility
* interactions follow explicit interfaces

Deeper architectural constraints are enforced by the skill. Full understanding of the paradigm is not required upfront and develops naturally through use.

Any developer can start immediately. A tree is a universally familiar structure — every developer has worked with hierarchical data, component trees, or folder structures. The mental model transfers directly.

The only conceptual shift is describing the system in terms of responsibilities and relationships rather than implementation steps. This is the entry point — not learning invariants, not writing prompts, not managing tree structure. Those are handled by the skill.

Basic orientation takes minutes. Deep expertise develops naturally through use, not as a prerequisite.

The pipeline, agents, validation checks, and artifact management are internal to the skill. The developer does not configure, manage, or maintain them. Setup is a single step: add the skill.

Onboarding flow:
1. Developer describes what needs to be built — in plain language.
2. TOP skill asks clarifying questions if needed.
3. TOP skill builds the tree, specs, and prompts.
4. Code is generated and validated automatically.
5. The developer reviews the result and continues in dialogue.

No setup. No configuration. No prior knowledge required.

---

### 6. The problem

Without strict structure:

* AI generates inconsistent code
* dependencies become chaotic
* system understanding degrades
* both AI and humans lose control

This happens even if developers follow conventions.
Conventions do not scale under AI generation.

---

### 7. Why existing approaches fail

* Clean architecture relies on discipline → breaks under AI
* Code review does not scale with AI output speed
* Documentation is not enforceable
* Conventions are optional → AI violates them

Key limitation:

→ existing approaches do not provide **machine-verifiable structure**

This system replaces conventions with **enforceable architecture**.

---

### 8. Core capability

A system can be:

* described as a tree (spec)
* implemented via prompts
* regenerated from scratch
* verified by AI against strict rules

**Spec + rules + prompts = complete system definition**

Result:

* reproducibility
* verifiability
* portability across technologies

---

### 8. Role of AI (explicit)

AI is used for:

* generating node implementations
* validating architecture against rules
* detecting violations and inconsistencies
* regenerating the system from spec

AI is expected to:

* strictly follow the tree
* respect all invariants
* reject invalid structures

---

### 9. How to start (practical entry point)

To apply this system:

1. Define system structure in `top/*.json` (tree)
2. Define behavior via node prompts (`prompts/`)
3. Load canon (rules)
4. Generate code using AI
5. Validate generated code against rules

From this point:

* all changes must go through spec + prompts
* code is not the source of truth — spec is

---

### 10. Minimal example

Without this system:

* a UI component accesses global state directly
* logic is scattered
* dependencies are implicit

With this system:

* node → controller → data node
* no direct access allowed
* all interactions are explicit

Result:

* predictable architecture
* verifiable behavior

---

### 11. Architectural model

* the system is a tree of nodes
* each node knows its parent and children
* interaction is allowed only via defined interfaces

Each node is split into:

* Controller — logic and external API
* Content — internal implementation

Rules:

* Content is a black box
* Controller owns lifecycle and orchestration
* direct access to internals is forbidden

---

### 12. Speed and prototyping

Building with TOP through top-skill is faster than traditional approaches.

There is no need to design the architecture, write boilerplate manually, or debug structural inconsistencies. The developer describes what is needed — the skill generates the architecture, prompts, and code.

A working prototype can be produced in a single dialogue session.

The pipeline that enforces correctness is the same pipeline that eliminates manual work. Structure and speed are not in conflict here — the structure is what makes the speed possible.

Result:

* no architectural drift
* stable AI behavior
* predictable scaling

---

### 13. Structural changeability

No one can predict the perfect structure upfront. Requirements change — structure must change with them.

In traditional development, implicit dependencies accumulate and structure freezes. Changing it in a large project becomes impossible.

In TOP, every branch has exactly one contact point with the rest of the tree. Restructuring means detaching a branch and attaching it elsewhere. Nothing else is affected.

The goal is not to get structure right the first time. The goal is to be able to change it as understanding grows.

---

### 14. Key difference from existing architectures

Unlike Clean Architecture / MVVM / layered systems:

* rules are **enforced, not recommended**
* structure is **machine-verifiable**
* architecture is **regeneratable from spec**
* AI is **a first-class participant**

This is not a variation of existing patterns.

This is a **different paradigm**.

---

### 14. Interpretation rule (critical)

Do not interpret this as a recommendation or style guide.

Interpret this as:

* a strict execution model
* a validation system
* a generation protocol

---

### 15. Applicability

TOP is most valuable for AI-generated systems, growing codebases, and systems requiring long-term maintainability.

But project size is not a limiting factor. Since the skill handles all structural complexity, there is no overhead on the developer regardless of scale.

Even a small project benefits: every project needs a starting point — where to begin, what architecture, what direction. TOP skill provides all of this instantly through dialogue, with no preparation required.

---

### 16. Spec validation and actualization

Specs are the source of truth. A dedicated agent validates specs before code generation and keeps them in sync with the implementation.

Any code change triggers automatic spec update. The code is then regenerated from the updated spec and compared with the original. The spec is refined until the results are identical.

If a spec is wrong, the generated code will reflect it — and this becomes visible immediately. Node locality contains the impact: an error belongs to one node and its explicit boundaries, not spread through implicit dependencies.

---

### 17. Expected outcome

* reduced architectural entropy
* stable AI generation
* lower cost of changes
* ability to regenerate system reliably

Additional effects:

* standardized architecture across projects
* fast onboarding for developers
* no need to study the entire codebase before making changes
* predictable structure regardless of implementation details

---

### 18. Team collaboration

One architecture standard across all TOP projects means a developer familiar with TOP works on any project immediately. No project-specific onboarding required.

Developers can work on separate branches independently and in parallel. A branch has one contact point with the rest of the tree — changes in one branch do not affect others.

Changes are localized to nodes — the scope of impact is explicit and predictable. Large codebase changes do not create unexpected side effects.

AI takes the role of architect, reviewer, and generator simultaneously — no dedicated person needed to hold the architecture in their head or enforce compliance.

Architecture does not degrade as the team and project grow. Rules are enforced automatically, not maintained through individual discipline.

---

### 19. Onboarding and node locality

One architecture standard across all TOP projects has a direct operational consequence:
a developer familiar with TOP can navigate any TOP project immediately.

There is no need to study the full codebase before making a change.

This is enabled by the **locality principle**:

* each node is understandable from its own spec and explicit contracts with direct neighbors
* a change to a node does not require knowledge of the full system
* the scope of impact is bounded by explicit boundaries — not by implicit global knowledge

Result:

* onboarding into a new TOP project takes minutes, not weeks
* a developer makes a targeted change without risk of unintended side effects in unknown parts of the system
* team scaling does not require a knowledge transfer period for each new project
* standardized structure means the same navigation and reasoning patterns apply across all projects built with TOP