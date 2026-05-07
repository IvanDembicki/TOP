# Validation Rejection Protocol

This protocol defines what happens when validation fails and how validation
must run incrementally.

Failed validation creates a repair obligation, not a discussion. A generator or
repair agent may repair artifacts. It may not override validation.

## Rejection ticket

When validation fails, the validator must produce a rejection ticket.

Required fields:

```text
rejection_id:
validator_agent:
phase:
artifact_under_review:
files_checked:
canon_rules_checked:
violation_code:
violation_summary:
evidence:
  - file:
  - location_or_pattern:
  - observed_problem:
why_invalid:
required_repair:
forbidden_repairs:
return_to_agent:
attempt_number:
```

Missing rejection traceability is `WF-027`.

## Rejection log entry

Every rejection must be appended by the validator to the public migration log.

The log entry must include:
- validator name;
- checked artifacts;
- violated rule;
- exact evidence summary;
- required repair;
- forbidden repair strategies;
- repair target agent;
- attempt number.

The migration log records chronology and evidence references. It is not a
replacement for the rejection ticket or validation evidence.

## Generator Learning Ledger

A validation rejection is a branch-local negative training example.

After the first validation rejection in a migration branch, the branch must have:

```text
top/migration/<branch-id>/GENERATOR_LEARNING_LEDGER.md
```

Each rejected strategy entry must use this shape:

```text
## Rejected Strategy <N>

Source:
Violation code:
Artifact:
Rejected strategy:
Why rejected:
Canon rule:
Forbidden from now on:
Required replacement pattern:
Applies to:
Repair attempt:
Validator result:
```

Before generating or repairing any next artifact in the same branch, the
generation or repair agent must:

1. read `GENERATOR_LEARNING_LEDGER.md` if it exists;
2. check whether the planned implementation repeats a rejected strategy;
3. avoid all forbidden strategies;
4. log that rejected strategies were applied as constraints.

Missing ledger read/update is `WF-028`. Repeating a rejected strategy is
`WF-029`.

## Repair obligation

Repair must:
- read the rejection ticket;
- repair only the rejected issues unless broader repair is required;
- avoid forbidden repair strategies;
- update the repair log;
- resubmit artifacts for validation.

Repair must not:
- repeat a previously rejected strategy;
- rename the same invalid structure;
- move the same violation to another file;
- mark a hard violation as accepted residual;
- broaden the violation into a vague migration waypoint.

## Repair circuit breaker

Canonical limits:

```text
max_repair_attempts_per_validation_gate: 3
max_same_violation_repeats: 2
```

If either limit is exceeded:

```text
status: blocked
reason: repeated validation failure
requires: human/top-skill rule update
```

Circuit breaker exhaustion is `WF-030`.

## Incremental validation rule

Validate the smallest meaningful artifact as soon as it exists.

Do not build on unvalidated architecture.

Validation has three granularities:

### Micro-check

Runs immediately after one small action or tiny artifact.

Examples:
- branch safety gate created;
- one spec node created;
- one prompt file created;
- one content/controller pair generated;
- one folder path created;
- one rejection ticket written;
- one generated file imports content.

Micro-checks may be partial and pattern-based. They catch obvious violations
early and trigger deeper validation when suspicious.

### Meso-check

Runs after a group of related actions.

Examples:
- scope discovery completed;
- decomposition proposal completed;
- spec skeleton completed;
- prompt set for a subtree completed;
- generated node group completed;
- adapter group completed.

Meso-checks validate consistency across related artifacts, topology, boundaries,
and drift.

### Macro-check

Runs after a full phase.

Examples:
- full modeling phase;
- full generation phase;
- full repair cycle;
- final integration.

Macro-checks verify whole-branch consistency, unresolved rejections, and
readiness status.

## Required migration checkpoint sequence

Migration must use this minimum sequence when applicable:

```text
git safety gate
-> micro-check: branch safety

scope discovery
-> micro-check: scope artifact exists
-> meso-check: scope boundaries valid

decomposition proposal
-> micro-check: candidate nodes have roles
-> meso-check: decomposition avoids giant nodes and wrapped legacy

spec skeleton
-> micro-check: node-like objects use type/doc/prompt/props/children shape
-> meso-check: spec tree topology valid

prompt creation
-> micro-check: each prompt has required sections
-> micro-check: prompt path matches spec
-> meso-check: prompt set is consistent with spec

generation per node
-> micro-check: generated controller/content/contracts shape
-> micro-check: no concrete content exposure
-> micro-check: no content conditionals
-> micro-check: folder path mirrors spec path

generation group
-> meso-check: controller tree composition
-> meso-check: no public wrappers around content
-> meso-check: no controller render fragments

post-generation validation
-> macro-check: full generated source architectural validation

repair cycle
-> micro-check: rejection ticket exists
-> micro-check: learning ledger updated
-> meso-check: repair did not repeat rejected strategy

final audit
-> macro-check: process, artifacts, logs, rejections, and readiness
```

## Early-warning escalation

A micro-check may return:
- PASS;
- REVIEW_REQUIRED;
- FAIL.

If a micro-check detects a suspicious pattern, it must trigger a deeper check
before the next large step.

Examples:
- large controller access surface -> decomposition review;
- public content import -> hard fail;
- public wrapper around content -> hard fail;
- generic `type: "Node"` in spec -> hard fail;
- content conditional -> hard fail;
- ambiguous black-box component -> review-required or fail;
- accepted deviation without target repair -> fail.

## Checkpoint log entry

Each checkpoint must append a compact log entry:

```text
checkpoint_id:
checkpoint_type: micro | meso | macro
phase:
agent:
artifact:
checks_performed:
result: PASS | REVIEW_REQUIRED | FAIL
if_fail:
  violation_code:
  evidence:
  required_repair:
next_action:
```

PASS entries should be short. FAIL and REVIEW_REQUIRED entries must contain
enough detail to reproduce the decision.

