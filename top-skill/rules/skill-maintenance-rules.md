# Skill Maintenance Rules

These rules apply when modifying top-skill itself: canon, rules, references,
prompts, agents, examples, validation wording, metadata, or release notes.

## 1. Generalize from symptom to canon

When a problem is found in a concrete output, first identify the underlying TOP
architectural failure. Do not encode the surface symptom as the rule.

Incorrect:
- forbid one target syntax because that is where the failure appeared.

Correct:
- state the platform-independent TOP ownership, lifecycle, typing, or access rule
  that the symptom violated.

## 2. Platform independence by default

TOP canon, validation rules, migration rules, and generation prompts are
platform-independent by default.

A target-specific rule is allowed only when the rule is genuinely target-specific
and is clearly marked as such.

## 3. Content before View

Use `Content` as the general category.

Use `View` only when the rule is specifically visual: `getView()`, opaque view
handles, visual placement, visual child output, or visual materialization.

Rules about constructors, ownership, lifecycle, protocol boundaries, and access
interfaces must be written for `Content` unless the rule is specifically about
visual materialization or opaque view output.

## 4. No exhaustive-looking technology lists

Do not list technologies as if the list were exhaustive.

Use general wording such as:
- any language, platform, UI framework, component model, or render/build mechanism.

If concrete examples are necessary, mark them explicitly as non-exhaustive
examples.

## 5. Update the whole rule surface

A canon change requires checking every affected part of the rule surface:
- `SKILL.md`
- `canon/*`
- `references/*`
- `rules/*`
- `prompts/*`
- `agents/*`
- `examples/*`, when examples are affected.

Do not make a single isolated rule change when surrounding validation,
generation, migration, or example text still teaches the old behavior.

## 6. Validation must become searchable

When adding a prohibition, include searchable detection terms that agents and
validators can look for.

Example terms:
- `parameter bag`
- `props-like object`
- `config/options`
- `callbacks/handlers bundle`
- `child-output getter bundle`
- `externally assembled access bundle`

A rule should be both architectural and operational.

## 7. Positive and negative form

Important rules should include:
- the correct form;
- the forbidden form;
- the violation signal.

Motivation alone is not enough for reliable repair.

## 8. Preserve ownership direction

When editing rules, preserve the TOP ownership direction:

```text
Content -> asks owner
Owner -> asks children when child output is required
Children -> expose opaque handles
```

Do not rewrite wording so that external/root/parent assembly appears to push
semantic inputs into Content.

## 9. Do not weaken canon by example

Examples must not legalize behavior that canon forbids.

If an example cannot be safely updated, mark it explicitly as legacy, known
deviation, or pending update.

## 10. Run a terminology consistency pass

After changing terminology, search for old wording and adjacent variants.

Examples:
- after generalizing `View` to `Content`, search for `View pulls`, `content/view`,
  `If content is view`, and similar phrases;
- after replacing platform-specific wording, search for old target names in the
  changed rule surface.

## 11. Do not add escape hatches

Canonical rules should use `must` and `must not`.

Avoid weakening words such as:
- usually
- prefer
- recommended
- where possible
- unless convenient
- can

Exceptions must be explicit, narrow, and justified.

## 12. Context objects are suspicious

Any appearance of `Context`, `RootContext`, `Options`, `Config`, `Props`,
`Access`, `Services`, or similar objects must be checked for a dependency
injection or semantic parameter-bag loophole.

## 13. Access interfaces are contracts, not bags

An access interface must be:
- a narrow typed contract;
- implemented by the owning controller or owning content as appropriate;
- not assembled externally as a bundle of data/functions;
- not used as a callback/data bag.

Correctly named methods do not make an externally assembled bundle valid.

## 14. AI must not patch around canon

If a repair needs a new architectural pattern, update canon/rules first or
propose the canon change explicitly.

Do not solve examples or prompts by inventing local workarounds that bypass the
model.

## 15. Release and push discipline

When the user asks to push changes:
1. check `git status`;
2. increment version;
3. update changelog;
4. run validation/tests;
5. run `git diff --check`;
6. stage only relevant files;
7. verify staged files;
8. commit;
9. push;
10. verify final branch/status;
11. report commit hash, pushed branch, changed files, and validation result.

Unrelated working-tree changes must not be silently included.

## 16. Known deviations must be explicit

If a contradiction remains after a change, do not leave it silently.

Either:
- fix it;
- mark it as known deviation;
- mark it as legacy;
- mark it as pending update with a reason.

## 17. Do not overfit to one agent failure

When one agent fails, close the class of failures, not only the exact generated
phrase.

The rule should prevent similar mistakes in other languages, targets, prompts,
and examples.

## 18. Keep rules small but load-bearing

Do not add long essays to `SKILL.md`.

`SKILL.md` should contain short mandatory invariants and links to detailed rule
files. Detailed maintenance guidance belongs in this file or another focused
reference.

## 19. Examples are secondary to canon

If an example is convenient or attractive but contradicts canon, change the
example. Do not weaken canon to preserve an example.

## 20. Search before editing

Before changing a rule, search for:
- where the rule is already described;
- nearby overlapping wording;
- validation/checklist/prompt references;
- examples that may contradict the change.

This prevents isolated edits that leave the skill internally inconsistent.

## 21. Missed case feedback loop

When a real violation, contradiction, or agent failure is discovered after a
top-skill change, do not treat it only as a local defect.

Ask:
- why did the existing rules fail to make this case obvious?
- was the rule missing, too narrow, too implicit, too platform-specific, or
  placed where agents would not load it?
- did validation, checklists, prompts, or examples lack searchable detection
  terms?
- did examples or references accidentally teach the old behavior?
- should this maintenance rule file be updated so the same class of maintenance
  mistake is less likely next time?

If the failure reveals a reusable maintenance lesson, propose an update to this
file together with the functional TOP rule change.

Do not only patch the immediate symptom. Close the rule gap that allowed the
symptom to survive.

## 22. Check for role-collapse variants

When a rule closes an access, construction, data-flow, or composition loophole,
also check whether the same failure can survive as role collapse.

Ask:
- can one TOP role be materialized as another role while the narrow access rule
  appears locally satisfied?
- can controller/content, model/materialization, adapter/controller, or
  spec/runtime identities be collapsed by target syntax?
- does validation detect both the data-flow violation and the role-purity
  violation?

If the role-collapse variant is possible, add a separate invariant or violation
code instead of hiding it under a nearby generic rule.
