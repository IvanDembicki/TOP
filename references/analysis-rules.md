# Analysis Rules

Rules for analyzing TOP systems. Used when analyzing existing
architecture, restoring the tree model, and finding violations.

---

## Step 1. Identify the input material

First, determine what constitutes the source material for the analysis:
- source code;
- a textual description of the system;
- UI mockups or screenshots;
- an architectural diagram;
- implementation prompts;
- mixed input.

If the input is mixed, explicitly separate:
- what was restored from the spec;
- what was restored from code;
- what was restored from prompts;
- what was restored from runtime behavior.

---

## Step 2. Determine the materialization mode

Before beginning an architectural assessment, determine in which mode
the system's materialization operates:
- `spec-first mode`
- `runtime-first mode`

If the project combines both modes, it is necessary to:
- identify the dominant mode;
- identify the secondary mode;
- not automatically treat runtime-first patterns as violations.

---

## Step 3. Restore the tree model

Based on the input material, restore the system's tree model.

Required:
- identify the root tree;
- identify the root node;
- restore parent-child relationships;
- identify root branches;
- identify the composition of child nodes;
- identify node types;
- determine whether each node has a controller;
- determine whether a node has content;
- for nodes with content, define the controller/content split;
- for nodes with content, determine `props.contentType` if it is present or can be inferred as the way the content type is stored in the spec;
- identify mutable nodes;
- identify single-child mutable nodes;
- identify library nodes;
- identify switchable nodes;
- identify state holders and state nodes;
- identify module branches and connectors;
- for composite nodes, identify hidden semantic subparts;
- for each state, identify the real owner node;
- identify the logical parent-child structure;
- identify render/materialization attachment targets;
- identify the source of truth;
- identify the runtime mutation policy;
- define the semantics of lifecycle methods if they exist:
  - replace
  - append
  - merge
  - guarded no-op
- define the semantic purpose of runtime/lifecycle methods;
- separately verify that a method such as `buildChildren()` is not being used as a general controller init method;
- define the default content lifecycle policy: create-on-demand / destroy-on-inactive or an explicitly declared retention pattern;
- verify that content is not treated as permanently alive by default;
- verify that the public node surface, `IContentAccess`, and `IControllerAccess` are separated, and that the public surface is not substituted by an internal access contract;
- verify that content does not access the public node surface;
- verify that `IContentAccess` and `IControllerAccess` are explicitly and maximally strictly typed where the language permits;
- verify that, where a separate content exists, a materialization internal access boundary is present;
- verify that access artifacts are materialized as named contract artifacts or other explicitly designated typed boundaries, not as anonymous object shapes;
- verify that the constructor/factory/method parameter accepting an access artifact is explicitly typed where the language permits;
- verify that the field/reference holding the access artifact is explicitly typed where the language permits;
- verify that the controller does not bypass the content boundary via direct access to the concrete implementation;
- do not treat a public/base-class primitive getter as proof of a correct boundary: if the controller uses it for attach/wiring/update/read of the concrete implementation, this is a possible or confirmed bypass depending on the evidence;
- explicitly check for controller-side access to the node's own render/view/native primitive, its platform API, or an equivalent exposed primitive handle; these are confirmed violations unless the code is implementing `getView()` itself or performing parent-owned placement/composition of an opaque child view;
- use technology-specific detection examples when auditing a concrete target platform; for DOM-like code, examples include `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, or `content.getView()` used for direct primitive manipulation;

Additionally:
- for nodes intended for prompt-based generation, verify the presence of an implementation prompt and its connection to the spec;
- verify that JSON spec and prompt files are treated as project-local TOP artifacts;
- verify that they are placed inside the `top/` directory if the project uses this convention;
- verify the presence of a modular hierarchy inside `top/` if the project is modular;
- verify the presence of `props.dir` where a node produces generated class files;
- verify that inheritance of `props.dir` by descendant nodes is interpreted correctly.

---

## Step 4. Classify trees along four axes

For each discovered tree, determine:
1. **Representation level**
2. **Content type**
3. **Statefulness**
4. **Materialization mode**

Separately verify:
- that the four axes are not mixed;
- that materialization mode is not substituted by representation level;
- that statefulness is not substituted by content type as a conceptual axis of classification;
- that runtime helper patterns and structural TOP principles are not confused.

---

## Step 5. Find TOP architecture violations

Violations must be checked across three separate classes.

### A. TOP-model violations

#### Tree structure violations
- graph-like connections instead of a strict tree hierarchy;
- hardcoded deep navigation chains;
- mixed composition of immutable and mutable child nodes;
- mixed composition of switchable and non-switchable child nodes;
- confusion between `switchable node` and `single-child mutable node`;
- a monolithic composite node hiding several semantic child nodes.

#### Model semantics violations
- absence of a controller as a required part of a node;
- content present without a designated separate content class;
- controller and concrete content mixed in one class where content exists;
- a node with content missing `props.contentType` where the content type must be explicitly recorded;
- `view` and `component` confused;
- concrete non-visual content exposed externally as a public interface;
- state incorrectly attributed to a control element;
- visual reflection of state mistakenly treated as local state;
- logical parent confused with render/materialization attachment;
- source of truth absent, implicit, or self-conflicting;
- local `lib:true` interpreted without accounting for its specific scenario;
- `childrenType` absent where the child policy is unclear without it;
- runtime-first helper patterns mistakenly treated as TOP violations without accounting for materialization mode;
- public node surface mixed with `IContentAccess` or `IControllerAccess`;
- content accessing the public node surface or parts of it;
- content receiving the full controller instead of a narrow `IControllerAccess`;
- controller receiving the full concrete content instead of a narrow `IContentAccess` where the technology permits an explicit boundary restriction;
- access object lacking an explicit contract where the language allows explicit typing;
- a node with separate content missing a materialized internal access boundary;
- `IControllerAccess` or `IContentAccess` containing external implementation objects, host/container references, parent/root links, or integration handles.

### B. Implementation/runtime violations

Verify:
- non-idempotent `init/reset/mount/rebuild/materialize`;
- implicit append where replace is expected by intent;
- direct state mutation bypassing lifecycle;
- inconsistent lifecycle hooks;
- prompt/code behavior drift;
- runtime mutation without reverse serialization where it is required;
- desynchronization between tree structure, runtime structure, and DOM/data structure;
- state switching not going through a single lifecycle-consistent path;
- modification of hidden data/content bypassing controller methods;
- a method such as `buildChildren()` used as a general controller init method;
- a class defining `buildChildren()` without runtime child construction;
- a runtime/lifecycle method performing actions outside its semantic role;
- content itself initiating attach/integrate/mount/remove/show/hide/destroy;
- controller using the internal content implementation as a communication channel;
- controller bypassing the content boundary via direct access to the concrete implementation or render/integration primitives;
- controller directly mutating or wiring its own platform primitive instead of calling named `this.content.<command>(...)` methods;
- a child node performing self-mounting in `onOpen()`, `constructor`, or any lifecycle hook — calling `parent.content.mount()`, any parent platform integration method (e.g., `parent.el.appendChild()` for DOM), or any equivalent on its own view (violation of Parent-Owned Materialization Invariant — see `canon/architectural-invariants.md` §11);
- constructor used as an init bucket merging content creation, child materialization, and activation phases — these must be separate semantic methods (violation of Phase Separation Invariant — see `canon/architectural-invariants.md` §9);
- a node with declared `contentType` lacking a separate content class, with platform construction inlined in the controller (violation of Content Materialization Invariant — see `canon/architectural-invariants.md` §11);
- positional access (`firstChild`, `lastChild`, `getChildAt(n)`, `children[i]`) used to access
  a static child with a distinct semantic role instead of a named, explicitly typed field —
  this is a violation of R5a; verify that each semantically distinct static child is stored
  in a named field on the parent;
- `findUpByType()` called outside the constructor or a dedicated init method — in event
  handlers, `refresh()`, `toggle()`, `update()`, `render()`, or any operational lifecycle
  method — this is a violation of R5b;
- `findUpByType()` called more than once for the same type within one class without a
  corresponding named capture field — violation of R5b;
- `findUpByType()` result used inline without storing:
  `(this.findUpByType(T)).method()` — violation of R5b;
- `findUpByType()` crossing from a lib subtree into ancestors whose type and existence
  are not guaranteed by an explicitly typed deployment context — violation of R5c
  and Invariant #5. A typed lib deployment chain remains permitted.

### C. Prompt-layer violations

Verify:
- search access (`findUpByType`, `findChildByType`, `findDescendantByType`) used where
  guaranteed access is structurally available — this is an architectural weakness;
- a nullable result of search access is not treated as nullable (missing null check or
  missing null handling);
- a node undergoing prompt-based generation has no implementation prompt;
- the prompt is not connected to the node spec;
- the prompt is not stored inside `top/` or in a project-local `prompts/` alongside the spec/branch;
- a single prompt covers multiple different nodes without sufficient justification;
- the prompt is too platform-specific and is not language-agnostic without necessity;
- prompt drift: code and prompt diverge persistently;
- verification loop absent where a node is generated from a prompt;
- verification loop is infinite or has no explicit attempt limit;
- no escalation after exhausting attempts;
- the prompt does not fix lifecycle semantics where this is critical;
- the prompt does not fix source-of-truth policy where this is critical;
- the prompt does not fix the render attachment model where the logical tree and render structure diverge;
- the prompt does not fix the controller/content split where content exists;
- the prompt does not fix `props.contentType` where the content type is important for the node architecture and must be explicitly recorded;
- the prompt describes `onOpen()` as performing self-mounting into the parent (`"mounts own view into parent X content area"` or equivalent) — this is a prompt-prescribed violation of Parent-Owned Materialization Invariant; correct form: `onOpen()` is called by the parent when this node becomes the active child; the parent controls view placement;
- the prompt describes construction without separating content creation and child materialization into distinct phases — merged lifecycle description is a prompt-level violation of Phase Separation Invariant;
- the prompt for a node with `contentType` does not describe a separate content class, describing instead inline element construction in the controller — this is a prompt-level omission that leads to Content Materialization Invariant violation.

### D. Tree artifact / convention violations

Verify:
- spec tree is not stored as `.json`;
- JSON spec and prompt files are not placed in the root project-local `top/` directory where the project uses this convention;
- a modular project is not reflected through a hierarchy inside `top/` when required;
- a code-generated node is missing `props.dir` where managed placement of generated files is required;
- directory structure diverges from `props.dir`;
- prompt path does not reflect the same semantic position in the tree as the corresponding code path (Structural Correspondence Rule violation — see `references/artifact-layout-and-branch-derivation.md`).

---

## Step 6. Verify the prompt verification pipeline

For nodes with implementation prompts, determine:
- whether reference behavior or reference code exists;
- how regeneration is performed;
- how the result is compared;
- how discrepancies are recorded;
- how the prompt is updated;
- what the attempt limit is;
- how escalation is structured;
- whether only text/code diff or also behavior mismatch is checked;
- whether idempotency is checked upon repeated materialization/initialization;
- whether drift between prompt, spec, and runtime behavior is tracked;
- whether the controller/content split is maintained;
- whether the semantics of `props.contentType` are not lost during regeneration.

If a terminological reference and a detailed pipeline description are needed,
use `references/prompt-verification-loop.md`.

---

## Step 7. Formulate the analysis result

The output must conform to `contracts/agent-output-contracts/analysis-output.md`.

Required sections: `goal`, `context`, `model`, `findings`, `recommendations`.

Findings are divided into four categories:
- `confirmed_violations` — the violation is explicitly confirmed;
- `possible_violations` — there are signs, but data is insufficient;
- `convention_issues` — deviation from conventions, not an architecture violation;
- `open_questions` — ambiguity or insufficient data, a firm conclusion is impossible.

Do not elevate an open_question to a violation without sufficient grounds.
Do not treat the absence of explicit confirmation as automatic refutation of a problem.


## Step 8. Apply node validation rules

After analyzing a generation/refactor result, it is mandatory to:
1. identify the class of violation;
2. classify it as `confirmed`, `possible`, or `ambiguity`;
3. indicate the canonical direction of correction;
4. verify that re-validation was performed after the fix.

If re-validation is absent, the result is not considered complete. Anything else is strictly prohibited.
