# Typing Checklist

An operational checklist for verifying typing.

Each item is a specific point in the code that the agent must check.

The principle in `canon/core-axioms.md` (Typing, Typing fallback hierarchy) remains normative.
This file is its operationalization.

---

## Platform-independence rule

The checklist itself is platform-independent: it describes **what** must be typed.
**How** to express this in a specific technology — is covered in the "Platform implementation notes" section of each item.

Typable elements are ownership and responsibility boundaries in the tree.
They exist in any TOP paradigm implementation regardless of platform.

---

## Checklist

### 1. Parent parameter in the Node constructor

**What to check:**
Each Node constructor receives exactly one semantic argument: its parent reference.
The type of parent must be declared as a concrete type — the one that actually creates this node.

For the root node only, the parent may be `null` or a special `RootContext`.
`RootContext` is a root ownership/bootstrap marker only. It must not carry application data,
callbacks, services, stores, child instances, view fragments, tokens, or arbitrary props.

**Insufficient:** generic base node type — it carries no information about the architectural position of the node.
**Sufficient:** concrete parent type (e.g., TreeItemRowNode).
**Acceptable:** union type, if the node is genuinely created by multiple different parents.

Violation signal:
- The parent parameter has no declared type
- The type of parent is declared as a generic base node type
- The constructor receives additional semantic arguments beyond the parent
- RootContext carries data/services/callbacks/stores/fragments instead of only root ownership/bootstrap context

*Platform implementation notes: in JavaScript/JSDoc — `@param {ConcreteType} parent`; in TypeScript — `parent: ConcreteType`.*

---

### 1a. Content/View constructor access parameter

**What to check:**
Each concrete TOP Content/View public constructor receives exactly one semantic argument:
a narrow typed access interface implemented by the owning Node/Controller.

The constructor parameter, stored field, and all Content/View references must be typed
as the access interface, not as the concrete controller class. The runtime object must
be the owning controller instance, but Content/View must not import, reference,
inspect, or downcast to the concrete controller type.

If the access interface has no permitted methods, it is an empty zero-contract
implemented by the owning controller. It must not be replaced by a separate dummy
runtime object such as `ControllerAccessZero`.

Violation signal:
- Content/View constructor has no declared access-interface type
- Content/View constructor is typed as the concrete controller class
- Content/View constructor has additional semantic parameters: data, callbacks, handlers, flags,
  state, stores, services, child components, slots, platform child views, child view handles,
  child-output getter bundles, view-model objects, config/options/props-like objects,
  parameter bags, runtime argument sets, prebuilt fragments, or arbitrary props
- The same semantic inputs are moved to any public runtime parameter, render/build parameter,
  component/native/platform field, composition mechanism, or other technology-specific entrypoint
- An externally assembled access bundle is passed instead of the owning controller typed as the owner access interface
- Content/View imports or downcasts to the concrete controller type
- A separate dummy zero-access object is passed instead of the owning controller typed as the zero-contract interface

*Platform implementation notes: internal platform/base constructor mechanics inside the Content/View implementation are allowed when they are not public TOP constructor inputs and do not become semantic injection channels.*

---

### 1b. Controller access to Content/View

**What to check:**
If a node has a separate content class/object, the controller stores and uses it
through a narrow `IContentAccess` or target-equivalent interface.

The controller field/reference must not be typed as the concrete Content/View class
when the technology can express a narrower boundary. This is especially important
when content wraps a platform component, native view, widget, or third-party object
with many public methods; the controller is allowed to see only the methods exposed
by `IContentAccess`.

Violation signal:
- Controller field is typed as the concrete Content/View class instead of `IContentAccess`
- Controller calls methods that are public on the concrete content class but absent from `IContentAccess`
- Concrete content implementation details are exposed to controller code through typing

*Platform implementation notes: if the target language cannot hide the concrete runtime object completely, use the strongest available interface, protocol, abstract class, adapter, or wrapper boundary and document the fallback.*

---

### 2. Return types of getters and methods

**What to check:**
All getters returning child nodes or related objects must declare a concrete return type.

Generic base node type — insufficient if a concrete subtype is actually returned.

Violation signal:
- Return type is not declared
- Declared as a base type where a concrete subtype is returned

*Platform implementation notes: in JavaScript/JSDoc — `@returns {ConcreteType}`; in TypeScript — `: ConcreteType`.*

---

### 3. Field declarations

**What to check:**
All class fields storing references to nodes, data, or state must have an explicitly declared type.

Special attention to:
- Fields storing references to child or sibling nodes
- Fields with model data (e.g., `data`)
- State fields (flags, modes)

Violation signal:
- Field declared without a type
- Type declared as `Object`, `any`, or equivalent — when a more concrete type is available

*Platform implementation notes: in JavaScript/JSDoc — `/** @type {ConcreteType} */` before the field; in TypeScript — `field: ConcreteType`.*

---

### 4. Content-facing protocol parameters

**What to check:**
The interface between controller and content (ContentFacing or equivalent) must be explicitly typed.
An empty interface is allowed only if documented as an intentional zero-access contract.

Violation signal:
- ContentFacing or equivalent has no declared type when passed
- Passed as an untyped object

---

### 5. Explicit type casts on tree search

**What to check:**
Calls to `findUpByType`, `findDownByType`, `findDeepByType` return a base type.
The result must be immediately cast to a concrete type.

Violation signal:
- Search result used without explicit cast to a concrete type
- Cast performed to a generic base node type instead of a concrete one

*Platform implementation notes: in JavaScript/JSDoc — inline cast `/** @type {ConcreteType} */ (expr)`; in TypeScript — `as ConcreteType`.*

---

## Application rule during analysis

An agent performing analysis must sequentially go through each checklist item for each file.
Behavioral analysis (pattern-recognition.md) and typing analysis are independent passes.
The absence of behavioral violations does not imply the absence of typing violations.
