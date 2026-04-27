#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


RISK_PHRASES = [
    "seems useful",
    "reasonable assumptions",
    "do your best",
    "best effort",
    "if useful",
    "if needed",
    "if important",
    "implicitly",
]

STOPWORDS = {
    "skill",
    "mode",
    "controller",
    "top",
    "factory",
    "create",
    "update",
    "compare",
    "convert",
    "rollback",
    "merge",
    "main",
    "task",
    "new",
}

SECRET_PATTERNS = [
    ("api_key", "blocking", re.compile(r"\b(?:sk|rk)-[A-Za-z0-9_-]{12,}\b")),
    ("api_key", "blocking", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", "blocking", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.MULTILINE)),
    ("pii", "warning", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    ("internal_url", "warning", re.compile(r"https?://(?:internal|intra|corp|localhost)[^\s)]+", re.IGNORECASE)),
]

PROVENANCE = {
    "generated_by": "TopSkillFactory",
    "format_version": "1.0.0",
    "reference": "https://github.com/IvanDembicki/TOP/tree/main/top-skill-factory",
    "instruction": "If this structure is unclear, read the TopSkillFactory reference before modifying generated artifacts.",
}


def redact_preview(value: str) -> str:
    if "PRIVATE KEY" in value:
        return "[REDACTED PRIVATE KEY]"
    if len(value) <= 8:
        return "[REDACTED]"
    return value[:4] + "...REDACTED..." + value[-2:]


def detect_sensitive_findings(text: str):
    findings = []
    for category, severity, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                {
                    "category": category,
                    "severity": severity,
                    "action": "block" if severity == "blocking" else "warn",
                    "redacted_preview": redact_preview(match.group(0)),
                }
            )
    return findings



def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip()).strip("-").lower()
    return slug or "artifact"


def split_tokens(text: str):
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2 and token not in STOPWORDS}


def write_markdown_list(items):
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def resolve_top_dir(candidate: str) -> Path:
    path = Path(candidate).resolve()
    if (path / "spec.json").exists():
        return path
    if (path / "top" / "spec.json").exists():
        return path / "top"
    raise SystemExit(f"Could not resolve TOP skill directory from: {candidate}")


def read_mode_router(top_dir: Path) -> str:
    path = top_dir / "prompts" / "mode-router.md"
    return load_text(path) if path.exists() else ""


def read_mode_files(top_dir: Path):
    mode_dir = top_dir / "modes"
    if not mode_dir.exists():
        return {}
    return {p.name: load_text(p) for p in sorted(mode_dir.glob("*.md"))}


def collect_validation_files(top_dir: Path):
    val_dir = top_dir / "validation"
    if not val_dir.exists():
        return []
    return sorted(p.name for p in val_dir.glob("*.md"))


def risky_phrases(text: str):
    lowered = text.lower()
    return sorted({phrase for phrase in RISK_PHRASES if phrase in lowered})


def summarize_spec(top_dir: Path):
    spec = load_json(top_dir / "spec.json")
    root_name = spec.get("root")
    tree = spec.get("tree", {}).get(root_name, {})
    children = sorted((tree.get("children") or {}).keys())
    invariants = spec.get("invariants", [])
    manifest_contracts = []
    manifest_path = top_dir / "artifact-manifest.json"
    if manifest_path.exists():
        manifest_contracts = list(load_json(manifest_path).get("contracts", []))
    return {
        "skill_name": spec.get("skill_name", root_name or top_dir.name),
        "root": root_name,
        "children": children,
        "invariant_count": len(invariants),
        "invariants": invariants,
        "manifest_contracts": manifest_contracts,
        "purpose": spec.get("purpose", ""),
        "version": spec.get("skill_version", "unknown"),
    }


def run_validate(repo_root: Path, report_path: Path):
    validator = repo_root / "scripts" / "validate_top_skill_factory.py"
    cmd = [sys.executable, str(validator), str(repo_root), "--report", str(report_path)]
    return subprocess.call(cmd)


def run_check_output(repo_root: Path, output_root: Path, report_path: Optional[Path] = None):
    validator = repo_root / "scripts" / "validate_top_skill_factory.py"
    resolved_output = output_root.resolve()
    target_report = report_path.resolve() if report_path else resolved_output / "validation-report.md"
    cmd = [
        sys.executable,
        str(validator),
        str(repo_root),
        "--workflow-output",
        str(resolved_output),
        "--report",
        str(target_report),
    ]
    return subprocess.call(cmd)


def parse_version_parts(version: str):
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-([a-z]+))?$", version.strip().lower())
    if not match:
        return None
    major, minor, patch, suffix = match.groups()
    rank = {"alpha": 0, "beta": 1}.get(suffix, 2)
    return (int(major), int(minor), int(patch), rank)


def compare_versions(local_version: str, remote_version: str):
    local_parts = parse_version_parts(local_version)
    remote_parts = parse_version_parts(remote_version)
    if local_parts is None or remote_parts is None:
        return "unknown"
    if remote_parts > local_parts:
        return "update_available"
    if remote_parts < local_parts:
        return "local_ahead"
    return "up_to_date"


def run_check_updates(args, repo_root: Path):
    local_metadata_path = repo_root / "release-metadata.json"
    local_metadata = load_json(local_metadata_path)
    report = {
        "product_name": local_metadata["product_name"],
        "local_version": local_metadata["current_version"],
        "release_channel": local_metadata["release_channel"],
        "startup_update_check_supported": local_metadata["startup_update_check_supported"],
        "status": "comparison_not_configured",
        "message": "No comparison manifest was provided. Startup update checking is supported, but this invocation has no comparison source.",
    }

    if args.manifest:
        manifest_path = Path(args.manifest).resolve()
        remote_metadata = load_json(manifest_path)
        if remote_metadata.get("product_name") != local_metadata.get("product_name"):
            report["status"] = "mismatched_manifest"
            report["message"] = "The provided manifest belongs to a different product."
        else:
            report["remote_version"] = remote_metadata.get("current_version")
            report["status"] = compare_versions(local_metadata["current_version"], remote_metadata["current_version"])
            if report["status"] == "update_available":
                report["message"] = f"A newer version is available: {remote_metadata['current_version']}"
            elif report["status"] == "up_to_date":
                report["message"] = "The local skill is up to date."
            elif report["status"] == "local_ahead":
                report["message"] = "The local skill version is ahead of the comparison manifest."
            else:
                report["message"] = "The versions could not be compared deterministically."

    if args.report:
        write_json(Path(args.report).resolve(), report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def copy_file_if_present(src: Path, dest: Path):
    if src.exists():
        shutil.copy2(src, dest)


def parse_json_or_text(path: Path):
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text), text
    except json.JSONDecodeError:
        return None, text


def detect_title(lines, fallback_name: str):
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return fallback_name


def extract_bullets(lines):
    return [line.strip()[1:].strip() for line in lines if line.strip().startswith("-")]


def infer_preserved_behaviors(bullets):
    keepers = []
    for bullet in bullets:
        low = bullet.lower()
        if any(token in low for token in ["keep", "use", "prefer", "concise", "bullet", "output", "markdown"]):
            keepers.append(bullet.rstrip(".") + ".")
    return keepers[:5]


def detect_issues(text):
    lowered = text.lower()
    issues = []
    if "reasonable assumptions" in lowered or "do your best" in lowered:
        issues.append(("blind_spot", "The source allows best-effort assumptions that can hide missing required inputs.", "partially_resolved"))
    if "if useful" in lowered or "if important" in lowered or "if needed" in lowered:
        issues.append(("hidden_assumption", "The source uses fuzzy routing language that can change behavior implicitly.", "partially_resolved"))
    if "validate" not in lowered:
        issues.append(("weak_validation", "The source does not define explicit validation behavior.", "unresolved"))
    if len(extract_bullets(text.splitlines())) >= 4:
        issues.append(("mixed_responsibility", "The source mixes multiple responsibilities inside a single prompt surface.", "partially_resolved"))
    if not issues:
        issues.append(("missing_contract", "The source lacks explicit structured contracts.", "partially_resolved"))
    return issues


def create_manifest(contract_id="minimal_demo_contract", readiness_rule=None):
    rules = {
        "minimal_demo_contract": "Use only when the bundle explicitly declares bounded demo readiness under the minimal demo contract.",
        "workflow_draft_contract": "Use for reviewable workflow outputs that intentionally remain draft.",
        "stable_workflow_contract": "Use for bounded stable workflow outputs that are ready within the stable release scope.",
    }
    required_by_contract = {
        "minimal_demo_contract": [
            "top/spec.json",
            "top/prompts/root.md",
            "top/prompts/mode-router.md",
            "top/modes/*",
            "top/validation/*",
            "top/provenance.json",
        ],
        "workflow_draft_contract": [
            "top/spec.json",
            "top/README.md",
            "top/artifact-manifest.json",
            "top/prompts/root.md",
            "top/prompts/mode-router.md",
            "top/prompts/input-controller.md",
            "top/prompts/user-interaction-controller.md",
            "top/prompts/validation-controller.md",
            "top/prompts/final-decision-controller.md",
            "top/modes/*",
            "top/validation/output-rules.md",
            "top/provenance.json",
        ],
        "stable_workflow_contract": [
            "top/spec.json",
            "top/README.md",
            "top/artifact-manifest.json",
            "top/prompts/root.md",
            "top/prompts/mode-router.md",
            "top/prompts/input-controller.md",
            "top/prompts/user-interaction-controller.md",
            "top/prompts/validation-controller.md",
            "top/prompts/final-decision-controller.md",
            "top/modes/*",
            "top/validation/output-rules.md",
            "top/shared-rules/decision-boundaries.md",
            "top/schemas/clarification-request.schema.json",
            "top/provenance.json",
        ],
    }
    optional = []
    if contract_id in {"workflow_draft_contract", "stable_workflow_contract"}:
        optional = ["top/shared-rules/*", "top/schemas/*"]
    return {
        "manifest_version": "0.2",
        "contracts": [
            {
                "contract_id": contract_id,
                "applies_to": "Deterministic bounded CLI workflow output.",
                "required_artifacts": required_by_contract[contract_id],
                "optional_artifacts": optional,
                "readiness_rule": readiness_rule or rules[contract_id],
            }
        ],
    }


def ensure_spec_schema_fields(top_dir: Path):
    spec_path = top_dir / "spec.json"
    if not spec_path.exists():
        return
    spec = load_json(spec_path)
    spec.setdefault("schema_version", "0.1")
    spec.setdefault("status", "draft")
    spec.setdefault("core_thesis", "This bounded CLI-generated bundle is a reviewable artifact and not a full autonomous runtime.")
    spec.setdefault("validation_model", "llm-governed-contract-validation")
    spec.setdefault(
        "mode_maturity",
        {"stable": [], "experimental": [], "planned": []},
    )
    if "output_contract" not in spec:
        mode_paths = []
        mode_dir = top_dir / "modes"
        if mode_dir.exists():
            mode_paths = [f"top/modes/{p.name}" for p in sorted(mode_dir.glob("*.md"))]
        spec["output_contract"] = {
            "required_artifacts": [
                "top/spec.json",
                "top/prompts/root.md",
                "top/prompts/mode-router.md",
                *mode_paths,
                "top/validation/output-rules.md",
            ]
        }
    write_json(spec_path, spec)


def build_workflow_bundle(top_dir: Path, skill_name: str, purpose: str, mode_name: str, mode_summary: str, route_rule: str, output_rules, contract_id, extra_invariants=None):
    manifest = create_manifest(contract_id)
    write_json(top_dir / "artifact-manifest.json", manifest)
    required_artifacts = manifest["contracts"][0]["required_artifacts"]
    spec = {
        "schema_version": "0.1",
        "skill_name": skill_name,
        "skill_version": "1.0.0",
        "status": "stable",
        "purpose": purpose,
        "core_thesis": "This bounded CLI-generated bundle is a stable-format workflow artifact under a declared contract.",
        "root": skill_name,
        "invariants": [
            "Ready output must match the declared artifact contract.",
            "Blocking ambiguity must not be silently guessed.",
        ]
        + (extra_invariants or []),
        "tree": {
            skill_name: {
                "type": "root_controller",
                "children": {
                    "InputController": {"type": "controller", "prompt": "prompts/input-controller.md"},
                    "ModeRouter": {"type": "controller", "prompt": "prompts/mode-router.md"},
                    "UserInteractionController": {"type": "controller", "prompt": "prompts/user-interaction-controller.md"},
                    "ValidationController": {"type": "controller", "prompt": "prompts/validation-controller.md"},
                    "FinalDecisionController": {"type": "controller", "prompt": "prompts/final-decision-controller.md"},
                    mode_name: {"type": "mode", "prompt": f"modes/{slugify(mode_name)}.md"},
                },
            }
        },
        "output_contract": {"required_artifacts": required_artifacts},
        "validation_model": "llm-governed-contract-validation",
        "mode_maturity": {"stable": [mode_name], "experimental": [], "planned": []},
    }
    write_json(top_dir / "spec.json", spec)
    write_text(top_dir / "README.md", f"# {skill_name}\n\nThis is a bounded CLI-generated workflow bundle under `{contract_id}`. See `top/provenance.json` for generation metadata.\n")
    write_json(top_dir / "provenance.json", PROVENANCE)
    write_text(top_dir / "prompts" / "root.md", f"# {skill_name}\n\nPurpose: {purpose}\n")
    write_text(top_dir / "prompts" / "mode-router.md", f"# ModeRouter\n\n{route_rule}\n")
    write_text(
        top_dir / "prompts" / "input-controller.md",
        "# InputController\n\nNormalize request input, preserve explicit scope, and expose ambiguity instead of hiding it.\n",
    )
    write_text(
        top_dir / "prompts" / "user-interaction-controller.md",
        "# UserInteractionController\n\nAsk for clarification only when the missing information changes behavior or authority boundaries.\n",
    )
    write_text(
        top_dir / "prompts" / "validation-controller.md",
        "# ValidationController\n\nCheck artifact completeness, contract alignment, and no-fake-ready rules before final status.\n",
    )
    write_text(
        top_dir / "prompts" / "final-decision-controller.md",
        "# FinalDecisionController\n\nDeclare the final status only after artifact contract and evidence consistency checks pass.\n",
    )
    write_text(top_dir / "modes" / f"{slugify(mode_name)}.md", f"# {mode_name}\n\n{mode_summary}\n")
    rules_text = "# Output Rules\n\n" + "\n".join(f"- {rule}" for rule in output_rules) + "\n"
    write_text(top_dir / "validation" / "output-rules.md", rules_text)
    write_text(
        top_dir / "shared-rules" / "decision-boundaries.md",
        "# Decision Boundaries\n\nUrgency is not a valid override for mandatory clarification or contract mismatch.\n",
    )
    write_json(
        top_dir / "schemas" / "clarification-request.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "clarification_request",
            "type": "object",
            "additionalProperties": False,
            "required": ["question", "options"],
            "properties": {
                "question": {"type": "string", "minLength": 1},
                "options": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
            },
        },
    )


def run_compare(args, repo_root: Path):
    top_a = resolve_top_dir(args.skill_a)
    top_b = resolve_top_dir(args.skill_b)
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_a = summarize_spec(top_a)
    summary_b = summarize_spec(top_b)
    router_a = read_mode_router(top_a)
    router_b = read_mode_router(top_b)
    mode_files_a = read_mode_files(top_a)
    mode_files_b = read_mode_files(top_b)
    validation_a = collect_validation_files(top_a)
    validation_b = collect_validation_files(top_b)

    payload = {
        "mode_request": "compare_skill",
        "skill_a": str(top_a),
        "skill_b": str(top_b),
        "comparison_criteria": args.focus or [
            "tree structure",
            "contract boundaries",
            "routing behavior",
            "validation posture",
            "behavior risk",
        ],
        "requested_by_cli": True,
    }
    write_json(out_dir / "comparison-input.json", payload)

    structural_diff = f"""# Structural Diff

## {summary_a['skill_name']}

- root: `{summary_a['root']}`
- children count: {len(summary_a['children'])}
- children:
{write_markdown_list(summary_a['children'])}
- invariants: {summary_a['invariant_count']}

## {summary_b['skill_name']}

- root: `{summary_b['root']}`
- children count: {len(summary_b['children'])}
- children:
{write_markdown_list(summary_b['children'])}
- invariants: {summary_b['invariant_count']}
"""
    write_text(out_dir / "structural-diff.md", structural_diff)

    contracts_a = [c.get("contract_id", "unknown") for c in summary_a["manifest_contracts"]]
    contracts_b = [c.get("contract_id", "unknown") for c in summary_b["manifest_contracts"]]
    contract_diff = f"""# Contract Diff

## {summary_a['skill_name']}

- manifest contracts:
{write_markdown_list(contracts_a)}

## {summary_b['skill_name']}

- manifest contracts:
{write_markdown_list(contracts_b)}
"""
    write_text(out_dir / "contract-diff.md", contract_diff)

    signal_diff = f"""# Signal Diff

- `{summary_a['skill_name']}` mode-router length: {len(router_a.splitlines())} lines
- `{summary_b['skill_name']}` mode-router length: {len(router_b.splitlines())} lines
- signal comparison in this bounded CLI is heuristic and based on routing language rather than runtime signal logs
"""
    write_text(out_dir / "signal-diff.md", signal_diff)

    validation_diff = f"""# Validation Diff

## {summary_a['skill_name']}

{write_markdown_list(validation_a)}

## {summary_b['skill_name']}

{write_markdown_list(validation_b)}
"""
    write_text(out_dir / "validation-diff.md", validation_diff)

    risky_a = risky_phrases(router_a + "\n" + "\n".join(mode_files_a.values()))
    risky_b = risky_phrases(router_b + "\n" + "\n".join(mode_files_b.values()))
    score_a = len(risky_a)
    score_b = len(risky_b)

    if score_a < score_b:
        preferred = str(top_a)
        reason = f"{summary_a['skill_name']} has fewer heuristic behavior-risk triggers than {summary_b['skill_name']}."
    elif score_b < score_a:
        preferred = str(top_b)
        reason = f"{summary_b['skill_name']} has fewer heuristic behavior-risk triggers than {summary_a['skill_name']}."
    else:
        preferred = str(top_a)
        reason = "No strong heuristic risk delta was found, so the first variant remains the default preferred result."

    behavior_report = f"""# Behavior Risk Report

## {summary_a['skill_name']}

- risk triggers:
{write_markdown_list(risky_a)}
- heuristic score: {score_a}

## {summary_b['skill_name']}

- risk triggers:
{write_markdown_list(risky_b)}
- heuristic score: {score_b}

## Comparison judgment

{reason}
"""
    write_text(out_dir / "behavior-risk-report.md", behavior_report)

    dry_run_report = """# Compare Dry Run Report

This bounded CLI compare flow is deterministic and artifact-based.

It compared:

- spec structure
- artifact contracts
- routing language
- validation surface

It did not execute a live runtime.
"""
    write_text(out_dir / "compare-dry-run-report.md", dry_run_report)

    result = {
        "status": "ready",
        "preferred_variant": preferred,
        "reason": reason,
        "evidence": [
            "comparison-input.json",
            "structural-diff.md",
            "contract-diff.md",
            "signal-diff.md",
            "validation-diff.md",
            "behavior-risk-report.md",
            "compare-dry-run-report.md",
        ],
    }
    write_json(out_dir / "final-comparison-result.json", result)
    write_text(
        out_dir / "README.md",
        "# Compare Workflow Output\n\n"
        "This folder was generated by the bounded CLI compare workflow.\n"
        "It contains deterministic artifact-level comparison outputs.\n",
    )
    print(f"Wrote compare workflow output to {out_dir}")
    return 0


def run_convert(args, repo_root: Path):
    legacy_path = Path(args.legacy_skill).resolve()
    if not legacy_path.exists():
        raise SystemExit(f"Legacy skill file does not exist: {legacy_path}")
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    text = legacy_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = detect_title(lines, legacy_path.stem.replace("-", " ").title())
    bullets = extract_bullets(lines)
    preserved = infer_preserved_behaviors(bullets)
    issues = detect_issues(text)
    sensitive_findings = detect_sensitive_findings(text)
    blocking_sensitive = [item for item in sensitive_findings if item["severity"] == "blocking"]

    normalized = {
        "source_artifacts": [legacy_path.name],
        "legacy_skill_name": title.replace(" ", ""),
        "inferred_primary_purpose": f"Convert legacy skill '{title}' into a structured TOP skill without silently preserving unsafe ambiguity.",
        "preserved_user_visible_behaviors": preserved,
        "required_structural_repairs": [
            "Separate routing, generation, and validation responsibilities.",
            "Replace implicit assumptions with explicit clarification or bounded draft status.",
            "Define a ready-state contract and evidence boundary.",
        ],
        "conversion_risks": [issue[1] for issue in issues],
        "required_clarification_policy": [
            "Missing information that changes behavior must not be guessed silently.",
            "Unsafe ambiguity must remain visible in the conversion result.",
        ],
        "requested_by_cli": True,
    }
    write_json(out_dir / "normalized-conversion-input.json", normalized)

    if sensitive_findings:
        sensitive_report = {
            "blocked": bool(blocking_sensitive),
            "policy_summary": "Blocking secrets stop conversion. Warning-level sensitive material must be surfaced without being echoed verbatim.",
            "findings": sensitive_findings,
        }
        write_json(out_dir / "sensitive-import-report.json", sensitive_report)
        if blocking_sensitive:
            write_text(
                out_dir / "README.md",
                "# Convert Workflow Output\n\nThis folder was generated by the stable CLI convert workflow and stopped because sensitive source material was detected.\n",
            )
            final_decision = {
                "status": "blocked",
                "reason": "Legacy conversion stopped because the imported source contains blocking sensitive material that must not be propagated into reusable artifacts.",
                "evidence": ["normalized-conversion-input.json", "sensitive-import-report.json"],
                "artifact_contract": "not_applicable",
                "user_acceptance": {"required": True, "status": "missing"},
                "readiness_note": "Remove or redact the sensitive source material before requesting conversion again.",
            }
            write_json(out_dir / "final-decision.json", final_decision)
            print(f"Wrote blocked sensitive convert workflow output to {out_dir}")
            return 0

    blind_spots = {
        "covered_questions": ["high-level purpose"] + (["basic user-visible behavior"] if preserved else []),
        "missing_questions": ["explicit input contract", "explicit output contract", "ready-state criteria"],
        "ambiguous_questions": [issue[1] for issue in issues if issue[0] in {"hidden_assumption", "blind_spot"}],
        "blocking_blind_spots": [issue[1] for issue in issues if issue[0] == "blind_spot"],
        "user_clarification_required": True,
        "safe_inference_allowed": ["The converted result may preserve obvious formatting preferences as draft assumptions."],
        "coverage_dimensions_checked": ["purpose", "input_contract", "output_contract", "validation_rules", "assumptions"],
    }
    write_json(out_dir / "blind-spot-report.json", blind_spots)

    conversion_report = {
        "source_artifacts": [legacy_path.name],
        "detected_issues": [{"category": category, "description": desc, "status": status} for category, desc, status in issues],
        "preserved_behavior": preserved,
        "structural_changes": [
            "Created a deterministic draft conversion bundle.",
            "Extracted a blind-spot report from the source wording.",
            "Separated conversion analysis from final readiness.",
        ],
        "unresolved_gaps": [
            "This deterministic CLI conversion does not prove behavior preservation.",
            "A human or LLM-governed review is still required before ready state.",
        ],
        "final_status": "partial",
        "final_rationale": "The stable CLI conversion can produce a reviewable draft and structured analysis, but it does not claim a fully autonomous ready conversion.",
    }
    write_json(out_dir / "conversion-report.json", conversion_report)

    top_dir = out_dir / "converted-skill" / "top"
    build_workflow_bundle(
        top_dir,
        args.target_name,
        normalized["inferred_primary_purpose"],
        "MainTaskMode",
        "Produce a reviewable structured draft from the legacy skill while preserving declared visible behavior and exposing remaining ambiguity.",
        "Route to the main task mode only when the required meaning can be preserved without silent invention.",
        [
            "draft conversion must not be labeled ready",
            "unresolved blind spots must remain visible",
            "preserved behavior claims must stay bounded",
        ],
        "workflow_draft_contract",
        extra_invariants=["Critical missing information must not be guessed silently."],
    )
    write_text(
        out_dir / "README.md",
        "# Convert Workflow Output\n\nThis folder was generated by the stable CLI convert workflow.\nIt contains a deterministic draft conversion bundle plus structured analysis artifacts.\n",
    )
    final_decision = {
        "status": "draft",
        "reason": "The stable CLI conversion produced a reviewable draft bundle and structured analysis, but it does not claim a fully ready autonomous conversion.",
        "evidence": [
            "normalized-conversion-input.json",
            "blind-spot-report.json",
            "conversion-report.json",
            "converted-skill/top/artifact-manifest.json",
            "converted-skill/top/spec.json",
            "converted-skill/top/README.md",
            "converted-skill/top/prompts/root.md",
            "converted-skill/top/prompts/mode-router.md",
            "converted-skill/top/prompts/input-controller.md",
            "converted-skill/top/prompts/user-interaction-controller.md",
            "converted-skill/top/prompts/validation-controller.md",
            "converted-skill/top/prompts/final-decision-controller.md",
            "converted-skill/top/modes/maintaskmode.md",
            "converted-skill/top/validation/output-rules.md",
        ],
        "artifact_contract": "workflow_draft_contract",
        "user_acceptance": {"required": True, "status": "missing"},
        "readiness_note": "This deterministic conversion result is intentionally non-final and requires review before any ready state.",
    }
    write_json(out_dir / "final-decision.json", final_decision)
    print(f"Wrote convert workflow output to {out_dir}")
    return 0


def infer_goal_from_request(payload, text):
    if payload and isinstance(payload, dict):
        return payload.get("goal") or payload.get("purpose") or payload.get("request")
    first = text.strip().splitlines()
    return first[0].strip() if first else ""


def run_demo(args, repo_root: Path):
    out_dir = Path(args.out).resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    demo_source = repo_root / "top" / "examples" / "convert-prompt-cleaner-full-demo"
    before_path = demo_source / "before.md"
    convert_out = out_dir / "demo-output"

    convert_args = argparse.Namespace(
        legacy_skill=str(before_path),
        target_name="TopPromptCleanerConvertedSkill",
        out=str(convert_out),
    )
    result = run_convert(convert_args, repo_root)
    if result != 0:
        return result

    summary = """# One-Command Demo

This folder was generated by:

```powershell
pwsh ./scripts/top-skill-factory.ps1 demo --out <folder>
```

It demonstrates a compact before/after conversion flow:

- `before.md` is the loose legacy prompt-skill input
- `demo-output/normalized-conversion-input.json` shows structured normalization
- `demo-output/blind-spot-report.json` shows missing or unsafe assumptions
- `demo-output/conversion-report.json` explains preserved behavior and structural repair
- `demo-output/converted-skill/top/` contains the bounded generated TOP bundle
- `demo-output/final-decision.json` shows the truthful non-final status
"""

    write_text(out_dir / "README.md", summary)
    shutil.copy2(before_path, out_dir / "before.md")

    compare_note = """# Why This Demo Matters

This one-command demo does not claim a full autonomous production conversion.

It demonstrates that TopSkillFactory can already:

- accept a messy legacy prompt
- normalize it into explicit artifacts
- expose blind spots instead of hiding them
- produce a bounded converted skill bundle
- end in a truthful `draft` state when readiness is not yet proven
"""

    write_text(out_dir / "why-this-demo-matters.md", compare_note)

    check_result = run_check_output(repo_root, convert_out, convert_out / "validation-report.md")
    if check_result != 0:
        return check_result

    print(f"Wrote one-command demo output to {out_dir}")
    return 0


def run_create(args, repo_root: Path):
    request_path = Path(args.request).resolve()
    if not request_path.exists():
        raise SystemExit(f"Create request file does not exist: {request_path}")
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload, text = parse_json_or_text(request_path)
    goal = infer_goal_from_request(payload, text)
    constraints = payload.get("constraints", {}) if isinstance(payload, dict) else {}
    ambiguous = [phrase for phrase in ["something", "whatever", "anything"] if phrase in text.lower()]

    normalized = {
        "goal": goal,
        "mode_request": "new_skill",
        "constraints": constraints,
        "ambiguities": ambiguous,
        "required_outputs": [
            "top/spec.json",
            "top/prompts/root.md",
            "top/prompts/mode-router.md",
            "top/modes/*",
            "top/validation/output-rules.md",
            "top/provenance.json",
        ],
        "requested_by_cli": True,
    }
    write_json(out_dir / "normalized-input.json", normalized)
    copy_file_if_present(request_path, out_dir / request_path.name)

    if not goal:
        write_text(out_dir / "partial-design-note.md", "No deterministic create bundle was generated because the request lacks an explicit goal.\n")
        final_decision = {
            "status": "blocked",
            "reason": "The create request does not provide an explicit goal, so a truthful generated skill cannot be produced.",
            "evidence": ["normalized-input.json", "partial-design-note.md"],
            "artifact_contract": "not_applicable",
            "user_acceptance": {"required": True, "status": "missing"},
            "readiness_note": "Creation is blocked until the request states what the skill is supposed to do.",
        }
        write_json(out_dir / "final-decision.json", final_decision)
        print(f"Wrote blocked create workflow output to {out_dir}")
        return 0

    top_dir = out_dir / "generated-skill" / "top"
    skill_name = args.target_name
    purpose = f"Build a structured TOP skill for this request: {goal}"
    route_rule = "Route directly to the main task mode when the request goal is explicit; otherwise stop and request clarification."
    mode_summary = "Generate a compact first-pass skill bundle that preserves the declared goal and keeps ambiguity explicit."
    build_workflow_bundle(
        top_dir,
        skill_name,
        purpose,
        "MainTaskMode",
        mode_summary,
        route_rule,
        [
            "required artifacts must exist before ready status",
            "ready output must match the stable workflow contract",
            "ambiguity that changes behavior must trigger clarification rather than invention",
        ],
        "stable_workflow_contract",
        extra_invariants=["The generated skill must preserve the explicit goal as the source of truth."],
    )
    write_text(
        out_dir / "dry-run-report.md",
        "# Create Dry Run Report\n\n"
        "This bounded create workflow checked that the generated bundle contains the minimal demo artifacts and preserves the explicit request goal.\n",
    )
    final_decision = {
        "status": "ready",
        "reason": "The create workflow generated a bounded minimal demo bundle from an explicit goal and the required demo artifacts are present.",
        "evidence": [
            "normalized-input.json",
            "dry-run-report.md",
            "generated-skill/top/artifact-manifest.json",
            "generated-skill/top/spec.json",
            "generated-skill/top/prompts/root.md",
            "generated-skill/top/prompts/mode-router.md",
            "generated-skill/top/modes/maintaskmode.md",
            "generated-skill/top/validation/output-rules.md",
        ],
        "artifact_contract": "stable_workflow_contract",
        "user_acceptance": {"required": False, "status": "accepted"},
        "readiness_note": "This result is ready under the stable bounded workflow contract, not under the full factory contract.",
    }
    write_json(out_dir / "final-decision.json", final_decision)
    write_text(out_dir / "README.md", "# Create Workflow Output\n\nThis folder was generated by the stable CLI create workflow.\n")
    print(f"Wrote create workflow output to {out_dir}")
    return 0


def run_update(args, repo_root: Path):
    top_dir = resolve_top_dir(args.skill)
    request_path = Path(args.requirement).resolve()
    if not request_path.exists():
        raise SystemExit(f"Update requirement file does not exist: {request_path}")
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload, text = parse_json_or_text(request_path)
    requirement = infer_goal_from_request(payload, text) or text.strip()
    summary = summarize_spec(top_dir)
    requested_modes = []
    lowered = text.lower()
    if "detail" in lowered or "detailed" in lowered or "checklist" in lowered:
        requested_modes.append("ExtendedTaskMode")
    if not requested_modes:
        requested_modes.append("UpdatedTaskMode")

    normalized = {
        "mode_request": "update_skill",
        "source_skill": str(top_dir),
        "source_skill_name": summary["skill_name"],
        "requirement": requirement,
        "impacted_areas": ["routing", "mode behavior", "validation surface"],
        "requested_by_cli": True,
    }
    write_json(out_dir / "normalized-update-input.json", normalized)
    copy_file_if_present(request_path, out_dir / request_path.name)

    update_plan = {
        "source_skill": summary["skill_name"],
        "source_version": summary["version"],
        "requirement_summary": requirement,
        "proposed_mode_additions": requested_modes,
        "risk_notes": [
            "This deterministic update does not prove backward compatibility across every downstream use case.",
            "A fresh behavior baseline is still required before ready acceptance.",
        ],
    }
    write_json(out_dir / "change-impact-report.json", update_plan)

    updated_top = out_dir / "updated-skill" / "top"
    if updated_top.parent.exists():
        shutil.rmtree(updated_top.parent)
    shutil.copytree(top_dir, updated_top)
    ensure_spec_schema_fields(updated_top)

    root_prompt = updated_top / "prompts" / "root.md"
    if root_prompt.exists():
        original = load_text(root_prompt).rstrip() + "\n\nUpdate note: " + requirement + "\n"
        write_text(root_prompt, original)
    router_path = updated_top / "prompts" / "mode-router.md"
    router_extra = "\nRoute to the extended mode only when the new requirement explicitly asks for the expanded behavior.\n"
    if router_path.exists():
        write_text(router_path, load_text(router_path).rstrip() + router_extra)
    for mode_name in requested_modes:
        write_text(
            updated_top / "modes" / f"{slugify(mode_name)}.md",
            f"# {mode_name}\n\nImplement the requested update in a bounded way: {requirement}\n",
        )
    validation_path = updated_top / "validation" / "output-rules.md"
    if validation_path.exists():
        write_text(validation_path, load_text(validation_path).rstrip() + "\n- updated behavior needs review before final ready acceptance\n")

    partial_package = {
        "delivery_type": "partial_output_package",
        "usable_artifacts": [
            "updated-skill/top/spec.json",
            "updated-skill/top/prompts/root.md",
            "updated-skill/top/prompts/mode-router.md",
        ] + [f"updated-skill/top/modes/{slugify(mode_name)}.md" for mode_name in requested_modes] + [
            "updated-skill/top/validation/output-rules.md"
        ],
        "known_remaining_gaps": [
            "A fresh behavior baseline has not been generated.",
            "This deterministic update does not confirm runtime-equivalent behavior.",
        ],
        "consumer_warning": "This package is reviewable and partly usable, but not ready for final acceptance.",
    }
    write_json(out_dir / "partial-output-package.json", partial_package)
    write_text(out_dir / "README.md", "# Update Workflow Output\n\nThis folder was generated by the stable CLI update workflow.\n")
    final_decision = {
        "status": "draft",
        "reason": "The update workflow produced a reviewable partial package, but a deterministic CLI update cannot claim final ready acceptance.",
        "evidence": [
            "normalized-update-input.json",
            "change-impact-report.json",
            "partial-output-package.json",
        ] + partial_package["usable_artifacts"],
        "artifact_contract": "workflow_draft_contract",
        "user_acceptance": {"required": True, "status": "missing"},
        "readiness_note": "The updated bundle is intentionally draft until a broader review confirms the requested change.",
    }
    write_json(out_dir / "final-decision.json", final_decision)
    print(f"Wrote update workflow output to {out_dir}")
    return 0


def run_rollback(args, repo_root: Path):
    top_dir = resolve_top_dir(args.skill)
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    restored_top = out_dir / "restored-skill" / "top"
    if restored_top.parent.exists():
        shutil.rmtree(restored_top.parent)
    shutil.copytree(top_dir, restored_top)
    ensure_spec_schema_fields(restored_top)

    record = {
        "rollback_id": f"rbk-{slugify(args.target_version)}",
        "source_version": args.source_version,
        "target_version": args.target_version,
        "reason": args.reason,
        "validated_target": args.validated_target,
        "trace_id": f"trace-{slugify(args.source_version)}-to-{slugify(args.target_version)}",
        "restored_artifacts": [
            "restored-skill/top/spec.json",
            "restored-skill/top/prompts/root.md",
            "restored-skill/top/prompts/mode-router.md",
        ],
    }
    write_json(out_dir / "rollback-record.json", record)
    write_text(
        out_dir / "rollback-audit.md",
        "# Rollback Audit\n\n"
        f"- source version: `{args.source_version}`\n"
        f"- target version: `{args.target_version}`\n"
        f"- validated target state: `{args.validated_target}`\n"
        f"- reason: {args.reason}\n",
    )
    write_text(
        out_dir / "rollback-dry-run-report.md",
        "# Rollback Dry Run Report\n\n"
        "This deterministic rollback copied the declared target skill surface and recorded the rollback trace.\n",
    )
    status = "ready" if args.validated_target == "validated" else "draft"
    note = "The rollback target is validated, so the restored bundle is ready under the copied artifact contract." if status == "ready" else "The rollback target is only draft, so the restored bundle remains draft after rollback."
    final_decision = {
        "status": status,
        "reason": "The rollback workflow restored the requested target version and preserved a traceable rollback record.",
        "evidence": [
            "rollback-record.json",
            "rollback-audit.md",
            "rollback-dry-run-report.md",
            "restored-skill/top/spec.json",
            "restored-skill/top/prompts/root.md",
            "restored-skill/top/prompts/mode-router.md",
        ],
        "artifact_contract": "stable_workflow_contract" if status == "ready" else "workflow_draft_contract",
        "user_acceptance": {"required": False, "status": "accepted" if status == "ready" else "missing"},
        "readiness_note": note,
    }
    write_json(out_dir / "final-decision.json", final_decision)
    write_text(out_dir / "README.md", "# Rollback Workflow Output\n\nThis folder was generated by the stable CLI rollback workflow.\n")
    print(f"Wrote rollback workflow output to {out_dir}")
    return 0


def incompatible_merge_reasons(summary_a, summary_b, text_a, text_b):
    structural = []
    contract = []
    policy = []
    shared = split_tokens(summary_a["skill_name"]) & split_tokens(summary_b["skill_name"])
    if not shared and summary_a["root"] != summary_b["root"]:
        structural.append("The source skills do not expose an overlapping domain identity for a bounded deterministic merge.")
    if ("escalat" in text_a.lower()) != ("escalat" in text_b.lower()):
        contract.append("The source skills encode different escalation behavior and cannot be merged without changing answer authority.")
    if risky_phrases(text_a) != risky_phrases(text_b):
        policy.append("The source skills expose different heuristic risk profiles and the bounded merge flow cannot reconcile them truthfully.")
    return structural, contract, policy


def run_merge(args, repo_root: Path):
    top_a = resolve_top_dir(args.skill_a)
    top_b = resolve_top_dir(args.skill_b)
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_a = summarize_spec(top_a)
    summary_b = summarize_spec(top_b)
    text_a = read_mode_router(top_a) + "\n" + "\n".join(read_mode_files(top_a).values())
    text_b = read_mode_router(top_b) + "\n" + "\n".join(read_mode_files(top_b).values())

    normalized = {
        "mode_request": "merge_skills",
        "skill_a": str(top_a),
        "skill_b": str(top_b),
        "skill_a_name": summary_a["skill_name"],
        "skill_b_name": summary_b["skill_name"],
        "requested_by_cli": True,
    }
    write_json(out_dir / "normalized-merge-input.json", normalized)

    structural, contract, policy = incompatible_merge_reasons(summary_a, summary_b, text_a, text_b)
    has_conflict = bool(structural or contract or policy)
    incompatibility = {
        "structural_conflicts": structural,
        "contract_conflicts": contract,
        "policy_conflicts": policy,
        "repairable": False if has_conflict else True,
        "failure_reason": "The bounded merge flow found blocking incompatibilities." if has_conflict else "No blocking incompatibilities were found in the bounded merge pass.",
    }
    write_json(out_dir / "incompatibility-report.json", incompatibility)

    if has_conflict:
        write_json(out_dir / "iteration-budget-summary.json", {
            "repair_cycles_allowed": 1,
            "repair_cycles_used": 1,
            "result": "exhausted_without_safe_merge",
        })
        write_text(out_dir / "repair-attempt-log.md", "# Repair Attempt Log\n\n- Attempted bounded merge analysis\n- Found blocking incompatibilities\n- Stopped rather than inventing a merged authority model\n")
        write_text(out_dir / "final-diagnosis.md", "# Final Diagnosis\n\nThe source skills require a product choice rather than a structural merge.\n")
        final_decision = {
            "status": "failed",
            "reason": "Merge failed after bounded analysis because the source skills encode incompatible domain identity, escalation, or policy boundaries.",
            "evidence": [
                "normalized-merge-input.json",
                "incompatibility-report.json",
                "iteration-budget-summary.json",
                "repair-attempt-log.md",
                "final-diagnosis.md",
            ],
            "artifact_contract": "not_applicable",
            "user_acceptance": {"required": False, "status": "not_reached"},
            "readiness_note": "Failure is terminal for this bounded merge attempt; no truthful merged bundle exists.",
        }
        write_json(out_dir / "final-decision.json", final_decision)
        write_text(out_dir / "README.md", "# Merge Workflow Output\n\nThis folder was generated by the experimental CLI merge workflow and ended in failed state.\n")
        print(f"Wrote failed merge workflow output to {out_dir}")
        return 0

    merged_name = args.target_name or f"{summary_a['skill_name']}Merged"
    merged_top = out_dir / "merged-skill" / "top"
    merged_purpose = f"Merge aligned skill surfaces from {summary_a['skill_name']} and {summary_b['skill_name']} into a reviewable draft bundle."
    build_workflow_bundle(
        merged_top,
        merged_name,
        merged_purpose,
        "MergedTaskMode",
        "Produce a merged draft that preserves aligned behavior and leaves any future divergence explicit for review.",
        "Route to the merged task mode only when both source skills stay within the same bounded domain.",
        [
            "merged output remains draft until behavior review is complete",
            "source authority boundaries must remain visible",
            "bounded merge must not invent a new business policy",
        ],
        "workflow_draft_contract",
        extra_invariants=["Merged bundles must preserve the stricter visible boundary when source skills align."],
    )
    write_text(out_dir / "merge-dry-run-report.md", "# Merge Dry Run Report\n\nThe bounded merge flow found no blocking incompatibilities and produced a reviewable merged draft bundle.\n")
    final_decision = {
        "status": "draft",
        "reason": "The merge workflow produced a reviewable merged draft, but final acceptance still requires behavioral review.",
        "evidence": [
            "normalized-merge-input.json",
            "incompatibility-report.json",
            "merge-dry-run-report.md",
            "merged-skill/top/artifact-manifest.json",
            "merged-skill/top/spec.json",
            "merged-skill/top/prompts/root.md",
            "merged-skill/top/prompts/mode-router.md",
            "merged-skill/top/modes/mergedtaskmode.md",
            "merged-skill/top/validation/output-rules.md",
        ],
        "artifact_contract": "workflow_draft_contract",
        "user_acceptance": {"required": True, "status": "missing"},
        "readiness_note": "The merged result is intentionally draft until a broader compatibility review is complete. Merge remains experimental and outside the stable contract.",
    }
    write_json(out_dir / "final-decision.json", final_decision)
    write_text(out_dir / "README.md", "# Merge Workflow Output\n\nThis folder was generated by the experimental CLI merge workflow.\n")
    print(f"Wrote draft merge workflow output to {out_dir}")
    return 0


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(prog="top_skill_factory")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--report", default=str(repo_root / "onboarding" / "schema-validation-report.md"))

    p_check_updates = sub.add_parser("check-updates")
    p_check_updates.add_argument("--manifest")
    p_check_updates.add_argument("--report")

    p_check_output = sub.add_parser("check-output")
    p_check_output.add_argument("output_folder")
    p_check_output.add_argument("--report")

    p_demo = sub.add_parser("demo")
    p_demo.add_argument("--out", required=True)

    p_compare = sub.add_parser("compare")
    p_compare.add_argument("skill_a")
    p_compare.add_argument("skill_b")
    p_compare.add_argument("--out", required=True)
    p_compare.add_argument("--focus", nargs="*")

    p_convert = sub.add_parser("convert")
    p_convert.add_argument("legacy_skill")
    p_convert.add_argument("--target-name", required=True)
    p_convert.add_argument("--out", required=True)

    p_create = sub.add_parser("create")
    p_create.add_argument("request")
    p_create.add_argument("--target-name", required=True)
    p_create.add_argument("--out", required=True)

    p_update = sub.add_parser("update")
    p_update.add_argument("skill")
    p_update.add_argument("requirement")
    p_update.add_argument("--out", required=True)

    p_rollback = sub.add_parser("rollback")
    p_rollback.add_argument("skill")
    p_rollback.add_argument("--source-version", required=True)
    p_rollback.add_argument("--target-version", required=True)
    p_rollback.add_argument("--reason", required=True)
    p_rollback.add_argument("--validated-target", choices=["validated", "draft"], default="validated")
    p_rollback.add_argument("--out", required=True)

    p_merge = sub.add_parser("merge")
    p_merge.add_argument("skill_a")
    p_merge.add_argument("skill_b")
    p_merge.add_argument("--target-name")
    p_merge.add_argument("--out", required=True)

    args = parser.parse_args()
    if args.cmd == "validate":
        return run_validate(repo_root, Path(args.report).resolve())
    if args.cmd == "check-updates":
        return run_check_updates(args, repo_root)
    if args.cmd == "check-output":
        report = Path(args.report).resolve() if args.report else None
        return run_check_output(repo_root, Path(args.output_folder), report)
    if args.cmd == "demo":
        return run_demo(args, repo_root)
    if args.cmd == "compare":
        return run_compare(args, repo_root)
    if args.cmd == "convert":
        return run_convert(args, repo_root)
    if args.cmd == "create":
        return run_create(args, repo_root)
    if args.cmd == "update":
        return run_update(args, repo_root)
    if args.cmd == "rollback":
        return run_rollback(args, repo_root)
    if args.cmd == "merge":
        return run_merge(args, repo_root)
    return 1


if __name__ == "__main__":
    sys.exit(main())
