# Prompt Verification Loop

This document describes the implementation prompt verification cycle.

---

## Goal

To ensure that the implementation prompt consistently produces a correct node implementation.

---

## Basic cycle

1. Record the node spec and the current implementation prompt.
2. Record the reference behavior or reference code.
3. Execute the prompt.
4. Obtain the regenerated code.
5. Compare the regenerated code with the reference implementation and node requirements.
6. Record mismatches.
7. Fix the implementation prompt.
8. Repeat the cycle.

---

## What to compare

The comparison must account for:
- completeness of behavior;
- event handling;
- state ownership;
- state transitions;
- child interaction rules;
- invariants;
- prohibited side effects;
- structural compatibility with the node spec;
- lifecycle semantics;
- render attachment model, if non-trivial;
- source-of-truth policy, if the node participates in mutable runtime behavior.

If the project is runtime-heavy, the comparison must not be limited to a superficial
text/code diff.

---

## What to verify separately in runtime-heavy nodes

If a node:
- is materialized repeatedly;
- manages mutable children;
- participates in add/remove/reorder flows;
- switches states;
- attaches content to an external render host;

then the verification loop must separately verify:
- re-init semantics;
- idempotency of repeated calls;
- replace vs append behavior;
- cleanup of stale child instances;
- lifecycle consistency;
- runtime behavior against source-of-truth policy.

For terminological reference, use:
- `references/runtime-model.md`
- `references/state-holder-api.md`
- `references/logical-vs-materialized-structure.md`
- `references/source-of-truth-and-serialization.md`

---

## When to stop the cycle

The cycle is considered successful if the prompt produces:
- a sufficiently stable result;
- without loss of required functionality;
- without systematic architectural violations.

The cycle is considered unsuccessful if:
- the result is unstable from run to run;
- the same omissions recur;
- the prompt becomes excessively complex yet still does not stabilize.

---

## Attempt limit

An explicit `maxAttempts` must exist.
Recommended default value: `10`.

---

## Escalation

After exhausting the attempt limit:
- stop automatic attempts;
- prepare a mismatch summary;
- present to the user:
  - which node was being verified;
  - which requirements are not being maintained;
  - which fixes were already applied to the prompt;
  - at which step instability occurs.

The decision is then made by a human:
- clarify semantics;
- simplify the node;
- split the node;
- change verification criteria;
- allow platform-specific prompt specialization.

---

## Verification of artifact placement and drift

During the verification loop, it is necessary to verify not only the behavior of generated code,
but also the absence of drift between JSON specs, implementation prompts, project-local TOP artifacts, and materialized implementation artifacts.

The verification loop must check:

- the prompt file must be located in the project-local `prompts/` alongside the JSON spec;
- generated class files must correspond to `props.dir` accounting for the inherited effective path;
- the directory layout must not contradict the tree structure;
- `sourcePath` values must be extensionless `.top` artifact stems and resolve to materialized target artifacts;
- `props.source`, `props.assetPath`, and `props.presentationPath` references must resolve relative to `top/`;
- Expected Materialization must match the public node class, internal contracts, companion artifacts, and materialization policy;
- child materialization points must match JSON `children` and prompt child-interaction rules.

---

## Minimum result of a good verification loop

A good verification loop must ultimately produce:
- a stable implementation prompt;
- a reproducible node implementation;
- a transparent mismatch summary;
- a clear escalation path;
- no hidden drift between spec, prompt, project-local TOP artifacts, code, and runtime behavior.
