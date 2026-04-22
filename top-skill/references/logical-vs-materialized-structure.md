# Logical vs Materialized Structure

This document captures the distinction between:
- **logical structure**;
- **materialized structure**;
- **render attachment**.

This distinction is required for correct analysis of runtime-first and mixed TOP systems.

---

## 1. Core Idea

In TOP, the logical tree and the visual/render structure do not have to coincide literally.

A node may:
- be the logical child of one parent;
- materialize its content in the host of a different node;
- participate in a runtime/render structure that does not map 1:1 to the logical tree.

This is not itself a violation of TOP, provided:
- logical ownership remains explicit;
- parent-child semantics are not lost;
- render attachment is explainable and consistent with the model.

---

## 2. Definitions

### 2.1. Logical parent
`Logical parent` — the node to which a child belongs according to the tree model's semantics.

The logical parent is the one that:
- determines structural ownership;
- determines child composition;
- determines the semantic position of the child in the system.

### 2.2. Structural parent
`Structural parent` — the parent in the tree hierarchy.

In most cases it coincides with the logical parent, but the term is useful
when tree-level ownership specifically needs to be emphasized.

### 2.3. Materialization parent
`Materialization parent` — the node relative to which a child is materialized at runtime.

It may or may not coincide with the logical parent.

### 2.4. Render attachment target
`Render attachment target` — the specific render host / container / DOM host /
view host into which a child attaches its materialized content.

This is the most concrete level of attachment.

---

## 3. Canonical Rule

A node may be the logical child of one parent but materialize content into the render host of a different ancestor node, provided:
- logical tree relations are explicitly recoverable;
- semantic ownership is not lost;
- this does not turn the structure into an implicit graph;
- render attachment follows an understandable model.

---

## 4. What Is Not a Violation

The following cases are not violations in themselves:

### 4.1. Skipping a logical node at render attachment
If a logical/state node has no render host of its own,
a child may attach to the host of an ancestor node.

### 4.2. A node without its own `el` / view host
A state node or purely structural node may:
- exist in the logical tree;
- participate in state/lifecycle semantics;
- have no visual container of its own.

### 4.3. Shared host belonging to an ancestor node
Multiple logical descendants may materialize content into a host
belonging to an ancestor node, provided ownership remains explicit.

### 4.4. Runtime-first rendering
In runtime-first systems, the actual visual tree may be the result of
runtime materialization and is not required to mirror the logical structure literally.

---

## 5. What Is Already a Violation

The following cases should be considered architecturally suspect or erroneous:

### 5.1. Loss of logical ownership
If after materialization it is impossible to determine who the logical parent is,
this is a violation or at minimum a severe ambiguity.

### 5.2. Render placement substituting semantic ownership
If a child is considered to belong to the node whose host it uses,
solely by virtue of attachment, this is an interpretation error.

### 5.3. Implicit graph through hosts
If render hosts create a hidden network of dependencies that cannot be
explained by the tree model, the system drifts into a graph-like structure.

### 5.4. Attachment without a model
If a child attaches "anywhere" without an explainable rule,
this is a violation of materialization discipline.

---

## 6. How to Analyze Such Cases

During analysis, three layers must be explicitly reconstructed:

1. **Logical structure**
   - who is whose child;
   - who owns child semantics;
   - where structural ownership lies.

2. **Materialization structure**
   - through whom a child is materialized;
   - what runtime path creates the instance/view/content.

3. **Render attachment structure**
   - into which host the content ends up;
   - who is actually the visual/render container.

These three layers cannot automatically be assumed to be identical.

---

## 7. Practical Formulation for Analysis

If a node is:
- logical child of `A`,
- materialized through a runtime path passing through `B`,
- attaches content into the host of node `C`,

the analysis must:
- preserve `A` as logical parent, if this matches the tree model;
- separately record the materialization path;
- separately record the render attachment target `C`.

---

## 8. Consequence for the Prompt Layer

If logical structure and render attachment diverge, the implementation prompt
should, where possible, explicitly capture:
- who the logical parent is;
- who the render host is;
- the attach model;
- the lifecycle semantics of the child node.

Otherwise there is a high risk that the next AI will:
- confuse visual placement with structural ownership;
- incorrectly "fix" a valid runtime-first model;
- destroy tree semantics.

---

## 9. Consequence for Runtime Design

During design, avoid situations where:
- render attachment is the only way to understand ownership;
- the logical tree exists only "in the author's head";
- lifecycle depends on implicit host assumptions.

Ideally, logical ownership should be recoverable without analyzing the DOM.

---

## 10. Short Rule

**Logical child** and **render-attached descendant** are not the same thing.

A child may be:
- a logical descendant of one node;
- a render-attached descendant of a different node.

This is acceptable, provided:
- tree semantics remains explicit;
- ownership is not lost;
- the materialization model remains explainable and disciplined.
