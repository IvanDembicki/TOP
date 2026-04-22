# Core Principles of TOP

This document lists the fundamental principles of Tree-Oriented Programming
that must not be violated regardless of the type of task.

---

## 1. A Program Is a Tree

The entire system is described as a tree of nodes with a strict hierarchy.
Not a graph, not a flat set of objects, not a list of components — specifically a tree.

If cross-references arise in the system that violate the tree structure,
this is an architectural violation and requires explicit justification or refactoring.

---

## 2. Strict Bidirectional Typing of Relations

Every parent-child relation is typed in both directions:
- a child node declares the permissible type of its parent;
- a parent node declares the permissible types of its child nodes.

A relation is valid only when both requirements are mutually satisfied.
This ensures the predictability of the structure and allows it to be analyzed statically.

---

## 3. Four Independent Classification Axes

Any tree in TOP is described along four independent axes:

- **Representation level**: `spec tree` / `class tree` / `instance tree`
- **Content type**: `*ui-tree*` / `*data-tree*` / `style-tree` / other
- **Statefulness**: whether the tree is a `state tree`
- **Materialization mode**: `spec-first mode` / `runtime-first mode`

Mixing these axes is not permitted.

---

## 4. Three Representation Levels

One and the same system exists simultaneously at three levels:

- **Spec tree** — a formal JSON description; defines the structure and rules
- **Class tree** — implementation in source code
- **Instance tree** — runtime objects, materialized in memory

These levels must not be confused.
For example, runtime state cannot be directly substituted by reasoning about the spec tree.

---

## 5. Node — the Minimal Unit of Composition

A program is built not from functions and not from screens, but from nodes.

A node:
- occupies a position in the tree;
- has a semantic role;
- has parent-child relations;
- can own state;
- can materialize content;
- can delegate part of its render/materialization behavior.

---

## 6. State Through Tree Structure

System state is not stored in arbitrary flags and variables.
It is determined by the configuration of the tree:
- which nodes are opened;
- which branch is opened;
- what the current tree structure is.

A state holder manages switching through child state nodes.
Switching must proceed through a single lifecycle-consistent path.
The specific form of entry may vary:
- `child.open()`
- `holder.openChild(child)`
- another equivalent mechanism, if it leads to the same canonical switching path

Direct public assignment to `openedChild` as an independent alternative API path must not introduce separate switching semantics.
For normative details of the canonical switching path, see `state-holder-api.md` and `tree-node-contracts.md`.

---

## 7. Isolation Through Parent-Child Discipline

Nodes interact only within strict rules:
- a parent manages child nodes;
- sibling nodes interact only through the interface of the common parent type;
- remote nodes are not accessible via hardcoded navigation chains.

---

## 8. State Belongs to the Owner Node

State belongs to the node that conceptually manages the corresponding entity.

Not necessarily:
- a button,
- a toggle,
- a tab bar,
- another control element

that merely visually reflects or switches state.

A control may initiate a change, but the state owner is determined by the tree architecture.

---

## 9. Composite Nodes Must Be Decomposed by Meaning

If a node contains multiple semantic parts, it must not automatically be treated as monolithic.

If a node contains:
- different areas of responsibility;
- different parts of the UI;
- independent events;
- separate states;
- child containers;

then such parts must be identified and, where possible, extracted into child nodes.

---

## 10. Logical Structure Takes Priority Over Visual Placement

Logical ownership and render placement must not be mixed.

A node can be the logical child of one parent, but materialize its content
in the render host of another node or ancestor, provided that:
- tree relations remain clear;
- lifecycle is not lost;
- ownership remains unambiguous.

DOM placement does not override tree semantics.

---

## 11. Mutable Child Composition Requires an Explicit Policy

If a node can create, delete, replace, or reorder children,
this must be explicitly described.

It must be clear:
- which child policy is used;
- whether `childrenType` is needed;
- who owns the child instances;
- what the re-init semantics are;
- what the source-of-truth policy is.

Otherwise, mutable behavior becomes unanalyzable.

---

## 12. The Prompt Layer Does Not Substitute Architecture

Implementation prompts are useful for code generation,
but do not define architecture on their own.

The authoritative source of architectural truth must remain in the tree model and related spec artifacts.

The prompt layer must:
- follow the tree model;
- not break semantic decomposition;
- not substitute state ownership;
- not distort the materialization mode.

---

## 13. Terminological Rigor

The canonical terminology from the root `glossary.md` of the skill is used.
In case of term conflict: root `glossary.md` → `paradigm.md` → domain-specific reference documents.

---

## 14. Composite Nodes Are Decomposed

Any node containing multiple parts must be broken down.

Every element with:
- behavior
- events
- state
- a distinct role
- independent visibility

must be a separate child node.

---

## 15. Architecture Takes Priority Over Convenience of the Current Implementation

Violations of the tree model cannot be justified by the fact that it is easier to implement
in a specific framework or faster to write code.

If the implementation requires:
- graph-like relations;
- global variables instead of owner state;
- mixing logical ownership and visual placement;
- implicit mutable children;
- lifecycle bypass;

this is a reason to change the implementation, not to dilute TOP principles.
