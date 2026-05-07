# Agent Power Separation

This canon defines how AI-agent authority is separated in top-skill workflows
across four branches.

The executor produces artifacts.
The validator produces verdicts.
The log records both.
The canon governs all.

No agent may judge its own output. No agent may be the lawmaker, executor,
judge, and public record for the same artifact.

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
