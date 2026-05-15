# Agent Power Separation

This canon defines how AI-agent authority is separated in top-skill workflows
across four branches.

Canonical name: **AI Separation of Powers**.

The executor produces artifacts.
The validator produces verdicts.
The log records both.
The canon governs all.

No agent may judge its own output. No agent may be the lawmaker, executor,
judge, and public record for the same artifact.

TOP workflow must separate rule-making, implementation, validation, and
reporting. When these powers collapse into one agent context, validation
becomes self-justification instead of control.

## No self-certified delivery

An agent that generated, migrated, refactored, repaired, or synchronized
artifacts may produce an executor report, but it must not be the final authority
that certifies those artifacts as valid or delivery-complete.

Delivery evidence is governed by `workflow/enforcement-evidence-model.md`.
`executionIsolationLevel` and `verificationEvidenceLevel` are separate axes and
must not be collapsed into one status.

The same agent pass must not:
- generate or repair implementation;
- validate that implementation;
- write the final audit;
- declare delivery complete.

A separate judicial validation pass is required after any executive generation
or repair pass. Delivery status may be changed to `complete` only when the
workflow has runner-enforced execution isolation, hard-check-verified validation
evidence, a valid independent judicial handoff artifact, and no required gate
with `fail` or `not_verified` status. Generation may report generation
completed; it must not report delivery completed.

Schema validation is not role isolation. Hard checks are not role isolation.
A single LLM invocation instructed to act as multiple agents is simulated
separation, not enforced separation, and cannot certify independent validation
or delivery complete.

Dishonest or self-referential validation becomes an alibi, not a check. A
validation report is invalid if it merely confirms the generator's own
interpretation without independently testing known violation classes against
the actual files.

## Legislative branch — canon and rules

The legislative branch defines the law.

It includes canon, architectural invariants, validation rules, violation
catalogs, forbidden patterns, agent contracts, output contracts, workflow
contracts, and mode manifests.

It defines:
- what is allowed;
- what is forbidden;
- what must be validated;
- what counts as evidence;
- which violations block progress;
- which status labels are legal.

Implementation, generation, migration, and repair agents must not modify the
rules they are currently being judged by. A workflow that changes canon is a
separate canon-update task, not part of validating the output of the same
generation, migration, or repair task.

If canon changes, artifacts produced before the canon change must be revalidated
against the new canon before they can be accepted.

## Executive branch — generation, migration, repair

The executive branch acts.

It includes generation agents, migration agents, implementation agents, repair
agents, and agents that modify specs, prompts, code, adapters, or migration
artifacts.

It may:
- create artifacts;
- modify artifacts;
- generate code;
- update specs and prompts;
- perform repairs;
- run mechanical checks;
- submit artifacts for validation.

It must not:
- issue final validation verdicts;
- declare its own work TOP-valid;
- claim CORE compliance;
- claim no violations;
- approve its own deviations;
- use its own rationale as evidence;
- change canon to fit generated output.

Executor reports are claims, not evidence. Executor self-validation claims are
`WF-023`.

## Judicial branch — validation and audit

The judicial branch judges.

It includes validation agents, canon precheck agents, audit agents, final audit
agents, and consistency checkers.

It must:
- validate current artifacts against current canon;
- inspect actual files, not only reports;
- cite rules checked;
- provide exact evidence;
- create rejection tickets when validation fails;
- block progression when evidence is missing.

It must not:
- trust generator explanations;
- accept generator self-checks as proof;
- treat executor-created accepted deviations as automatically valid;
- continue the generator's reasoning context;
- pass artifacts based on claims.

The validator is not a continuation of the executor. The validator is an
independent, adversarial reviewer of the artifact.

Contaminated validation context is `WF-024`. Validation without artifact
evidence is `WF-025`. Final Audit accepting unproven validation is `WF-026`.

## Public record — logs and trace

The public record preserves accountability.

It includes migration logs, validation reports, rejection history, repair
history, generator learning ledgers, forensic traces, and decision history.

It must record:
- who acted;
- which files were read;
- which files were changed;
- what was validated;
- what failed;
- why it failed;
- which rule was violated;
- what repair was requested;
- whether the same error repeated;
- whether the validator accepted or rejected the repair.

Logs are not decorative reports. Logs are accountability artifacts for the
human owner. A log entry is not itself validation proof; it is chronology and an
evidence index.

The public record branch may summarize judicial findings, but it must not
upgrade blocked, partial, or not-verified status to complete. A `complete`
status without delivery-law evidence is itself a workflow violation.

## Required judicial pass after executive work

After generation, migration materialization, spec/code synchronization, or
repair, the judicial pass must:
- read the actual generated or changed files;
- ignore `complete`, `pass`, or `fixed` claims unless independently verified;
- compare implementation against specs, prompts, and contracts;
- run explicit negative checks for known violation classes;
- report `blocked` when a blocking violation remains;
- report `not_verified` when required files or evidence are unavailable.

At minimum, post-generation or post-repair validation must explicitly check:
- Node/controller files contain no framework rendering identity such as JSX,
  widgets, composables, render/build functions, or equivalent target-renderable
  controller roles;
- locally implemented content does not import, instantiate, or type against
  child concrete content directly;
- prompt contracts match implementation contracts unless an approved
  target-specific downgrade updated the prompt/spec;
- Node/controller files do not directly access global stores, route/navigation
  hooks, UI framework hooks, runtime singleton state, or target hook APIs except
  through explicit bridge/runtime/data boundaries;
- bridge callbacks are exposed through explicit boundary contracts rather than
  raw callback injection when they cross into TOP objects;
- Expected Materialization files exist;
- route/framework adapters remain thin;
- TypeScript, lint, schema, and other mechanical checks are reported honestly,
  with out-of-scope failures separated from in-scope failures.

## Valid report evidence

A report is not valid unless it contains:
- files checked;
- commands or search checks run;
- violation classes checked;
- what passed;
- what failed;
- what could not be verified;
- whether the result is complete, partial, blocked, or not verified.

If required files are missing from the submitted archive or working copy, the
report must say `not_verified`, not `pass`.

## Claims vs evidence

Agent claims are not evidence. Artifacts are evidence.

Claims include:
- implemented successfully;
- validated;
- fixed;
- no violations found;
- matches canon;
- CORE-015 clean;
- TOP-valid;
- ready_for_use;
- validation passed.

Claims are never sufficient for validation.

Evidence includes:
- actual files;
- exact diffs;
- exact quoted fragments;
- exact search results;
- exact generated artifacts;
- validation checklists;
- rule references;
- test output;
- type-check output;
- lint output;
- schema validation output;
- audit reports with evidence;
- rejection tickets.

A validator must cite evidence for every pass/fail decision.
