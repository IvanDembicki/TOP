# Hybrid Systems

A hybrid system is a system in which part is implemented in TOP
and part remains in another paradigm.

The TOP part always operates independently.

---

## Two directions of integration

### TOP in a non-TOP system

A TOP tree is connected as a module to a project not implemented in TOP.

The connector implements the interface expected by the external system.
The TOP tree does not know and must not know what lies outside —
it interacts only through its connector.

```
[External non-TOP system]
         │
[Connector node]  ← adapts external calls to module interface
         │
[TOP tree]
```

### Non-TOP component in a TOP system

An external component is connected as the content of a regular node.

The node consists of a controller and content.
The content is the external component, connected as a black box.
In the spec, such a node has `props.contentType: "component"`.

```
[TOP tree]
    │
[Node]
  ├── Controller
  └── Content = external component (black-box)
```

The controller interacts with the component only through its external interface.
The internal structure of the component is inaccessible and irrelevant to TOP.

---

## Canonical rule

When integrating a TOP tree into a non-TOP system, the boundary is always established through a connector.
Direct interaction of TOP nodes with non-TOP code bypassing the connector is forbidden.

When connecting an external component into a TOP system, it is a content node.
Direct access to the component's internal implementation from the controller is forbidden.

---

## Analyzing a hybrid system

When analyzing a hybrid system, determine:
- which part of the system is implemented in TOP;
- which part remains outside TOP;
- where the boundary lies and whether it is correctly established.

Non-TOP parts are not automatically treated as violations —
the mode of each part must be explicitly identified.

## Analysis boundaries

Non-TOP parts of the system are excluded from TOP analysis.

An external component with `props.contentType: "component"` is a black box.
Its internal structure is not analyzed.

Everything beyond the connector is outside the scope of analysis
during the development of the TOP tree.

A deliberately left non-TOP part is not a violation.
