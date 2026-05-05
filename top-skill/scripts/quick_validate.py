#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


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
    "canon/controller-content-rules.md",
    "canon/forbidden-confusions.md",
    "canon/validation-rules.md",
    "rules/violation-catalog.md",
    "rules/pattern-recognition.md",
    "rules/spec-sync-rules.md",
    "rules/review-checklist.md",
    "contracts/top-folder-contract.md",
    "rules/typing-checklist.md",
    "references/node-model.md",
    "references/code-generation.md",
    "references/event-model.md",
    "references/pattern-cards.md",
    "references/node-validation-rules.md",
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
        "agents/migration-infrastructure-agent.md",
        "agents/migration-planning-agent.md",
        "contracts/agent-output-contracts/migration-infrastructure-output.md",
        "contracts/agent-output-contracts/migration-plan-output.md",
        "top/schemas/migration-workflow.schema.json",
    ]
    for item in required_migration_reads:
        if item not in quickstart:
            errors.append(f"QUICKSTART_MIN_READS.md migration minimum missing: {item}")

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
        ("rules/skill-maintenance-rules.md", "No exhaustive-looking technology lists"),
        ("rules/skill-maintenance-rules.md", "Missed case feedback loop"),
        ("rules/violation-catalog.md", "CORE-026"),
        ("rules/violation-catalog.md", "CORE-027"),
        ("rules/violation-catalog.md", "CORE-028"),
        ("rules/violation-catalog.md", "CORE-029"),
        ("rules/violation-catalog.md", "CORE-030"),
        ("rules/violation-catalog.md", "CORE-031"),
        ("rules/violation-catalog.md", "CORE-032"),
        ("rules/violation-catalog.md", "Locally implemented content"),
        ("rules/pattern-recognition.md", "Locally implemented content conditional selection"),
        ("rules/pattern-recognition.md", "Context data injection"),
        ("rules/pattern-recognition.md", "reports candidates for Validation Agent review"),
        ("rules/violation-catalog.md", "CONV-007"),
        ("rules/violation-catalog.md", "CONV-008"),
        ("rules/violation-catalog.md", "WF-010"),
        ("rules/violation-catalog.md", "WF-011"),
        ("rules/violation-catalog.md", "WF-012"),
        ("rules/violation-catalog.md", "WF-013"),
        ("rules/violation-catalog.md", "WF-014"),
        ("rules/violation-catalog.md", "WF-015"),
        ("rules/violation-catalog.md", "WF-016"),
        ("contracts/top-folder-contract.md", "top_src/<branch-id>/"),
        ("contracts/top-folder-contract.md", "top/specs/settings-branch.json"),
        ("contracts/top-folder-contract.md", "MIGRATION_WORKFLOW.json"),
        ("contracts/top-folder-contract.md", "MIGRATION_PLAN.md"),
        ("contracts/top-folder-contract.md", "MIGRATION_LOG.md"),
        ("canon/migration.md", "Migration artifact layout must be canonical"),
        ("canon/migration.md", "Migration workflow tree, plan, and action log are mandatory"),
        ("agents/migration-infrastructure-agent.md", "MIGRATION_PLAN.md"),
        ("agents/migration-infrastructure-agent.md", "MIGRATION_WORKFLOW.json"),
        ("agents/migration-planning-agent.md", "MIGRATION_PLAN.md"),
        ("agents/migration-planning-agent.md", "MIGRATION_WORKFLOW.json"),
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
        ("references/event-model.md", "Presentation content reports intent"),
        ("references/pattern-cards.md", "explicit ancestor/context contract"),
        ("prompts/generate-top-node.md", "do not generate conditional selection logic inside locally implemented"),
        ("prompts/verify-node-implementation-prompt.md", "locally implemented content contains no conditional"),
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
        ("examples/tree-editor/README.md", "canonical for top-skill 1.1.18"),
        ("rules/pattern-recognition.md", "Output derivation inside locally implemented content"),
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
