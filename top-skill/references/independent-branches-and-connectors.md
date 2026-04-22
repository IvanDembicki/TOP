# Independent Branches and Connectors

---

## Module branch

A **module branch** is a child branch of a tree representing a self-contained part of the system.

A module branch:
- has its own internal structure;
- has its own logic;
- has its own state;
- can be developed, described, and used as a separate module.

A module branch is connected to the main system not through direct knowledge of its internal
structure, but through an external **module interface**.

This allows the same module to be used in different systems
and in different contexts without changing its internal implementation.

---

## Module branch interface

A **module branch interface** is a set of methods, properties, and events through which
the module interacts with the external system.

The module interface:
- defines the boundary between the module's internal implementation and its external environment;
- is the sole point of interaction with the module from outside;
- hides the module's internal structure.

The external system interacts with the module **only through the module interface**.
Direct access to the module's internal nodes is forbidden.

---

## Module branch connector

A **module branch connector** is a tree node that acts as an adapter
between the main system and the connected module.

The connector transforms method calls, events, and data
from the main system's format into the module interface format — and vice versa.

The connector is a regular tree node.

Thanks to the connector, the same module can be embedded in different systems
without changing its internal implementation.

---

## Interaction diagram

```
Main system
      │
      ▼
[Module branch connector]
      │  (implements module interface)
      ▼
[Module branch interface]
      │  (hides internal structure)
      ▼
[Module branch]
  ├── internal node A
  ├── internal node B
  └── internal node C
```

---

## Usage rules

- The external system **does not access** the module's internal nodes directly.
- The connector **must not** penetrate inside the module beyond the interface.
- The module **must not** know about the details of the main system — only about the connector interface.
- Events from the module are passed outward through the module interface.
- Commands into the module are passed inward through the module interface.

---

## Independence of module branches

A module branch is called an **independent branch** if it:
- is developed in isolation;
- is tested in isolation;
- can be replaced by another implementation without changing the main system.

The condition for independence is strict adherence to the module interface.

---

See also:
- `references/composite-systems.md` — use of connectors in tree-of-trees systems
- `references/hybrid-systems.md` — use of connectors on the boundary between TOP and non-TOP
