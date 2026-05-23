#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from validate_execution_evidence import validate_document
except Exception as exc:  # pragma: no cover - reported by package validation
    validate_document = None
    validate_execution_evidence_import_error = exc
else:
    validate_execution_evidence_import_error = None

try:
    from top_protocol_runner import run_workflow
except Exception as exc:  # pragma: no cover - reported by package validation
    run_workflow = None
    top_protocol_runner_import_error = exc
else:
    top_protocol_runner_import_error = None

try:
    from certify_orchestration_run import certify as certify_orchestration_run
    from certify_orchestration_run import verify_snapshot as verify_certification_snapshot
except Exception as exc:  # pragma: no cover - reported by package validation
    certify_orchestration_run = None
    verify_certification_snapshot = None
    certify_orchestration_run_import_error = exc
else:
    certify_orchestration_run_import_error = None

try:
    from update_orchestration_state import update_state as update_orchestration_state
except Exception as exc:  # pragma: no cover - reported by package validation
    update_orchestration_state = None
    update_orchestration_state_import_error = exc
else:
    update_orchestration_state_import_error = None

try:
    from validate_orchestration_run import validate_run as validate_orchestration_run
except Exception as exc:  # pragma: no cover - reported by package validation
    validate_orchestration_run = None
    validate_orchestration_run_import_error = exc
else:
    validate_orchestration_run_import_error = None

try:
    from run_orchestration_workflow import drive as run_orchestration_workflow
except Exception as exc:  # pragma: no cover - reported by package validation
    run_orchestration_workflow = None
    run_orchestration_workflow_import_error = exc
else:
    run_orchestration_workflow_import_error = None

try:
    from validate_orchestration_regressions import run_regressions as run_orchestration_regressions
except Exception as exc:  # pragma: no cover - reported by package validation
    run_orchestration_regressions = None
    run_orchestration_regressions_import_error = exc
else:
    run_orchestration_regressions_import_error = None

try:
    from validate_repair_artifact_fixture import validate as validate_repair_artifact_fixture
except Exception as exc:  # pragma: no cover - reported by package validation
    validate_repair_artifact_fixture = None
    validate_repair_artifact_fixture_import_error = exc
else:
    validate_repair_artifact_fixture_import_error = None


REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "skill.json",
    "release-metadata.json",
    "hydration-manifest.json",
    "AI_PRELOAD_CONTEXT.md",
    "rules/skill-maintenance-rules.md",
    "canon/architectural-invariants.md",
    "canon/agent-power-separation.md",
    "canon/controller-content-rules.md",
    "canon/forbidden-confusions.md",
    "canon/validation-rejection-protocol.md",
    "canon/validation-rules.md",
    "rules/violation-catalog.md",
    "rules/pattern-recognition.md",
    "rules/spec-sync-rules.md",
    "rules/review-checklist.md",
    "contracts/top-folder-contract.md",
    "rules/typing-checklist.md",
    "scripts/validate_execution_evidence.py",
    "scripts/top_protocol_runner.py",
    "scripts/adapters/llm_api_adapter.py",
    "scripts/certify_orchestration_run.py",
    "scripts/create_orchestration_run.py",
    "scripts/update_orchestration_state.py",
    "scripts/validate_orchestration_run.py",
    "scripts/validate_orchestration_regressions.py",
    "scripts/validate_repair_artifact_fixture.py",
    "scripts/run_orchestration_workflow.py",
    "references/node-model.md",
    "references/code-generation.md",
    "references/event-model.md",
    "references/pattern-cards.md",
    "references/node-validation-rules.md",
    "references/state-tree.md",
    "references/state-holder-api.md",
    "prompts/generate-top-node.md",
    "prompts/generate-top-tree.md",
    "prompts/refactor-to-top.md",
    "agents/migration-infrastructure-agent.md",
    "agents/migration-planning-agent.md",
    "agents/migration-agent.md",
    "agents/behavior-preservation-agent.md",
    "agents/generation-agent.md",
    "agents/validation-agent.md",
    "agents/repair-agent.md",
    "agents/target-adaptation-agent.md",
    "contracts/agent-output-contracts/migration-infrastructure-output.md",
    "contracts/agent-output-contracts/migration-plan-output.md",
    "contracts/agent-output-contracts/behavior-preservation-output.md",
    "top/spec.json",
    "top/README.md",
    "top/artifact-manifest.json",
    "top/modes/mode-manifest.json",
    "top/validation/output-rules.md",
    "top/shared-rules/skill-governance.md",
    "workflow/enforcement-evidence-model.md",
    "workflow/activation-and-operating-procedure.md",
    "workflow/task-capsule-format.md",
    "workflow/handoff-artifact-format.md",
    "workflow/role-packs.md",
    "workflow/orchestrator-protocol.md",
    "workflow/runner-contract.md",
    "workflow/pass-invocation-contract.md",
    "workflow/llm-api-adapter-contract.md",
    "workflow/repair-pass-contract.md",
    "workflow/delivery-certification-procedure.md",
    "workflow/run-state-machine.md",
    "workflow/run-package-layout.md",
    "top/schemas/fragments/execution-evidence.schema.json",
    "top/schemas/task-capsule.schema.json",
    "top/schemas/handoff-artifact.schema.json",
    "top/schemas/runner-workflow.schema.json",
    "top/schemas/runner-report.schema.json",
    "top/schemas/context-package.schema.json",
    "top/schemas/pass-invocation-evidence.schema.json",
    "top/schemas/certification-snapshot.schema.json",
    "top/schemas/run-state.schema.json",
    "top/schemas/agent-workflow.schema.json",
    "top/schemas/validation-report.schema.json",
    "top/schemas/delivery-certification.schema.json",
    "top/schemas/migration-workflow.schema.json",
    "top/provenance.json",
]


def read_text(path):
    return path.read_text(encoding="utf-8")


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def rel(path, root):
    return str(path.relative_to(root)).replace("\\", "/")


def check_required_paths(root):
    errors = []
    for item in REQUIRED_PATHS:
        path = root / item
        if not path.exists():
            errors.append(f"missing required path: {item}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"empty required file: {item}")
    return errors


def check_json_parse(root):
    errors = []
    for path in sorted(root.glob("**/*.json")):
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f"{rel(path, root)}: invalid JSON: {exc}")
    return errors


def check_manifest_references(root):
    errors = []
    skill_path = root / "skill.json"
    if not skill_path.exists():
        return ["missing skill.json"]
    try:
        skill = load_json(skill_path)
    except Exception as exc:
        return [f"skill.json: invalid JSON: {exc}"]

    scalar_refs = ["entrypoint", "ai_preload", "onboarding", "changelog"]
    list_refs = ["agents", "canon", "examples"]

    for key in scalar_refs:
        value = skill.get(key)
        if value and not (root / value).exists():
            errors.append(f"skill.json {key} reference missing: {value}")

    for key in list_refs:
        for value in skill.get(key, []):
            if not (root / value).exists():
                errors.append(f"skill.json {key} reference missing: {value}")

    top_governance = skill.get("top_governance", {})
    if isinstance(top_governance, dict):
        for key, value in top_governance.items():
            if value and not (root / value).exists():
                errors.append(f"skill.json top_governance.{key} reference missing: {value}")

    return errors


def collect_hydration_paths(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(collect_hydration_paths(item))
        return result
    if isinstance(value, dict):
        result = []
        for item in value.values():
            result.extend(collect_hydration_paths(item))
        return result
    return []


def check_hydration_manifest(root):
    errors = []
    manifest_path = root / "hydration-manifest.json"
    if not manifest_path.exists():
        return ["missing hydration-manifest.json"]

    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        return [f"hydration-manifest.json: invalid JSON: {exc}"]

    skill = load_json(root / "skill.json")
    release = load_json(root / "release-metadata.json")
    version = skill.get("version")

    if manifest.get("version") != version:
        errors.append("hydration-manifest.json version does not match skill.json version")
    if release.get("hydration_manifest") != "hydration-manifest.json":
        errors.append("release-metadata.json hydration_manifest does not point to hydration-manifest.json")
    if release.get("runtime_freshness_strategy") != "hydration-manifest":
        errors.append("release-metadata.json runtime_freshness_strategy must be hydration-manifest")

    always = manifest.get("always")
    task = manifest.get("task")
    full = manifest.get("full")
    if not isinstance(always, list) or not always:
        errors.append("hydration-manifest.json always tier must be a non-empty list")
    if not isinstance(task, dict) or not task:
        errors.append("hydration-manifest.json task tier must be a non-empty object")
    if not isinstance(full, list) or not full:
        errors.append("hydration-manifest.json full tier must be a non-empty list")

    required_always = [
        "workflow/enforcement-evidence-model.md",
        "workflow/activation-and-operating-procedure.md",
        "workflow/task-capsule-format.md",
        "workflow/handoff-artifact-format.md",
        "workflow/role-packs.md",
        "workflow/orchestrator-protocol.md",
        "workflow/runner-contract.md",
        "workflow/pass-invocation-contract.md",
        "workflow/llm-api-adapter-contract.md",
        "workflow/repair-pass-contract.md",
        "workflow/delivery-certification-procedure.md",
        "workflow/run-state-machine.md",
        "workflow/run-package-layout.md",
        "scripts/validate_execution_evidence.py",
        "scripts/top_protocol_runner.py",
        "scripts/adapters/llm_api_adapter.py",
        "scripts/certify_orchestration_run.py",
        "scripts/create_orchestration_run.py",
        "scripts/update_orchestration_state.py",
        "scripts/validate_orchestration_run.py",
        "scripts/validate_orchestration_regressions.py",
        "scripts/validate_repair_artifact_fixture.py",
        "scripts/run_orchestration_workflow.py",
        "top/schemas/fragments/execution-evidence.schema.json",
        "top/schemas/task-capsule.schema.json",
        "top/schemas/handoff-artifact.schema.json",
        "top/schemas/runner-workflow.schema.json",
        "top/schemas/runner-report.schema.json",
        "top/schemas/context-package.schema.json",
        "top/schemas/pass-invocation-evidence.schema.json",
        "top/schemas/certification-snapshot.schema.json",
        "top/schemas/run-state.schema.json",
        "top/schemas/agent-workflow.schema.json",
        "top/schemas/validation-report.schema.json",
        "top/schemas/delivery-certification.schema.json",
    ]
    always_set = set(always) if isinstance(always, list) else set()
    for item in required_always:
        if item not in always_set:
            errors.append(f"hydration-manifest.json always tier missing execution governance file: {item}")

    referenced_paths = []
    referenced_paths.extend(collect_hydration_paths(always))
    referenced_paths.extend(collect_hydration_paths(task))
    referenced_paths.extend(collect_hydration_paths(full))

    for item in sorted(set(referenced_paths)):
        if not (root / item).exists():
            errors.append(f"hydration-manifest.json reference missing: {item}")

    return errors


def extract_version_from_markdown(text):
    match = re.search(r"\*\*Version:\*\*\s*([0-9]+\.[0-9]+\.[0-9]+)", text)
    return match.group(1) if match else None


def check_version_consistency(root):
    errors = []
    skill = load_json(root / "skill.json")
    release = load_json(root / "release-metadata.json")
    top_spec = load_json(root / "top/spec.json")
    version = skill.get("version")

    if release.get("current_version") != version:
        errors.append("release-metadata.json current_version does not match skill.json version")
    if top_spec.get("skill_version") != version:
        errors.append("top/spec.json skill_version does not match skill.json version")

    for item in ["SKILL.md", "README.md", "CHANGELOG.md"]:
        text = read_text(root / item)
        if version not in text:
            errors.append(f"{item}: version {version} not present")

    skill_md_version = extract_version_from_markdown(read_text(root / "SKILL.md"))
    readme_version = extract_version_from_markdown(read_text(root / "README.md"))
    if skill_md_version and skill_md_version != version:
        errors.append("SKILL.md version does not match skill.json version")
    if readme_version and readme_version != version:
        errors.append("README.md version does not match skill.json version")

    return errors


def collect_top_spec_artifacts(node):
    artifacts = []
    if isinstance(node, dict):
        for item in node.get("artifacts", []):
            artifacts.append(item)
        for value in node.values():
            artifacts.extend(collect_top_spec_artifacts(value))
    elif isinstance(node, list):
        for value in node:
            artifacts.extend(collect_top_spec_artifacts(value))
    return artifacts


def check_top_governance_consistency(root):
    errors = []
    skill = load_json(root / "skill.json")
    top_spec = load_json(root / "top/spec.json")
    mode_manifest = load_json(root / "top/modes/mode-manifest.json")
    hydration = load_json(root / "hydration-manifest.json")

    top_artifacts = set(collect_top_spec_artifacts(top_spec.get("tree", {})))
    skill_agents = set(skill.get("agents", []))
    for agent in sorted(skill_agents):
        if agent not in top_artifacts:
            errors.append(f"top/spec.json Agents artifacts missing skill.json agent: {agent}")

    if "canon/migration.md" not in skill.get("canon", []):
        errors.append("skill.json canon missing canon/migration.md")

    stable_modes = {
        item.get("mode")
        for item in mode_manifest.get("modes", [])
        if item.get("maturity") == "stable"
    }
    skill_modes = set(skill.get("modes", []))
    if stable_modes != skill_modes:
        errors.append(
            "top/modes/mode-manifest.json stable modes do not match skill.json modes: "
            f"stable={sorted(stable_modes)} skill={sorted(skill_modes)}"
        )

    quickstart = read_text(root / "QUICKSTART_MIN_READS.md")
    required_migration_reads = [
        "canon/agent-power-separation.md",
        "canon/validation-rejection-protocol.md",
        "agents/migration-infrastructure-agent.md",
        "agents/migration-planning-agent.md",
        "agents/canon-precheck-agent.md",
        "agents/final-audit-agent.md",
        "contracts/agent-output-contracts/migration-infrastructure-output.md",
        "contracts/agent-output-contracts/migration-plan-output.md",
        "contracts/agent-output-contracts/canon-precheck-output.md",
        "contracts/agent-output-contracts/generation-output.md",
        "contracts/agent-output-contracts/spec-sync-output.md",
        "contracts/agent-output-contracts/repair-output.md",
        "contracts/agent-output-contracts/final-audit-output.md",
        "prompts/generate-top-node.md",
        "top/schemas/migration-workflow.schema.json",
    ]
    for item in required_migration_reads:
        if item not in quickstart:
            errors.append(f"QUICKSTART_MIN_READS.md migration minimum missing: {item}")

    required_modeling_reads = [
        "canon/migration.md",
        "canon/agent-power-separation.md",
        "canon/validation-rejection-protocol.md",
        "agents/canon-precheck-agent.md",
        "contracts/agent-output-contracts/migration-infrastructure-output.md",
        "contracts/agent-output-contracts/migration-plan-output.md",
        "contracts/agent-output-contracts/top-modeling-output.md",
        "contracts/agent-output-contracts/repair-output.md",
        "contracts/top-folder-contract.md",
        "top/schemas/migration-workflow.schema.json",
    ]
    for item in required_modeling_reads:
        if item not in quickstart:
            errors.append(f"QUICKSTART_MIN_READS.md modeling-refactor minimum missing: {item}")

    task_hydration = hydration.get("task", {})
    agent_file_by_name = {
        "TOP Modeling Agent": "agents/top-modeling-agent.md",
        "Canon Precheck Agent": "agents/canon-precheck-agent.md",
        "Semantic Interpreter Agent": "agents/semantic-interpreter-agent.md",
        "Target Adaptation Agent": "agents/target-adaptation-agent.md",
        "Generation Agent": "agents/generation-agent.md",
        "Spec Sync Agent": "agents/spec-sync-agent.md",
        "Validation Agent": "agents/validation-agent.md",
        "Migration Infrastructure Agent": "agents/migration-infrastructure-agent.md",
        "Migration Planning Agent": "agents/migration-planning-agent.md",
        "Migration Agent": "agents/migration-agent.md",
        "Behavior Preservation Agent": "agents/behavior-preservation-agent.md",
        "Repair Agent": "agents/repair-agent.md",
        "Final Audit Agent": "agents/final-audit-agent.md",
        "Spec Change Verification Agent": "agents/spec-change-verification-agent.md",
    }
    for mode_item in mode_manifest.get("modes", []):
        mode_name = mode_item.get("mode")
        if mode_name not in task_hydration:
            continue
        hydrated_items = set(task_hydration.get(mode_name, []))
        for agent_name in mode_item.get("required_agents", []) + mode_item.get("conditional_agents", []):
            agent_file = agent_file_by_name.get(agent_name)
            if agent_file and agent_file not in hydrated_items:
                errors.append(f"hydration-manifest.json task.{mode_name} missing mode agent: {agent_file}")

    hydration_required = {
        "migration": [
            "canon/agent-power-separation.md",
            "canon/validation-rejection-protocol.md",
            "agents/canon-precheck-agent.md",
            "contracts/agent-output-contracts/canon-precheck-output.md",
            "agents/final-audit-agent.md",
            "contracts/agent-output-contracts/final-audit-output.md",
            "contracts/agent-output-contracts/generation-output.md",
            "contracts/agent-output-contracts/spec-sync-output.md",
            "contracts/agent-output-contracts/repair-output.md",
            "prompts/generate-top-node.md",
        ],
        "generation-pipeline": [
            "canon/agent-power-separation.md",
            "canon/validation-rejection-protocol.md",
            "agents/top-modeling-agent.md",
            "contracts/agent-output-contracts/top-modeling-output.md",
            "agents/canon-precheck-agent.md",
            "contracts/agent-output-contracts/canon-precheck-output.md",
            "contracts/agent-output-contracts/generation-output.md",
            "contracts/agent-output-contracts/repair-output.md",
            "prompts/generate-top-node.md",
            "prompts/verify-node-implementation-prompt.md",
        ],
        "modeling-refactor": [
            "canon/migration.md",
            "canon/agent-power-separation.md",
            "canon/validation-rejection-protocol.md",
            "references/migration-heuristics.md",
            "agents/canon-precheck-agent.md",
            "contracts/agent-output-contracts/migration-infrastructure-output.md",
            "contracts/agent-output-contracts/migration-plan-output.md",
            "contracts/agent-output-contracts/top-modeling-output.md",
            "contracts/agent-output-contracts/repair-output.md",
        ],
    }
    for task_name, required_items in hydration_required.items():
        hydrated_items = set(task_hydration.get(task_name, []))
        for item in required_items:
            if item not in hydrated_items:
                errors.append(f"hydration-manifest.json task.{task_name} missing: {item}")

    migration_hydration = set(task_hydration.get("migration", []))
    for item in [
        "agents/canon-precheck-agent.md",
        "contracts/agent-output-contracts/canon-precheck-output.md",
        "agents/final-audit-agent.md",
        "contracts/agent-output-contracts/final-audit-output.md",
        "contracts/agent-output-contracts/generation-output.md",
    ]:
        if item not in migration_hydration:
            errors.append(f"migration hydration missing required pipeline file: {item}")

    behavior_contract = read_text(root / "contracts/agent-output-contracts/behavior-preservation-output.md")
    for status in [
        "behavior_preservation_status",
        "blocked_by_ambiguity",
        "blocked_by_scope_problem",
        "blocked_by_existing_top_contradiction",
        "blocked_by_coverage_gap",
    ]:
        if status not in behavior_contract:
            errors.append(f"behavior-preservation-output.md missing status: {status}")

    if "../CONTRIBUTING.md" in read_text(root / "AGENTS.md"):
        errors.append("AGENTS.md contains broken ../CONTRIBUTING.md reference")

    return errors


def extract_markdown_links(text):
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def check_markdown_links(root):
    errors = []
    for path in sorted(root.glob("**/*.md")):
        text = read_text(path)
        for target in extract_markdown_links(text):
            if target.startswith(("http://", "https://", "mailto:", "#", "app://", "plugin://")):
                continue
            clean = target.strip("<>")
            if ":" in clean and clean[1:3] != ":/":
                clean = clean.split(":", 1)[0]
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                errors.append(f"{rel(path, root)}: broken local markdown link -> {target}")
    return errors


def check_required_phrases(root):
    checks = [
        ("SKILL.md", "Pull-Based Construction / Locality of Object Birth"),
        ("SKILL.md", "Controller Role Purity"),
        ("SKILL.md", "rules/skill-maintenance-rules.md"),
        ("SKILL.md", "Content constructor receives exactly one semantic argument"),
        ("SKILL.md", "RootContext"),
        ("SKILL.md", "TOP spec props are declarative metadata"),
        ("SKILL.md", "canonical top-level field order"),
        ("SKILL.md", "Library Object External Context Boundary"),
        ("SKILL.md", "Downward query/event propagation is node-owned"),
        ("SKILL.md", "Tell-only propagation follows from node boundary ownership"),
        ("SKILL.md", "Switchable holders use non-null active-state operation delegation"),
        ("SKILL.md", "owner-held mode flag"),
        ("canon/core-axioms.md", "owner-held mode flag"),
        ("canon/validation-rules.md", "owner-held mode flag"),
        ("canon/validation-rules.md", "Switchable active-state delegation check"),
        ("canon/validation-rules.md", "Node-owned downward propagation check"),
        ("canon/validation-rules.md", "Propagation is tell-only"),
        ("rules/violation-catalog.md", "owner-held mode flag"),
        ("rules/violation-catalog.md", "delegating to `openedChild`"),
        ("rules/violation-catalog.md", "CORE-038"),
        ("rules/violation-catalog.md", "CORE-039"),
        ("rules/pattern-recognition.md", "owner-held state inside the same node"),
        ("rules/pattern-recognition.md", "Active-state operation/query delegation"),
        ("rules/pattern-recognition.md", "Node-owned downward query/event propagation"),
        ("rules/pattern-recognition.md", "ask-then-handle"),
        ("references/event-model.md", "Downward query/event propagation"),
        ("references/event-model.md", "Tell-only propagation and no-op boundaries"),
        ("references/state-tree.md", "Active-state operation delegation"),
        ("references/state-holder-api.md", "Active-State Operation Delegation"),
        ("references/tree-node-contracts.md", "`openedChild` is never null"),
        ("references/node-validation-rules.md", "Switchable and Downward Propagation Validation"),
        ("references/node-validation-rules.md", "ask-then-handle"),
        ("references/node-model.md", "Propagation ownership follows from the same node boundary"),
        ("references/code-generation.md", "Requirements for downward propagation"),
        ("rules/review-checklist.md", "switchable holders have at least one state/candidate child"),
        ("rules/review-checklist.md", "no preflight capability checks"),
        ("prompts/generate-top-node.md", "generate at least one state/candidate child"),
        ("prompts/generate-top-node.md", "generate tell-only propagation"),
        ("prompts/generate-node-implementation-prompt.md", "Downward query/event propagation must be node-owned"),
        ("prompts/generate-node-implementation-prompt.md", "Propagation must be tell-only"),
        ("references/tree-node-contracts.md", "owner-held mode flag"),
        ("agents/validation-agent.md", "owner-held fields on the same node"),
        ("agents/validation-agent.md", "active-state operation delegation validation"),
        ("agents/validation-agent.md", "node-owned downward propagation validation"),
        ("agents/validation-agent.md", "tell-only propagation validation"),
        ("agents/canon-precheck-agent.md", "active-state operations/queries"),
        ("agents/canon-precheck-agent.md", "downward query/event propagation is node-owned"),
        ("agents/canon-precheck-agent.md", "tell-only propagation is preserved"),
        ("agents/repair-agent.md", "repair switchable active-state operation traversal"),
        ("agents/repair-agent.md", "repair external/global-walker downward propagation"),
        ("agents/repair-agent.md", "repair ask-then-handle propagation"),
        ("agents/generation-agent.md", "generate downward query/event propagation as tell-only"),
        ("prompts/verify-node-implementation-prompt.md", "owner-held fields"),
        ("prompts/verify-node-implementation-prompt.md", "active-state operations/queries"),
        ("prompts/verify-node-implementation-prompt.md", "downward query/event propagation"),
        ("prompts/verify-node-implementation-prompt.md", "downward propagation is tell-only"),
        ("references/tree-model.md", "canonical top-level field order"),
        ("references/pattern-cards.md", "Library Object External Context Boundary"),
        ("references/pattern-cards.md", "Tell-Only Downward Propagation"),
        ("references/node-model.md", "Library Object External Context Boundary"),
        ("references/interaction-contracts.md", "Library object external context boundary"),
        ("rules/pattern-recognition.md", "Library object external context boundary signals"),
        ("references/node-validation-rules.md", "Library Object External Context Boundary review"),
        ("agents/validation-agent.md", "Library Object External Context Boundary review"),
        ("prompts/generate-top-node.md", "Library Object External Context Boundary pattern"),
        ("rules/skill-maintenance-rules.md", "No exhaustive-looking technology lists"),
        ("rules/skill-maintenance-rules.md", "Missed case feedback loop"),
        ("rules/violation-catalog.md", "CORE-026"),
        ("rules/violation-catalog.md", "CORE-027"),
        ("rules/violation-catalog.md", "CORE-028"),
        ("rules/violation-catalog.md", "CORE-029"),
        ("rules/violation-catalog.md", "CORE-030"),
        ("rules/violation-catalog.md", "CORE-031"),
        ("rules/violation-catalog.md", "CORE-032"),
        ("rules/violation-catalog.md", "CORE-033"),
        ("rules/violation-catalog.md", "CORE-034"),
        ("rules/violation-catalog.md", "CORE-035"),
        ("rules/violation-catalog.md", "CORE-036"),
        ("rules/violation-catalog.md", "CORE-037"),
        ("rules/violation-catalog.md", "Locally implemented content"),
        ("rules/pattern-recognition.md", "Locally implemented content conditional selection"),
        ("rules/pattern-recognition.md", "Context data injection"),
        ("rules/pattern-recognition.md", "reports candidates for Validation Agent review"),
        ("rules/violation-catalog.md", "CONV-007"),
        ("rules/violation-catalog.md", "CONV-008"),
        ("rules/violation-catalog.md", "CONV-009"),
        ("rules/violation-catalog.md", "CONV-010"),
        ("rules/violation-catalog.md", "WF-010"),
        ("rules/violation-catalog.md", "WF-011"),
        ("rules/violation-catalog.md", "WF-012"),
        ("rules/violation-catalog.md", "WF-013"),
        ("rules/violation-catalog.md", "WF-014"),
        ("rules/violation-catalog.md", "WF-015"),
        ("rules/violation-catalog.md", "WF-016"),
        ("rules/violation-catalog.md", "WF-017"),
        ("rules/violation-catalog.md", "WF-018"),
        ("rules/violation-catalog.md", "WF-019"),
        ("rules/violation-catalog.md", "WF-020"),
        ("rules/violation-catalog.md", "WF-021"),
        ("rules/violation-catalog.md", "WF-022"),
        ("rules/violation-catalog.md", "WF-023"),
        ("rules/violation-catalog.md", "WF-024"),
        ("rules/violation-catalog.md", "WF-025"),
        ("rules/violation-catalog.md", "WF-026"),
        ("rules/violation-catalog.md", "WF-027"),
        ("rules/violation-catalog.md", "WF-028"),
        ("rules/violation-catalog.md", "WF-029"),
        ("rules/violation-catalog.md", "WF-030"),
        ("rules/violation-catalog.md", "WF-031"),
        ("contracts/top-folder-contract.md", "top_src/<branch-id>/"),
        ("contracts/top-folder-contract.md", "top/specs/settings-branch.json"),
        ("contracts/top-folder-contract.md", "MIGRATION_WORKFLOW.json"),
        ("contracts/top-folder-contract.md", "MIGRATION_PLAN.md"),
        ("contracts/top-folder-contract.md", "MIGRATION_LOG.md"),
        ("contracts/top-folder-contract.md", "The active migration workspace is agent-owned"),
        ("contracts/top-folder-contract.md", "top-migration/<branch-id>"),
        ("contracts/top-folder-contract.md", "Git safety gate"),
        ("contracts/top-folder-contract.md", "top/migration/<branch-id>/MIGRATION_WORKFLOW.json"),
        ("contracts/top-folder-contract.md", "Shared artifacts are `top/migration/MIGRATION_LOG.md`"),
        ("contracts/top-folder-contract.md", "Canonical node field order"),
        ("canon/migration.md", "Migration artifact layout must be canonical"),
        ("canon/migration.md", "Migration workflow tree, plan, and action log are mandatory"),
        ("canon/migration.md", "Migration means discovering and externalizing hidden structure"),
        ("canon/migration.md", "Scope is not node boundary"),
        ("canon/migration.md", "Recursive decomposition is mandatory"),
        ("canon/migration.md", "PanelDisplayStyle is not decomposition"),
        ("canon/migration.md", "Runtime Branch Binding Pattern"),
        ("canon/migration.md", "Active migration workspace ownership"),
        ("canon/migration.md", "Shared migration artifacts are not branch-owned"),
        ("canon/migration.md", "Mandatory dedicated git branch"),
        ("canon/migration.md", "top-migration/<branch-id>"),
        ("canon/migration.md", "remote push: forbidden unless the user explicitly requests push"),
        ("canon/agent-power-separation.md", "four branches"),
        ("canon/agent-power-separation.md", "AI Separation of Powers"),
        ("canon/agent-power-separation.md", "No self-certified delivery"),
        ("canon/agent-power-separation.md", "Agent claims are not evidence"),
        ("canon/agent-power-separation.md", "The executor produces artifacts"),
        ("top/schemas/agent-workflow.schema.json", "TOP Agent Workflow Separation of Powers"),
        ("top/schemas/validation-report.schema.json", "TOP Validation Report"),
        ("top/schemas/delivery-certification.schema.json", "TOP Delivery Certification"),
        ("top/schemas/fragments/execution-evidence.schema.json", "TOP Execution Evidence"),
        ("top/schemas/task-capsule.schema.json", "TOP Task Capsule"),
        ("top/schemas/handoff-artifact.schema.json", "TOP Handoff Artifact"),
        ("workflow/enforcement-evidence-model.md", "Delivery Law"),
        ("workflow/enforcement-evidence-model.md", "Protocol-Only Mode"),
        ("workflow/enforcement-evidence-model.md", "False Substitutes"),
        ("workflow/enforcement-evidence-model.md", "executionIsolationLevel"),
        ("workflow/enforcement-evidence-model.md", "verificationEvidenceLevel"),
        ("workflow/enforcement-evidence-model.md", "runner-enforced"),
        ("workflow/enforcement-evidence-model.md", "hard-check-verified"),
        ("workflow/activation-and-operating-procedure.md", "Activation Triggers"),
        ("workflow/activation-and-operating-procedure.md", "Protocol-Only Bridge"),
        ("workflow/activation-and-operating-procedure.md", "Status Reporting"),
        ("workflow/task-capsule-format.md", "one microprocess pass"),
        ("workflow/handoff-artifact-format.md", "Required executionEvidence"),
        ("workflow/role-packs.md", "Role packs define minimal context"),
        ("workflow/orchestrator-protocol.md", "Workflow, Not Free Agent Loop"),
        ("workflow/orchestrator-protocol.md", "Write"),
        ("workflow/orchestrator-protocol.md", "Select"),
        ("workflow/orchestrator-protocol.md", "Compress"),
        ("workflow/orchestrator-protocol.md", "Isolate"),
        ("workflow/runner-contract.md", "The runner is the executable harness layer"),
        ("workflow/runner-contract.md", "The report is evidence. It is not a judicial verdict by itself"),
        ("workflow/runner-contract.md", "Portable Commands"),
        ("workflow/runner-contract.md", "scriptRef"),
        ("workflow/runner-contract.md", "without adapter-provided model invocation evidence is also `not_verified`"),
        ("workflow/pass-invocation-contract.md", "Runner-Enforced Isolation Gate"),
        ("workflow/pass-invocation-contract.md", "modelInvocationEvidence"),
        ("workflow/pass-invocation-contract.md", "process adapter without model invocation evidence cannot certify"),
        ("workflow/pass-invocation-contract.md", "placeholder context slices"),
        ("workflow/llm-api-adapter-contract.md", "scripts/adapters/llm_api_adapter.py"),
        ("workflow/llm-api-adapter-contract.md", "freshContext: true"),
        ("workflow/llm-api-adapter-contract.md", "modelInvocationEvidence: true"),
        ("workflow/repair-pass-contract.md", "Post-Repair Judicial Law"),
        ("workflow/repair-pass-contract.md", "maxRepairAttempts"),
        ("workflow/repair-pass-contract.md", "A repair result is not a verdict"),
        ("workflow/delivery-certification-procedure.md", "scripts/certify_orchestration_run.py"),
        ("workflow/delivery-certification-procedure.md", "runner report execution evidence is `runner-enforced`"),
        ("workflow/delivery-certification-procedure.md", "Runner report is evidence. Judicial handoff is verdict"),
        ("workflow/delivery-certification-procedure.md", "SNAPSHOT_STALE"),
        ("workflow/run-state-machine.md", "The state machine does not certify delivery by itself"),
        ("workflow/run-state-machine.md", "scripts/update_orchestration_state.py"),
        ("workflow/run-state-machine.md", "skip-state-update"),
        ("workflow/run-state-machine.md", "certified"),
        ("workflow/run-state-machine.md", "stale"),
        ("workflow/run-package-layout.md", "top/orchestration/<workflow-id>/<run-id>/"),
        ("workflow/run-package-layout.md", "A scaffolded run package starts as `protocol-defined` and `not-certified`"),
        ("workflow/run-package-layout.md", "scripts/certify_orchestration_run.py"),
        ("workflow/run-package-layout.md", "--verify-snapshot"),
        ("workflow/run-package-layout.md", "run-state.json"),
        ("workflow/run-package-layout.md", "final-audit.md"),
        ("scripts/validate_execution_evidence.py", "delivery complete requires executionIsolationLevel runner-enforced"),
        ("scripts/validate_execution_evidence.py", "required hard check must be pass for delivery complete"),
        ("scripts/validate_execution_evidence.py", "ARTIFACT_VALID"),
        ("scripts/top_protocol_runner.py", "Run or validate a TOP runner workflow"),
        ("scripts/top_protocol_runner.py", "accept_external_runner_evidence"),
        ("scripts/top_protocol_runner.py", "TOP_CONTEXT_PACKAGE"),
        ("scripts/top_protocol_runner.py", "modelInvocationEvidence"),
        ("scripts/top_protocol_runner.py", "python-script"),
        ("scripts/top_protocol_runner.py", "skip_state_update"),
        ("scripts/adapters/llm_api_adapter.py", "openai-responses"),
        ("scripts/adapters/llm_api_adapter.py", "TOP_CONTEXT_PACKAGE"),
        ("scripts/adapters/llm_api_adapter.py", "modelInvocationEvidence"),
        ("scripts/adapters/llm_api_adapter.py", "dry-run"),
        ("scripts/adapters/llm_api_adapter.py", "resolvedFrom"),
        ("scripts/adapters/llm_api_adapter.py", "artifactWriteRequests"),
        ("scripts/adapters/llm_api_adapter.py", "artifactWrites"),
        ("scripts/certify_orchestration_run.py", "Certify a TOP orchestration run package"),
        ("scripts/certify_orchestration_run.py", "certify_orchestration_run: COMPLETE"),
        ("scripts/certify_orchestration_run.py", "SNAPSHOT_STALE"),
        ("scripts/certify_orchestration_run.py", "skip_state_update"),
        ("scripts/certify_orchestration_run.py", "post-repair-judicial-validation"),
        ("scripts/certify_orchestration_run.py", "repairedRefs"),
        ("scripts/create_orchestration_run.py", "Create a TOP orchestration run package"),
        ("scripts/create_orchestration_run.py", "protocol-defined"),
        ("scripts/create_orchestration_run.py", "final-audit.md"),
        ("scripts/create_orchestration_run.py", "--repair-loop"),
        ("scripts/create_orchestration_run.py", "--repair-artifact-dogfood"),
        ("scripts/create_orchestration_run.py", "repair-artifact-fixture"),
        ("scripts/update_orchestration_state.py", "Derive and write TOP orchestration run state"),
        ("scripts/update_orchestration_state.py", "STATE_WRITTEN"),
        ("scripts/update_orchestration_state.py", "invalid run state transition"),
        ("scripts/validate_orchestration_run.py", "Validate one TOP orchestration run package"),
        ("scripts/validate_orchestration_run.py", "RUN_VALID certified"),
        ("scripts/validate_orchestration_run.py", "RUN_STALE"),
        ("scripts/validate_orchestration_run.py", "RUN_INVALID"),
        ("scripts/validate_orchestration_run.py", "delivery complete required pass must have modelInvocationEvidence true"),
        ("scripts/validate_orchestration_run.py", "delivery complete after repair requires"),
        ("scripts/validate_orchestration_run.py", "repaired refs"),
        ("scripts/validate_orchestration_regressions.py", "Run TOP orchestration regression fixtures"),
        ("scripts/validate_orchestration_regressions.py", "missing judicial handoff"),
        ("scripts/validate_orchestration_regressions.py", "process-only false complete"),
        ("scripts/validate_orchestration_regressions.py", "required hard check not_verified"),
        ("scripts/validate_orchestration_regressions.py", "RUN_VALID not-certified"),
        ("scripts/validate_orchestration_regressions.py", "repair_without_post_judicial"),
        ("scripts/validate_repair_artifact_fixture.py", "Validate the repair artifact dogfood fixture"),
        ("scripts/validate_repair_artifact_fixture.py", "validate_repair_artifact_fixture: OK"),
        ("scripts/run_orchestration_workflow.py", "Run a TOP orchestration workflow driver"),
        ("scripts/run_orchestration_workflow.py", "RUN_VALID not-certified"),
        ("scripts/run_orchestration_workflow.py", "CERTIFICATION_NOT_CERTIFIED"),
        ("top/schemas/runner-workflow.schema.json", "TOP Runner Workflow"),
        ("top/schemas/runner-report.schema.json", "TOP Runner Report"),
        ("top/schemas/context-package.schema.json", "TOP Context Package"),
        ("top/schemas/pass-invocation-evidence.schema.json", "TOP Pass Invocation Evidence"),
        ("top/schemas/pass-invocation-evidence.schema.json", "artifactWrites"),
        ("top/schemas/task-capsule.schema.json", "artifactWriteRequests"),
        ("top/schemas/certification-snapshot.schema.json", "TOP Certification Snapshot"),
        ("top/schemas/run-state.schema.json", "TOP Orchestration Run State"),
        ("top/schemas/migration-workflow.schema.json", "separationOfPowers"),
        ("top/schemas/migration-workflow.schema.json", "executionEvidence"),
        ("top/artifact-manifest.json", "top/schemas/agent-workflow.schema.json"),
        ("top/artifact-manifest.json", "workflow/enforcement-evidence-model.md"),
        ("top/modes/mode-manifest.json", "protocol_only_default"),
        ("top/modes/mode-manifest.json", "Delivery complete requires an independent judicial validation pass"),
        ("top/spec.json", "delivery-certification.schema.json"),
        ("top/spec.json", "workflow/enforcement-evidence-model.md"),
        ("top/validation/output-rules.md", "runner-enforced"),
        ("top/shared-rules/skill-governance.md", "Protocol-only execution must not be reported as runner-enforced execution"),
        ("canon/validation-rejection-protocol.md", "Validate the smallest meaningful artifact"),
        ("canon/validation-rejection-protocol.md", "micro-check"),
        ("canon/validation-rejection-protocol.md", "meso-check"),
        ("canon/validation-rejection-protocol.md", "macro-check"),
        ("canon/validation-rejection-protocol.md", "GENERATOR_LEARNING_LEDGER.md"),
        ("agents/migration-infrastructure-agent.md", "MIGRATION_PLAN.md"),
        ("agents/migration-infrastructure-agent.md", "MIGRATION_WORKFLOW.json"),
        ("agents/migration-infrastructure-agent.md", "dedicated migration branch"),
        ("agents/migration-infrastructure-agent.md", "git safety gate"),
        ("agents/migration-planning-agent.md", "MIGRATION_PLAN.md"),
        ("agents/migration-planning-agent.md", "MIGRATION_WORKFLOW.json"),
        ("agents/migration-agent.md", "Migration means discovering and externalizing hidden structure"),
        ("agents/canon-precheck-agent.md", "Canon Precheck Agent"),
        ("agents/final-audit-agent.md", "Final Audit Agent"),
        ("agents/validation-agent.md", "post-generation source validation"),
        ("rules/spec-sync-rules.md", "missing_source_root"),
        ("rules/spec-sync-rules.md", "missing_migration_control_plane"),
        ("top/shared-rules/skill-governance.md", "A skill is a controlled TOP tree"),
        ("top/validation/output-rules.md", "Migration-mode project outputs include"),
        ("top/schemas/migration-workflow.schema.json", "TOP Migration Workflow"),
        ("canon/migration.md", "Legacy tests are requirements evidence"),
        ("canon/migration.md", "no ad hoc accepted deviations"),
        ("canon/validation-rules.md", "accepted core deviation"),
        ("canon/architectural-invariants.md", "Shared derived fact repair rule"),
        ("references/functional-composition-target.md", "Single owning controller input, not decomposed props"),
        ("references/functional-composition-target.md", "Child Node runtime input is not a TOP access boundary"),
        ("agents/behavior-preservation-agent.md", "Behavior Preservation Plan"),
        ("contracts/agent-output-contracts/behavior-preservation-output.md", "Legacy tests are requirements evidence"),
        ("contracts/agent-output-contracts/behavior-preservation-output.md", "behavior_preservation_status"),
        ("canon/migration.md", "explicitly declared obsolete by an approved behavior-level decision"),
        ("QUICKSTART_MIN_READS.md", "agents/migration-infrastructure-agent.md"),
        ("QUICKSTART_MIN_READS.md", "agents/migration-planning-agent.md"),
        ("QUICKSTART_MIN_READS.md", "top/schemas/migration-workflow.schema.json"),
        ("SKILL.md", "IContentAccess` is not a data channel"),
        ("SKILL.md", "Locally implemented content must contain no conditional selection logic"),
        ("canon/forbidden-confusions.md", "Locally implemented content must contain no conditional selection logic"),
        ("canon/validation-rules.md", "Locally implemented content conditional selection logic is a hard validation"),
        ("references/node-validation-rules.md", "locally implemented content contains no conditional selection logic"),
        ("references/code-generation.md", "Locally implemented content must be structurally and decisionally static"),
        ("references/code-generation.md", "Canonical Rich Typed TOP Node Pseudocode"),
        ("references/code-generation.md", "richest reasonable typed form"),
        ("references/code-generation.md", "IIdentifiableNode"),
        ("references/code-generation.md", "IDeviceEntityAccess"),
        ("references/code-generation.md", "Rules for target-language downgrading"),
        ("references/event-model.md", "Presentation content reports intent"),
        ("references/pattern-cards.md", "explicit ancestor/context contract"),
        ("prompts/generate-top-node.md", "Canonical Rich Typed TOP Node Pseudocode"),
        ("prompts/generate-top-node.md", "do not generate conditional selection logic inside locally implemented"),
        ("prompts/verify-node-implementation-prompt.md", "locally implemented content contains no conditional"),
        ("agents/generation-agent.md", "canonical rich typed pseudocode example"),
        ("agents/validation-agent.md", "locally implemented content conditional selection validation"),
        ("agents/validation-agent.md", "controller-to-content presentation push validation"),
        ("agents/repair-agent.md", "repair locally implemented content conditional selection"),
        ("agents/repair-agent.md", "replace controller-to-content presentation commands"),
        ("canon/controller-content-rules.md", "Controller must not imperatively command"),
        ("prompts/verify-node-implementation-prompt.md", "controller does not push show/hide/update"),
        ("canon/architectural-invariants.md", "Objects are not assembled outside the tree and pushed inward"),
        ("canon/architectural-invariants.md", "Context attachment, not data injection"),
        ("canon/architectural-invariants.md", "Controller Role Purity Invariant"),
        ("canon/core-axioms.md", "Presentation content reports intent"),
        ("canon/core-axioms.md", "controllers mutate data"),
        ("canon/core-axioms.md", "must not derive output values"),
        ("canon/core-axioms.md", "Absolute content privacy"),
        ("canon/core-axioms.md", "One controller, zero-or-one content"),
        ("canon/core-axioms.md", "Controller is not a renderer"),
        ("canon/core-axioms.md", "Content-owned setters do not cross the boundary"),
        ("examples/tree-editor/README.md", "canonical for top-skill 1.1.18"),
        ("rules/pattern-recognition.md", "Output derivation inside locally implemented content"),
        ("rules/pattern-recognition.md", "Migration wrapper and giant-node signals"),
        ("rules/pattern-recognition.md", "Concrete content privacy and fragment-output signals"),
        ("rules/pattern-recognition.md", "Spec shape and generated layout signals"),
        ("rules/pattern-recognition.md", "Missing checkpoint / non-independent validation signals"),
        ("rules/pattern-recognition.md", "Required post-generation delivery gate signals"),
        ("rules/pattern-recognition.md", "Migration git branch safety signals"),
        ("references/migration-heuristics.md", "Giant controller access surface"),
        ("references/pattern-cards.md", "Runtime Branch Binding Pattern"),
        ("SKILL.md", "Runtime-created branch roots may additionally receive one canonical binding input"),
        ("canon/validation-rules.md", "Runtime-created branch roots may receive parent/context plus one canonical"),
        ("hydration-manifest.json", "contracts/agent-output-contracts/canon-precheck-output.md"),
        ("contracts/agent-output-contracts/final-audit-output.md", "readiness_status"),
        ("contracts/agent-output-contracts/validation-output.md", "concrete_content_privacy_check"),
        ("contracts/agent-output-contracts/validation-output.md", "independent_checkpoint_check"),
        ("contracts/agent-output-contracts/validation-output.md", "dedicated_migration_branch_check"),
        ("contracts/agent-output-contracts/migration-infrastructure-output.md", "git_safety_gate"),
        ("canon/core-axioms.md", "The executor produces artifacts"),
        ("canon/core-axioms.md", "The validator produces verdicts"),
        ("canon/core-axioms.md", "No agent may validate its own output"),
        ("rules/violation-catalog.md", "Generator self-validation claim"),
        ("rules/violation-catalog.md", "Contaminated validation context"),
        ("rules/violation-catalog.md", "Validation without artifact evidence"),
        ("rules/violation-catalog.md", "Final audit accepted unproven validation"),
        ("contracts/agent-output-contracts/validation-output.md", "rejection_id"),
        ("contracts/top-folder-contract.md", "GENERATOR_LEARNING_LEDGER.md"),
        ("canon/core-axioms.md", "max_repair_attempts_per_validation_gate"),
        ("rules/violation-catalog.md", "Public wrapper around concrete content"),
        ("canon/core-axioms.md", "Node atomicity"),
        ("canon/core-axioms.md", "Folder structure must mirror"),
        ("canon/core-axioms.md", "Runtime controller tree"),
        ("canon/core-axioms.md", "A controller without tree position is not a TOP controller"),
        ("canon/architectural-invariants.md", "TOP runtime is a tree of controller objects"),
        ("canon/architectural-invariants.md", "TOP generation must produce a controller tree"),
        ("canon/validation-rules.md", "generated-controller-runtime-shape"),
        ("canon/validation-rules.md", "controller-tree-topology"),
        ("canon/validation-rejection-protocol.md", "After repair, validation restarts from the nearest complete validation gate"),
        ("references/node-model.md", "A controller without tree position is not a TOP controller"),
        ("references/node-validation-rules.md", "Runtime Controller Tree Validation"),
        ("references/code-generation.md", "TOP generation must produce a controller tree"),
        ("references/migration-heuristics.md", "Controller-shaped service instead of runtime node"),
        ("rules/pattern-recognition.md", "Runtime controller tree shape signals"),
        ("agents/generation-agent.md", "generated-controller-runtime-shape"),
        ("agents/validation-agent.md", "runtime controller tree validation"),
        ("agents/repair-agent.md", "repair `CORE-037`"),
        ("agents/final-audit-agent.md", "controller tree audit"),
        ("prompts/generate-top-node.md", "A controller without tree position is not a TOP controller"),
        ("prompts/verify-node-implementation-prompt.md", "runtime controller tree"),
        ("contracts/agent-output-contracts/generation-output.md", "generated_controller_runtime_shape_self_check"),
        ("contracts/agent-output-contracts/validation-output.md", "controller_runtime_shape_check"),
        ("contracts/agent-output-contracts/final-audit-output.md", "controller_tree_audit"),
        ("contracts/agent-output-contracts/validation-output.md", "content_child_import_check"),
        ("contracts/agent-output-contracts/validation-output.md", "prompt_code_contract_drift_check"),
        ("contracts/agent-output-contracts/validation-output.md", "node_global_store_access_check"),
        ("contracts/agent-output-contracts/validation-output.md", "bridge_callback_injection_check"),
        ("contracts/agent-output-contracts/validation-output.md", "self_audited_pass_report_check"),
        ("contracts/agent-output-contracts/validation-output.md", "execution_evidence"),
        ("contracts/agent-output-contracts/validation-output.md", "runner_enforcement_claim_check"),
        ("contracts/agent-output-contracts/validation-output.md", "Required hard-check status `fail` or `not_verified` blocks delivery complete"),
        ("contracts/agent-output-contracts/final-audit-output.md", "separation_of_powers_audit"),
        ("contracts/agent-output-contracts/final-audit-output.md", "delivery_certification_audit"),
        ("contracts/agent-output-contracts/final-audit-output.md", "execution_evidence_audit"),
        ("contracts/agent-output-contracts/final-audit-output.md", "must not use `complete`, `certified`, `delivery complete`"),
        ("canon/validation-rules.md", "`type` names the actual node type"),
        ("hydration-manifest.json", "canon/agent-power-separation.md"),
        ("hydration-manifest.json", "canon/validation-rejection-protocol.md"),
        ("skill.json", "canon/agent-power-separation.md"),
        ("skill.json", "canon/validation-rejection-protocol.md"),
    ]
    errors = []
    for file_name, phrase in checks:
        text = read_text(root / file_name)
        if phrase not in text:
            errors.append(f"{file_name}: required phrase missing: {phrase}")
    return errors


def check_known_risky_patterns(root):
    errors = []
    patterns = [
        (r"new\s+ControllerAccessZero\s*\(", "dummy ControllerAccessZero construction"),
        (r"new\s+\w+Content\s*\(\s*access\s*\)", "externally named access object passed to Content"),
        (r"should usually|canon change usually", "weak maintenance wording"),
    ]
    for path in sorted(root.glob("**/*")):
        if path.is_dir() or path.suffix.lower() not in {".md", ".ts", ".js", ".json"}:
            continue
        text = read_text(path)
        for pattern, label in patterns:
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel(path, root)}:{line}: risky pattern ({label})")
    return errors


ABSOLUTE_PARENT_ONLY_RE = re.compile(
    r"(all|every|each)?\s*(top\s+)?node\s+constructors?\s+"
    r"(must\s+)?(receives?|receive|has|have)\s+"
    r"(exactly\s+one\s+semantic\s+argument:\s+)?(only\s+)?(its\s+)?parent",
    re.IGNORECASE,
)


def check_runtime_branch_binding_consistency(root):
    errors = []
    if "Runtime Branch Binding Pattern" not in read_text(root / "canon/migration.md"):
        return errors

    hard_paths = [
        "SKILL.md",
        "canon/core-axioms.md",
        "canon/architectural-invariants.md",
        "canon/controller-content-rules.md",
        "canon/validation-rules.md",
        "canon/migration.md",
        "references/node-model.md",
        "references/interaction-contracts.md",
        "references/code-generation.md",
        "references/node-validation-rules.md",
        "rules/violation-catalog.md",
        "rules/pattern-recognition.md",
        "prompts/generate-top-node.md",
        "prompts/generate-node-implementation-prompt.md",
        "prompts/verify-node-implementation-prompt.md",
        "agents/migration-agent.md",
        "agents/generation-agent.md",
        "agents/validation-agent.md",
        "agents/repair-agent.md",
    ]
    exception_terms = re.compile(
        r"static node|runtime-created|Runtime Branch Binding|entity context|identity key|typed immutable DTO",
        re.IGNORECASE,
    )
    for file_name in hard_paths:
        path = root / file_name
        if not path.exists():
            continue
        lines = read_text(path).splitlines()
        for index, line in enumerate(lines):
            if not ABSOLUTE_PARENT_ONLY_RE.search(line):
                continue
            window = "\n".join(lines[max(0, index - 2): index + 4])
            if not exception_terms.search(window):
                errors.append(
                    f"{file_name}:{index + 1}: constructor-only-parent wording "
                    "does not mention static-node scope or Runtime Branch Binding exception"
                )
    return errors


def check_branch_scoped_migration_control_consistency(root):
    errors = []
    required_phrases = [
        ("canon/migration.md", "top/migration/<branch-id>/MIGRATION_WORKFLOW.json"),
        ("canon/migration.md", "Shared migration artifacts are not branch-owned"),
        ("contracts/top-folder-contract.md", "top/migration/<branch-id>/MIGRATION_WORKFLOW.json"),
        ("contracts/top-folder-contract.md", "Shared artifacts are `top/migration/MIGRATION_LOG.md`"),
        ("rules/violation-catalog.md", "top/migration/<branch-id>/**"),
    ]
    for file_name, phrase in required_phrases:
        if phrase not in read_text(root / file_name):
            errors.append(f"{file_name}: branch-scoped migration control phrase missing: {phrase}")

    for file_name in ["canon/migration.md", "contracts/top-folder-contract.md", "rules/violation-catalog.md"]:
        if "top/migration/**" in read_text(root / file_name):
            errors.append(f"{file_name}: broad top/migration/** ownership remains")
    return errors


def check_migration_git_branch_safety_consistency(root):
    errors = []
    required_phrases = [
        ("canon/migration.md", "Mandatory dedicated git branch"),
        ("canon/migration.md", "top-migration/<branch-id>"),
        ("canon/migration.md", "remote push: forbidden unless the user explicitly requests push"),
        ("canon/migration.md", "Git safety gate:"),
        ("contracts/top-folder-contract.md", "top-migration/<branch-id>"),
        ("contracts/top-folder-contract.md", "Git safety gate:"),
        ("agents/migration-infrastructure-agent.md", "dedicated migration branch"),
        ("agents/migration-infrastructure-agent.md", "git safety gate"),
        ("agents/validation-agent.md", "dedicated migration branch validation"),
        ("agents/final-audit-agent.md", "dedicated migration branch"),
        ("contracts/agent-output-contracts/migration-infrastructure-output.md", "git_safety_gate"),
        ("contracts/agent-output-contracts/validation-output.md", "dedicated_migration_branch_check"),
        ("rules/violation-catalog.md", "WF-022"),
        ("rules/pattern-recognition.md", "Migration git branch safety signals"),
    ]
    for file_name, phrase in required_phrases:
        if phrase not in read_text(root / file_name):
            errors.append(f"{file_name}: migration git branch safety phrase missing: {phrase}")

    no_push_terms = [
        ("canon/migration.md", "push"),
        ("contracts/top-folder-contract.md", "push"),
        ("agents/migration-infrastructure-agent.md", "push"),
        ("contracts/agent-output-contracts/final-audit-output.md", "push"),
    ]
    for file_name, phrase in no_push_terms:
        if phrase not in read_text(root / file_name).lower():
            errors.append(f"{file_name}: no-push policy wording missing")
    return errors


def check_validation_control_consistency(root):
    errors = []
    required_phrases = [
        ("canon/core-axioms.md", "The executor produces artifacts"),
        ("canon/core-axioms.md", "The validator produces verdicts"),
        ("canon/core-axioms.md", "No agent may validate its own output"),
        ("canon/validation-rules.md", "clean, adversarial context"),
        ("contracts/agent-output-contracts/validation-output.md", "validation_evidence"),
        ("contracts/agent-output-contracts/validation-output.md", "generator_self_validation_claim_check"),
        ("contracts/agent-output-contracts/validation-output.md", "rejection_id"),
        ("contracts/top-folder-contract.md", "GENERATOR_LEARNING_LEDGER.md"),
        ("contracts/agent-output-contracts/final-audit-output.md", "validator_audit_check"),
        ("rules/violation-catalog.md", "WF-023"),
        ("rules/violation-catalog.md", "WF-024"),
        ("rules/violation-catalog.md", "WF-025"),
        ("rules/violation-catalog.md", "WF-026"),
        ("rules/violation-catalog.md", "WF-027"),
        ("rules/violation-catalog.md", "WF-028"),
        ("rules/violation-catalog.md", "WF-029"),
        ("rules/violation-catalog.md", "WF-030"),
        ("rules/violation-catalog.md", "WF-031"),
        ("canon/agent-power-separation.md", "No self-certified delivery"),
        ("top/schemas/agent-workflow.schema.json", "selfCertificationAllowed"),
        ("top/schemas/validation-report.schema.json", "checkedFiles"),
        ("top/schemas/delivery-certification.schema.json", "generationAndValidationSeparate"),
        ("top/schemas/fragments/execution-evidence.schema.json", "executionIsolationLevel"),
        ("top/schemas/fragments/execution-evidence.schema.json", "verificationEvidenceLevel"),
        ("top/schemas/delivery-certification.schema.json", "judicialHandoffRef"),
        ("top/schemas/delivery-certification.schema.json", "noRequiredGateFailedOrNotVerified"),
        ("contracts/agent-output-contracts/validation-output.md", "delivery_report_gate_check"),
        ("contracts/agent-output-contracts/validation-output.md", "execution_evidence"),
        ("contracts/agent-output-contracts/validation-output.md", "runner-enforced"),
        ("contracts/agent-output-contracts/final-audit-output.md", "delivery_certification_audit"),
        ("contracts/agent-output-contracts/final-audit-output.md", "runner-enforced"),
        ("workflow/enforcement-evidence-model.md", "Simulated separation cannot certify independent validation"),
    ]
    for file_name, phrase in required_phrases:
        if phrase not in read_text(root / file_name):
            errors.append(f"{file_name}: validation control phrase missing: {phrase}")

    executor_files = [
        "agents/generation-agent.md",
        "agents/repair-agent.md",
        "agents/top-modeling-agent.md",
        "agents/migration-agent.md",
        "prompts/generate-top-node.md",
    ]
    for file_name in executor_files:
        text = read_text(root / file_name)
        if "WF-023" not in text or "validation passed" not in text:
            errors.append(f"{file_name}: generator self-validation prohibition missing")
    return errors


def check_execution_evidence_validator_smoke(root):
    errors = []
    if validate_document is None:
        return [f"scripts/validate_execution_evidence.py import failed: {validate_execution_evidence_import_error}"]

    protocol_only_not_certified = {
        "status": "not-certified",
        "executionEvidence": {
            "executionIsolationLevel": "protocol-followed-by-agent",
            "verificationEvidenceLevel": "agent-claimed",
            "runnerName": None,
            "separateInvocationIds": [],
            "schemaValidationCommand": None,
            "hardCheckCommands": [],
            "limitations": ["Protocol-only mode; no runner evidence."],
        },
    }

    invalid_complete = {
        "deliveryStatus": "complete",
        "executionEvidence": {
            "executionIsolationLevel": "protocol-followed-by-agent",
            "verificationEvidenceLevel": "agent-claimed",
            "runnerName": None,
            "separateInvocationIds": [],
            "schemaValidationCommand": None,
            "hardCheckCommands": [],
            "limitations": ["Single context."],
        },
        "judicialHandoffRef": "",
        "validationReportRef": "",
        "requiredHardChecks": [
            {
                "id": "quick-validate",
                "description": "Package sanity validation",
                "requiredForComplete": True,
                "status": "not_verified",
                "command": None,
                "evidence": [],
            }
        ],
        "noRequiredGateFailedOrNotVerified": False,
    }

    valid_complete = {
        "deliveryStatus": "complete",
        "executionEvidence": {
            "executionIsolationLevel": "runner-enforced",
            "verificationEvidenceLevel": "hard-check-verified",
            "runnerName": "top-runner",
            "separateInvocationIds": ["executive-pass", "judicial-pass"],
            "schemaValidationCommand": "python scripts/quick_validate.py D:/TOP/top-skill",
            "hardCheckCommands": ["python scripts/quick_validate.py D:/TOP/top-skill"],
            "limitations": ["Smoke fixture only."],
        },
        "judicialHandoffRef": "handoff://judicial-pass",
        "validationReportRef": "report://validation",
        "requiredHardChecks": [
            {
                "id": "quick-validate",
                "description": "Package sanity validation",
                "requiredForComplete": True,
                "status": "pass",
                "command": "python scripts/quick_validate.py D:/TOP/top-skill",
                "evidence": ["quick_validate: OK"],
            }
        ],
        "blockingChecks": [
            {
                "checkId": "delivery-law",
                "status": "pass",
                "evidence": ["Delivery law fixture passed."],
            }
        ],
        "noBlockingInScopeViolations": True,
        "generationAndValidationSeparate": True,
        "noUnverifiedRequiredGates": True,
        "noRequiredGateFailedOrNotVerified": True,
    }

    protocol_errors = validate_document(protocol_only_not_certified, "protocol-only-smoke")
    if protocol_errors:
        errors.append("execution evidence validator rejected protocol-only not-certified smoke fixture")
        errors.extend(protocol_errors)

    invalid_errors = validate_document(invalid_complete, "invalid-complete-smoke")
    if not invalid_errors:
        errors.append("execution evidence validator failed to reject invalid delivery complete smoke fixture")

    valid_errors = validate_document(valid_complete, "valid-complete-smoke")
    if valid_errors:
        errors.append("execution evidence validator rejected valid delivery complete smoke fixture")
        errors.extend(valid_errors)

    return errors


def write_smoke_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def smoke_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_top_protocol_runner_smoke(root):
    errors = []
    if run_workflow is None:
        return [f"scripts/top_protocol_runner.py import failed: {top_protocol_runner_import_error}"]

    with tempfile.TemporaryDirectory(prefix="top-runner-smoke-") as temp_name:
        temp_root = Path(temp_name).resolve()
        capsule = {
            "schemaVersion": "1.0",
            "workflowId": "runner-smoke",
            "taskId": "executive-task",
            "role": "executive",
            "objective": "Produce a smoke handoff.",
            "allowedActions": ["write handoff"],
            "forbiddenActions": ["validate own output", "certify delivery"],
            "inputReferences": [],
            "contextSlices": ["smoke"],
            "outputContract": "handoff-artifact",
            "mayEditFiles": True,
            "mayValidate": False,
            "mayRepair": False,
            "mayReport": False,
            "mayCertifyDelivery": False,
            "stopCondition": "handoff written",
        }
        handoff = {
            "schemaVersion": "1.0",
            "workflowId": "runner-smoke",
            "passId": "executive-pass",
            "taskId": "executive-task",
            "role": "executive",
            "agentName": "smoke-executive",
            "taskCapsuleRef": "capsules/executive-task.json",
            "inputReferences": [],
            "outputReferences": ["handoffs/executive-pass.json"],
            "filesRead": ["capsules/executive-task.json"],
            "filesChanged": [],
            "commandsRun": [],
            "status": "done",
            "executionEvidence": {
                "executionIsolationLevel": "protocol-followed-by-agent",
                "verificationEvidenceLevel": "agent-claimed",
                "runnerName": None,
                "separateInvocationIds": [],
                "schemaValidationCommand": None,
                "hardCheckCommands": [],
                "limitations": ["Smoke handoff is not runner-enforced."],
            },
            "mayEditFiles": True,
            "mayValidate": False,
            "mayRepair": False,
            "mayReport": False,
            "mayCertifyDelivery": False,
            "limitations": ["Smoke handoff."],
            "didNotDo": ["did not validate", "did not certify delivery"],
            "handoffTo": "judicial",
        }
        runner_workflow = {
            "schemaVersion": "1.0",
            "workflowId": "runner-smoke",
            "runId": "runner-smoke-run",
            "runnerName": "top-protocol-runner",
            "mode": "validation",
            "runnerCapabilities": {
                "launchesSeparateProcesses": False,
                "launchesSeparateInvocations": False,
                "isolatesContexts": False,
                "executesHardChecks": True,
                "validatesHandoffs": True,
            },
            "passes": [
                {
                    "passId": "executive-pass",
                    "role": "executive",
                    "taskCapsuleRef": "capsules/executive-task.json",
                    "handoffArtifactRef": "handoffs/executive-pass.json",
                    "invocationId": "invocation-executive",
                    "contextId": "context-executive",
                    "command": None,
                    "cwd": None,
                    "timeoutSeconds": 30,
                    "requiredForDelivery": False,
                }
            ],
            "hardChecks": [
                {
                    "id": "python-smoke",
                    "description": "Python command smoke check",
                    "requiredForComplete": True,
                    "command": [sys.executable, "-B", "-c", "print('runner smoke ok')"],
                    "cwd": None,
                    "timeoutSeconds": 30,
                }
            ],
            "deliveryCertificationRef": None,
            "limitations": ["Smoke run does not prove runner-enforced isolation."],
        }

        write_smoke_json(temp_root / "capsules" / "executive-task.json", capsule)
        write_smoke_json(temp_root / "handoffs" / "executive-pass.json", handoff)

        report, runner_errors = run_workflow(
            runner_workflow,
            temp_root,
            execute_passes=False,
            execute_hard_checks=True,
            accept_external_runner_evidence=False,
        )
        if runner_errors:
            errors.append("top_protocol_runner rejected valid smoke workflow")
            errors.extend(runner_errors)
        if report.get("runnerStatus") != "pass":
            errors.append("top_protocol_runner smoke report did not pass")
        if report.get("executionEvidence", {}).get("verificationEvidenceLevel") != "hard-check-verified":
            errors.append("top_protocol_runner did not produce hard-check-verified evidence")
        if report.get("executionEvidence", {}).get("executionIsolationLevel") == "runner-enforced":
            errors.append("top_protocol_runner claimed runner-enforced without accepted external evidence")
        pass_result = report.get("passResults", [{}])[0]
        if not pass_result.get("contextPackageRef"):
            errors.append("top_protocol_runner smoke did not record contextPackageRef")
        if not pass_result.get("invocationEvidenceRef"):
            errors.append("top_protocol_runner smoke did not record invocationEvidenceRef")
        if pass_result.get("modelInvocationEvidence") is True:
            errors.append("top_protocol_runner process smoke falsely claimed modelInvocationEvidence")
        if not (temp_root / "contexts" / "executive-pass.context-package.json").exists():
            errors.append("top_protocol_runner smoke did not materialize context package")
        if not (temp_root / "invocations" / "executive-pass.invocation-evidence.json").exists():
            errors.append("top_protocol_runner smoke did not record invocation evidence")

        broken = dict(runner_workflow)
        broken["hardChecks"] = [
            {
                "id": "missing-required-command",
                "description": "Invalid required hard check",
                "requiredForComplete": True,
                "command": None,
            }
        ]
        _report, broken_errors = run_workflow(
            broken,
            temp_root,
            execute_passes=False,
            execute_hard_checks=True,
            accept_external_runner_evidence=False,
        )
        if not broken_errors:
            errors.append("top_protocol_runner failed to reject missing required hard-check command")

    return errors


def check_orchestration_certifier_smoke(root):
    errors = []
    if certify_orchestration_run is None:
        return [f"scripts/certify_orchestration_run.py import failed: {certify_orchestration_run_import_error}"]

    with tempfile.TemporaryDirectory(prefix="top-certifier-smoke-") as temp_name:
        temp_root = Path(temp_name).resolve()
        execution_evidence = {
            "executionIsolationLevel": "runner-enforced",
            "verificationEvidenceLevel": "hard-check-verified",
            "runnerName": "top-protocol-runner",
            "separateInvocationIds": ["resp-executive", "resp-judicial"],
            "schemaValidationCommand": "python scripts/top_protocol_runner.py <runner-workflow.json>",
            "hardCheckCommands": ["python -B scripts/quick_validate.py ."],
            "limitations": ["Smoke fixture only."],
        }
        runner_workflow = {
            "schemaVersion": "1.0",
            "workflowId": "certifier-smoke",
            "runId": "certifier-smoke-run",
            "runnerName": "top-protocol-runner",
            "mode": "validation",
            "runnerCapabilities": {
                "launchesSeparateProcesses": True,
                "launchesSeparateInvocations": True,
                "isolatesContexts": True,
                "executesHardChecks": True,
                "validatesHandoffs": True,
            },
            "passes": [
                {
                    "passId": "executive",
                    "role": "executive",
                    "taskCapsuleRef": "capsules/executive.task-capsule.json",
                    "handoffArtifactRef": "handoffs/executive.handoff.json",
                    "invocationId": "resp-executive",
                    "contextId": "resp-executive-fresh-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/executive.context-package.json",
                    "invocationEvidenceRef": "invocations/executive.invocation-evidence.json",
                    "freshContextRequired": True,
                    "command": None,
                    "cwd": None,
                    "timeoutSeconds": 300,
                    "requiredForDelivery": True,
                },
                {
                    "passId": "judicial",
                    "role": "judicial",
                    "taskCapsuleRef": "capsules/judicial.task-capsule.json",
                    "handoffArtifactRef": "handoffs/judicial.handoff.json",
                    "invocationId": "resp-judicial",
                    "contextId": "resp-judicial-fresh-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/judicial.context-package.json",
                    "invocationEvidenceRef": "invocations/judicial.invocation-evidence.json",
                    "freshContextRequired": True,
                    "command": None,
                    "cwd": None,
                    "timeoutSeconds": 300,
                    "requiredForDelivery": True,
                },
            ],
            "hardChecks": [
                {
                    "id": "quick-validate",
                    "description": "Package validation",
                    "requiredForComplete": True,
                    "commandType": "python-script",
                    "scriptRef": "scripts/quick_validate.py",
                    "scriptBaseRef": "skill-root",
                    "args": ["."],
                    "cwdRef": "skill-root",
                    "timeoutSeconds": 300,
                }
            ],
            "deliveryCertificationRef": "reports/delivery-certification.json",
            "limitations": ["Smoke runner workflow."],
        }
        runner_report = {
            "schemaVersion": "1.0",
            "workflowId": "certifier-smoke",
            "runId": "certifier-smoke-run",
            "runnerName": "top-protocol-runner",
            "runnerStatus": "pass",
            "executionEvidence": execution_evidence,
            "passResults": [
                {
                    "passId": "executive",
                    "role": "executive",
                    "invocationId": "resp-executive",
                    "contextId": "resp-executive-fresh-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/executive.context-package.json",
                    "invocationEvidenceRef": "invocations/executive.invocation-evidence.json",
                    "freshContext": True,
                    "receivedOnlyContextPackage": True,
                    "modelInvocationEvidence": True,
                    "status": "pass",
                    "exitCode": 0,
                    "errors": [],
                },
                {
                    "passId": "judicial",
                    "role": "judicial",
                    "invocationId": "resp-judicial",
                    "contextId": "resp-judicial-fresh-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/judicial.context-package.json",
                    "invocationEvidenceRef": "invocations/judicial.invocation-evidence.json",
                    "freshContext": True,
                    "receivedOnlyContextPackage": True,
                    "modelInvocationEvidence": True,
                    "status": "pass",
                    "exitCode": 0,
                    "errors": [],
                },
            ],
            "hardCheckResults": [
                {
                    "id": "quick-validate",
                    "requiredForComplete": True,
                    "status": "pass",
                    "command": "python -B scripts/quick_validate.py .",
                    "exitCode": 0,
                    "evidence": ["quick_validate: OK"],
                }
            ],
            "deliveryCertificationResult": {
                "status": "pass",
                "ref": "reports/delivery-certification.json",
                "errors": [],
            },
            "limitations": ["Smoke runner report."],
        }
        judicial_handoff = {
            "schemaVersion": "1.0",
            "workflowId": "certifier-smoke",
            "passId": "judicial",
            "taskId": "judicial-task",
            "role": "judicial",
            "agentName": "judicial-smoke",
            "taskCapsuleRef": "capsules/judicial.task-capsule.json",
            "inputReferences": ["handoffs/executive.handoff.json"],
            "outputReferences": ["handoffs/judicial.handoff.json"],
            "filesRead": ["runner/runner-report.json"],
            "filesChanged": ["handoffs/judicial.handoff.json"],
            "commandsRun": [],
            "status": "done",
            "executionEvidence": {
                "executionIsolationLevel": "protocol-followed-by-agent",
                "verificationEvidenceLevel": "agent-claimed",
                "runnerName": None,
                "separateInvocationIds": [],
                "schemaValidationCommand": None,
                "hardCheckCommands": [],
                "limitations": ["Judicial smoke handoff."],
            },
            "mayEditFiles": False,
            "mayValidate": True,
            "mayRepair": False,
            "mayReport": True,
            "mayCertifyDelivery": False,
            "limitations": ["Smoke judicial handoff."],
            "didNotDo": ["did not repair", "did not certify delivery"],
            "handoffTo": "certification",
        }

        write_smoke_json(temp_root / "runner" / "runner-workflow.json", runner_workflow)
        write_smoke_json(temp_root / "runner" / "runner-report.json", runner_report)
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)

        class Args:
            root = str(temp_root)
            runner_workflow = "runner/runner-workflow.json"
            runner_report = "runner/runner-report.json"
            judicial_handoff = "handoffs/judicial.handoff.json"
            validation_report = "reports/validation-report.json"
            delivery_certification = "reports/delivery-certification.json"
            final_audit = "reports/final-audit.md"
            snapshot = "reports/certification-snapshot.json"

        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            result = certify_orchestration_run(Args)
        if result != 0:
            errors.append("certify_orchestration_run smoke did not complete")

        delivery = load_json(temp_root / "reports" / "delivery-certification.json")
        validation = load_json(temp_root / "reports" / "validation-report.json")
        if delivery.get("deliveryStatus") != "complete":
            errors.append("certify_orchestration_run smoke did not write complete delivery certification")
        certification_errors = validate_document(delivery, "certifier-smoke-delivery")
        validation_errors = validate_document(validation, "certifier-smoke-validation")
        if certification_errors:
            errors.append("certify_orchestration_run wrote invalid delivery certification")
            errors.extend(certification_errors)
        if validation_errors:
            errors.append("certify_orchestration_run wrote invalid validation report")
            errors.extend(validation_errors)
        snapshot = load_json(temp_root / "reports" / "certification-snapshot.json")
        if not snapshot.get("artifacts"):
            errors.append("certify_orchestration_run did not write snapshot artifacts")
        with contextlib.redirect_stdout(io.StringIO()):
            snapshot_result = verify_certification_snapshot(Args)
        if snapshot_result != 0:
            errors.append("certify_orchestration_run snapshot verification did not report current")

        judicial_handoff["limitations"] = ["Smoke judicial handoff changed after certification."]
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)
        with contextlib.redirect_stdout(io.StringIO()):
            stale_result = verify_certification_snapshot(Args)
        if stale_result == 0:
            errors.append("certify_orchestration_run snapshot verification failed to detect stale artifact")

    return errors


def check_orchestration_state_smoke(root):
    errors = []
    if update_orchestration_state is None:
        return [f"scripts/update_orchestration_state.py import failed: {update_orchestration_state_import_error}"]

    with tempfile.TemporaryDirectory(prefix="top-state-smoke-") as temp_name:
        temp_root = Path(temp_name).resolve()
        runner_workflow = {
            "schemaVersion": "1.0",
            "workflowId": "state-smoke",
            "runId": "state-smoke-run",
            "runnerName": "top-protocol-runner",
            "mode": "validation",
            "runnerCapabilities": {
                "launchesSeparateProcesses": True,
                "launchesSeparateInvocations": True,
                "isolatesContexts": True,
                "executesHardChecks": True,
                "validatesHandoffs": True,
            },
            "passes": [],
            "hardChecks": [],
            "deliveryCertificationRef": "reports/delivery-certification.json",
            "limitations": ["State smoke workflow."],
        }
        runner_report = {
            "schemaVersion": "1.0",
            "workflowId": "state-smoke",
            "runId": "state-smoke-run",
            "runnerName": "top-protocol-runner",
            "runnerStatus": "pass",
            "executionEvidence": {
                "executionIsolationLevel": "runner-enforced",
                "verificationEvidenceLevel": "hard-check-verified",
                "runnerName": "top-protocol-runner",
                "separateInvocationIds": ["executive-invocation", "judicial-invocation"],
                "schemaValidationCommand": "python -B scripts/quick_validate.py .",
                "hardCheckCommands": ["python -B scripts/quick_validate.py ."],
                "limitations": ["State smoke evidence."],
            },
            "passResults": [
                {
                    "passId": "executive",
                    "role": "executive",
                    "invocationId": "executive-invocation",
                    "contextId": "executive-context",
                    "status": "pass",
                    "errors": [],
                },
                {
                    "passId": "judicial",
                    "role": "judicial",
                    "invocationId": "judicial-invocation",
                    "contextId": "judicial-context",
                    "status": "pass",
                    "errors": [],
                },
            ],
            "hardCheckResults": [],
            "deliveryCertificationResult": {
                "status": "pass",
                "ref": "reports/delivery-certification.json",
                "errors": [],
            },
            "limitations": ["State smoke report."],
        }
        judicial_handoff = {
            "schemaVersion": "1.0",
            "workflowId": "state-smoke",
            "passId": "judicial",
            "taskId": "judicial-task",
            "role": "judicial",
            "agentName": "judicial-smoke",
            "taskCapsuleRef": "capsules/judicial.task-capsule.json",
            "inputReferences": ["handoffs/executive.handoff.json"],
            "outputReferences": ["handoffs/judicial.handoff.json"],
            "filesRead": ["runner/runner-report.json"],
            "filesChanged": ["handoffs/judicial.handoff.json"],
            "commandsRun": [],
            "status": "done",
            "executionEvidence": {
                "executionIsolationLevel": "protocol-followed-by-agent",
                "verificationEvidenceLevel": "agent-claimed",
                "runnerName": None,
                "separateInvocationIds": [],
                "schemaValidationCommand": None,
                "hardCheckCommands": [],
                "limitations": ["State smoke judicial handoff."],
            },
            "mayEditFiles": False,
            "mayValidate": True,
            "mayRepair": False,
            "mayReport": True,
            "mayCertifyDelivery": False,
            "limitations": ["State smoke judicial handoff."],
            "didNotDo": ["did not repair", "did not certify delivery"],
            "handoffTo": "certification",
        }
        delivery = {
            "schemaVersion": "1.0",
            "certificationId": "state-smoke-run-delivery-certification",
            "workflowId": "state-smoke",
            "deliveryStatus": "complete",
            "executionEvidence": runner_report["executionEvidence"],
            "judicialValidationRef": "reports/validation-report.json",
            "judicialHandoffRef": "handoffs/judicial.handoff.json",
            "validationReportRef": "reports/validation-report.json",
            "finalAuditReportRef": "reports/final-audit.md",
            "generationOrRepairPassIds": ["executive"],
            "judicialPassId": "judicial",
            "separationOfPowersProof": ["State smoke proof."],
            "requiredHardChecks": [],
            "blockingChecks": [],
            "knownExclusions": [],
            "noBlockingInScopeViolations": True,
            "generationAndValidationSeparate": True,
            "noUnverifiedRequiredGates": True,
            "noRequiredGateFailedOrNotVerified": True,
        }

        write_smoke_json(temp_root / "runner" / "runner-workflow.json", runner_workflow)
        write_smoke_json(temp_root / "runner" / "runner-report.json", runner_report)
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)
        write_smoke_json(temp_root / "reports" / "delivery-certification.json", delivery)
        snapshot = {
            "schemaVersion": "1.0",
            "workflowId": "state-smoke",
            "runId": "state-smoke-run",
            "snapshotStatus": "current",
            "certifiedAt": "2026-05-13T00:00:00Z",
            "certifiedBy": "quick_validate smoke",
            "deliveryStatus": "complete",
            "executionEvidence": runner_report["executionEvidence"],
            "artifacts": [
                {
                    "ref": "runner/runner-report.json",
                    "role": "runner-report",
                    "sha256": smoke_sha256(temp_root / "runner" / "runner-report.json"),
                },
                {
                    "ref": "handoffs/judicial.handoff.json",
                    "role": "judicial-handoff",
                    "sha256": smoke_sha256(temp_root / "handoffs" / "judicial.handoff.json"),
                },
                {
                    "ref": "reports/delivery-certification.json",
                    "role": "delivery-certification",
                    "sha256": smoke_sha256(temp_root / "reports" / "delivery-certification.json"),
                },
            ],
            "limitations": ["State smoke snapshot."],
        }
        write_smoke_json(temp_root / "reports" / "certification-snapshot.json", snapshot)

        class Args:
            root = str(temp_root)
            state = "run-state.json"
            runner_workflow = "runner/runner-workflow.json"
            runner_report = "runner/runner-report.json"
            judicial_handoff = "handoffs/judicial.handoff.json"
            delivery_certification = "reports/delivery-certification.json"
            certification_snapshot = "reports/certification-snapshot.json"
            verify = False
            force = False

        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            result = update_orchestration_state(Args)
        if result != 0:
            errors.append("update_orchestration_state smoke did not write state")
        state = load_json(temp_root / "run-state.json")
        if state.get("currentState") != "certified":
            errors.append("update_orchestration_state smoke did not derive certified state")

        judicial_handoff["limitations"] = ["State smoke judicial handoff changed after certification."]
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)
        with contextlib.redirect_stdout(io.StringIO()):
            stale_result = update_orchestration_state(Args)
        if stale_result != 0:
            errors.append("update_orchestration_state smoke did not allow certified to stale transition")
        stale_state = load_json(temp_root / "run-state.json")
        if stale_state.get("currentState") != "stale":
            errors.append("update_orchestration_state smoke did not derive stale state")

    return errors


def check_orchestration_run_verifier_smoke(root):
    errors = []
    if validate_orchestration_run is None:
        return [f"scripts/validate_orchestration_run.py import failed: {validate_orchestration_run_import_error}"]
    if update_orchestration_state is None:
        return [f"scripts/update_orchestration_state.py import failed: {update_orchestration_state_import_error}"]

    with tempfile.TemporaryDirectory(prefix="top-run-verifier-smoke-") as temp_name:
        temp_root = Path(temp_name).resolve()
        execution_evidence = {
            "executionIsolationLevel": "runner-enforced",
            "verificationEvidenceLevel": "hard-check-verified",
            "runnerName": "top-protocol-runner",
            "separateInvocationIds": ["executive-invocation", "judicial-invocation"],
            "schemaValidationCommand": "python -B scripts/top_protocol_runner.py runner/runner-workflow.json",
            "hardCheckCommands": ["python -B scripts/quick_validate.py ."],
            "limitations": ["Verifier smoke evidence."],
        }
        runner_workflow = {
            "schemaVersion": "1.0",
            "workflowId": "run-verifier-smoke",
            "runId": "run-verifier-smoke-run",
            "runnerName": "top-protocol-runner",
            "mode": "validation",
            "runnerCapabilities": {
                "launchesSeparateProcesses": True,
                "launchesSeparateInvocations": True,
                "isolatesContexts": True,
                "executesHardChecks": True,
                "validatesHandoffs": True,
            },
            "passes": [
                {
                    "passId": "executive",
                    "role": "executive",
                    "taskCapsuleRef": "capsules/executive.task-capsule.json",
                    "handoffArtifactRef": "handoffs/executive.handoff.json",
                    "invocationId": "executive-invocation",
                    "contextId": "executive-context",
                    "requiredForDelivery": True,
                },
                {
                    "passId": "judicial",
                    "role": "judicial",
                    "taskCapsuleRef": "capsules/judicial.task-capsule.json",
                    "handoffArtifactRef": "handoffs/judicial.handoff.json",
                    "invocationId": "judicial-invocation",
                    "contextId": "judicial-context",
                    "requiredForDelivery": True,
                },
            ],
            "hardChecks": [],
            "deliveryCertificationRef": "reports/delivery-certification.json",
            "limitations": ["Verifier smoke workflow."],
        }
        runner_report = {
            "schemaVersion": "1.0",
            "workflowId": "run-verifier-smoke",
            "runId": "run-verifier-smoke-run",
            "runnerName": "top-protocol-runner",
            "runnerStatus": "pass",
            "executionEvidence": execution_evidence,
            "passResults": [
                {
                    "passId": "executive",
                    "role": "executive",
                    "invocationId": "executive-invocation",
                    "contextId": "executive-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/executive.context-package.json",
                    "invocationEvidenceRef": "invocations/executive.invocation-evidence.json",
                    "freshContext": True,
                    "receivedOnlyContextPackage": True,
                    "modelInvocationEvidence": True,
                    "status": "pass",
                    "exitCode": 0,
                    "errors": [],
                },
                {
                    "passId": "judicial",
                    "role": "judicial",
                    "invocationId": "judicial-invocation",
                    "contextId": "judicial-context",
                    "adapterKind": "llm-api",
                    "contextPackageRef": "contexts/judicial.context-package.json",
                    "invocationEvidenceRef": "invocations/judicial.invocation-evidence.json",
                    "freshContext": True,
                    "receivedOnlyContextPackage": True,
                    "modelInvocationEvidence": True,
                    "status": "pass",
                    "exitCode": 0,
                    "errors": [],
                },
            ],
            "hardCheckResults": [],
            "deliveryCertificationResult": {
                "status": "pass",
                "ref": "reports/delivery-certification.json",
                "errors": [],
            },
            "limitations": ["Verifier smoke report."],
        }
        judicial_handoff = {
            "schemaVersion": "1.0",
            "workflowId": "run-verifier-smoke",
            "passId": "judicial",
            "taskId": "judicial-task",
            "role": "judicial",
            "agentName": "judicial-smoke",
            "taskCapsuleRef": "capsules/judicial.task-capsule.json",
            "inputReferences": ["handoffs/executive.handoff.json"],
            "outputReferences": ["handoffs/judicial.handoff.json"],
            "filesRead": ["runner/runner-report.json"],
            "filesChanged": ["handoffs/judicial.handoff.json"],
            "commandsRun": [],
            "status": "done",
            "executionEvidence": {
                "executionIsolationLevel": "protocol-followed-by-agent",
                "verificationEvidenceLevel": "agent-claimed",
                "runnerName": None,
                "separateInvocationIds": [],
                "schemaValidationCommand": None,
                "hardCheckCommands": [],
                "limitations": ["Verifier smoke judicial handoff."],
            },
            "mayEditFiles": False,
            "mayValidate": True,
            "mayRepair": False,
            "mayReport": True,
            "mayCertifyDelivery": False,
            "limitations": ["Verifier smoke judicial handoff."],
            "didNotDo": ["did not repair", "did not certify delivery"],
            "handoffTo": "certification",
        }
        delivery = {
            "schemaVersion": "1.0",
            "certificationId": "run-verifier-smoke-run-delivery-certification",
            "workflowId": "run-verifier-smoke",
            "deliveryStatus": "complete",
            "executionEvidence": execution_evidence,
            "judicialValidationRef": "reports/validation-report.json",
            "judicialHandoffRef": "handoffs/judicial.handoff.json",
            "validationReportRef": "reports/validation-report.json",
            "finalAuditReportRef": "reports/final-audit.md",
            "generationOrRepairPassIds": ["executive"],
            "judicialPassId": "judicial",
            "separationOfPowersProof": ["Verifier smoke proof."],
            "requiredHardChecks": [],
            "blockingChecks": [],
            "knownExclusions": [],
            "noBlockingInScopeViolations": True,
            "generationAndValidationSeparate": True,
            "noUnverifiedRequiredGates": True,
            "noRequiredGateFailedOrNotVerified": True,
        }

        write_smoke_json(temp_root / "runner" / "runner-workflow.json", runner_workflow)
        write_smoke_json(temp_root / "runner" / "runner-report.json", runner_report)
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)
        write_smoke_json(temp_root / "reports" / "delivery-certification.json", delivery)
        snapshot = {
            "schemaVersion": "1.0",
            "workflowId": "run-verifier-smoke",
            "runId": "run-verifier-smoke-run",
            "snapshotStatus": "current",
            "certifiedAt": "2026-05-13T00:00:00Z",
            "certifiedBy": "quick_validate smoke",
            "deliveryStatus": "complete",
            "executionEvidence": execution_evidence,
            "artifacts": [
                {
                    "ref": "runner/runner-report.json",
                    "role": "runner-report",
                    "sha256": smoke_sha256(temp_root / "runner" / "runner-report.json"),
                },
                {
                    "ref": "handoffs/judicial.handoff.json",
                    "role": "judicial-handoff",
                    "sha256": smoke_sha256(temp_root / "handoffs" / "judicial.handoff.json"),
                },
                {
                    "ref": "reports/delivery-certification.json",
                    "role": "delivery-certification",
                    "sha256": smoke_sha256(temp_root / "reports" / "delivery-certification.json"),
                },
            ],
            "limitations": ["Verifier smoke snapshot."],
        }
        write_smoke_json(temp_root / "reports" / "certification-snapshot.json", snapshot)

        class StateArgs:
            root = str(temp_root)
            state = "run-state.json"
            runner_workflow = "runner/runner-workflow.json"
            runner_report = "runner/runner-report.json"
            judicial_handoff = "handoffs/judicial.handoff.json"
            delivery_certification = "reports/delivery-certification.json"
            certification_snapshot = "reports/certification-snapshot.json"
            verify = False
            force = False

        class VerifyArgs:
            root = str(temp_root)
            state = "run-state.json"
            runner_workflow = "runner/runner-workflow.json"
            runner_report = "runner/runner-report.json"
            judicial_handoff = "handoffs/judicial.handoff.json"
            delivery_certification = "reports/delivery-certification.json"
            certification_snapshot = "reports/certification-snapshot.json"

        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            state_result = update_orchestration_state(StateArgs)
        if state_result != 0:
            errors.append("run verifier smoke could not write state")

        status, delivery_status, invalid, stale = validate_orchestration_run(VerifyArgs)
        if status != "RUN_VALID certified" or delivery_status != "complete" or invalid or stale:
            errors.append("validate_orchestration_run did not accept valid certified smoke run")
            errors.extend(invalid)
            errors.extend(stale)

        judicial_handoff["limitations"] = ["Verifier smoke judicial handoff changed after certification."]
        write_smoke_json(temp_root / "handoffs" / "judicial.handoff.json", judicial_handoff)
        status, _delivery_status, invalid, stale = validate_orchestration_run(VerifyArgs)
        if status != "RUN_STALE" or invalid or not stale:
            errors.append("validate_orchestration_run did not report stale smoke run")
            errors.extend(invalid)

    return errors


def check_orchestration_workflow_driver_smoke(root):
    errors = []
    if run_orchestration_workflow is None:
        return [f"scripts/run_orchestration_workflow.py import failed: {run_orchestration_workflow_import_error}"]

    with tempfile.TemporaryDirectory(prefix="top-workflow-driver-smoke-") as temp_name:
        temp_root = Path(temp_name).resolve()
        workflow_id = "workflow-driver-smoke"
        run_id = "workflow-driver-smoke-run"
        (temp_root / "capsules").mkdir(parents=True, exist_ok=True)
        (temp_root / "runner").mkdir(parents=True, exist_ok=True)
        (temp_root / "reports").mkdir(parents=True, exist_ok=True)
        (temp_root / "scratch").mkdir(parents=True, exist_ok=True)
        (temp_root / "handoffs").mkdir(parents=True, exist_ok=True)

        adapter_script = r'''
import json
import os
from pathlib import Path

root = Path.cwd().resolve()
context_ref = os.environ["TOP_CONTEXT_PACKAGE"]
handoff_ref = os.environ["TOP_HANDOFF_ARTIFACT"]
context = json.loads((root / context_ref).read_text(encoding="utf-8"))
capsule = json.loads((root / context["taskCapsuleRef"]).read_text(encoding="utf-8"))
role = capsule["role"]
pass_id = context["passId"]
handoff = {
    "schemaVersion": "1.0",
    "workflowId": context["workflowId"],
    "passId": pass_id,
    "taskId": capsule["taskId"],
    "role": role,
    "agentName": f"{role}-process-smoke",
    "taskCapsuleRef": context["taskCapsuleRef"],
    "inputReferences": capsule.get("inputReferences", []),
    "outputReferences": [handoff_ref],
    "filesRead": [context_ref, context["taskCapsuleRef"]],
    "filesChanged": [handoff_ref],
    "commandsRun": ["scratch/process_pass.py"],
    "status": "done",
    "executionEvidence": {
        "executionIsolationLevel": "protocol-followed-by-agent",
        "verificationEvidenceLevel": "agent-claimed",
        "runnerName": None,
        "separateInvocationIds": [],
        "schemaValidationCommand": None,
        "hardCheckCommands": [],
        "limitations": ["Process smoke pass cannot prove model context isolation."],
    },
    "limitations": ["Process smoke pass completed without model invocation evidence."],
    "didNotDo": capsule.get("forbiddenActions", []),
    "handoffTo": "judicial" if role == "executive" else "certification",
    "mayEditFiles": bool(capsule.get("mayEditFiles")),
    "mayValidate": bool(capsule.get("mayValidate")),
    "mayRepair": bool(capsule.get("mayRepair")),
    "mayReport": bool(capsule.get("mayReport")),
    "mayCertifyDelivery": bool(capsule.get("mayCertifyDelivery")),
}
(root / handoff_ref).parent.mkdir(parents=True, exist_ok=True)
(root / handoff_ref).write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
'''
        (temp_root / "scratch" / "process_pass.py").write_text(adapter_script.strip() + "\n", encoding="utf-8")

        def capsule(pass_id, role):
            is_judicial = role == "judicial"
            return {
                "schemaVersion": "1.0",
                "workflowId": workflow_id,
                "taskId": f"{pass_id}-task",
                "role": role,
                "objective": f"Run {role} driver smoke pass.",
                "allowedActions": ["write scoped handoff"],
                "forbiddenActions": ["certify delivery", "use hidden prior chat"],
                "inputReferences": ["handoffs/executive.handoff.json"] if is_judicial else [],
                "contextSlices": [f"Concrete context for {role} driver smoke pass."],
                "outputContract": f"handoffs/{pass_id}.handoff.json",
                "requiredChecks": [],
                "stopCondition": "Write one handoff artifact and stop.",
                "mayEditFiles": False,
                "mayValidate": is_judicial,
                "mayRepair": False,
                "mayReport": is_judicial,
                "mayCertifyDelivery": False,
            }

        for pass_id, role in [("executive", "executive"), ("judicial", "judicial")]:
            write_smoke_json(temp_root / "capsules" / f"{pass_id}.task-capsule.json", capsule(pass_id, role))

        runner_workflow = {
            "schemaVersion": "1.0",
            "workflowId": workflow_id,
            "runId": run_id,
            "runnerName": "top-protocol-runner",
            "mode": "validation",
            "runnerCapabilities": {
                "launchesSeparateProcesses": True,
                "launchesSeparateInvocations": False,
                "isolatesContexts": False,
                "executesHardChecks": True,
                "validatesHandoffs": True,
            },
            "passes": [
                {
                    "passId": pass_id,
                    "role": role,
                    "taskCapsuleRef": f"capsules/{pass_id}.task-capsule.json",
                    "handoffArtifactRef": f"handoffs/{pass_id}.handoff.json",
                    "invocationId": f"{run_id}-{pass_id}-invocation",
                    "contextId": f"{run_id}-{pass_id}-context",
                    "adapterKind": "process",
                    "contextPackageRef": f"contexts/{pass_id}.context-package.json",
                    "invocationEvidenceRef": f"invocations/{pass_id}.invocation-evidence.json",
                    "freshContextRequired": True,
                    "commandType": "python-script",
                    "scriptRef": "process_pass.py",
                    "scriptBaseRef": "scratch",
                    "cwdRef": "runner-root",
                    "timeoutSeconds": 60,
                    "requiredForDelivery": True,
                }
                for pass_id, role in [("executive", "executive"), ("judicial", "judicial")]
            ],
            "hardChecks": [],
            "deliveryCertificationRef": "reports/delivery-certification.json",
            "limitations": ["Driver smoke uses process passes, not model invocation evidence."],
        }
        write_smoke_json(temp_root / "runner" / "runner-workflow.json", runner_workflow)

        protocol_evidence = {
            "executionIsolationLevel": "protocol-defined",
            "verificationEvidenceLevel": "none",
            "runnerName": None,
            "separateInvocationIds": [],
            "schemaValidationCommand": None,
            "hardCheckCommands": [],
            "limitations": ["Initial driver smoke certification placeholder."],
        }
        delivery = {
            "schemaVersion": "1.0",
            "certificationId": f"{run_id}-delivery-certification",
            "workflowId": workflow_id,
            "deliveryStatus": "not-certified",
            "executionEvidence": protocol_evidence,
            "judicialValidationRef": "reports/validation-report.json",
            "judicialHandoffRef": "handoffs/judicial.handoff.json",
            "validationReportRef": "reports/validation-report.json",
            "finalAuditReportRef": "reports/final-audit.md",
            "generationOrRepairPassIds": [],
            "judicialPassId": "judicial",
            "separationOfPowersProof": ["Driver smoke starts not-certified."],
            "requiredHardChecks": [],
            "blockingChecks": [
                {
                    "checkId": "runner-evidence",
                    "status": "not_verified",
                    "evidence": ["Runner has not produced evidence yet."],
                }
            ],
            "knownExclusions": [],
            "noBlockingInScopeViolations": False,
            "generationAndValidationSeparate": False,
            "noUnverifiedRequiredGates": False,
            "noRequiredGateFailedOrNotVerified": False,
        }
        write_smoke_json(temp_root / "reports" / "delivery-certification.json", delivery)

        skill_root = str(root)

        class Args:
            root = skill_root
            run_root = str(temp_root)
            workflow_id = None
            run_id = None
            mode = "validation"
            runner_name = "top-protocol-runner"
            adapter_kind = "process"
            llm_smoke = False
            adapter_dry_run = False
            pass_ = None
            force = False
            create = False
            skip_create = True
            skip_runner = False
            skip_certification = False
            skip_snapshot_verify = False
            execute_passes = True
            execute_hard_checks = False
            accept_external_runner_evidence = False
            stop_on_runner_failure = False
            runner_workflow = "runner/runner-workflow.json"
            runner_report = "runner/runner-report.json"
            judicial_handoff = "handoffs/judicial.handoff.json"
            validation_report = "reports/validation-report.json"
            delivery_certification = "reports/delivery-certification.json"
            final_audit = "reports/final-audit.md"
            certification_snapshot = "reports/certification-snapshot.json"
            state = "run-state.json"

        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            status, delivery_status, invalid, stale, run_root = run_orchestration_workflow(Args)
        if status != "RUN_VALID not-certified":
            errors.append(f"run_orchestration_workflow smoke expected RUN_VALID not-certified, got {status}")
        if delivery_status != "not-certified":
            errors.append(f"run_orchestration_workflow smoke expected not-certified delivery, got {delivery_status}")
        if invalid:
            errors.extend(invalid)
        if stale:
            errors.extend(stale)
        state = load_json(temp_root / "run-state.json")
        if state.get("currentState") != "not-certified":
            errors.append("run_orchestration_workflow smoke did not derive not-certified state")

    return errors


def check_orchestration_regression_fixtures(root):
    if run_orchestration_regressions is None:
        return [f"scripts/validate_orchestration_regressions.py import failed: {run_orchestration_regressions_import_error}"]
    return run_orchestration_regressions()


CONTENT_SOURCE_SUFFIXES = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
    ".kt",
    ".swift",
    ".dart",
    ".java",
    ".cs",
    ".go",
    ".rs",
}

SKIP_PREFILTER_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".expo",
}

CONTENT_BOUNDARY_RE = re.compile(
    r"\b(class|function|struct|object)\s+[A-Za-z_][A-Za-z0-9_]*Content\b"
    r"|\b[A-Za-z_][A-Za-z0-9_]*Content\s*[:=]\s*(function|\(|class\b)"
)

CONDITIONAL_CONSTRUCT_RE = re.compile(
    r"\bif\s*\("
    r"|\belse\b"
    r"|\bswitch\s*\("
    r"|\bcase\b"
    r"|\bmatch\b"
    r"|\bwhen\b"
    r"|\bguard\b"
    r"|\?.*:"
    r"|&&"
    r"|\|\|"
)

TOP_OBJECT_CONSTRUCTOR_RE = re.compile(
    r"\bnew\s+[A-Za-z_][A-Za-z0-9_]*(Node|Content|Connector|Boundary)\s*\(([^)]*)\)"
)

CONSTRUCTOR_SIGNATURE_RE = re.compile(r"\bconstructor\s*\(([^)]*)\)")

SUSPICIOUS_ARG_NAME_RE = re.compile(
    r"\b(data|config|options|props|callbacks?|handlers?|state|flags?|services?|stores?|title|label|text|visible|visibility|token|children|child|view)\b",
    re.IGNORECASE,
)

POST_CONSTRUCTION_PUSH_RE = re.compile(
    r"\.\s*(applyConfig|applyState|setData|setCallbacks|setVisible|setText|setStyle|setClass|setPaddingLeft|updateText|updateFromState|updateToggle|renderWith)\s*\("
)

CONTENT_PRIVACY_RE = re.compile(
    r"\bimport\s+\{[^}]*[A-Za-z_][A-Za-z0-9_]*Content\b"
)

CONTROLLER_FRAGMENT_OUTPUT_RE = re.compile(
    r"\b(get|render|build)[A-Za-z0-9_]*(View|Content|Fragment|Widget|Element)\s*\([^)]*\)\s*"
    r"(:\s*(React\.ReactNode|React\.ReactElement|ReactElement|JSX\.Element|HTMLElement|Element|View|Widget|Fragment)|=>\s*<)",
    re.IGNORECASE,
)

CONTENT_SETTER_HANDLE_RE = re.compile(
    r"\b(set[A-Z][A-Za-z0-9_]*|update[A-Z][A-Za-z0-9_]*)\b.*\b(IControllerAccess|IContentAccess|controller|parent|adapter|helper)\b"
    r"|\b(this\.)?_[A-Za-z0-9_]*(setter|set[A-Z]|update[A-Z])[A-Za-z0-9_]*\s*=",
    re.IGNORECASE,
)

EXAMPLE_TEXT_SUFFIXES = {".md", ".json", ".ts", ".tsx", ".js", ".jsx"}

EXAMPLE_INVALID_PATTERN_RE = re.compile(
    r"legacy-invalid"
    r"|legacy invalid"
    r"|named content command"
    r"|content command"
    r"|\bContent/View\b"
    r"|setText\s*\("
    r"|setVisible\s*\("
    r"|setStyle\s*\("
    r"|setClass\s*\("
    r"|setPaddingLeft\s*\("
    r"|updateText\s*\("
    r"|updateFromState\s*\("
    r"|updateToggle\s*\("
    r"|applyState\s*\("
    r"|renderWith\s*\("
    r"|commands and data descend"
    r"|parent passes command"
    r"|sourceData"
    r"|mount\s*\([^)]*source"
    r"|Text content format"
    r"|__BUILD_TIME__"
    r"|text content\s+[\"']"
    r"|content-side derivation",
    re.IGNORECASE,
)

EXPLICIT_INVALID_MARKER_RE = re.compile(
    r"invalid|failure case|anti-pattern|anti pattern|not canonical",
    re.IGNORECASE,
)


def is_within_skipped_dir(path, root):
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_PREFILTER_DIRS for part in parts)


def is_content_candidate_path(path):
    stem = path.stem.lower()
    return stem.endswith("content") or "-content" in stem or "_content" in stem


def iter_content_boundary_lines(text, scan_entire_file):
    lines = text.splitlines()
    if scan_entire_file:
        for line_number, line in enumerate(lines, start=1):
            yield line_number, line
        return

    inside = False
    depth = 0
    for line_number, line in enumerate(lines, start=1):
        if not inside and CONTENT_BOUNDARY_RE.search(line):
            inside = True
            depth = 0

        if inside:
            yield line_number, line
            depth += line.count("{") - line.count("}")
            if depth <= 0 and "{" in line:
                inside = False


def check_locally_implemented_content_conditional_prefilter(root):
    """Platform-neutral candidate scan only; Validation Agent makes verdicts."""
    candidates = []
    for path in sorted(root.glob("**/*")):
        if path.is_dir() or is_within_skipped_dir(path, root):
            continue
        if path.suffix.lower() not in CONTENT_SOURCE_SUFFIXES:
            continue

        text = read_text(path)
        scan_entire_file = is_content_candidate_path(path)
        if not scan_entire_file and not CONTENT_BOUNDARY_RE.search(text):
            continue

        for line_number, line in iter_content_boundary_lines(text, scan_entire_file):
            if CONDITIONAL_CONSTRUCT_RE.search(line):
                candidates.append(
                    f"{rel(path, root)}:{line_number}: candidate locally implemented "
                    "content conditional selection construct; Validation Agent must review"
                )

    return candidates


def has_multiple_args(args_text):
    stripped = args_text.strip()
    if not stripped:
        return False
    return "," in stripped


def check_context_attachment_prefilter(root):
    """Platform-neutral candidate scan only; Validation Agent makes verdicts."""
    candidates = []
    for path in sorted(root.glob("**/*")):
        if path.is_dir() or is_within_skipped_dir(path, root):
            continue
        if path.suffix.lower() not in CONTENT_SOURCE_SUFFIXES:
            continue

        text = read_text(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in TOP_OBJECT_CONSTRUCTOR_RE.finditer(line):
                args_text = match.group(2)
                if has_multiple_args(args_text) or SUSPICIOUS_ARG_NAME_RE.search(args_text):
                    candidates.append(
                        f"{rel(path, root)}:{line_number}: candidate context data injection "
                        "in TOP object construction; Validation Agent must review"
                    )

            for match in CONSTRUCTOR_SIGNATURE_RE.finditer(line):
                args_text = match.group(1)
                if has_multiple_args(args_text) and SUSPICIOUS_ARG_NAME_RE.search(args_text):
                    candidates.append(
                        f"{rel(path, root)}:{line_number}: candidate constructor data/config/state "
                        "injection; Validation Agent must review"
                    )

            if POST_CONSTRUCTION_PUSH_RE.search(line):
                candidates.append(
                    f"{rel(path, root)}:{line_number}: candidate setter-style post-construction "
                    "data/config/state push; Validation Agent must review"
                )

    return candidates


def check_example_consistency_prefilter(root):
    """Example/documentation scan only; Validation Agent reviews architecture."""
    candidates = []
    examples_root = root / "examples"
    if not examples_root.exists():
        return candidates

    for path in sorted(examples_root.glob("**/*")):
        if path.is_dir() or is_within_skipped_dir(path, root):
            continue
        if path.suffix.lower() not in EXAMPLE_TEXT_SUFFIXES:
            continue
        text = read_text(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not EXAMPLE_INVALID_PATTERN_RE.search(line):
                continue
            if EXPLICIT_INVALID_MARKER_RE.search(line):
                continue
            candidates.append(
                f"{rel(path, root)}:{line_number}: example may demonstrate an old "
                "content-command/data-injection pattern; Validation Agent must review"
            )

    return candidates


def check_content_privacy_prefilter(root):
    """Platform-neutral-ish source scan; Validation Agent makes verdicts."""
    candidates = []
    for path in sorted(root.glob("**/*")):
        if path.is_dir() or is_within_skipped_dir(path, root):
            continue
        if path.suffix.lower() not in CONTENT_SOURCE_SUFFIXES:
            continue
        text = read_text(path)
        owning_controller_hint = path.stem.lower().endswith("node") or "controller" in path.stem.lower()
        for line_number, line in enumerate(text.splitlines(), start=1):
            if CONTENT_PRIVACY_RE.search(line) and not owning_controller_hint:
                if "DomContent" in line and not re.search(r"\b[A-Za-z_][A-Za-z0-9_]+Content\b", line.replace("DomContent", "")):
                    continue
                candidates.append(
                    f"{rel(path, root)}:{line_number}: candidate concrete content privacy "
                    "breach; Validation Agent must review"
                )
            if CONTROLLER_FRAGMENT_OUTPUT_RE.search(line):
                if re.search(r"\bgetView\s*\(\)\s*:\s*HTMLElement\b", line):
                    continue
                candidates.append(
                    f"{rel(path, root)}:{line_number}: candidate controller platform/content "
                    "fragment output; Validation Agent must review"
                )
            if CONTENT_SETTER_HANDLE_RE.search(line):
                candidates.append(
                    f"{rel(path, root)}:{line_number}: candidate content-owned setter bridge; "
                    "Validation Agent must review"
                )
    return candidates


def check_project_spec_shape(root):
    errors = []
    spec_paths = []
    specs_root = root / "top" / "specs"
    if specs_root.exists():
        spec_paths.extend(sorted(specs_root.glob("**/*.json")))
    for candidate in (root / "top" / "spec.json", root / "top" / "tree.json"):
        if candidate.exists():
            spec_paths.append(candidate)
    examples_root = root / "examples"
    if examples_root.exists():
        spec_paths.extend(sorted(examples_root.glob("**/*.json")))
    if not spec_paths:
        return errors

    canonical_node_order = ["type", "doc", "prompt", "props", "children"]

    def enforces_canonical_type(path):
        try:
            return specs_root.exists() and specs_root in path.parents
        except Exception:
            return False

    def visit(value, path, trail):
        if isinstance(value, dict):
            looks_like_node = any(key in value for key in ("children", "prompt", "props", "doc"))
            if enforces_canonical_type(path) and looks_like_node and "type" not in value and ("id" in value or "name" in value):
                errors.append(f"{rel(path, root)}:{trail}: node-like object lacks canonical type field")
            if "type" in value and looks_like_node:
                actual_order = [key for key in value.keys() if key in canonical_node_order]
                expected_order = [key for key in canonical_node_order if key in value]
                if actual_order != expected_order:
                    errors.append(
                        f"{rel(path, root)}:{trail}: TOP node fields must use canonical order "
                        "`type`, `doc`, `prompt`, `props`, `children`"
                    )
            for key, child in value.items():
                visit(child, path, f"{trail}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, path, f"{trail}[{index}]")

    for path in spec_paths:
        try:
            data = load_json(path)
        except Exception:
            continue
        visit(data, path, "$")
    return errors


def check_repair_artifact_fixture_smoke(root):
    if validate_repair_artifact_fixture is None:
        return [f"scripts/validate_repair_artifact_fixture.py import failed: {validate_repair_artifact_fixture_import_error}"]

    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        artifact = Path(tmp) / "repair-target.json"
        artifact.write_text(
            json.dumps(
                {
                    "component": "DriverStatusBadge",
                    "statusLabel": "Ready",
                    "isValid": True,
                    "repairedBy": "repair-1",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        if validate_repair_artifact_fixture(artifact):
            errors.append("validate_repair_artifact_fixture did not accept valid repaired artifact")

        artifact.write_text(
            json.dumps(
                {
                    "component": "DriverStatusBadge",
                    "statusLabel": "Broken",
                    "isValid": False,
                    "repairedBy": "repair-1",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        if not validate_repair_artifact_fixture(artifact):
            errors.append("validate_repair_artifact_fixture did not reject invalid repaired artifact")
    return errors


def run(root):
    hard_checks = [
        ("required paths", check_required_paths),
        ("json parse", check_json_parse),
        ("manifest references", check_manifest_references),
        ("hydration manifest", check_hydration_manifest),
        ("version consistency", check_version_consistency),
        ("top governance consistency", check_top_governance_consistency),
        ("markdown links", check_markdown_links),
        ("required phrases", check_required_phrases),
        ("risky patterns", check_known_risky_patterns),
        ("runtime branch binding consistency", check_runtime_branch_binding_consistency),
        ("branch-scoped migration control", check_branch_scoped_migration_control_consistency),
        ("migration git branch safety", check_migration_git_branch_safety_consistency),
        ("validation control consistency", check_validation_control_consistency),
        ("execution evidence validator smoke", check_execution_evidence_validator_smoke),
        ("top protocol runner smoke", check_top_protocol_runner_smoke),
        ("orchestration certifier smoke", check_orchestration_certifier_smoke),
        ("orchestration state smoke", check_orchestration_state_smoke),
        ("orchestration run verifier smoke", check_orchestration_run_verifier_smoke),
        ("orchestration workflow driver smoke", check_orchestration_workflow_driver_smoke),
        ("orchestration regression fixtures", check_orchestration_regression_fixtures),
        ("repair artifact fixture smoke", check_repair_artifact_fixture_smoke),
        ("project spec shape", check_project_spec_shape),
    ]
    all_errors = []
    for name, check in hard_checks:
        errors = check(root)
        if errors:
            all_errors.append((name, errors))

    agent_review_candidates = []
    agent_review_candidates.extend(check_locally_implemented_content_conditional_prefilter(root))
    agent_review_candidates.extend(check_context_attachment_prefilter(root))
    agent_review_candidates.extend(check_example_consistency_prefilter(root))
    agent_review_candidates.extend(check_content_privacy_prefilter(root))

    if all_errors:
        print("quick_validate: FAILED")
        for name, errors in all_errors:
            print(f"\n[{name}]")
            for error in errors:
                print(f"- {error}")
        if agent_review_candidates:
            print("\n[agent review candidates]")
            for candidate in agent_review_candidates:
                print(f"- {candidate}")
        return 1

    if agent_review_candidates:
        print("quick_validate: REVIEW REQUIRED")
        print(f"validated: {root}")
        print(f"hard_checks: {len(hard_checks)}")
        print("\n[agent review candidates]")
        for candidate in agent_review_candidates:
            print(f"- {candidate}")
        return 0

    print("quick_validate: OK")
    print(f"validated: {root}")
    print(f"hard_checks: {len(hard_checks)}")
    print("agent_review_candidates: 0")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Quick sanity validation for top-skill package.")
    parser.add_argument("root", nargs="?", default=".", help="Path to top-skill root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"quick_validate: root does not exist: {root}", file=sys.stderr)
        return 2
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
