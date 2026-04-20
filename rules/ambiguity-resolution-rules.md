# Ambiguity Resolution Rules

This file defines how ambiguity must be handled across the TOP agent pipeline.

## Core rule

Critical ambiguity must never be silently absorbed into architecture, code, or validation conclusions.

## What counts as critical ambiguity

Ambiguity is critical if it can change any of the following:

- task type
- ownership
- controller/content boundary
- protocol boundary
- lifecycle responsibility
- typing contract
- architectural role of an artifact
- validation outcome

## What counts as non-critical ambiguity

Ambiguity may be considered non-critical only if it does not affect:

- canonical structure
- ownership
- protocol design
- lifecycle
- validation status
- handoff decision

Non-critical ambiguity must still be documented if it remains visible in the result.

## Required behavior

When ambiguity exists, the responsible agent must:

1. identify it explicitly;
2. state why it matters or does not matter;
3. separate resolved points from unresolved points;
4. mark unsafe assumptions as unsafe;
5. block the next stage if the ambiguity affects canonical structure.

## Forbidden behavior

Agents must not:

- silently pick the easiest interpretation;
- replace ambiguity with industry convention;
- hide ambiguity behind vague wording;
- continue generation when architecture is still ambiguous;
- finalize a result whose validity depends on unconfirmed assumptions.

## Resolution priority

Resolve ambiguity using the following priority order:

1. canon
2. validation rules
3. contracts
4. existing project context
5. explicit user instruction

If ambiguity remains unresolved after these sources, the affected stage must stop.

## Assumption rule

Assumptions are allowed only when all of the following are true:

- the assumption is explicitly marked;
- the assumption does not alter canonical structure;
- the assumption does not downgrade typing, ownership, or protocol clarity;
- the assumption does not affect final validity.

If any of these conditions fail, the assumption is unsafe and the stage must be blocked.

## Output requirement

Any ambiguity-handling output must distinguish:

- resolved ambiguity
- unresolved ambiguity
- safe assumptions
- unsafe assumptions
- impact on next stage

## Final rule

A result is not safe to finalize if unresolved ambiguity can affect architecture, validation, or canonicality.

## Project context constraint

`Project context` is considered a valid basis for resolution only if at least one of the following conditions is met:

- an explicit artifact exists in the `top/` directory
- an explicit user instruction exists in the current session
- a canonical precedent exists in the same tree
- an already approved artifact exists in the current pipeline that can be referenced explicitly

The following do not count as valid `project context`:
- general assumptions about the project
- implicit expectations about team style
- familiar decisions from other projects
- "this is probably what was meant"
- conclusions that cannot be tied to a specific artifact or explicit instruction

If `project context` cannot be stated explicitly and precisely:
- it cannot be used as a basis for ambiguity resolution
