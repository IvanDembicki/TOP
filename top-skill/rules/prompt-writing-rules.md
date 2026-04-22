# Prompt Writing Rules

Rules for writing prompts for nodes of a TOP tree.

---

## Primary quality criterion

A prompt is considered complete if it allows **recreating the node's behavior on another platform** without referring to the existing code.

This means:
- a developer using React, SwiftUI, or any other stack must understand all behavior from the prompt;
- the existing code is one possible implementation of the prompt, but not the only one.

Completeness test: close the code and try to answer the question — "Is it clear from the prompt how this node behaves in every situation?"

---

## Spec consistency requirement

The prompt **must not contradict** the JSON spec.

- JSON spec — the source of truth for **structure**: node type, children, props, contentType.
- Prompt — the source of truth for **behavior**: lifecycle, events, delegations, invariants.

If a contradiction arises between spec and prompt — this is a spec/prompt conflict requiring explicit resolution.

---

## Core rule: WHAT, not HOW

The prompt describes the **observable behavior** of the node, not the mechanism of its implementation.

Test: ask the question — "Does this describe WHAT happens, or HOW it is implemented?"

- Describes **WHAT** → allowed in behavioral sections
- Describes **HOW** → allowed only in the "Platform implementation notes" section


## Semantic UI layer requirement

Behavioral sections are Layer B inputs. They must describe semantic intent, not source-platform primitives.

For UI/content-facing behavior, prompts must capture the relevant semantic categories:

- structure role;
- interaction intent;
- feedback intent;
- layout intent;
- state model;
- constraints;
- accessibility semantics.

The vocabulary is open. A term is valid only if it represents platform-independent meaning and can be mapped to more than one target.

Platform artifacts found while migrating or auditing a prompt must be converted into semantic meaning. They may appear only in `Platform implementation notes` as source evidence or current-target notes, never as portable behavior.
## Platform-neutral behavior and platform notes

Behavioral sections must remain platform-neutral. They describe the node semantics that must
survive transfer to another technology: responsibility, abstract inputs/events, state ownership,
lifecycle, child interaction, side effects, constraints, invariants, and non-goals.

`Platform implementation notes` are the only section where technology-specific details may appear.
They are notes for the current implementation target, not portable behavior requirements.

When a prompt is reused for another technology:
- platform notes may be read as explanatory context;
- platform notes may help identify edge cases, implementation pressures, and likely pitfalls;
- platform notes must not be copied mechanically into the new technology;
- the generator must make an independent target-appropriate implementation decision.

Example: a React note about a host element, `createRoot`, or synthetic/native event behavior
may explain why the current implementation is shaped a certain way. A SwiftUI, Flutter, DOM,
or other target must not imitate that mechanism unless it is the correct native mechanism
for that target.

## Definition of a platform-dependent element

A prompt element is platform-dependent if its meaning requires knowledge of a specific technology, language, or runtime — and if changing the platform would require rewriting that element.

TOP paradigm elements are platform-independent by definition and are allowed in any prompt section.

## Two levels — allowability

| Level | Examples | Allowability |
|---|---|---|
| **TOP paradigm** (platform-independent) | holder, state, switchable, ownership, lifecycle, controller, content, node, openedChild, findUpByType | Any section |
| **Platform** | DOM, HTML tags, CSS properties, specific language APIs, runtime specifics | Only "Platform implementation notes" |

## Prompt structure

Required sections (behavioral, platform-neutral):

1. **Node identity and role** — the node's role in the tree, its type (leaf, holder, state, etc.)
2. **Responsibility** — what it is responsible for
3. **Inputs and events** — what it receives, what it reacts to (in abstract terms)
4. **State ownership** — what it owns, what does not belong to it
5. **Child interaction rules** — how it interacts with child nodes
6. **Lifecycle** — when created, activated, deactivated, destroyed
7. **Side effects** — side effects (in abstract terms)
8. **Constraints and invariants** — what must always be true
9. **Non-goals** — what it explicitly does not do

Optional section:

10. **Platform implementation notes** *(optional)* — platform-specific implementation details. The content of this section is not carried over mechanically when changing platform; it may only be used as context for an independent target-specific decision.

## Completeness requirement

The prompt must be sufficient to restore the current behavior of the node.

Completeness check — all of the following aspects must be covered:

- All public methods and their semantics
- All lifecycle hooks (onOpen, onClose, refresh, etc.; onBranchOpen, onBranchClose — if the subclass uses them)
- All conditions for state or visibility changes
- All delegations to other nodes (to whom, under what condition)
- All invariants (what must never happen)

## Requirements by node type

### Switchable node

Must describe:
- whether the switchable node is fixed or dynamic;
- the switching condition (when and who initiates the openedChild change);
- which child is the default, fallback, or initial selected/opened child;
- what happens on onOpen of each child or candidate type;
- what happens on onClose of each child or candidate type;
- for dynamic switchable: candidate child type policy, candidate-set source of truth, selected-child source of truth, create/remove lifecycle, and behavior when the opened child is removed;
- whether branch hooks (onBranchOpen/onBranchClose) are used, and if so — who calls them and under what traversal policy;
- who is the owner of switching (controller, not content and not the state node itself).

### Node with content (contentType is present)

Must describe:
- what is the content and what is the controller;
- what role the content plays (view / component / data / other);
- what content/view receives from controller via `IControllerAccess` and why the full public node surface is not available;
- what controller receives from content via `IContentAccess` (if anything);
- what content is not allowed to do independently;
- if the node is visual, exactly how the view-part receives child visual content through `IControllerAccess`;
- whether the node is an ordinary visual node with named child-view endpoints or a `DynamicCollectionViewNode`;
- if it is an ordinary visual node, exactly which named child-view endpoints are available and why the view does not iterate `children`;
- if it is a `DynamicCollectionViewNode`, exactly which direct child collection counts as the collection boundary, why it is homogeneous, and what its order is.

### Lib:true node

Must describe:
- who creates instances and under what condition;
- the base type of instances;
- instance lifecycle: when created, when destroyed;
- how the parent manages the collection (create / remove / reorder).

### Mutable container

Must describe:
- what is the source of truth for the content;
- re-init semantics: replace or append;
- cleanup policy on child removal.

---

## Rule: access to child nodes

### Static child (created at build time, never removed)

- Stored in a private field
- Accessed via the private field, not via search
- A public getter is not needed

### Dynamic child (collection of same-type nodes, lib:true)

- Navigation via positional properties: firstChild, lastChild, getChildAt(i), length
- Search by type does not apply — there are many nodes of the same type

#### findDownByType — special case

Allowed only when:
- children are different subclasses of the same type;
- it is necessary to find the first one of a specific type.

Even in this case, the search must be shallow (direct children only, not deep).

### Invariant

Child nodes are implementation details. The public interface of a node consists of behavioral methods and properties, not references to internal nodes.

---

## Forbidden prompt patterns

The following phrases and descriptions are architectural violations and must not appear in any prompt section (including "Platform implementation notes"):

### Self-mounting language (violation of Parent-Owned Materialization Invariant)

❌ `onOpen(): mounts own view into parent X content area`
❌ `onOpen(): appends el to parent.el`
❌ `onClose(): removes own el from parent`
❌ `Appended to parent.el during construction`
❌ Any form of "child attaches itself into parent"

✓ Correct form: `onOpen()` is called by the parent when this node becomes the active child. The parent controls view placement; this node only exposes its view through `getView()`.

If the node is responsible for managing its own DOM tree (detach/reattach), that is an internal operation — it must not extend to inserting itself into an external parent container.

### Merged lifecycle description (violation of Phase Separation Invariant)

❌ `On construction: creates el, creates children, mounts view, wires events`
❌ `Constructor: builds content, initializes children, opens default state`

✓ Correct form: describe construction, content materialization, child materialization, and `onOpen()` as separate semantic lifecycle steps, each with its own role. A target implementation may materialize one or more phases inside a constructor or another platform-native method, but the prompt must still make the phase responsibilities explicit.

### Missing content class for node with contentType (violation of Content Materialization Invariant)

❌ For a node with `contentType: "view"` in spec: prompt describes `el = document.createElement(...)` in the controller without mentioning a separate content class.

✓ Correct form: for every node with `contentType`, the prompt must describe the content class — its name, what it owns, what platform structure it creates, and how it is accessed through `IContentAccess`.

---

## Self-check before finalizing the prompt

Before considering the prompt ready, verify:

- [ ] All public methods are described with their semantics
- [ ] All lifecycle hooks are covered (onOpen, onClose, refresh; onBranchOpen, onBranchClose — if used)
- [ ] All conditions for state or visibility changes are described
- [ ] All delegations to other nodes are described
- [ ] All invariants are described (what must never happen)
- [ ] The prompt contains no platform-dependent details outside "Platform implementation notes"
- [ ] Platform notes are written as target-specific notes, not as portable behavioral requirements
- [ ] Platform notes do not instruct another technology to copy the current technology's mechanism mechanically
- [ ] UI/content semantics are described as platform-neutral roles, intents, feedback, layout intent, constraints, and accessibility semantics where applicable
- [ ] Platform artifacts have been converted to semantic meaning or quarantined as current-target notes
- [ ] The prompt does not contradict the JSON spec (type, children, props)
- [ ] The prompt is sufficient to implement on another platform without referring to the code
- [ ] The prompt does not describe self-mounting behavior in onOpen or any lifecycle hook
- [ ] Lifecycle phases (construction, content materialization, child materialization, activation) are described with separate responsibilities, even if the target implementation materializes them inside one platform-native method
- [ ] If the node has contentType, the prompt describes a separate content class

---

## Examples (correct / incorrect)

```
✗  Creates a <div class="tree-item-row"> as this.el
✓  Creates a block container element representing the item row

✗  el.style.display = 'none' when not in edit mode
✓  Hidden when not in edit mode

✗  addEventListener('dragstart', ...) forwarded to parent
✓  Drag start event forwarded to ancestor TreeItem

✗  cursor: grab style
✓  Visual affordance indicating the element is draggable

✓  Switches openedChild to EditState when isEditMode is true   ← TOP paradigm, allowed
✓  Uses findUpByType to locate ancestor TreeEditor              ← TOP paradigm, allowed
```
