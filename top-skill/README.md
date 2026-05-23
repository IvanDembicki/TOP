# TOP Skill — Tree-Oriented Programming

**Version:** 2.0.3 | **License:** MIT | **Invocation:** `/top`

**TOP turns architecture from a weak social norm into a strong machine-verifiable protocol.**

A skill for AI-driven design, generation, and validation of systems built with the **Tree-Oriented Programming (TOP)** paradigm.

Migration safety rule: every TOP migration must create or switch to a dedicated
git branch, normally `top-migration/<branch-id>`, and log the git safety gate
before any migration write. Migration agents must not push to remote unless the
user explicitly requests push.

This product is the foundational skill layer in the broader TOP product line:
- use `top-skill` for TOP architecture, canon, modeling, and generation protocol;
- use `top-prompt-cleaner` when the problem is still a single messy prompt;
- use `top-skill-factory` when the prompt or skill now needs lifecycle control, contracts, validation gates, compare, update, or rollback.

---

## What is TOP?

TOP is a programming paradigm in which any system is modeled as a strictly typed tree of nodes.

The tree is the structural model of the entire system. It defines composition, state organization, and how the system evolves over time.

TOP extends OOP: if OOP defines how individual objects work, TOP defines strict rules for their composition and interaction within the system as a whole.

The practical goal is **complexity control**. Without explicit structural constraints, cross-dependencies tend to grow as O(n²). TOP constrains them through a typed tree and keeps growth closer to O(n).

---

## Problems TOP solves

**Architectural entropy under AI generation.** AI accelerates code production — and equally accelerates the accumulation of hidden dependencies, inconsistent decisions, and lost intent. Conventions do not scale under AI generation. TOP replaces conventions with machine-verifiable structure.

**Loss of architectural intent.** Code stores *what*; it rarely stores *why*. In AI-assisted development this compounds: if prompts are lost or never formalized, the reasoning behind the system disappears. TOP externalizes intent into `spec + prompt` — the source of truth that survives refactoring and platform changes.

**Expensive onboarding and poor change locality.** A developer fixing one node should not need to read the entire project. TOP enforces explicit boundaries so that scope of change stays local by design — critical for teams with high turnover or parallel development.

**Platform dependency.** TOP separates the structural model from implementation: one spec tree, platform-neutral semantics, per-target adaptation. The architecture transfers; only the generated code changes. In many cases this fully eliminates the need to redesign when adding a new platform.

**Architectural rules cannot be verified automatically.** Most teams rely on code review, wikis, and senior authority. TOP replaces this with canon rules, audit agents, and explicit contracts — rules that run automatically, not rules that people try to remember.

---

## What this skill provides

This is a complete AI-native development system:

- **Architectural model** — typed tree, node contracts, controller/content split, state machines
- **Generation protocol** — pipeline `spec → prompt → code → verification`
- **Validation system** — canon rules, violation catalog, audit agents
- **Harness protocol** — task capsules, handoff artifacts, execution evidence,
  and delivery certification gates
- **Multi-target generation** — one spec tree generates implementations for Web, Android, React Native, and other platforms

The sufficient operational unit in TOP is the pair **`spec + prompt`**. Code is a derived artifact. The spec and prompts remain the source of truth.

---

## Skill governance

`top-skill` now carries its own TOP governance layer under `top/`:

- `top/spec.json` — skill execution tree and invariants
- `top/artifact-manifest.json` — required package and migration contracts
- `top/modes/mode-manifest.json` — stable mode boundaries
- `workflow/enforcement-evidence-model.md` — root contract for delivery
  honesty and protocol-only vs runner-enforced evidence
- `workflow/activation-and-operating-procedure.md` — activation triggers and
  operating loop for delivery-affecting 2.0 orchestration
- `workflow/task-capsule-format.md` — one-pass input contract
- `workflow/handoff-artifact-format.md` — one-pass output contract
- `workflow/role-packs.md` — minimal role-specific context packs
- `workflow/orchestrator-protocol.md` — workflow control and routing contract
- `workflow/runner-contract.md` — executable harness contract for runner
  workflow and runner report artifacts
- `workflow/pass-invocation-contract.md` — context package and invocation
  evidence contract for runner-enforced isolation
- `workflow/llm-api-adapter-contract.md` — contract for launching one pass
  through a separate LLM API request
- `workflow/repair-pass-contract.md` — bounded repair authority and
  post-repair judicial validation contract
- `workflow/delivery-certification-procedure.md` — executable post-run
  delivery certification gate
- `workflow/run-state-machine.md` — process state model for one run package
- `workflow/run-package-layout.md` — canonical filesystem package for one
  orchestration run
- `top/schemas/migration-workflow.schema.json` — schema for project migration workflow trees
- `top/schemas/fragments/execution-evidence.schema.json` — reusable execution
  evidence schema fragment
- `top/schemas/task-capsule.schema.json` — schema for task capsules
- `top/schemas/handoff-artifact.schema.json` — schema for handoff artifacts
- `top/schemas/runner-workflow.schema.json` — schema for protocol runner input
- `top/schemas/runner-report.schema.json` — schema for protocol runner output
- `top/schemas/context-package.schema.json` — schema for runner-materialized
  context packages
- `top/schemas/pass-invocation-evidence.schema.json` — schema for pass
  invocation evidence
- `top/schemas/certification-snapshot.schema.json` — schema for stale
  certification detection snapshots
- `top/schemas/run-state.schema.json` — schema for derived run package state
- `top/schemas/agent-workflow.schema.json` — schema for separated agent passes
- `top/schemas/validation-report.schema.json` — schema for judicial reports
- `top/schemas/delivery-certification.schema.json` — schema for delivery
  certification
- `scripts/validate_execution_evidence.py` — executable protocol-layer hard
  validator for delivery evidence gates
- `scripts/top_protocol_runner.py` — executable runner gate for pass handoffs
  and hard-check commands
- `scripts/adapters/llm_api_adapter.py` — LLM API pass adapter that writes
  handoff and invocation evidence artifacts
- `scripts/certify_orchestration_run.py` — post-run certification gate that
  writes validation report, delivery certification, and final audit artifacts
- `scripts/create_orchestration_run.py` — scaffold a new run package under
  `top/orchestration/<workflow-id>/<run-id>/`, including `--llm-smoke` packages
  for testing real `llm-api` invocation evidence and `--repair-loop` packages
  for bounded repair revalidation, plus `--repair-artifact-dogfood` packages
  for testing exact-ref repair artifact writes
- `scripts/update_orchestration_state.py` — derive `run-state.json` from runner,
  judicial, certification, and snapshot artifacts
- `scripts/validate_orchestration_run.py` — read-only verifier for one complete
  run package, returning `RUN_VALID`, `RUN_STALE`, or `RUN_INVALID`
- `scripts/validate_orchestration_regressions.py` — no-network regression
  fixtures that block false `complete` scenarios
- `scripts/validate_repair_artifact_fixture.py` — hard-check validator for the
  repair artifact dogfood fixture
- `scripts/run_orchestration_workflow.py` — ordered driver for create, runner,
  certification, snapshot verification, and final run-package verification
- `top/validation/output-rules.md` — readiness checks for skill outputs

Migration projects must keep branch-owned control artifacts under
`top/migration/<branch-id>/` and shared multi-branch status/log artifacts under
`top/migration/`. `MIGRATION_LOG.md` is append-only; shared status updates must
preserve prior branch history.

---

## Benefits

1. **Complexity grows linearly** — typed tree constrains cross-dependencies; growth stays near O(n) instead of O(n²)
2. **Multi-platform from one spec** — one tree generates Web, Android, React Native, and other targets without rewriting architecture
3. **Verifiable architecture** — canon rules and audit agents validate structural correctness at any point
4. **Control under AI generation** — the system stays controllable and transparent even when AI generates most of the code
5. **Full regenerability** — spec and prompts are the source of truth; code can be regenerated at any time on any platform
6. **Local context per node** — each node is self-contained; AI works effectively without knowing the entire system
7. **Parallel development by design** — independent branches can be developed simultaneously without conflicts

---

## After updating TOP Skill

**Restarting an AI session is not sufficient after an update.**

When you update TOP Skill files on disk, the AI's loaded skill package may still contain the old version. The skill package is a cached bootstrap snapshot that does not update automatically when files change on disk.

To use the updated version:

1. **Reinstall or refresh the skill package** using the skill refresh mechanism provided by your AI environment.
2. Start a new AI session only after the refreshed package is available.
3. Confirm that the agent reports the expected TOP Skill version before continuing serious work.

> A stale package can bootstrap hydration correctly only if it already contains the hydration rule introduced in version 1.1.6. Packages older than 1.1.6 must be reinstalled to enable hydration.

---

## Getting started

Open the TOP workspace:

```
https://github.com/IvanDembicki/TOP
```

Then start with the `top-skill` package when the task is architectural, tree-based, or TOP-native. Type `/top` to begin.

---

## Pipeline

```
Spec tree (JSON)
    ↓
Node Implementation Prompts (language-agnostic)
    ↓
Generated code (any platform)
    ↓
Verification (canon rules + audit agents)
```

The architecture stays recoverable and regenerable at any point. AI generates and verifies within the model — it does not replace architectural decisions.

---

## Agent pipeline

The skill includes a full agent pipeline:

**Intake → Domain Structuring → TOP Modeling → Canon Precheck → Semantic Interpretation → Target Adaptation → Generation → Spec Sync → Validation → Repair → Final Audit**

Task modes: `analysis-only` · `modeling-refactor` · `generation-pipeline` · `migration` · `spec-change`

---

## License

MIT — free to use, modify, and distribute, including in commercial projects.
