# Review Checklist

This checklist must be applied before any result is considered final.

## Core rule

A result is not valid until all checklist items pass.

---

## 1. Canon compliance

- structure follows TOP canon
- no forbidden confusions present
- ownership boundaries are explicit

---

## 2. Validation completeness

- all required validations executed
- no skipped checks
- no softened violations

---

## 3. Typing strength

- all boundaries explicitly typed
- no implicit contracts
- no weak shape-based typing where avoidable

---

## 4. Protocol integrity

- all interactions go through protocols
- no direct implementation access
- no bypass paths

---

## 5. Lifecycle correctness

- lifecycle ownership is explicit
- no hidden retention
- no uncontrolled creation/destruction

---

## 6. Controller vs Content

- controller owns behavior
- content remains passive
- no architectural logic in content

---

## 7. Generation discipline

- no architecture changes during generation
- implementation matches model

---

## 8. Repair correctness

- only targeted fixes applied
- no unnecessary rewrite
- no new violations introduced

---

## 9. Ambiguity handling

- all critical ambiguity resolved or blocked
- assumptions explicitly stated
- no silent decisions

---

## 10. Readability

- naming is clear and descriptive
- no unnecessary abbreviations
- code is understandable to humans

---

## 11. Final status

- not just working, but canonical
- no remaining critical risks
- ready for use justified

---

## Final rule

If any item fails, result must not be finalized.
