# Paradigm Definition

## Definition

Tree-Oriented Programming (TOP) is a strict architectural paradigm in which a
software system is organized as a typed tree of nodes with explicitly defined
composition rules, ownership rules, and interaction boundaries.

TOP is not a framework and not a prompt orchestration technique.
It is the architectural model itself.

## Mandatory interpretation

In TOP:

- tree is the mandatory form of system organization;
- architectural structure must be reconstructed before implementation;
- node boundaries must be explicit;
- allowed relations must remain structurally constrained;
- AI may execute, derive, regenerate, and verify within the model,
  but must not silently replace the model with its own architectural choices.

## What is primary

The primary layer in TOP is not code.
The primary layer is the formal architectural structure.

At minimum, this includes:

- typed node composition;
- explicit parent-child discipline;
- explicit state ownership;
- explicit behavioral and interaction boundaries;
- explicit interface/content separation where node modeling requires it.

## Spec + Prompt as a sufficient unit

For AI-oriented workflows, `spec + prompt` form a sufficient unit for:

- regeneration;
- verification;
- architectural continuity;
- controlled evolution.

This does not mean the prompt layer replaces the paradigm.
It means the paradigm becomes operationally executable through AI.

## Locality claim

TOP is built around locality.

A node should be understandable, generatable, and verifiable with mostly local
context plus explicit structural contracts.
If the system can only be reasoned about as a hidden graph of global knowledge,
its TOP structure is either missing or broken.

## Complexity claim

The central practical goal of TOP is not stylistic purity.
Its goal is complexity control.

Without strict structural constraints, cross-dependencies tend to grow faster
than the number of components, pushing the system toward `O(n²)` behavior.

TOP limits this growth by enforcing locality, typed composition, and explicit
structural boundaries, pushing the system toward `O(n)`-like scaling.

## Distinction from neighboring concepts

TOP is not equivalent to:

- OOP;
- DDD;
- Clean Architecture;
- a UI tree framework;
- a code generation pipeline;
- prompt engineering.

These may coexist with TOP, but they do not define it.

## Human and AI roles

In TOP, the human remains responsible for architectural decisions and for the
validity of the paradigm-level model.

AI is allowed to:

- derive structure from inputs;
- generate artifacts from defined structure;
- verify artifacts against canonical rules;
- regenerate artifacts after prompt or spec changes.

AI is not allowed to:

- replace tree discipline with hidden graph logic;
- reinterpret optional convenience as architectural freedom;
- silently invent architecture where the model is absent.
