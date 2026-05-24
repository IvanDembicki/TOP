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
- a valid state-holder always has exactly one opened child;
- if no state was explicitly selected, the first state child is the default
  opened child;
- if there are no state/candidate children, the node is not a switchable
  state-holder;
- `openedChild` absence is a construction/lifecycle error, not a normal value
  to handle during active behavior propagation;
- a child state node must not change owner-managed state via an arbitrary bypass;
- no external helper logic may silently bypass the lifecycle.

---

## 3. Canonical Switching Path

The system must have one canonical way to switch state.

The public switching request targets the child state node that is being opened:

- `child.open()`

The child may override `open()` to run its own opening protocol, validation, or
pre-delegation behavior. That protocol must not be bypassed by external code.

The holder still owns the `openedChild` reference. The only valid direct use of
the holder commit primitive is from the opened child's `open()` implementation:

```text
parent.openChild(this)
```

`openChild(...)` must not become a competing public switching API that allows a
caller to force some other child open while skipping that child's own `open()`
contract. Calls such as `holder.openChild(target)`, `this.openChild(target)`, or
`parent.openChild(otherChild)` are not valid public switching requests.

If the technology uses a setter such as `openedChild = ...`, it must not create
a separate public switching semantics and must remain an internal low-level
primitive or participate only inside the same lifecycle-aware commit path.

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
   - call `onClose()` on the old state;
   - perform branch-close propagation, if the model requires it;
3. record new state as the owner-managed active/opened child;
4. call `onOpen()` on the new state;
5. perform branch-open propagation, if the model requires it.

The exact set of hooks may differ, but:
- the order must be uniform;
- different switching paths must not carry different semantics.

---

## 4a. Active-State Operation Delegation

State holders own the active/opened state reference. For any operation or query
whose meaning is "answer according to the currently active state", the holder
must delegate to `openedChild` only.

Canonical form:

```text
return openedChild.operation(args)
```

The holder must not loop over all state children, ask closed sibling states for
active behavior, or branch on mode/status/phase to decide which behavior should
answer. A closed sibling is retained state, not part of the active behavior
surface.

The holder also must not implement active-state behavior through ask-then-handle
preflight, such as probing `canHandle`, `hasCapability`, or `isInteractive` on
state children and then choosing a child from that result. It delegates the
operation/query to the non-null `openedChild`; the state child owns result,
no-result, no-op, or deeper delegation.

Each state child owns its own response policy. For example, a non-interactive
state returns a no-result value; an editing state may expose editing targets; a
display state may expose display targets. The holder and external traversal
mechanisms do not encode that taxonomy.

Nullable opened-child fallback is forbidden for active-state operations. The
state selection mechanism must establish an opened child before active
propagation begins. No-result belongs to the state child's answer, not to a
missing `openedChild`.

This rule is not limited to pointer hit-test. It applies to active-state target
lookup, event routing, active command availability, active capability checks,
and active output requests. Explicit all-state introspection or persistence is
allowed only when declared as non-behavioral metadata/validation logic.

---

## 5. Child-triggered Switching

Switching is normally child-initiated through `open()` or a semantically
equivalent child-side method. This is acceptable only if:

- the child does not bypass owner semantics;
- the child delegates the state commit to the owning holder by calling exactly
  `parent.openChild(this)`;
- there is no second, incompatible semantics for the same action.

Otherwise a dual switching model arises:
- one through the child `open()` protocol;
- another through a direct owner-side commit or mutation.

This is not acceptable.

---

## 6. Setter Semantics

If a setter such as:
- `openedChild = ...`
- `activeChild = ...`
- `currentState = ...`

is used, it must be an internal low-level primitive inside the
`parent.openChild(this)` commit path.

It must not be used as a public switching path. Public switching goes through
the child state node's `open()` method.

---

## 7. `open()` Semantics

If a child state node has `open()`:
- `open()` must not silently bypass the owner lifecycle;
- `open()` must not create a separate state management model;
- `open()` may run child-owned opening protocol before delegation;
- `open()` must delegate the final state commit to the holder-owned canonical
  commit path by calling exactly `parent.openChild(this)`.

A switch/state node must not expose `close()` as a public state-switching API.
Closing a previously opened state is an owner-side lifecycle effect of opening
another child. The holder calls `onClose()` on the outgoing child inside the
canonical commit path.

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

### 10.6. Nullable opened child
A switchable holder treats missing/null `openedChild` as a normal runtime case,
or active behavior uses nullable opened-child fallback instead of repairing
state selection.

### 10.7. Mixed child policy
A node mixes switchable state-holder semantics with a generic runtime/library
collection child policy. Runtime/library collection children do not make a node
switchable unless they are explicitly modeled as the switchable candidate set
with one selected/opened child.

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
- the "official" one through the child `open()` request and holder commit;
- and the "quick" one through direct mutation.
