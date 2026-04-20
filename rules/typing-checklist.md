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

### 1. Parent parameter in the constructor

**What to check:**
Each node accepts a parent in the constructor. The type of parent must be declared as a concrete type — the one that actually creates this node.

**Insufficient:** generic base node type — it carries no information about the architectural position of the node.
**Sufficient:** concrete parent type (e.g., TreeItemRowNode).
**Acceptable:** union type, if the node is genuinely created by multiple different parents.

Violation signal:
- The parent parameter has no declared type
- The type of parent is declared as a generic base node type

*Platform implementation notes: in JavaScript/JSDoc — `@param {ConcreteType} parent`; in TypeScript — `parent: ConcreteType`.*

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
