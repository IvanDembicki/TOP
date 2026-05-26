# Descending Recursive Semantic Analysis

Canonical method name: **Method of Descending Recursive Semantic Analysis**.

This method migrates a legacy project into TOP by treating the current migration scope as a temporary root node, then recursively discovering and externalizing hidden semantic structure.

## Core Definition

1. Place the target application or scope inside a temporary root node.
2. Analyze the current node for a semantically independent child candidate.
3. Extract exactly one meaningful child boundary at a time.
4. Define the child responsibility, parent contract, allowed external relations, source files, and initial validation obligations.
5. Log the extraction.
6. Immediately delegate the extracted child node to an independent child agent/task when possible.
7. Continue analyzing the remaining parent content.
8. Repeat until the parent contains no further valid decomposition candidates.
9. Classify the final residual as a meaningful child, connector, black-box component, local implementation detail, or temporary residual with expiry.
10. Aggregate readiness bottom-up.

This is semantic analysis, not file splitting. Legacy files, routes, screens, classes, and framework components are evidence. They are not final TOP boundaries.

## Extraction Criteria

A child candidate is plausible when it owns at least one of:

- distinct responsibility;
- distinct lifecycle;
- state or state alternative;
- mutation authority;
- async workflow;
- external integration boundary;
- data ownership boundary;
- form, modal, list, item, card, row, panel, selector, status panel, or action panel behavior;
- reusable semantic pattern;
- bridge/adapter boundary.

Do not extract on visual proximity or line count alone.

## Child Delegation

After extraction, the child task receives:

- node path;
- source slice;
- parent contract;
- allowed dependencies;
- behavior expectations;
- active migration profile;
- checkpoint policy;
- rollback anchor;
- required output artifacts.

The child agent must not modify the parent contract directly. It may submit a contract change request.

## Parent Continuation

The parent agent continues with the remaining code. The remaining code must not become an unexamined "leftover" container.

If the final residual has no clear semantic responsibility, review earlier extractions. A meaningless residual usually means the previous boundary choices were wrong or incomplete.

## Leaf Rule

A leaf is accepted only when the agent has checked that no further TOP-worthy decomposition is justified. The leaf must report why it is irreducible:

- no independent state holder;
- no independent lifecycle;
- no hidden async workflow;
- no internal form/modal/list/item/card/row needing ownership;
- no hidden data ownership boundary;
- no reusable semantic pattern;
- no large bridge cluster;
- no giant controller surface.

Leaf claims should be checked by an independent decomposition validator in strict mode.

## Bottom-Up Readiness

A parent node becomes structurally ready only after all children report readiness and the parent has passed its local integration checkpoint.

Readiness travels upward:

```text
leaf -> parent -> sibling group -> grandparent -> root
```

Do not treat a child `done` claim as delivery evidence. It is only one input into parent readiness.
