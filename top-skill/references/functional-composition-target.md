# Functional Composition Target

Materialization guidance for TOP branches deployed to targets where a branch's
view output is represented as an opaque composable value — an opaque typed view handle
that the parent controller holds, passes, and places without inspection.

This file describes how existing TOP semantics materialize in functional
composition targets. It does not introduce new architectural rules. All canonical
TOP rules apply unchanged; this file provides target-specific materialization form.

See `references/target-adaptation-layer.md` for the general target adaptation
workflow. See Rule 23 in the core skill file for the canonical opaque view handle
placement rule that FC-1 materializes.

---

## FC-1. Opaque typed view handle placement

In a functional composition target, a child branch's view output is a first-class
composable value: an opaque typed handle that the parent controller can hold, pass,
and assign to a named typed field in `IContentAccess`.

The parent controller:
- instantiates the child branch;
- receives or holds the child's opaque view handle;
- assigns it to a named, explicitly typed field in `IContentAccess`.

Content:
- receives the handle as a typed field;
- places it into the layout at the position designated by the controller;
- must not inspect the handle, read from it, attach listeners to it, or pass it
  outside the branch boundary.

This is the functional-composition-target materialization of Rule 23 (opaque view
handle placement through parent-owned materialization). The semantics are identical
to the canonical rule; only the concrete form of the handle changes with the target.

The handle must remain opaque throughout its lifetime in content. Treating it as
anything other than a placement unit is a content boundary violation.

---

## FC-2. Thin framework-boundary file

Certain deployment frameworks require specific files to exist at fixed structural
paths — routing entries, module entry points, or platform application roots — that
cannot be relocated to align with the TOP branch root.

When this constraint applies, the canonical form is:

- The framework-boundary file contains only a re-export or thin delegation to the
  actual TOP branch root controller.
- The framework-boundary file is not a TOP node. It has no controller logic, no
  contracts, and no state.
- The TOP branch root remains the actual controller; the framework-boundary file is
  a framework integration adapter only.

The thin delegation must not accumulate logic. If additional logic appears in the
framework-boundary file over time, that logic must be moved into the root controller
or a child branch, preserving the framework-boundary file as an adapter only.

---

## FC-3. Forced residual responsibility

Some deployment frameworks require state, configuration, or lifecycle setup that
can only be expressed from within the execution context of the framework-boundary
file. When the framework mandates placement at that structural position, the
responsibility may be owned by the root controller of the branch whose
framework-boundary file provides the delegation entry point.

This is called forced residual responsibility.

### Requirements for declaring forced residual

A responsibility may be declared forced residual only when all of the following are
satisfied:

1. **Framework origin is documented.** The responsibility must trace directly to a
   framework constraint, not to a design preference. The constraint and its source
   must be recorded in the migration spec or implementation prompt.

2. **Mg-3 justification is satisfied.** The responsibility must also satisfy at
   least one justification in `canon/migration.md` Mg-3: it must be genuinely
   cross-cutting, framework-mandated, or a multi-branch orchestration point. Forced
   residual does not exempt a responsibility from the Mg-3 evaluation — it adds the
   framework-constraint condition on top of it.

3. **The responsibility is not a decomposition candidate.** If the responsibility
   could be moved to a child branch without losing the framework constraint, it must
   be moved.

### What forced residual is not

Forced residual is not a category of convenience. Any responsibility attributed to
this pattern without a documented framework constraint is a decomposition defect
that must be corrected.

The forced residual declaration must appear in the implementation prompt. An
undocumented responsibility remaining in the root controller does not qualify as
forced residual — it is an unjustified residual (see `canon/migration.md` Mg-3).
