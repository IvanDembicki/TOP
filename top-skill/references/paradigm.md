# Tree-Oriented Programming (TOP)

## Goal and Motivation

The AI context window grows. The human context window does not.
But decisions are made by humans — and humans bear the responsibility.
Therefore, a program must be understandable to humans.
TOP makes a system understandable to humans and simultaneously verifiable by AI.

The goal of Tree-Oriented Programming is to preserve human control over code in the era
of mass AI-generation.

When using TOP and developing within this paradigm, even with intensive AI-assisted code
generation, the system remains transparent, comprehensible, and easy to modify — it does not
require a complete study of the entire structure for local changes, and does not degrade into
spaghetti code.

TOP is aimed at unifying the structure of software systems both within individual companies and
across the industry as a whole. It defines a single way of representing a program and uniform
rules for composing its parts, which simplifies collaboration between developers and accelerates
onboarding into new projects.

Another important goal of TOP is to raise the level of abstraction, at which a system is
described primarily as a tree, and code becomes a derived representation of that structure
that can be translated for various platforms and programming languages.

---

## Definition

**Tree-Oriented Programming (TOP)** is a programming paradigm that extends OOP. While OOP defines the structure of individual objects, TOP establishes strict rules for their composition and interaction within the system as a whole.

In TOP, a program is viewed as a tree that changes its state over time.

Within TOP, a program and all its parts are conceived, described, and developed as elements
of a tree: nodes, branches, and their relations. This defines not only the structure of the system,
but also the developer's way of thinking — the program is perceived as a single hierarchical structure.

The tree in TOP is not static. It can change its state, and it is precisely the change of the
tree's state that makes it a program rather than merely a data structure.

The current state of the tree is determined by:
- state nodes;
- opened nodes;
- the current opened branch;
- and, when necessary, changes to its structure at runtime —
  adding and removing nodes and subtrees.

Thus, a program in TOP is not simply a tree, but a tree that can exist in
various states and transition between them.

The interaction of nodes in TOP follows strict rules and constraints that define
the permissible ways of navigating and exchanging data within the tree. These rules are
an integral part of the paradigm and ensure the predictability of system behavior and the
isolation of its parts.

---

## Representation Levels

TOP distinguishes three levels of tree representation.

**Spec tree** — the tree is defined formally, for example as a JSON document. It defines
the structure of the system, the permissible node types, and possible configurations. Each node
at this level is a node spec.

**Class tree** — the tree is represented as a hierarchy of classes corresponding to the spec. This
level reflects the structure defined in the spec tree and likewise remains structurally stable.
Each node at this level is a node class.

**Instance tree** — the tree is represented as objects at the execution level (`runtime`). At this
level, the actual work of the system takes place: switching states, handling events, and, when
necessary, changing the tree's structure — adding and removing nodes. Each node
at this level is a node instance.

Thus, one and the same system exists simultaneously as a spec tree, as a class tree,
and as an executable instance tree.

---

## Tree Materialization Modes

TOP supports two equally valid modes of working with a tree: `spec-first mode` and
`runtime-first mode`.

In `spec-first mode`, the tree is first defined as a formal description, after which
the class tree, code, and runtime structure are formed based on it.

In `runtime-first mode`, the tree is created or restored directly at
runtime, for example from server data or other runtime sources.

Both modes represent different ways of materializing the same tree model
and do not change the fundamental principles of TOP.

---

## State Model

One of the key properties of TOP is the representation of state through the tree structure.

During execution, a program can exist in various states. The number of such
states is potentially unlimited. However, the entire space of possible states can be
described by a finite tree structure.

A state holder is a switchable node that manages child state nodes and switching between
them: at any given moment, only one of them is opened. A state holder defines the permissible
state configurations of the corresponding part of the system.

The current state of the system is determined by the current configuration of the tree — which nodes
are opened, which branch is opened, and what changes have occurred in the tree structure itself.

State changes occur through:
- switching between child nodes;
- opening nodes;
- opening the entire branch to root via `openBranch()`;
- changing the tree structure.

Thus, the tree describes the space of possible system states, while the specific
configuration of the tree at any given moment determines its current state.

---

## State Tree

A state tree is a tree that contains at least one state node.

Thus, a state tree is not a separate specialized kind of tree, but a
characteristic of a tree. Any tree can be a state tree if it
contains at least one state node.

This means that:
- a *ui-tree* can be a state tree;
- a *data-tree* can be a state tree;
- other specialized trees can also possess this property.

Previously, state tree could be understood as the tree of the user interface and its
states. However, such an understanding is a special case. To eliminate ambiguity,
a tree describing the user interface should be identified as a separate type —
*ui-tree*.

---

## State Node

A state node is a tree node representing one of the possible states of an element,
component, or larger part of the system.

For example:
- `SendButton` (state holder) may contain state nodes `Normal`, `Hover`, `Down`, `Disabled`;
- `UploadPage` (state holder) may contain state nodes `InputForm`, `Loading`, `Loaded`, `Error`.

A state node in the description and a state node in the implementation represent the same
structural entity at different levels of representation.

In a software implementation, a state node is a derived implementation of its description and
may include:
- controller;
- content;
- references to parent and child nodes.

Controller:
- contains the state logic;
- manages child nodes;
- manages the node's interaction with the external system;
- encapsulates `content` and restricts access to it.

Content:
- represents the substantive part of the node;
- can be represented as:
  - a `view` for nodes of a *ui-tree*;
  - data for nodes of a *data-tree*;
  - styles or other content types;
- is not directly accessible from outside and is used through the controller.

References to parent and child nodes:
- define the node's position in the tree;
- enable navigation through the tree structure;
- are used by the controller for management and interaction between nodes.

---

## Tree Structure and Dynamics

In TOP, a tree simultaneously possesses two properties:
- at the description and architecture level, it is strictly defined and stable;
- at the runtime level, it can change.

The tree description defines the permissible structure of the system, node types, and rules for
their composition. This structure is the foundation of the entire system and does not change
during program execution.

At the same time, at the `runtime` level, the tree can change within the defined constraints:
- nodes can be added;
- nodes can be removed;
- branches can be restructured.

Such changes do not violate the overall architecture, since they occur within the bounds
of the predefined description.

---

## Compatibility and Incremental Adoption

TOP does not require the entire system to be implemented exclusively within this paradigm.

Individual parts of a program can be implemented using TOP and coexist with
components written in other styles. A branch of the tree may terminate with a component not
implemented in TOP, and conversely, individual components implemented within TOP can be
used outside the tree.

This makes incremental adoption of TOP possible. A system can be migrated to this approach
in parts without losing operability or testability.

---

## OOP and TOP: Separation of Concerns

OOP describes the object itself.
TOP describes the structural relations between objects.

OOP provides mechanisms for organizing an object.
TOP provides mechanisms for organizing objects into a single structured system.

---

## Summary

Tree-Oriented Programming represents a program as a tree with a formally defined structure and
a dynamically changing state.

This approach makes it possible to:
- strictly define the system's architecture;
- standardize the interaction between its parts;
- isolate complexity;
- increase the predictability of changes;
- maintain control over the system under conditions of intensive AI use.

See `references/ai-native.md` — TOP as AI-native architecture and portability through AI artifacts.
