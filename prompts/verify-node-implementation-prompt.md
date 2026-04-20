# Prompt: Verify Node Implementation Prompt

agent: Validation Agent

input_contract:
- node_spec
- implementation_prompt
- regenerated_code
- current_attempt
- max_attempts

output_contract:
- decision (pass / refine-prompt / escalate)
- mismatch_list
- prompt_refinement_suggestions

rules:
- if current_attempt >= max_attempts and not stable → escalate
- pass requires full behavior coverage

---

Use this prompt to verify that the implementation prompt stably produces a correct node implementation.

---

## Input data

Provide:
- node spec;
- implementation prompt;
- reference implementation or expected behavior;
- regenerated code;
- previous mismatch reports (if any);
- current attempt number;
- maxAttempts.

---

## What to do

### 1. Compare regenerated code against node requirements
Check:
- behavior coverage;
- event handling;
- state ownership;
- state transitions;
- child interactions;
- invariants;
- forbidden behavior;
- compliance with `props.dir` and expected directory placement of generated files;
- presence and correctness of an explicit restricted access artifact for content, if content exists;
- materialization of the artifact as a named contract type, not an anonymous object shape;
- explicit typing of the constructor/factory/method parameter receiving the artifact, if the language allows;
- explicit typing of the field/reference storing the artifact, if the language allows;
- absence of empty formal protocol objects where content access to controller is permitted;
- if the protocol artifact is empty, explicit confirmation that this is a zero-contract with full prohibition of content access to controller;
- absence of controller bypass to concrete implementation;
- absence of cases where a public/base-class primitive getter is used to justify controller access to concrete implementation;
- absence of controller-side platform primitive access for anything other than implementing `getView()` or parent-owned placement/composition of an opaque child view (detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()`);
- compliance with `references/node-validation-rules.md`;
- preservation of Layer B semantic intent;
- absence of source-platform leakage in a non-source target;
- adherence to Layer C target adaptation decisions.

### 2. Identify mismatches
Categorize them as:
- missing behavior;
- wrong state ownership;
- structural mismatch;
- missing child interaction;
- platform-specific leakage;
- instability / ambiguity in prompt;
- artifact placement mismatch.

### 3. Determine whether the prompt can be fixed
If yes:
- propose precise changes to the implementation prompt.
If no:
- explain why the prompt remains unstable.

### 4. Make a decision
Output one of the statuses:
- `pass`
- `refine-prompt`
- `escalate`

### 5. Account for the attempt limit
If `currentAttempt >= maxAttempts` and stability has not been reached,
you must output `escalate`.

---

## Expected output format

1. Coverage summary
2. Mismatch list
3. Prompt refinement suggestions
4. Canonical fix direction
5. Re-validation status
6. Decision
7. Escalation note if needed
