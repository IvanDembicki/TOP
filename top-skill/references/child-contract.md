# Child Contract

A child contract is a declaration of children in the JSON description of a node.

A node can have one of two child contract modes. They are mutually exclusive.

---

## Mode 1: Static children

Static children are listed in the spec.

- created when the parent is created;
- destroyed when the parent is destroyed;
- count and types are fixed in the spec;
- may be of different types;
- may be any number.

Static is the default mode. `lib:false` is not written.

Example:
```json
{
  "type": "ProfileScreen",
  "children": [
    { "type": "Avatar" },
    { "type": "UserInfo" },
    { "type": "ActionPanel" }
  ]
}
```

---

## Mode 2: Dynamic children (lib:true)

If a node creates children through a library, a single lib entry is declared in the spec.

Rules:
- exactly one lib entry;
- no other children alongside it;
- the lib entry declares the base type;
- all runtime instances inherit from this base type;
- there may be any number of concrete subclasses.

### Children array

A node with `lib:true` must have an array for storing created instances.

The array is typed by the base lib type:

```ts
children: NewsItem[] = [];
```

Concrete subclasses (`TextNews`, `VideoNews`, `PictureNews`) are stored
in this array via the base class type.

The absence of a children array on a node with `lib:true` is a model violation.

### Example

Spec:
```json
{
  "type": "NewsFeed",
  "children": [
    { "type": "NewsItem", "lib": true }
  ]
}
```

Runtime: `TextNews`, `VideoNews`, `PictureNews` are created — all inheriting from `NewsItem`.
`NewsFeed` knows only the base type and stores instances in `NewsItem[]`.

---

## Canonical rule

The two modes are not mixed.

If `lib:true` is present — there are no other children.
If children are static — `lib:true` is not used.

---

## Violations

| Violation | Description |
|-----------|-------------|
| Mixed contract | `lib:true` and static children at the same time |
| Two lib entries | more than one `lib:true` on a single parent |
| Inheritance violation | a runtime instance does not inherit from the declared lib type |
| Missing children array | a node with `lib:true` has no typed instance array |
| Undeclared child | a node creates children not declared in the spec |
