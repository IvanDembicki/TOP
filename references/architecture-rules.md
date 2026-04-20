# Architecture Rules

A list of strict TOP architectural rules. Violation of any of them is an
architectural defect that requires explicit justification or correction.

---

## Tree Structure Rules

### R1. The System Is Described as a Tree, Not a Graph

Relations between nodes form a strict parent-child hierarchy.
Cross-references, cycles, and arbitrary cross-tree relations are not permitted.

If a cross-reference is necessary, it is implemented through an explicit mechanism
(events, module interface, connector), not through direct references.

### R2. Bidirectional Typing of Relations Is Required

Every parent-child relation must be typed in both directions.
A child declares the type of its parent. A parent declares the permissible types of its child nodes.

### R3. A Mutable Node Contains Only Library Node Instances

Child nodes of a mutable node are instances of library nodes.
A library node is defined either locally (`"lib": true` in props),
or in the project `Library` branch under the single root (referenced by full type-path with a `lib:` prefix).

A project `Library` branch may keep a namespace node's detailed subtree in an external spec file via `props.source`. The external file describes the same node type; it does not create a second root or a second tree.

If a mutable node allows several different library child nodes, they must
inherit from a common base type. The parent declares this base type
via `props.childrenType`, not by listing concrete implementations.

Mixed composition is prohibited: a single node cannot mix immutable and mutable child nodes.
When a combination is needed, the mutable part is extracted into a separate immutable child node.

### R3a. A Single-Child Mutable Node Is a Distinct Mutable Node Pattern

If a parent node always contains exactly one child node at runtime, but the concrete type
of that child node is determined by data and can be replaced entirely, such a node
must be treated as a `single-child mutable node`.

This pattern is not a `switchable node` merely because it has one active child. It is single-child mutable when no candidate set is retained and the active slot is replaced by a runtime-created child instance. A dynamic switchable node is different: it owns a dynamic candidate set and switches the opened child among candidates through the canonical switching path.

### R3b. Do Not Confuse Switchable Node and Mutable Node with Library Children

These are distinct patterns with different semantics:

- **Fixed switchable node** — the same element changes among a fixed architectural set of state children
  (e.g., `Normal`, `Hover`, `Disabled`).
- **Dynamic switchable node** — the parent owns a dynamic candidate child set and one selected/opened child among those candidates. Candidate children may be created or removed at runtime, but selection still follows the canonical switching path.
- **Single-child mutable node** — the parent always contains exactly one child slot, and the concrete child instance in that slot is replaced by data. No retained candidate set is required.
- **Mutable node with library children** — a container to which elements are added and removed at runtime without the container necessarily owning one lifecycle-opened selected child.

### R4. Mixing Switchable and Non-Switchable Child Nodes Is Prohibited

A single node cannot mix switchable and non-switchable child nodes. For a dynamic switchable node, the dynamic candidate set is the switchable child set; ordinary non-switchable child responsibilities must be extracted into separate child nodes or explicit supporting branches.

### R4a. A Composite Node Must Be Decomposed into Semantic Child Nodes

If a composite node contains multiple visual parts, each part must be extracted
into a separate child node if at least one of the following conditions is met:

- the part has its own behavior;
- the part has its own event handlers;
- the part has its own independent visibility;
- the part has its own switchable representation;
- the part has its own UI role in the composition;
- the part can be materialized, hidden, activated, or changed
  independently of the other parts.

Purely decorative fragments may be left inside a content node only if
they have no behavior, state, lifecycle, or independent role in the tree.

### R4b. A Monolithic Composite Node with Multiple Interactive Elements Is a Defect

If a single node or single class materializes multiple interactive elements internally,
attaches independent events to them directly, and independently manages their separate
visibility, activity, text, icon, or state, this must be treated as an
architectural decomposition defect.

### R4c. State Must Belong to Its Owner Node

If a control element merely initiates a state change in another element or branch,
the state holder must be the owner node of the managed entity, not the control node.

### R4d. Every Node That Undergoes Prompt-Based Code Generation Must Have a Separate Implementation Prompt File

The node spec must contain a reference to this prompt via the `prompt` field.
If no prompt is present, the node is considered incompletely defined for code generation.

### R4e. One Prompt — One Node

One implementation prompt must describe exactly one node.
A single shared prompt for multiple semantic nodes is not permitted if they have different:
- responsibility;
- state model;
- event handling;
- invariants;
- child interaction rules.

### R4f. Behavioral Prompt Sections Must Be Platform-Neutral

An implementation prompt must describe:
- the node's responsibility;
- behavior;
- events;
- state ownership;
- transitions;
- child interaction;
- constraints and invariants;

These behavioral sections must not be tightly coupled to a specific language,
framework syntax, runtime primitive, or platform mechanism.

Platform-specific details are permitted only in `Platform implementation notes`.
Those notes may be used as explanatory context when generating for another technology,
but they must not be copied mechanically. A generator for another technology must
preserve the platform-neutral behavior and choose a native target-appropriate mechanism.

### R4g. When a Node Changes, Its Implementation Prompt Is Updated Too

Code cannot be kept up to date while leaving the implementation prompt outdated.
When the semantics of a node change, the following must be updated synchronously:
- node spec;
- implementation prompt;
- generated code;
- verification expectations.

### R4h. Prompt Drift Is an Architectural Defect

If the current node code and the implementation prompt have diverged persistently,
this is considered an architectural defect at the level of implementation artifacts.

### R4i. The Spec Tree File Must Be `.json`

The target standard for project tree descriptions is `.json`.

### R4j. All Project-Local TOP Artifacts Must Be Stored Inside `top/`

TOP artifacts are project artifacts, not skill artifacts.

JSON tree descriptions and prompt files must be stored inside the root project directory:

```text
top/
```

Project-local source assets used by TOP prompts, examples, fixtures, or demo data may also
be stored under `top/assets/`. If generated code depends on such data, the asset must be
explicitly referenced or materialized from `top/assets/`; it must not appear only as an
unexplained hardcoded literal inside generated code.
Every file under `top/assets/` must be represented in the project JSON tree under a
model-only `Assets` branch, using `props.assetPath` for the file path relative to `top/`.

Project-local presentation source artifacts used by TOP prompts, examples, themes, style
references, design tokens, or user styling inputs may be stored under `top/presentation/`.
Every file under `top/presentation/` must be represented in the project JSON tree under a `Presentation` branch or another explicitly named presentation branch, using `props.presentationPath` for the file path relative to `top/`.

Presentation artifacts are generation input, not necessarily runtime artifacts. The canonical
presentation source must be stored in a project/platform-neutral TOP presentation format.
Generators must interpret that source into a platform-neutral presentation model and materialize target implementation output according to the declared branch materialization policy.
When importing an existing project, its styling system is converted into the TOP presentation
format before it becomes part of the TOP project.

When the Presentation branch is materialized as runtime nodes, it follows normal TOP subtree rules: controller/content, contract, lifecycle, and topology. When it is target-compiled, externally provided, or source/model only, the policy must be explicit. Other runtime branches access presentation through typed connectors/contracts or declared target-appropriate boundaries, not through direct sideways traversal or by parsing source presentation files themselves.

### R4k. Project-Local Prompt Files Must Be Stored Alongside the JSON Spec Inside `top/`

Implementation prompt files must:
- be stored inside `top/`;
- be placed alongside the JSON project description or the corresponding branch;
- be located in the `prompts/` directory;
- be referenced from the node spec via a relative path in the `prompt` field.

For modular projects, a hierarchy of the following form is permitted:

```text
top/
  root.json
  prompts/
  modules/
    editor/
      tree.json
      prompts/
```

### R4l. Generated Class Files Must Be Placed via `props.dir`

If class files or other code artifacts are generated for a node,
their directory must be specified via `props.dir`.

`props.dir` stores a relative path within the project structure
and must reflect the branch/tree organization, not an arbitrary file placement.

Generated code artifacts do not have to be stored inside `top/`.
`top/` is intended for model artifacts and prompt artifacts.

If `props.dir` is set on a node, that path is inherited by all descendant nodes until overridden.
A child node must not redundantly specify the same `dir` if it is already inherited from the parent.
If a child node specifies its own `dir`, it must be treated as a subdirectory or an explicit override of the effective path.

### R4m. An Implementation Prompt Must Declare Its Primary Implementation Artifact Stem via `sourcePath`

Each implementation prompt must contain a metadata block at the top of the file with a `sourcePath` field —
a path relative to the project root pointing to the extensionless primary implementation artifact stem the prompt describes.

The `.top` segment is the stable TOP artifact marker. The concrete language or platform extension
(`.js`, `.ts`, `.tsx`, `.swift`, `.dart`, etc.) is a target-specific materialization detail and
must not be hardcoded in platform-neutral TOP fronts.

```
---
sourcePath: src/path/to/node.top
---
```

A prompt without `sourcePath` is considered incompletely bound:
the link between spec, prompt, and code is not explicit and cannot be verified automatically.

`sourcePath` identifies the primary artifact stem only. It does not prohibit companion
artifacts. If the target technology, project convention, or generation strategy splits a
node across multiple files, the prompt's `Expected Materialization` section must declare
the companion artifact stems and their roles.

**Detection rules (for AI validators):**

Flag as violation:
- prompt file has no frontmatter block;
- frontmatter block is present but `sourcePath` is missing;
- `sourcePath` includes a concrete platform extension such as `.js`, `.ts`, `.tsx`, `.swift`, or `.dart`;
- for a concrete generation target, no materialized implementation artifact can be resolved from the stem using the target's declared extension rules.

### R4n. Expected Materialization Must Describe All Node Implementation Artifacts

An implementation prompt describes one semantic node. It may materialize as one physical file
or multiple physical files.

The prompt must include an `Expected Materialization` section that declares:
- primary artifact stem;
- public node/controller class;
- materialization policy;
- internal access contracts in both directions (`IContentAccess` and `IControllerAccess`, or explicit zero-contracts);
- companion artifact stems and roles if the node is split across multiple files.

If a node has separate content, omitting the content-to-controller direction is a violation,
even when the current implementation only needs local low-level event subscription. The correct
form is either a narrow named `IControllerAccess` contract or an explicit zero-contract.

Raw callbacks, anonymous protocol objects, full controller references, or full concrete content
references must not be treated as valid internal contract materialization where the technology
can express named typed boundaries.

---

## Navigation and Access Rules

See `references/interaction-contracts.md` for the full access model:
guaranteed access / search access / forbidden access.

### R5. Hardcoded Navigation Chains Are Prohibited

Constructs such as `parent.parent.parent`, `firstChild.firstChild.nextSibling`, and their equivalents
are not permitted.

These are a form of forbidden access: they hardcode traversal depth and bypass
the structural contract. Use `findUpByType(T)` within an architecturally guaranteed chain instead.

### R5a. Named Fields Required for Static Children with Semantic Roles

A parent node that statically owns child nodes with distinct, fixed semantic roles
must store each such child in a dedicated field at construction time.

Each such field must be:
- **named** to reflect the child's semantic role (e.g. `_viewState`, `_toolbar`, `_editToggleBtn`);
- **explicitly typed** to the concrete or narrowest applicable child type where the language permits.

Access to these children must go through their named fields.

Positional accessors — `firstChild`, `lastChild`, `getChildAt(index)`, `children[0]`,
and their equivalents — are not the canonical form for accessing semantically distinct children,
even when the result is structurally guaranteed.

**Exception:** positional or collection-based access is permitted for **uniform operations**
applied identically to all children, where the logic does not determine the semantic role
of a specific child and does not make a structural decision based on position.

**Why this rule matters:**
- Positional access couples code to structural order and breaks silently on reorder or insertion.
- Named fields make each child's semantic role explicit and statically verifiable.
- Explicit typing enables IDE navigation, refactoring safety, and correct prompt generation.
- `this.lastChild` does not communicate intent; `this._editModeState` does.

### R5b. A Guaranteed Static Ancestor Must Be Resolved Once and Cached

If `findUpByType()` targets an ancestor whose presence is guaranteed by the static parent
chain, that dependency must be resolved **exactly once**, stored in a named explicitly typed
field, and accessed exclusively through that field thereafter.

**The rule is not about placement** (constructor vs. build phase vs. lazy getter).
The rule is about repetition: repeated dynamic lookup of a statically guaranteed
ancestor is forbidden regardless of where it appears.

---

**Capture pattern — required for all guaranteed ancestor lookups.**

```javascript
// In constructor — when the field is only used at runtime
constructor(parent) {
    super(parent);
    this._editor = /** @type {TreeEditorNode} */ (this.findUpByType(TreeEditorNode));
}

// During the target-specific materialization phase — when a later phase uses the field`nmaterializeContent() {`n    this._treeItem = /** @type {TreeItemNode} */ (this.findUpByType(TreeItemNode));`n    this.setContent(new MyContent(new MyControllerAccessZero()));`n}

// Lazy getter — also valid: resolves once on first access, caches in backing field
get _editor() {
    return this.__editor ??= /** @type {TreeEditorNode} */ (this.findUpByType(TreeEditorNode));
}

// All downstream access goes through the field
_onClick() {
    this._editor.editorModeHolder.toggle();
}
```

The invariant: a guaranteed ancestor is resolved at most once per node instance.

---

**Permitted:**
- Single `findUpByType()` call at any point before first use — constructor, build phase, or lazy getter
- Result stored in a named, explicitly typed field
- All subsequent access through that field
- The dependency is architecturally guaranteed by the parent chain (see R5c for boundary rules)

**Forbidden:**
- Repeated calls for the same ancestor type in the same class
- Inline usage without storing: `(this.findUpByType(T)).method()` — single call but no field
- Calling `findUpByType()` for an ancestor that was already resolved and cached elsewhere in the same class
- Using the repeated lookup pattern as a substitute for declaring a proper field

---

**Detection rules (for AI validators):**

Flag as violation:
- Same ancestor type searched more than once within one class
- Result used inline without a corresponding named field
- A method calls `findUpByType()` for a type that is already captured in a field of the same class

Consider valid:
- Single call anywhere (constructor, build method, lazy getter, first-access initializer)
- Result stored in a named, explicitly typed field (`this._editor`, `this._treeItem`, etc.)
- All downstream access goes through the stored field

---

**Motivation:**

An architecturally guaranteed ancestor does not change over the node's lifetime.
Resolving it repeatedly is a hidden cost with no architectural value — it couples
every call site to the tree structure instead of expressing the dependency once, explicitly.
A named typed field makes the dependency visible, verifiable, and refactoring-safe.

---

**For non-guaranteed access (nullable result):**

When `findUpByType()` crosses a boundary where the parent chain is not architecturally
guaranteed (see R5c), the result is nullable and must be treated as search access.

In this case, caching the result is context-dependent:

- If the branch's attachment context is stable for the node's full lifecycle, caching
  on first access is acceptable — but the field must be nullable.
- If the connector can change, or if the branch can be reattached under a different
  parent, caching may produce a stale reference. In such cases, do not cache or
  re-resolve on each access.

This is a recommendation, not a strict rule. The correct approach depends on the
specific lifecycle of the branch and its connector.

### R5c. findUpByType() Must Not Cross the Boundary of the Guaranteed Parent Chain

`findUpByType()` is permitted only within a continuous upward chain where the type of
every parent node is architecturally guaranteed and statically known.

The boundary is defined not by a label (such as `lib: true`) but by the point where
the parent type ceases to be guaranteed. A node inside a library may use `findUpByType()`
freely if the full chain up to the target is guaranteed, including the library's
deployment parent. If the same library can be attached under multiple unrelated parents,
the chain above the attachment point is not guaranteed unless a typed deployment contract fixes it.
A node outside a library must stop at any point where the chain becomes untyped or external.

Once the chain reaches a boundary — a connector, interface boundary, abstract host,
or external attachment point — `findUpByType()` must stop there.
The required external dependency must be:
- intercepted at the boundary,
- expressed through a typed contract (interface, abstract class, or connector),
- stored as an explicit typed reference,
- and used exclusively through that reference downstream.

---

**Permitted:**
- `findUpByType()` traversing only nodes whose parent types are architecturally fixed
- The target type is guaranteed to exist in that chain by the tree structure
- The chain does not cross any boundary where parent typing becomes unknown or external

**Forbidden:**
- `findUpByType()` continuing above a point where the parent type is no longer guaranteed
- Crossing a connector or interface boundary via direct lookup instead of a contract
- Using `findUpByType()` as runtime navigation through an untyped or external structure
- Searching for a type that should be provided through a contract, not discovered by traversal

---

**Boundary interception — required pattern when the chain ends:**

```javascript
// The boundary node intercepts what lies above and provides it as a typed contract.
// Nodes below the boundary receive the dependency through the contract,
// never by searching above it directly.
```

---

**Detection rules (for AI validators):**

Flag as violation:
- `findUpByType()` reaches an ancestor that is not part of the caller's architecturally guaranteed chain
- The search path passes through an untyped connector, interface, abstract host, external attachment point, or lib attachment context where the parent chain above the boundary is not architecturally guaranteed
- The searched type could only be reached by traversing into an external or untyped structure
- A dependency that should be injected via contract is instead discovered by upward traversal

Consider valid:
- Every node on the path from caller to target has a statically known, architecturally fixed type
- The target type's presence follows from the tree structure, not from a runtime assumption
- Any crossed lib/deployment boundary is explicitly typed, and the chain remains architecturally guaranteed up to the target ancestor

---

**Motivation:**

This rule preserves the portability and independence of subtrees.
A node that navigates above its guaranteed context silently depends on the host environment.
This dependency is invisible in the type system, undetectable without running the tree,
and breaks when the subtree is moved, reused, or composed differently.
Requiring a typed contract at the boundary makes the dependency explicit, enforceable,
and structurally honest.

### R6. Sibling Nodes Interact Only Through the Parent Type Interface

After obtaining a reference to a sibling, only the methods
and properties defined in the common parent type may be used.
Using methods of a concrete sibling subtype is not permitted.

---

## State Rules

### R7. State Is Determined by the Tree Configuration

State is not stored in arbitrary external flags or variables.
The current state is determined by: `openedChild` on each switchable node,
the membership of nodes in the opened branch, and the current tree structure.

### R8. Switching Is Performed Through the Parent

A child node calls `open()`, delegating switching to the parent.
The parent closes the previous `openedChild`, reassigns `openedChild`,
and may call local lifecycle hooks `onClose()` / `onOpen()` on
the corresponding child nodes.

Branch hooks `onBranchClose(node)` and `onBranchOpen(node)` exist in the canon
as extension points, but automatic propagation policy for them is not
part of the base switching contract. If branch propagation is genuinely needed,
its scope and traversal policy must be explicitly defined in a subclass or implementation contract.

### R9. State Tree Is a Characteristic, Not a Content Type

No tree may be called a `state tree` without verifying the presence of a state node.
A state tree is a tree with at least one state node.

---

## Materialization Rules

### R10. Materialization Mode Must Be Explicitly Determined When Analyzing a Project

When analyzing the architecture, the mode in which the system operates must be determined first:
- `spec-first mode`
- `runtime-first mode`

### R11. Runtime-First Patterns Are Not Defects in Themselves

In `runtime-first mode`, the following are permitted:
- library-based runtime creation;
- deferred runtime creation;
- single-child mutable replacement;
- dynamic switchable candidate creation/removal with owner-managed selected/opened child;
- inherited context;
- lazy resource delegation;
- other runtime helper-patterns,

provided they do not violate the tree model, parent-child discipline, and bidirectional typing.

---

## Prompt Verification Rules

### R12. A Code Generation Node Must Go Through a Verification Loop

If a node is implemented through an implementation prompt, its implementation must go through the cycle:
- prompt execution;
- code generation;
- comparison against reference behavior/code;
- prompt refinement when necessary.

### R13. The Verification Loop Must Be Bounded in Attempts

The automatic refinement cycle must not be infinite.
An explicit `maxAttempts` must exist (for example, 10).

### R14. After the Limit Is Exhausted, Escalation Is Required

If a prompt cannot be stabilized within the attempt limit,
the automated workflow must:
- stop;
- save the attempt results;
- record the unresolved mismatch;
- escalate the issue to the user or architect.

---

## Representation Rules

### R15. Implementation Is Derived from the Description

Code artifacts are derived from the tree model and the implementation prompt.
Code must not be generated before the tree model and prompt are defined.

---

## Terminology Rules

### R16. Use Canonical Terminology

Terms must conform to `glossary.md`.
In case of conflict: `glossary.md` → `paradigm.md` → domain-specific reference documents.

### R17. The Four Classification Axes Must Not Be Mixed

Representation level, content type, statefulness, and materialization mode are
independent axes.
