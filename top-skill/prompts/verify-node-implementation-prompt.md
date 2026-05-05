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
- pass requires preserved legacy test-covered behavior to be represented in prompts and covered by TOP-compatible tests when the node belongs to a migration scope

---

Use this prompt to verify that the implementation prompt stably produces a correct node implementation.

---

## Input data

Provide:
- node spec;
- implementation prompt;
- reference implementation or expected behavior;
- Behavior Preservation Plan when applicable;
- regenerated code;
- previous mismatch reports (if any);
- current attempt number;
- maxAttempts.

---

## What to do

### 1. Compare regenerated code against node requirements
Check:
- behavior coverage;
- behavior preservation coverage for legacy test-covered requirements;
- event handling;
- state ownership;
- state transitions;
- child interactions;
- invariants;
- forbidden behavior;
- compliance with `props.dir` and expected directory placement of generated files;
- compliance with `props.sourceRoot`, canonical `top_src/` source-root layout,
  and `top/specs/` branch spec placement;
- presence and correctness of an explicit restricted access artifact for content, if content exists;
- materialization of the artifact as a named contract type, not an anonymous object shape;
- explicit typing of the constructor/factory/method parameter receiving the artifact, if the language allows;
- explicit typing of the field/reference storing the artifact, if the language allows;
- absence of empty formal protocol objects where content access to controller is permitted;
- if the content-to-controller protocol artifact is empty, explicit confirmation that this is a zero-contract implemented by the owning controller and not a separate dummy runtime object;
- confirmation that controller fields/references to content are typed through `IContentAccess`, not through the concrete Content class where the technology permits;
- confirmation that the public node/controller artifact is not itself a renderable framework component, widget, composable, render/build function, platform UI lifecycle object, or equivalent target-renderable entity;
- confirmation that documented renderable-controller waypoints remain reported as `CORE-026` and do not produce validation/final-audit pass;
- confirmation that render output is produced only by Content or adapter-side artifacts;
- confirmation that child Nodes/Controllers do not receive semantic runtime input such as parent-derived values, state, callbacks, services, props/config/options, parameter bags, or runtime argument sets (`CORE-029`);
- confirmation that shared derived fact repairs do not swap `CORE-029` and Invariant 14: no parent-derived runtime input, no duplicate child derivation from the same cross-cutting source, and an explicit typed access/update boundary or connector if the fact is shared;
- confirmation that any public runtime input object/value used to materialize Content carries exactly one value: the owning controller instance typed only as `IControllerAccess`/target-equivalent, optionally inside a target-required technical envelope;
- confirmation that Content does not receive decomposed `IControllerAccess` members as separate props/parameters/JSX attributes, method bags, facade/adapters, or inline object literals (`CORE-030`);
- confirmation that Controller does not receive decomposed `IContentAccess` members as method bags, facade/adapters, concrete Content types, platform primitives, or inline object literals (`CORE-031`);
- confirmation that `IContentAccess` is not used as a data/view-model/state/callback bag for Content;
- confirmation that `IControllerAccess` methods exposed to Content are controller-boundary methods owned by the controller, not raw imported functions, external method references, service methods, store actions, or callbacks;
- absence of controller bypass to concrete implementation;
- absence of cases where a public/base-class primitive getter is used to justify controller access to concrete implementation;
- absence of controller-side platform primitive access for anything other than implementing `getView()` or parent-owned placement/composition of an opaque child view (detection examples for DOM-like targets: `this.el`, `this.getView().classList`, `this.getView().style`, `this.getView().addEventListener`, `this.getView().setAttribute`, `querySelector`, `content.getView()`);
- compliance with `references/node-validation-rules.md`;
- preservation of Layer B semantic intent;
- confirmation that behavior extracted from migrated tests is represented in the implementation prompt;
- confirmation that each prompt requirement derived from legacy tests has preserved, adapted, replaced, or newly generated TOP-compatible test coverage;
- confirmation that discarded legacy tests have explicit behavior-level justifications;
- absence of source-platform leakage in a non-source target;
- adherence to Layer C target adaptation decisions.

### 2. Identify mismatches
Categorize them as:
- missing behavior;
- missing preserved test-covered behavior;
- wrong state ownership;
- structural mismatch;
- missing child interaction;
- platform-specific leakage;
- missing prompt representation for a migrated behavior requirement;
- missing TOP-compatible test coverage for a prompt requirement;
- invalid pass with remaining accepted core deviation (`WF-011`);
- ad hoc accepted-deviation label for a core violation with no TOP-canon-defined
  waypoint (`WF-012`);
- Node/Controller semantic runtime input (`CORE-029`);
- decomposed owner access input into Content (`CORE-030`);
- decomposed content access input into Controller (`CORE-031`);
- invalid shared derived fact repair that swaps `CORE-029` with Invariant 14 or Invariant 14 with `CORE-029`;
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
