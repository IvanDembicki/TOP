# Anti-Patterns

A list of typical errors and pitfalls when analyzing and designing TOP systems.

For positive patterns and canonical forms, see `pattern-cards.md`.

---

## 1. Confusing Switchable Node, Dynamic Switchable Node, and Single-Child Mutable Node

### What the error is
Treating any node with one active child as the same pattern, without distinguishing:
- fixed switchable: a fixed architectural state/candidate set;
- dynamic switchable: a dynamic candidate set plus one owner-managed selected/opened child;
- single-child mutable: one child slot whose concrete instance is replaced without retaining a candidate set.

### Why this is harmful
- classification breaks down;
- the distinction between selection semantics and mutable replacement is lost;
- lifecycle semantics are designed incorrectly;
- source-of-truth policy for the candidate set or selected child remains implicit.

### What to look for
- whether there is a candidate set or only one replaceable slot;
- whether one child is selected/opened through the canonical switching path;
- whether the candidate set is fixed or dynamic;
- whether child creation/removal and active-child removal behavior are explicit.

---

## 2. Confusing State Owner and Visual Trigger

### What the error is
Treating the UI element that visually switches the state as the state owner.

### Why this is harmful
- local state is attributed to the wrong node;
- tree model is replaced by UI mechanics;
- state ownership analysis becomes false.

### What to look for
- who holds the active/opened child;
- who actually controls the lifecycle state switch.

---

## 3. Confusing Logical Ownership and Render Placement

### What the error is
Treating the node into whose render/materialization container the child content attaches as the parent node.

### Why this is harmful
- the logical tree dissolves into the visual structure;
- correct analysis of state nodes and helper nodes becomes impossible;
- ownership and lifecycle become unclear.

### What to look for
- who is the logical parent;
- who is the render host;
- who is the lifecycle owner.

---

## 4. Treating Render Tree as Equivalent to TOP Tree

### What the error is
Attempting to restore the TOP model from visual nesting alone.

### Why this is harmful
- structural nodes without their own view disappear;
- state holders and logical grouping nodes are lost;
- visual hierarchy mistakenly becomes the architectural model.

### What to look for
- the semantic role of a node;
- structural ownership;
- hidden semantic subparts.

---

## 5. Storing State Only as Flags Where State Nodes Are Needed

### What the error is
Reducing full state branching behavior to a set of boolean flags
without an explicit state structure.

### Why this is harmful
- state ceases to be part of the tree model;
- lifecycle transitions are hidden;
- the project becomes harder to analyze and extend.

### What to look for
- whether there is a fixed set of semantic states;
- whether a separate state holder / state nodes are needed.

---

## 6. Mutable Node Without an Explicit Child Policy

### What the error is
Having mutable children without describing:
- `childrenType`;
- create/remove rules;
- ownership;
- cleanup policy.

### Why this is harmful
- the behavior of the child container becomes implicit;
- runtime defects are masked;
- AI starts generating incompatible implementations.

### What to look for
- who owns the children;
- how replacement occurs;
- what re-init semantics look like.

---

## 7. `lib:true` Without a Documented Type

### What the error is
Using `lib:true` without declaring the base type of the child node in the spec.

### Why this is harmful
- AI cannot determine what type of instances is created at runtime;
- the child contract is violated — the type is not declared.

### What to look for
- whether the base type is declared in the lib entry;
- whether there is a children array typed with the base type;
- whether all runtime instances inherit from the declared type.

---

## 8. Direct Deep Parent Chain Navigation

### What the error is
Building behavior through long chains such as parent.parent.parent
as the primary means of semantic coordination.

### Why this is harmful
- the tree becomes fragile;
- ownership implicitly flows through the structure;
- even a minor tree restructuring breaks the logic.

### What to look for
- whether there is a semantic owner;
- whether a connector is needed;
- whether the model is being replaced by accidental navigation through ancestors.

---

## 9. Re-init Without Declared Semantics

### What the error is
A repeated `init/reset/mount/materialize` exists, but it is not defined
what it does: replace, append, merge, or no-op.

### Why this is harmful
- hidden duplicates appear;
- prompt and code start to diverge;
- runtime defects are hard to reproduce and analyze.

### What to look for
- repeated call behavior;
- cleanup of old instances;
- idempotency expectations.

---

## 10. Runtime Mutation Without Source-of-Truth Policy

### What the error is
User actions change the runtime tree, but it is unclear:
- whether the authoritative model is updated or not;
- who is responsible for serialization back;
- what constitutes temporary UI-only state.

### Why this is harmful
- editor-like systems become logically incomplete;
- desynchronization between UI and data arises;
- analysis cannot determine the correctness of behavior.

### What to look for
- where the source of truth is;
- who performs the reverse sync;
- when an operation is considered complete.

---

## 11. Mixing TOP-Model Violations and Implementation Violations

### What the error is
Failing to distinguish between:
- an architectural model problem;
- a defect in a specific implementation.

### Why this is harmful
- recommendations become imprecise;
- a debate about the model turns into a debate about a bug;
- the priority of fixes is lost.

### What to look for
- whether the problem is in tree semantics or in runtime code;
- whether the canon is violated or it is simply implementation drift.

---

## 12. Treating Runtime-First Patterns as Structural Violations Without Determining the Mode

### What the error is
Immediately declaring a runtime-oriented structure a TOP violation
without determining the `materialization mode`.

### Why this is harmful
- runtime-first projects are analyzed unfairly;
- helper patterns are mistakenly declared anti-TOP.

### What to look for
- first determine the dominant materialization mode;
- only then assess the architecture.

---

## 13. One Prompt for Multiple Different Nodes Without Explicit Justification

### What the error is
A single implementation prompt covers multiple semantic nodes,
but this is not recorded or explained.

### Why this is harmful
- prompt drift accelerates;
- verification becomes difficult;
- it is unclear which node the prompt actually describes.

### What to look for
- one prompt = one node by default;
- any deviation requires explicit explanation.

---

## 14. Ignoring Hidden Semantic Subparts

### What the error is
Treating a composite node as indivisible simply because it is implemented as a single class/component.

### Why this is harmful
- the real roles within the system are hidden;
- the state owner, content host, and child container become mixed;
- analysis loses accuracy.

### What to look for
- whether there are multiple semantic responsibilities inside the node;
- whether a decomposition can be restored.

---


## 15. Protocol Leakage

### What the error is
Using `IControllerAccess` or `IContentAccess` as a hidden channel for crossing the content boundary,
or passing through them external objects, host/container references, parent/root links,
integration handles, or other implementation primitives outside the permitted private boundary.

### Why this is harmful
- content ceases to be isolated from the outside world;
- the private protocol becomes a transport for bypassing architectural constraints;
- the controller/content boundary becomes blurred;
- replacing the internal implementation once again starts to affect neighboring classes.

### What to look for
- whether the private protocol contains references to parent/root/host/container/external objects;
- whether the protocol object is used as surrogate access to the outside world;
- whether the protocol remains strictly whitelist-only.

---

## 16. Architectural Will Inside Content

### What the error is
Content itself initiating attach/detach/integrate/show/hide/navigation/lifecycle actions
or otherwise making architectural decisions on its own behalf.

### Why this is harmful
- content ceases to be an implementation boundary;
- lifecycle and orchestration lose a single owner;
- node behavior spreads between controller and content;
- closed branches and inactive nodes start behaving unpredictably.

### What to look for
- whether content decides when to attach or destroy itself;
- whether content initiates structural or lifecycle actions;
- whether content interprets its own events as system commands.

---

## 17. Permanent Content by Default

### What the error is
Treating a runtime content instance as permanently existing by default
and retaining it in inactive/closed branches without a separately declared retention pattern.

### Why this is harmful
- the content lifecycle ceases to match the branch/node lifecycle;
- closed branches retain unnecessary runtime instances and state;
- the analyzer and generator stop distinguishing on-demand creation from permanent retention;
- re-opening a branch starts depending on previously created hidden state.

### What to look for
- whether content is created on demand;
- whether content is destroyed on deactivate/close by default;
- whether a retention pattern is separately declared if content lives longer than the active branch.

---

## 18. `buildChildren()` as Init Bucket

### What the error is
Using a method such as `buildChildren()` as a general place for initializing the controller, content, listeners, and initial sync.

### Why this is harmful
- the semantic purpose of runtime/lifecycle methods becomes blurred;
- child materialization is mixed with controller initialization;
- runtime mode and non-runtime mode start to become confused;
- AI begins to perceive `buildChildren()` as a universal init hook.

### What to look for
- whether content of the current node is being created inside `buildChildren()`;
- whether listeners of the current node are being registered there;
- whether initial sync of the current node is being performed there;
- whether `buildChildren()` exists in a class without runtime child construction.

### Correct alternative
`buildChildren()` is used only for runtime child materialization.
If runtime child construction is absent, such a method must not exist in the class.
General controller initialization and lifecycle content must reside in separate semantic paths.

---

## 19. How to Use Anti-Patterns

When analyzing:
1. do not limit yourself to the name of the anti-pattern;
2. record the specific symptom;
3. indicate whether this is a model issue or an implementation issue;
4. provide a targeted recommendation, not generic criticism.

When designing:
1. run important nodes through the anti-patterns list;
2. fix ownership, lifecycle, and source of truth in advance;
3. separately check mutable and runtime-heavy branches.
