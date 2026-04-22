# State Holder API

This document establishes the rules for state switching in TOP systems.

Goals:
- prevent ambiguous channels for changing active/opened state;
- ensure lifecycle-consistent transitions;
- preserve owner-state semantics.

---

## 1. Core Idea

State switching must not occur as an arbitrary write to a field.

If the system uses:
- `openedChild`,
- `activeChild`,
- `currentState`,
- similar owner-managed state references,

then a **single canonical switching path** must exist.

This path must be lifecycle-consistent.

---

## 2. Owner Rule

Only the state-holder owns the reference to the active/opened state child.

This means:
- the state-holder determines who is currently active;
- a child state node must not change owner-managed state via an arbitrary bypass;
- no external helper logic may silently bypass the lifecycle.

---

## 3. Canonical Switching Path

The system must have one canonical way to switch state.

Different API forms are acceptable, for example:
- `child.open()`
- `holder.openChild(child)`
- `holder.setCurrentState(child)`

But regardless of the external form, the internal semantics must be identical.
If the technology uses a setter such as `openedChild = ...`, it must not create a separate public switching semantics and must either align with the canonical lifecycle-aware path or remain an internal low-level primitive.

### Canonical requirement
No public state-switching path may bypass:
- `onClose`
- `onBranchClose`
- `onOpen`
- `onBranchOpen`

if these hooks are part of the model.

---

## 4. Lifecycle-consistent Transition

When switching state, the order must be consistent and predictable.

Typical lifecycle order:

1. determine old state;
2. if old state exists and differs from new state:
   - perform close of old state;
   - perform branch-close propagation, if the model requires it;
3. record new state as the owner-managed active/opened child;
4. perform open of new state;
5. perform branch-open propagation, if the model requires it.

The exact set of hooks may differ, but:
- the order must be uniform;
- different switching paths must not carry different semantics.

---

## 5. Child-triggered Switching

If a child node triggers switching via `open()` or a similar method,
this is acceptable only if:

- the child does not bypass owner semantics;
- the call leads to the same lifecycle-consistent path as switching through the holder API;
- there is no second, incompatible semantics for the same action.

Otherwise a dual switching model arises:
- one through the owner API;
- another through direct internal mutation.

This is not acceptable.

---

## 6. Setter Semantics

If a setter such as:
- `openedChild = ...`
- `activeChild = ...`
- `currentState = ...`

is used, it must be explicitly defined whether the setter is:
- a canonical lifecycle-aware API;
- or an internal low-level primitive.

These two modes must not be mixed implicitly.

### If the setter is canonical
Then it must:
- close the old state;
- open the new state;
- trigger branch lifecycle, if that is part of the model.

### If the setter is low-level
Then:
- it must not be used as a public switching path;
- the public API must go through a separate lifecycle-aware method.

---

## 7. `open()` / `close()` Semantics

If a child state node has `open()`:
- `open()` must not silently bypass the owner lifecycle;
- `open()` must not create a separate state management model;
- `open()` must either delegate to the holder API or be part of the same canonical mechanism.

If a child state node has `close()`:
- `close()` must also not destroy owner semantics;
- it must be clear what close means:
  - close itself;
  - reset the holder reference;
  - transition to default state;
  - or perform some other canonical transition.

---

## 8. `isOpened()` / `isActive()` / `isBranchOpened()`

State predicates must have stable and clear semantics.

### 8.1. Explicit contract
The following must be clearly captured:
- whether these are methods or properties;
- exactly what they check;
- whether they include ancestor-owned activation;
- whether they include branch-level openness.

### 8.2. Inadmissible ambiguity
The following situations must not be allowed:
- in one place `isOpened` is used as a method;
- in another as a field/property;
- `isBranchOpened()` actually depends on implicit traversal logic;
- different helper functions interpret "opened" differently.

### 8.3. Recommended rule
State predicates must be:
- uniform;
- side-effect free;
- separate from lifecycle mutation logic.

---

## 9. Branch Lifecycle

If the model distinguishes:
- local open/close;
- branch open/close;
- ancestor-induced close;
- descendant-induced open,

this must be formalized explicitly.

For example:
- `onClose()`
- `onOpen()`
- `onBranchClose(node)`
- `onBranchOpen(node)`

Then the following must be defined:
- when each hook is called;
- in what order;
- who the initiator is;
- whether hooks may be called directly.

For branch hooks, the canon fixes only the semantic meaning of the extension point.
Automatic branch-wide propagation is not required to exist in the base implementation and must be explicitly defined in a specific subclass/policy.
When propagation is used, `node` denotes the branch-root that opened or closed itself and from which the event propagates down through its subtree.

Directly calling lifecycle hooks outside the canonical transition path is not permitted.

---

## 10. What Counts as a Violation

### 10.1. Lifecycle bypass
The active/opened child is changed by direct write to the owner field,
while lifecycle hooks are partially or fully skipped.

### 10.2. Dual switching semantics
One API path triggers the lifecycle;
another performs direct mutation.

### 10.3. Ambiguous ownership
It is unclear who owns the active/opened reference:
- holder,
- child,
- helper,
- external controller.

### 10.4. Inconsistent state predicates
`isOpened`, `isActive`, `isBranchOpened` are interpreted differently in different places.

### 10.5. Hidden branch rules
Branch open/close propagation exists but is never explicitly described.

---

## 11. What an Implementation Prompt Must Capture

If a node participates in state switching, the prompt should, where possible, explicitly specify:
- who the state-holder is;
- who the state children are;
- what the canonical switching path is;
- which hooks are required;
- what the lifecycle order is;
- how `isOpened()` / `isBranchOpened()` and similar predicates are interpreted.

Otherwise the next AI will easily produce an incompatible implementation.

---

## 12. Short Rule

State switching must go through **one** lifecycle-consistent mechanism.

There must not be two different truths:
- the "official" one through holder lifecycle;
- and the "quick" one through direct mutation.
