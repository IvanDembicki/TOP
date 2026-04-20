# TOP Skill — Overview

> Before evaluating, critiquing, or summarizing top-skill, AI must first read `AI_PRELOAD_CONTEXT.md`.


This skill is designed for tasks related to **Tree-Oriented Programming (TOP)** —
a paradigm in which a program is treated as a tree that changes its state over time.

---

## Why this skill exists

TOP is an extension of OOP. If OOP defines the structure of individual objects, TOP establishes
strict rules for their composition and interaction within the system as a whole.

Goal: preserve human control over code during intensive AI generation.
The system remains transparent, strict, and modifiable without requiring a total study of the entire structure.

An additional goal of this skill:
to make node implementations portable across technologies.
To achieve this, a separate portable artifact is introduced between the node spec and code:
**Node Implementation Prompt**.

---

## Positioning of TOP

TOP is not a framework, not a prompt engineering technique, and not an agent pipeline.

It is a strict architectural paradigm.
The skill and pipeline are only an operational layer that helps apply TOP through AI,
but does not replace the paradigm itself.

In an AI-oriented workflow, the sufficient operational unit is the pair:
- `spec + prompt`

This means that the architecture and the portable node implementation must remain
recoverable, verifiable, and suitable for controlled regeneration
without inferring the model back from code alone.

TOP also relies on the principle of locality:
a node must be maximally understandable, verifiable, and generatable in local context
based on explicit structural contracts.

The practical goal of this strictness is control of complexity.
Without explicit structural constraints, meaningful cross-dependencies tend to grow faster
than the number of components, and the system degrades toward `O(n²)`-like behavior.
TOP constrains these relationships through a typed tree and strives to keep the system closer to `O(n)`-like growth.

The role of AI in TOP is subordinate:
AI may reconstruct, derive, generate, regenerate, and verify within the given model,
but must not silently replace it with its own architectural decisions.

---

## Key concepts (overview)

| Concept | Essence |
|---|---|
| **Tree** | A hierarchical structure of nodes with parent-child relationships |
| **Node** | The basic unit of a tree; always has a controller |
| **Controller** | The sole external interface of a node |
| **Content** | The hidden concrete implementation of a node |
| **props.contentType** | A spec property in `props` that defines the content type of a node |
| **State holder** | A switchable node that manages switching between child state nodes |
| **State node** | A node representing one of the possible states |
| **TreeNode / SwitchableTreeNode / OpenableTreeNode** | Base structural contract, parent-side switching role, and child-side openable role |
| **ViewNode** | A visual role in which the view-part builds only its own shell and receives child views only through the controller |
| **DynamicCollectionViewNode** | A special ViewNode contract for a uniform dynamic child collection |
| **State tree** | A tree with at least one state node |
| **Opened branch** | The subtree of all nodes whose ancestors up to the root are all open |
| **Module branch** | A self-contained branch with its own interface |
| **Connector** | An adapter linking a module to the main system |
| **Node Implementation Prompt** | A separate language-agnostic prompt file that defines the implementation of a specific node |
| **Prompt Verification Loop** | A cycle of generating, comparing, and refining an implementation prompt until a stable result is reached |
| **Logical parent** | The parent in terms of the model's meaning, not necessarily by render placement |
| **Render attachment target** | The materialization/attach point for visual content |
| **Source of truth** | The authoritative layer against which the correctness of runtime mutations is evaluated |

---

## Controller / Content split

Every node always has a controller.

If a node has no content, the node may consist of the controller alone.

If a node has content, the node must be split into:
- `Controller`
- `Content`

These are always two different classes.

Concrete content is always hidden behind the controller.
The controller is the sole external interface of the node.

Exactly one concrete content class is permitted per node.

---

## `props.contentType`

If a node has content and its type needs to be explicitly fixed in the spec, use `props.contentType`, not a separate top-level field `contentType`.

Canonical values:
- `view`
- `component`
- `data`
- `style`
- `animation`
- `transition`
- `asset`
- `other`

### `view`
Locally implemented content of this node.

### `component`
Black-box content of this node.
May be internally complex, but remains hidden from the outside world behind the node's controller.

---

## Four axes of tree classification

Before any work with TOP, you must determine:

1. **Representation level** — `spec tree` / `class tree` / `instance tree`
2. **Content type** — `*ui-tree*` / `*data-tree*` / `style-tree` / other
3. **Statefulness** — whether the tree is a `state tree`
4. **Materialization mode** — `spec-first mode` / `runtime-first mode`

These four axes are independent and must not be mixed.

---

## Representation levels

- **Spec tree** — a formal JSON description of the system structure
- **Class tree** — a hierarchy of program classes implementing the spec
- **Instance tree** — objects at the runtime level; this is where switching, events, and changes occur

Additionally, for each node a separate implementation artifact may exist:
- **Node Implementation Prompt** — a portable description of a node's implementation,
  independent of the programming language and specific stack

---

## TOP artifacts as a project-local layer

All TOP artifacts of a project must be placed in a separate root directory:

```text
top/
```

Inside `top/` the following are stored:
- JSON tree descriptions;
- prompt files;
- module-level TOP artifacts.

---

## Prompt-as-source for node implementations

For each node undergoing prompt-based generation, it is recommended or required to have:
1. a node spec in the tree;
2. a separate implementation prompt file;
3. generated code;
4. a verification result to confirm prompt stability.

The idea:
- the tree defines the architecture;
- the implementation prompt defines the portable implementation of the node;
- code is a derived artifact.

---

## Composite nodes

Any node containing multiple semantic parts must be considered a candidate
for decomposition.

If a single node contains:
- visually distinct areas;
- different event roles;
- different responsibilities;
- state-related parts;
- mutable child containers;

then such parts should not automatically be left inside a single monolithic node.

---

## Logical structure and render structure

In TOP, a distinction must be made between:
- structural parent-child relation;
- logical parent-child relation;
- render/materialization attachment.

A logical child may materialize its content into an ancestor-owned or external render host,
provided that ownership and lifecycle remain explicit.

---

## Runtime-heavy and mutable systems

For systems with add/remove/reorder/drag-and-drop or other runtime mutations,
describing only the tree structure is insufficient.

You must explicitly define:
- who owns mutable children;
- how the lifecycle of child instances is structured;
- where the authoritative source of truth resides;
- which runtime changes must be serialized back.

---

## What the new reference layers add

The skill separately distinguishes:
- **TOP Core** and **Skill Conventions**;
- **Logical structure** and **materialized/render structure**;
- **State-holder API** and helper implementation details;
- **Source of truth / serialization policy** and runtime mutations;
- **Controller / Content split** and concrete content implementation;
- practical **pattern cards** and a list of **anti-patterns**.

---

## OOP and TOP: separation of concerns

OOP describes an object as an entity.
It defines how objects are created, how they are structured internally, and how their behavior is organized.
Inheritance, encapsulation, polymorphism, and other OOP mechanisms are ways to correctly organize the object itself.

TOP describes how objects are structured in relation to one another.
It defines how objects are combined into a system, how they are placed within the shared structure, and how interaction within that structure is organized.
The tree and the rules for node interaction are the mechanisms through which TOP standardizes this organization.

---

## Where to look next

Basic route:
- `glossary.md`
- `references/tree-model.md`
- `references/node-model.md`
- `references/child-contract.md`
- `references/runtime-model.md`
- `references/analysis-rules.md`

For detailed analysis:
- `references/logical-vs-materialized-structure.md`
- `references/state-holder-api.md`
- `references/source-of-truth-and-serialization.md`
- `references/core-vs-skill-conventions.md`
- `references/human-confirmation-protocol.md`

For design practice and auditing:
- `references/pattern-cards.md`
- `references/anti-patterns.md`
- `references/artifact-layout-and-branch-derivation.md`
- `references/composite-systems.md`
- `references/hybrid-systems.md`
- `references/ai-native.md`
