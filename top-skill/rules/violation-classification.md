# Violation Classification

This file defines the mandatory separation of violation types.

## Required categories

Every analysis, validation, or audit result must distinguish:

1. `core_violations`
2. `skill_convention_violations`
3. `workflow_gaps`

---

## 1. core_violations

These are TOP Core violations.

Examples:
- ownership violation
- bypass boundaries
- protocol violation
- behavioural logic inside content
- hidden lifecycle ownership

A core violation affects architectural correctness.

---

## 2. skill_convention_violations

These are violations of skill-specific conventions, but not necessarily TOP Core itself.

Examples:
- naming convention mismatch
- file layout mismatch
- organization rules outside TOP Core
- docs / folder conventions

A skill convention violation must not automatically be treated as a TOP Core violation.

---

## 3. workflow_gaps

These are violations of the execution process.

Examples:
- missed pipeline stage
- missing output contract
- unresolved ambiguity
- missing checklist pass
- invalid task mode routing

A workflow gap relates to process validity, not to TOP Core itself.

---

## Core rule

These three categories must not be merged into a single general severity group.

If a violation belongs only to convention or workflow,
it must not be automatically marked as a TOP Core violation.

## Violation codes

All violations must be reported using canonical codes defined in:
- `rules/violation-catalog.md`

Format: `[CODE] Short description of the specific instance.`
