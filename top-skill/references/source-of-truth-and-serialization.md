# Source of Truth and Serialization

This document establishes rules for TOP systems in which:
- structure changes at runtime;
- a mutable tree exists;
- reverse serialization is required or may be required.

Especially important for editor-like systems.

---

## 1. The Core Question

For any mutable system, the following must be answered explicitly:

**Where is the authoritative source of truth?**

Without this, reliable analysis is impossible for:
- runtime edits;
- add/remove/reorder;
- drag&drop;
- rename;
- structural mutations;
- reverse serialization;
- sync between UI, runtime tree, and data model.

---

## 2. Possible Sources of Truth

Source of truth may reside in different layers.

### 2.1. Spec tree
The spec tree is the authoritative source.

Then:
- runtime structure is derived from spec;
- mutable edits are either forbidden or formalized as changes to spec;
- serialization back means updating the spec layer.

### 2.2. Raw data tree
The authoritative source is a raw data model, e.g. a JSON tree.

Then:
- runtime instances are derived from raw data;
- all structural edits must ultimately be reflected in raw data;
- the runtime tree is a derived layer.

### 2.3. Runtime instance tree
The authoritative source is the runtime tree itself.

Then:
- raw data may be absent or a secondary projection;
- serialization back is an export, not a primary mutation path;
- export policy must be described especially explicitly.

### 2.4. External/domain model
The authoritative source is an external model layer:
- domain entities;
- store/state manager;
- backend-backed model;
- command log;
- event-sourced model.

Then:
- the runtime tree and raw data may be mere representations;
- mutation policy is determined by the external model.

---

## 3. Mandatory Rule

In a mutable project, source of truth must not remain implicit.

The following must be defined explicitly:
- authoritative layer;
- derived layers;
- allowed mutation entry points;
- required reverse sync path, if needed.

---

## 4. Runtime Mutation Policy

For each type of runtime change, the following must be defined:

- where the mutation is initiated;
- which layer changes first;
- which derived layers must be updated;
- whether the operation is required to be reversibly serializable.

At minimum, this must be defined for:
- add child;
- remove child;
- reorder children;
- move subtree;
- rename/edit properties;
- switch state, if state affects serializable structure;
- drag&drop operations.

---

## 5. Serialization Policy

The following must be stated explicitly:

### 5.1. Immediate synchronization
Each runtime mutation immediately updates the source of truth.

### 5.2. Deferred synchronization
Runtime edits exist temporarily in isolation,
then are serialized on an explicit command:
- save,
- export,
- apply changes,
- commit.

### 5.3. One-way materialization only
The runtime tree is materialized from the source model,
but reverse serialization is not supported and not required.

### 5.4. Partial serialization
Only certain kinds of changes are serialized;
the rest are UI-only or session-only.

---

## 6. UI-only Runtime State

A distinction must be made between:
- structural/runtime edits;
- UI-only state.

Not everything that changes at runtime must be serialized.

Examples of UI-only state:
- expanded/collapsed;
- selection highlight;
- hover state;
- temporary focus;
- drag preview;
- scroll position.

Mixing the following is an error:
- runtime UI state,
- serializable structural state,
- domain data.

---

## 7. Editor-like Systems

For editors, serialization policy is a mandatory part of the model.

### Must be defined explicitly:
- what constitutes the editable structure;
- what is considered temporary UI state;
- which operations change the authoritative model;
- which operations are visual-only;
- how save/export works;
- how the structure is restored after reload.

### Typical operations requiring explicit description:
- add node;
- delete node;
- move node;
- reorder siblings;
- drag&drop;
- rename;
- property editing;
- structural wrap/unwrap;
- branch duplication.

If this is not captured, an editor almost inevitably begins living in two incompatible versions of truth:
- runtime version;
- saved/exported version.

---

## 8. Analytical Rule

When analyzing mutable TOP systems, always build a **source-of-truth map**.

At minimum it must contain:
- authoritative layer;
- derived layers;
- mutation entry points;
- reverse sync path;
- serialization boundaries;
- UI-only runtime layers.

---

## 9. What Counts as a Violation

### 9.1. Implicit source of truth
It is unclear where the authoritative truth resides.

### 9.2. Conflicting truths
Multiple layers behave as authoritative simultaneously,
but reconciliation rules are not described.

### 9.3. Runtime mutation without sync model
The runtime tree changes, but it is unclear:
- whether this should be persisted;
- where it is persisted;
- when it is persisted.

### 9.4. Serialization illusion
The system looks visually editable,
but most changes have no correct reverse path.

### 9.5. UI state mixed with structural data
Expanded/collapsed, selection, hover, and other UI states
are mixed with data that should be structural/domain truth.

---

## 10. What an Implementation Prompt Must Capture

If a node or branch participates in mutable behavior, the prompt should, where possible, explicitly state:
- where the source of truth is;
- who is authoritative;
- who is derived;
- which runtime operations must be serialized;
- which runtime operations are UI-only;
- what the sync/serialization policy is;
- whether replace/append semantics apply on re-init after mutation.

Otherwise, AI easily produces an editor that:
- works visually;
- but has no reliable save model.

---

## 11. Short Rule

If a system allows runtime edits, it must explicitly answer three questions:

1. Where is the truth?
2. Which changes are required to reach it?
3. When and how does that happen?

Without this, a mutable TOP system remains underspecified.
