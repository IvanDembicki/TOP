# Naming Conventions

Naming rules for TOP projects.

---

## Base class

The base class for all nodes is called `TreeNode`.

The name `Node` is not used — it is reserved on many platforms.

---

## Spec and class correspondence

The node type in the spec matches the class name without the `Node` suffix:

```
spec type: "TreeItem"   →   class: TreeItemNode
spec type: "NodeIcon"   →   class: NodeIconNode
```

---

## Node names

All nodes are named with the `Node` suffix.

```
TreeItemNode          ✓
TreeItemComponent     ✗
```

---

## Implementation artifact naming

TOP fronts must refer to implementation artifacts by an extensionless artifact stem.
The `.top` segment is the TOP marker and belongs to the stable artifact name:

```text
tree_item.top
```

Concrete generated files add a target-platform extension during materialization:

```text
tree_item.top.*
```

Implementation prompts, tree specs, and other platform-neutral TOP fronts must not
hardcode a concrete language extension such as `.js`, `.ts`, `.tsx`, `.swift`,
or `.dart` when naming the implementation artifact.
