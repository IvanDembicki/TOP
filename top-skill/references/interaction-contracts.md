# Interaction Contracts

## Access model

Node access in TOP is divided into three categories:

- **Guaranteed access** — non-nullable, typed, no search required.
- **Search access** — nullable, result is not guaranteed by the structure.
- **Forbidden access** — hardcoded traversal chains that bypass the contract.

These categories are not about proximity in the tree.
They are about the basis on which access is made.

---

## 1. Guaranteed access

Guaranteed access is access to nodes whose existence is defined in advance by the architecture.

This includes:

- the direct parent node;
- statically defined child nodes;
- ancestors reachable via `findUpByType(T)` **within an architecturally guaranteed chain** — the architecture guarantees the type and existence of every node in it at all times.

Guaranteed access does not require search.
It must be typed and non-nullable.
No null checks are needed — the node either always exists or the architecture is wrong.

**Canonical form for static children:** guaranteed access to a statically defined child node
must go through a named, explicitly typed field on the parent — not through positional
accessors (`firstChild`, `lastChild`, `getChildAt(n)`).
Positional access is structurally correct but semantically opaque and fragile.
See `references/architecture-rules.md` R5a for the full rule and its exception.

**Canonical form for guaranteed ancestors:** `findUpByType()` for a guaranteed ancestor
must be called exactly once — in the constructor or init phase — and the result stored
in a named, explicitly typed field. Runtime lookup (in handlers, `refresh()`, etc.) is
forbidden even when the ancestor is guaranteed.
See `references/architecture-rules.md` R5b for the full rule, patterns, and detection rules.

**Preferred form:** always use guaranteed access where it is available.

---

## 2. Search access

Search access is access to nodes that are not structurally guaranteed to exist.

This includes:

- `findUpByType(T)` when the chain to the ancestor passes through an untyped,
  external, abstract, or runtime-dependent attachment context where the target
  ancestor's type and existence are not guaranteed. A lib node by itself does not
  break the guarantee; it breaks the guarantee only when its attachment context is
  not explicitly typed;
- `findChildByType(T)` / `findDescendantByType(T)` — a matching descendant may or may
  not exist in the current tree configuration;
- any search that depends on runtime tree state rather than architectural definition.

Search access is nullable. The caller must treat the result as potentially absent
and handle the null case explicitly.

**Rule:** search access is acceptable only where guaranteed access is impossible
or architecturally inappropriate.

Using search access where guaranteed access is available is an architectural weakness —
it hides a dependency that could be made explicit and statically safe.

---

## 3. Forbidden access

Forbidden access is any hardcoded traversal that bypasses the tree contract.

Forbidden:

- chains such as `parent.parent.parent`, `firstChild.firstChild.nextSibling`, and equivalents;
- direct access to non-adjacent nodes without going through `findUpByType` or an explicit
  structural contract;
- cross-branch access — reaching into nodes outside the direct parent-child-sibling
  boundary without a connector;
- reading global state as a substitute for tree-level access;
- accessing a sibling's concrete subtype directly (only the common parent type interface
  is permitted — see `references/architecture-rules.md` R6).

---

## 4. TOP expands the non-nullable zone

This is one of the structural advantages of TOP.

In a system without a strict hierarchy, most inter-node access requires search or
runtime lookup — and therefore produces nullable, fragile dependencies.

In TOP, the architecture itself defines which nodes exist and where.
The stricter the hierarchy, the more connections are known upfront and can be
accessed directly — without search, without null checks, without guessing.

**The goal is to maximize guaranteed access and minimize search access.**
Every time a connection that used to require search can be expressed as a
guaranteed structural contract, the system becomes more readable, safer, and
easier to generate correctly from a prompt.

---

## 5. Interaction boundary

A node's interaction universe is bounded:

| Category      | Access type         | Notes                                          |
|---------------|---------------------|------------------------------------------------|
| Direct parent | Guaranteed          | Always non-nullable                            |
| Static children | Guaranteed        | Non-nullable when architecturally static       |
| Ancestors     | Guaranteed or search | Guaranteed within an architecturally guaranteed typed chain, including through typed lib deployment; nullable only after the guarantee breaks |
| Descendants   | Search              | Always nullable                                |
| Siblings      | Guaranteed (via parent contract) | Only through parent type interface |
| Any other node | Forbidden          | Requires a connector if the relationship exists |

Everything outside this boundary requires an explicit connector modeled in the spec.

---

## See also

- `canon/architectural-invariants.md` — Invariant #5: Static Chain / Typed Ancestor Guarantee
- `references/architecture-rules.md` — R5 (no hardcoded chains), R5a (named fields for static children), R5b (ancestor lookup: capture-once, no runtime navigation), R6 (sibling access rules)
- `references/independent-branches-and-connectors.md` — when a connector is required
