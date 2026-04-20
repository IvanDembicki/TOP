# Three Trees

TOP distinguishes three separate tree representations.
They must not be collapsed into a single undifferentiated description.

---

## 1. Spec Tree

The formal architectural description of the system.

- Primary source of truth.
- Defines node types, composition rules, ownership, and boundaries.
- Does not contain runtime or class-level implementation detail.

---

## 2. Class Tree

The implementation-level structure derived from the spec tree.

- Maps spec nodes to concrete classes or modules.
- Preserves the topology defined in the spec tree.
- Code-level representation of architectural intent.

---

## 3. Runtime Tree

The runtime instance tree — the system as it exists during execution.

- Instantiated from the class tree.
- A runtime tree may also be a state tree if it contains at least one `state node`.
- Carries live state, lifecycle phases, and opened/closed branches.

---

## Relationships between the three trees

- **Spec → Class**: derivation. The spec defines what class must exist and where.
- **Class → Runtime**: instantiation. A class is instantiated into a live node.
- **Spec ≠ Runtime**: specification is not the same as execution instance.
- Deriving spec from runtime observation is forbidden. Runtime observation is not architectural definition.

---

## Invariant

The three trees are related but distinct.
Each level has its own type of content and its own rules.
Mixing levels — treating spec nodes as runtime instances, or using
runtime observations as spec — is a structural violation.

---

## Forbidden

- Treating spec tree and runtime tree as interchangeable descriptions.
- Collapsing class tree and spec tree into one undifferentiated layer.
- Deriving spec from runtime observation.

---

## See also

- `references/tree-model.md` — tree model and composition rules.
- `references/state-tree.md` — state tree semantics and branch state model.
