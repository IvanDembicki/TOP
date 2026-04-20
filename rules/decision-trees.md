# Decision Trees

This file defines mandatory decision logic for agent transitions and TOP workflow choices.

## Global rule

Decision logic must follow canon and validation rules.
No decision may be justified by convenience, brevity, familiarity, or local functionality.

## Decision tree: task entry

1. Is the task type explicit?
   - yes -> continue
   - no -> route to `Intake Agent`

2. Does the task contain critical ambiguity?
   - yes -> route to `Ambiguity Resolver Agent`
   - no -> continue

3. Is the domain already structured?
   - yes -> route to `TOP Modeling Agent`
   - no -> route to `Domain Structuring Agent`

## Decision tree: pre-generation

1. Does a TOP model exist?
   - no -> generation is forbidden
   - yes -> continue

2. Has the TOP model passed canon precheck?
   - no -> route to `Canon Precheck Agent`
   - yes -> continue

3. Has platform-neutral semantic interpretation produced Layer B?
   - no -> route to `Semantic Interpreter Agent`
   - yes -> continue

4. Has target adaptation produced Layer C for the active target?
   - no -> route to `Target Adaptation Agent`
   - yes -> continue

5. Does the model contain unresolved architectural or semantic ambiguity?
   - yes -> route to `Ambiguity Resolver Agent`
   - no -> generation may proceed

## Decision tree: post-generation

1. Has Spec Sync been performed after generation?
   - no -> route to `Spec Sync Agent`
   - yes -> continue

2. Has validation been performed?
   - no -> route to `Validation Agent`
   - yes -> continue

3. Did validation pass all required checks?
   - no -> route to `Repair Agent`
   - yes -> continue

4. Has final audit been performed?
   - no -> route to `Final Audit Agent`
   - yes -> ready for delivery

## Decision tree: ambiguity handling

1. Is the ambiguity semantic only and non-architectural?
   - yes -> document it and continue if safe
   - no -> continue

2. Does the ambiguity change ownership, boundaries, lifecycle, typing, or protocol structure?
   - yes -> task is blocked until resolved
   - no -> continue with explicit note

3. Can the ambiguity be resolved from canon, contracts, or existing project context?
   - yes -> resolve explicitly and continue
   - no -> keep unresolved and block the affected stage

## Decision tree: repair loop

1. Did validation identify concrete violations?
   - yes -> repair only those violations and revalidate
   - no -> do not perform speculative repair

2. Does the repair change architecture rather than implementation detail?
   - yes -> return to `Canon Precheck Agent`
   - no -> did the repair change any synchronized artifact (src/, generated artifacts, JSON specs, prompts, top/assets/, top/presentation/, top/semantic/, top/adaptations/)?
     - yes -> route to `Spec Sync Agent` before `Validation Agent`
     - no -> return to `Validation Agent`

3. Does repair require new assumptions?
   - yes -> route to `Ambiguity Resolver Agent`
   - no -> continue

## Decision tree: finalization

1. Have all required stages completed?
   - no -> finalization is forbidden
   - yes -> continue

2. Do any canonical violations remain?
   - yes -> finalization is forbidden
   - no -> continue

3. Is the result merely functional but not architecturally canonical?
   - yes -> finalization is forbidden
   - no -> result may be finalized

## Task complexity tiers

### Tier 1 — simple change (leaf level)
Examples:
- adding a leaf node
- changing a single property
- a local fix without structural changes

Pipeline:
- Intake
- Canon Precheck (lightweight)
- Semantic Interpreter
- Target Adaptation
- Generation
- Spec Sync
- Validation
- Final Audit

Requirements:
- a simplified checklist is permitted
- domain structuring and full modeling are not required

---

### Tier 2 — subtree change

Examples:
- changing a group of related nodes
- changing local interaction logic
- adding a new component

Pipeline:
- Intake
- Ambiguity Resolver (if needed)
- Domain Structuring
- TOP Modeling
- Canon Precheck
- Semantic Interpreter
- Target Adaptation
- Generation
- Spec Sync
- Validation
- Final Audit

---

### Tier 3 — full system design

Examples:
- designing a new system
- changing core architecture
- changing ownership / boundaries

Pipeline:
- the full generation-pipeline from `agents/index.md` is mandatory, including Semantic Interpreter and Target Adaptation before Generation

---

## Decision tree: switching vs. dynamic composition

1. Does the node own one active/opened child selected from a candidate child set?
   - no → use add/remove or another dynamic composition pattern
   - yes → continue

2. Is the candidate set fixed by architecture?
   - yes → use fixed switchable if candidates represent mutually exclusive states/representations of the same owner
   - no → continue

3. Is the dynamic candidate set explicit, typed, and governed by a source-of-truth and creation/removal policy?
   - no → the model is incomplete; define child policy before choosing the pattern
   - yes → continue

4. Does selection among candidates follow the canonical lifecycle-consistent switching path?
   - no → use mutable collection/single-child mutable or repair the lifecycle model
   - yes → use dynamic switchable

5. If the currently opened child is removed, is fallback/null/empty-state behavior explicit?
   - no → the model is incomplete
   - yes → dynamic switchable is valid

**Core rule:** switching is defined by owner-managed active/opened selection and lifecycle-consistent transition. The candidate set may be fixed or dynamic. Add/remove without active/opened selection is dynamic composition, not switching.

---

## Decision tree: tier selection

Use this tree to determine the proposed tier algorithmically. Do not rely on example analogy alone.

1. Does the task change any of the following: ownership, protocol boundaries, lifecycle ownership, controller/content split, or tree structure?
   - yes → Tier 3

2. Does the task affect more than one node?
   - no → Tier 1

3. Does the task change interaction logic between nodes?
   - yes → Tier 2
   - no → Tier 1

Note: this tree produces `proposed_tier`. Effective tier is confirmed by Canon Precheck Agent.

---

## Rules

- Intake Agent only proposes Tier; effective Tier is confirmed by Canon Precheck Agent
- Tier must be stated explicitly
- Tier selection requires justification using the decision tree above
- Downgrading Tier (e.g. Tier 3 → Tier 1) is a violation

## Tier 1 pipeline clarification

Tier 1 is not exempt from precheck.

Tier 1 uses `Canon Precheck (lightweight)`.

Tier 1 pipeline:

- Intake
- Canon Precheck (lightweight)
- Semantic Interpreter
- Target Adaptation
- Generation
- Spec Sync
- Validation
- Final Audit

### Lightweight precheck rules

Lightweight precheck must verify that the task does NOT change:

- ownership
- protocol boundaries
- lifecycle ownership
- controller/content split
- tree structure

If any of these points are affected:
- Tier 1 is considered invalid
- the task must be escalated to at least Tier 2
- `Generation Agent` cannot continue working within Tier 1

## Tier-aware pre-generation gate

0. Is this a Tier 1 task?

- yes and lightweight precheck passed →
  route to Semantic Interpreter; generation is allowed only after Target Adaptation

- yes and lightweight precheck not passed →
  route to Canon Precheck (lightweight)

- no →
  continue standard pre-generation tree
