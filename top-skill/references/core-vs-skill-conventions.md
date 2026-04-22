# TOP Core vs Skill Conventions

This document establishes the boundary between:
- **TOP Core** — the canonical principles of the paradigm itself;
- **TOP Skill Conventions** — the conventions of this skill, used for prompt-based development, analysis, and organization of project-local artifacts.

This boundary must be maintained explicitly during analysis, discussion, and edits.

---

## 1. TOP Core

TOP Core comprises the concepts that describe the TOP model itself, not the specific organization of the skill package.

### 1.1. Tree model
Core includes:
- tree as the fundamental structural unit;
- root tree and root node;
- parent-child structure;
- strict tree hierarchy;
- allowed semantic branches;
- module branches;
- connectors as special linking nodes, provided they do not break the tree model.

### 1.2. Node model
Core includes:
- node as the fundamental structural unit;
- distinction between structural role and semantic role;
- child composition;
- composite decomposition;
- hidden semantic subparts;
- mutable nodes;
- single-child mutable nodes;
- library nodes;
- switchable nodes;
- child policy, including `childrenType` when child semantics would otherwise be ambiguous.

### 1.3. State model
Core includes:
- state holders;
- state nodes;
- owner-state semantics;
- visual reflection state as a distinct entity, not equivalent to local state;
- state switching rules;
- the requirement for lifecycle-consistent state transitions.

### 1.4. Runtime model
Core includes:
- runtime-first and spec-first as materialization modes;
- materialization semantics;
- runtime instance tree;
- rules for mutable/runtime behavior;
- the permissibility of a difference between logical structure and materialized/rendered structure, provided it is explicitly described and does not break tree ownership.

### 1.5. Library model
Core includes:
- `lib:` as part of the library nodes model;
- local `lib:true`, when used as part of tree semantics rather than as a purely tooling marker;
- the requirement to interpret local `lib:true` according to the specific scenario, not by a single universal meaning.

### 1.6. Four axes classification
Core includes the classification of trees along four independent axes:
1. Representation level
2. Content type
3. Statefulness
4. Materialization mode

None of these axes should substitute for another.

---

## 2. TOP Skill Conventions

TOP Skill Conventions are the conventions of this particular skill, not of the TOP paradigm itself.

### 2.1. Project-local artifact layout
Conventions include:
- the `top/` directory as the root of project-local TOP artifacts;
- placement of spec files, prompt files, and auxiliary artifacts inside `top/`;
- modular hierarchy inside `top/` for modular projects;
- conventions for the layout of branch-level artifacts.

### 2.2. Spec file conventions
Conventions include:
- storing tree/branch specs as `.json`;
- placing spec files alongside the corresponding prompts or branch artifacts;
- naming conventions for spec files;
- the relationship between spec files and implementation prompts.

### 2.3. Prompt file conventions
Conventions include:
- having implementation prompts in `prompts/`;
- placing prompt files alongside spec or branch-level artifacts;
- language-agnostic prompt style where possible;
- designating the prompt layer as a project-local artifact layer.

### 2.4. Generated code placement conventions
Conventions include:
- `props.dir`;
- inheritance of `props.dir` by descendant nodes;
- rules for placing generated class files;
- correspondence between directory structure and `props.dir` values.

### 2.5. Verification conventions
Conventions include:
- prompt verification loop;
- regeneration attempts;
- comparison rules;
- escalation after reaching max attempts;
- rules for recording prompt/code drift;
- rules for recording behavior mismatch.

### 2.6. Analysis workflow conventions
Conventions include:
- the analysis prompts used;
- the format of analysis results;
- the accepted violation categories;
- splitting results into TOP-model, implementation/runtime, and prompt-layer findings.

---

## 3. Interpretation Rule

### 3.1. Do not mix levels
A violation of a skill convention must not automatically be treated as a violation of TOP Core.

Examples:
- a spec file stored outside `top/` — this may be a skill convention violation, but not necessarily a TOP model violation;
- a prompt not located alongside its spec — this may degrade the workflow, but is not always a TOP architectural error;
- absence of `props.dir` — this may be a generation convention violation, but does not necessarily break tree semantics.

### 3.2. What counts as a Core violation
The following should be treated as TOP Core violations:
- breaking the tree hierarchy;
- incorrect child composition model;
- incorrect state ownership semantics;
- mixing the four axes;
- incorrect interpretation of mutable/switchable/single-child mutable semantics;
- loss of explicit logical ownership;
- conflicting source of truth;
- state switching outside a lifecycle-consistent model.

### 3.3. What counts as a Convention violation
The following should be treated as TOP Skill Convention violations:
- incorrect organization of `top/`;
- incorrect placement of prompts/spec files;
- absence of expected prompt artifacts;
- violations of `props.dir` conventions;
- absence of a verification pipeline where this skill expects one.

---

## 4. Analysis Rule

When analyzing a project, results should explicitly separate, where possible:

1. **TOP Core findings**
   - reconstructed model;
   - Core violations;
   - semantic ambiguities.

2. **Skill Convention findings**
   - artifact layout issues;
   - prompt workflow issues;
   - generation/placement issues;
   - verification issues.

---

## 5. Practical Implication

If something:
- is inconvenient for the workflow,
- breaks the prompt pipeline,
- makes generation harder,
- obstructs verification,

this does not necessarily mean a TOP Core violation has occurred.

Conversely, a project may:
- formally comply with artifact conventions,
- yet have an incorrect tree model,
- incorrect state ownership semantics,
- incorrect mutable semantics.

Therefore, Core and Conventions must always be analyzed separately.
