# Runtime Model

Rules for describing and analyzing runtime behavior in TOP systems.

The runtime model describes not the tree as such, but the behavior of an already materialized
or materializing system:
- creation of runtime instances;
- re-initialization;
- state switching;
- mutable child lifecycle;
- render/materialization attachment;
- the relationship between runtime mutations and the source of truth.

---

## 1. What belongs to the runtime model

The runtime model includes:
- instance creation;
- lifecycle methods;
- materialization order;
- state transitions;
- mutable child creation/removal;
- re-initialization behavior;
- render attachment behavior;
- serialization back to the authoritative model, if required.

The runtime model does not replace the tree model.
The tree model must be restored first; only then is runtime behavior analyzed.

---

## 2. Runtime methods must have explicit semantics

If a node uses methods such as:
- `init`
- `reset`
- `mount`
- `materialize`
- `rebuild`
- `open`
- `close`

then the semantics of each method must be explicitly defined.

Permitted base variants:
- **replace** — the old state/content is removed and recreated;
- **append** — new content is added to what already exists;
- **merge** — the existing state is partially reused and partially updated;
- **guarded no-op** — a repeated call is permitted, but does nothing once the state has already been reached.

Implicit semantics is considered a runtime model defect.

---


## 2.1. Strict purpose of runtime/lifecycle methods

Each runtime/lifecycle method must have one clearly defined semantic role.
Using a method of one role as a general-purpose init bucket is strictly prohibited.

In particular, a method such as `buildChildren()` is only permitted as a runtime child materialization method. The same rule applies to any analogous materialization/lifecycle methods with a narrow semantic role.
It is not a general controller init method.

`buildChildren()` may only be used for:
- creating child nodes;
- attaching child nodes as children of the current node;
- actions directly necessary for those child nodes to appear as child nodes.

Using `buildChildren()` for the following is prohibited:
- creating the content of the current node;
- registering listeners of the current node;
- initial render/update of the current node;
- general initialization of the controller instance;
- any actions unrelated to child materialization.

If a class does not perform runtime child construction, `buildChildren()` must not exist in that class. Anything else is strictly prohibited.

## 3. Re-initialization semantics

If a runtime method permits repeated calls, its re-entry behavior must be
explicitly defined.

The following questions must be answered:
- does a repeated `init()` clear old children or not;
- does a repeated `mount()` re-materialize the subtree or not;
- does a repeated `rebuild()` recreate instances or reuse them;
- does a repeated `materialize()` re-attach content or is it skipped;
- is a repeated `open()` permitted as a no-op or does it trigger a repeated lifecycle.

### Canonical rule
Implicit repeated append is not permitted where replace semantics are expected by intent.

### Examples of correct declarations
- `init()` uses replace semantics
- `mount()` is guarded no-op after first successful mount
- `rebuild()` uses merge semantics with child reuse
- `materialize()` is append-only by design

---

## 4. Idempotency

If a method can be called repeatedly from the runtime flow, its idempotency must be:
- either guaranteed;
- or explicitly rejected with an explanation of why a repeated call is impossible by the model.

For materialization and initialization methods, it is especially important to define:
- safe repeated call;
- repeated call with cleanup;
- repeated call forbidden by invariant.

### Error
A situation where a prompt or spec implies idempotent/replace behavior,
but the implementation actually performs append, is considered a runtime violation.

---

## 5. Mutable child ownership

For each mutable container, the following must be explicitly defined:
- who creates child instances;
- who holds the reference to child instances;
- who removes child instances;
- who clears stale children on replace/re-init;
- who is responsible for consistency between the child collection and rendered children.

### Canonical rule
The owner of mutable children must be unambiguous.

If one layer considers itself the owner of child instances, while another layer removes/creates
them directly without a coordinated model, this is a runtime defect.

---


## 6. Content lifecycle by default

A runtime content instance is not considered permanently alive by default.
By default, content must be created on demand and destroyed when the corresponding
node/branch becomes inactive or closed. Any other default is strictly prohibited.

The following must be explicitly defined:
- who creates the content instance;
- when content is first materialized;
- who destroys the content instance;
- what constitutes the canonical destroy path on deactivate/close;
- whether a separately declared retention pattern exists.

### Canonical rule
If a separate retention pattern is not explicitly declared, the content lifecycle must follow the
active branch/node lifecycle: create on demand, destroy on inactive.

### What constitutes a violation
- permanent content by default without a separately declared retention pattern;
- hidden reuse of an old content instance after re-opening a branch without an explicit model;
- content instances persisting in closed branches as implicit system state.

## 7. State switching and lifecycle

State switching belongs to the runtime model and must go through a single
lifecycle-consistent path.

The following must be explicitly defined:
- who owns the active/opened child;
- who initiates the switch;
- in what order close/open hooks are executed;
- whether direct assignment of the active child is permitted;
- what constitutes the canonical switching path.

### Canonical rule
No public means of state switching must bypass lifecycle hooks
if the system declares hooks as part of the model.

---

## 8. Logical structure vs render/materialization attachment

The runtime model must distinguish between:
- **logical parent**
- **structural parent**
- **materialization parent**
- **render attachment target**

Logical ownership and render placement are not the same thing.

A node may be the logical child of one parent, but materialize its content:
- into a render host ancestor node;
- into a shared external container;
- into a delegated render target,

if this explicitly corresponds to the model.

### What is considered correct
- the logical tree is preserved;
- the owner node remains clear;
- render attachment is explainable and stable;
- the runtime flow does not hide structural relations.

### What constitutes a violation
- visual placement substitutes for logical ownership;
- attachment rules are not described and are unpredictable;
- a child loses a clear owner due to a render shortcut.

---

## 9. Runtime model and source of truth

For mutable/runtime-changing systems, the following must be explicitly stated:
- where the authoritative source of truth resides;
- which runtime structures are derived;
- which runtime mutations must be serialized back;
- which runtime changes are acceptable as UI-only.

Possible sources of truth:
- spec tree;
- runtime instance tree;
- raw data tree;
- external domain model.

### Canonical rule
Runtime mutation without a source-of-truth policy is not permitted for editor-like systems
and other systems where the user changes the structure or state of the model.

---

## 10. Runtime model in editor-like systems

For editor-like systems, a policy must be defined for the following operations:
- add child
- remove child
- reorder
- drag and drop
- rename
- move subtree
- replace subtree

For each operation, the following must be defined:
- who changes the runtime tree;
- who changes the data/source model;
- who initiates serialization back;
- what constitutes a completed consistent operation.

If the UI already shows the result of an operation but the authoritative model has not been updated,
and this is not declared as a temporary UI-only state, the model is incomplete.

---

## 11. Runtime violations

Typical runtime violations include:
- non-idempotent `init/reset/mount/rebuild/materialize` without an explicit declaration;
- hidden append instead of replace;
- direct state mutation bypassing lifecycle;
- permanent content by default without a separately declared retention pattern;
- inconsistent child ownership;
- runtime mutation without a serialization policy;
- desynchronization between the logical tree, runtime tree, and rendered output;
- undescribed render attachment bypass.

---

## 12. What a good runtime analysis should contain

A good runtime analysis must answer the following questions:
1. What runtime methods exist?
2. What are their semantics?
3. Which repeated calls are permitted?
4. What is the default content lifecycle policy?
5. Who owns mutable children?
6. How does state switching proceed?
7. Where is logical ownership, and where is render attachment?
8. Where is the source of truth?
9. Which runtime mutations require serialization back?
10. Which runtime defects are already present?
