# Role Packs

## Purpose

Role packs define minimal context for each pass type. They do not restate TOP
architectural canon.

## Orchestrator Role Pack

Receives workflow state, prior handoffs, mode rules, capsule formats, and
delivery gate status. It creates capsules, accepts or rejects handoffs, routes
repair loops, and controls progression.

## Context Builder Role Pack

Receives the target task, allowed role, relevant artifact references, and
context minimization rules. It builds a task capsule and must not implement,
validate, repair, or certify delivery.

## Executive Role Pack

Receives the task capsule, implementation goal, relevant source artifacts, and
output contract. It may create or modify authorized artifacts and must return a
handoff. It must not validate or certify its own work.

## Judicial Role Pack

Receives actual artifacts, validation contracts, required hard-check evidence,
and violation classes. It validates current files and returns a verdict
handoff. It must not repair implementation artifacts.

## Repair Role Pack

Receives validation failures, exact repair scope, relevant canon slice, and
output contract. It performs only the scoped repair and returns a handoff. It
must not revalidate its own repair.

## Reporting / Certification Role Pack

Receives handoff records, judicial verdicts, hard-check evidence, and delivery
certification constraints. It summarizes evidence and must not upgrade blocked,
partial, failed, or not-verified results to complete.

## Forbidden Cross-Role Context

Role packs must not receive unrelated role instructions or delivery authority.
Executor packs must not receive validation authority. Validator packs must not
receive repair authority. Reporting packs must not receive power to invent
judicial verdicts.
