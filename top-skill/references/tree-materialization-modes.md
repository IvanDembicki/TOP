# Tree Materialization Modes

---

## Purpose

In TOP, the same tree can be used in different materialization modes.

Tree materialization refers to the manner in which the tree model is turned into
an actually working software structure.

TOP allows two equal materialization modes for a tree:

- `spec-first mode`
- `runtime-first mode`

These modes do not alter the fundamental principles of TOP.
They differ not in the system model, but in the moment and method of building the working tree.

---

## General principle

In both modes:

- the tree remains the canonical model of the system;
- parent-child relations are preserved;
- bidirectional typing is preserved;
- composition rules are preserved;
- the state model is preserved;
- branch rules are preserved;
- interfaces and connectors are preserved if needed.

The only difference is when and how the tree becomes a runtime structure.

---

## Spec-first mode

### Definition

`Spec-first mode` is a tree working mode in which the tree is first defined
as a formal description, and then the following are formed from it:

- `spec tree`
- `class tree`
- program code
- `instance tree`

In this mode, the tree description is the primary artifact, and code is
a derived representation of that structure.

### General sequence

Typical sequence of work in `spec-first mode`:

1. A tree description is formed.
2. A `spec tree` is built from it.
3. A `class tree` is formed from the `spec tree`.
4. Code is generated or regenerated from the `class tree`.
5. An `instance tree` is created at runtime.

### When this mode is particularly appropriate

`Spec-first mode` is particularly appropriate when:

- the system is designed top-down;
- strict structural consistency is required;
- AI code generation is heavily used;
- code needs to be quickly rebuilt after tree changes;
- edit-time control over architecture is important;
- the tree structure must be formally fixed before runtime.

### Advantages

Advantages of `spec-first mode`:

- the tree description becomes the single source of truth;
- code generation and regeneration are simplified;
- the architecture is easier to analyze automatically;
- the integrity of parent-child typing is easier to control;
- less need for runtime compromises and local workaround patterns;
- code is easier to synchronize with structural changes.

### Implementation notes

In `spec-first mode`, many structural constraints can be reflected immediately
in the generated code.

For example:

- the `parent` type can be generated correctly right away;
- allowed child types can be generated right away;
- many auxiliary typed accessors become not a required norm,
  but merely an optional technical technique.

In other words, in this mode it is preferable not to reconstruct typing
on top of already-written runtime code, but to generate it correctly
from the tree description from the start.

---

## Runtime-first mode

### Definition

`Runtime-first mode` is a tree working mode in which the tree is created
or reconstructed directly during program execution.

In this mode, the tree is materialized not through the prior construction of a complete
class tree and not necessarily through the prior generation of all code, but through
runtime construction.

### General sequence

Typical sequence of work in `runtime-first mode`:

1. During execution, data, commands, or another structural description arrives.
2. A runtime tree is built or reconstructed from it.
3. Nodes are created and linked directly at runtime.
4. The tree begins to function as an `instance tree`.

### When this mode is particularly appropriate

`Runtime-first mode` is particularly appropriate when:

- the tree is built dynamically;
- the tree comes from a server;
- the tree must be reconstructed on the client from runtime data;
- the technology or language does not assume prior generation of a complete `class tree`;
- runtime flexibility is the priority;
- part of the structure is not known in advance and is determined only during system execution.

### Advantages

Advantages of `runtime-first mode`:

- high runtime flexibility;
- ability to build the tree from external data;
- natural operation with server-driven structure;
- ability to materialize the tree only when it is actually needed;
- less dependency on a prior code generation phase.

### Implementation notes

In `runtime-first mode`, some things that are conveniently specified in advance in `spec-first mode`
may require additional runtime patterns.

For example:

- typing of `parent` and child relations may require additional
  validation mechanisms;
- helper patterns for typed access may be used;
- some constraints are controlled not by edit-time generation, but by runtime logic.

It is important to understand that such technical patterns are not the foundation of TOP,
but merely a way to implement the same tree model under runtime-first
materialization conditions.

---


## Application root and branch materialization policies

For an executable application, the top-level application root is normally materialized as the runtime composition root. During incremental migration or staged generation, a project may explicitly mark that root as pending, delegated, externally provided, or otherwise not yet materialized; the policy must make that status verifiable.

This does not mean that every child branch of that root must be materialized in the same way.

A branch may be materialized as runtime nodes, used as source/model input, used during generation, compiled into target-specific artifacts, provided by external infrastructure, or handled by another explicitly described project/target policy.

The list of branch materialization policies is open. Common examples include:
- runtime branch;
- source/model branch;
- generation-support branch;
- runtime-library-reference branch;
- target-optional runtime branch;
- target-compiled branch;
- externally provided branch;
- model-only branch.

`Library`, `Assets`, and `Presentation` are examples of branches that often use policies different from the main executable feature branch. They are not special hardcoded exceptions, and they are not the only possible branches of an application root.

A branch that is present in JSON but not materialized as runtime nodes is not drift by itself. It becomes drift only when the declared materialization policy says that the branch should be runtime-materialized, or when no policy exists and the surrounding docs/prompts imply runtime materialization.

Projects may record the branch policy in `props.materializationPolicy` or an equivalent project-local `props` field. The policy must be explicit enough for verification.
## Equality of modes

`Spec-first mode` and `runtime-first mode` are equal modes of TOP.

Neither cancels the other or makes the other mode "incorrect."

The choice between them depends on:

- platform;
- language;
- technology stack;
- source of the tree description;
- project priorities;
- exactly when the tree materialization must occur.

---

## What not to confuse

Do not confuse:

- `spec-first mode` and `runtime-first mode`
- with the tree's content type;
- with representation levels;
- with `state tree`.

These are different classification axes.

For example:

- a `*ui-tree*` can be materialized in either `spec-first mode` or `runtime-first mode`;
- a `*data-tree*` can also be materialized in either mode;
- a `state tree` can exist in either mode;
- `spec tree`, `class tree`, and `instance tree` are representation levels,
  not materialization modes.

---

## Practical difference

The difference can be summarized briefly:

- in `spec-first mode`, the description and code are formed first, then the runtime tree;
- in `runtime-first mode`, the tree is created or reconstructed directly during execution.

---

## Implications for code generation

In `spec-first mode`, code generation is typically a central part of the workflow.

In `runtime-first mode`, code generation may:
- be absent entirely;
- be used partially;
- be used only for base node classes;
- be combined with runtime construction.

Consequently, code generation in TOP is not a mandatory characteristic
of the paradigm as such.
It is one of the possible ways to implement the tree model.

---

## Implications for architecture analysis

When analyzing a TOP system, it is important to first determine in which materialization mode
the tree operates:

- `spec-first mode`
- `runtime-first mode`

Without this, it is easy to mistakenly treat runtime patterns as fundamental TOP principles,
or conversely, to treat code-generation assumptions as a mandatory part of any TOP system.

---

## Canonical rule

TOP allows both the edit-time construction of a class tree from a formal description
and the runtime-first construction or reconstruction of the tree during execution.

These modes are different ways of materializing the same tree model
and do not alter the fundamental principles of the paradigm.
