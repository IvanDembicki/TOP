#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_BY_FILENAME = {
    "final-decision.json": "final-decision.schema.json",
    "conversion-report.json": "conversion-report.schema.json",
    "blind-spot-report.json": "blind-spot-report.schema.json",
    "artifact-manifest.json": "artifact-manifest.schema.json",
    "final-comparison-result.json": "comparison-result.schema.json",
    "partial-output-package.json": "partial-output-package.schema.json",
    "incompatibility-report.json": "incompatibility-report.schema.json",
    "rollback-record.json": "rollback-record.schema.json",
    "sensitive-import-report.json": "sensitive-import-report.schema.json",
    "provenance.json": "provenance.schema.json",
}

STABLE_MODE_EXAMPLES = {
    "CreateNewSkillMode": ["create-new-skill-end-to-end", "create-new-skill-blocked-case"],
    "ConvertLegacySkillMode": ["convert-legacy-skill-before-after"],
    "UpdateExistingSkillMode": ["update-existing-skill-partial-case"],
    "CompareSkillMode": ["compare-skill-end-to-end"],
    "RollbackMode": ["rollback-skill-end-to-end"],
}
STABLE_COMMANDS = ["validate", "check-output", "demo", "create", "convert", "update", "compare", "rollback"]

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def check_type(value, expected):
    mapping = {"object": dict, "array": list, "string": str, "boolean": bool, "number": (int, float), "null": type(None)}
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, mapping[expected])

def validate(value, schema, path="$"):
    errors = []
    if "oneOf" in schema:
        if not any(not validate(value, option, path) for option in schema["oneOf"]):
            errors.append(f"{path}: value does not match any allowed schema option")
        return errors
    if "type" in schema and not check_type(value, schema["type"]):
        return [f"{path}: expected {schema['type']}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{path}: invalid date-time format")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                errors.extend(validate(item, item_schema, f"{path}[{idx}]"))
        if schema.get("uniqueItems"):
            seen = set()
            for idx, item in enumerate(value):
                key = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if key in seen:
                    errors.append(f"{path}[{idx}]: duplicate item in uniqueItems array")
                seen.add(key)
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        for key, sub_schema in properties.items():
            if key in value:
                errors.extend(validate(value[key], sub_schema, f"{path}.{key}"))
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value.keys()) - set(properties.keys()))
            for key in extra:
                errors.append(f"{path}: unexpected key {key!r}")
    for conditional in schema.get("allOf", []):
        condition = conditional.get("if")
        then = conditional.get("then")
        if condition and then and not validate(value, condition, path):
            errors.extend(validate(value, then, path))
    return errors

def validate_json_file(json_path: Path, schema_path: Path):
    return validate(load_json(json_path), load_json(schema_path), str(json_path))

def find_files(root: Path, name: str):
    return sorted(root.glob(f"**/{name}"))

def check_required_artifacts(repo_root: Path, manifest_path: Path):
    manifest = load_json(manifest_path)
    errors = []
    full_contract = {entry["contract_id"]: entry for entry in manifest["contracts"]}["full_factory_contract"]
    for pattern in full_contract["required_artifacts"]:
        matches = list(repo_root.glob(pattern)) if "*" in pattern else [repo_root / pattern]
        if not matches or not any(match.exists() for match in matches):
            errors.append(f"missing required artifact or pattern: {pattern}")
        for match in matches:
            if match.exists() and match.is_file() and match.stat().st_size == 0:
                errors.append(f"empty required artifact: {match}")
    return errors

def extract_markdown_links(text: str):
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)

def check_markdown_links(repo_root: Path):
    errors = []
    for path in sorted(repo_root.glob("**/*.md")):
        if path.name in {"schema-validation-report.md", "validation-report.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "D:/" in text or "D:\\" in text:
            errors.append(f"{path}: contains absolute Windows path")
        for target in extract_markdown_links(text):
            if target.startswith(("http://", "https://", "mailto:", "#", "app://", "plugin://")):
                continue
            clean = target.strip("<>")
            if ":" in clean and clean[1:3] != ":/":
                clean = clean.split(":", 1)[0]
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(repo_root.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                errors.append(f"{path}: broken local link -> {target}")
    return errors

def check_contract_scopes(repo_root: Path):
    errors = []
    for final_decision_path in find_files(repo_root / "top" / "examples", "final-decision.json"):
        data = load_json(final_decision_path)
        contract = data.get("artifact_contract")
        rel = str(final_decision_path.relative_to(repo_root)).replace("\\", "/")
        if contract == "minimal_demo_contract" and not rel.startswith("top/examples/"):
            errors.append(f"{final_decision_path}: minimal_demo_contract used outside top/examples")
    return errors

def check_release_metadata_consistency(repo_root: Path):
    errors = []
    release_metadata = load_json(repo_root / "release-metadata.json")
    spec = load_json(repo_root / "top" / "spec.json")
    version = release_metadata.get("current_version")
    if version != spec.get("skill_version"):
        errors.append("release-metadata.json current_version does not match top/spec.json skill_version")
    for path in [repo_root / "RELEASE_NOTES.md", repo_root / "VALIDATION_REPORT.md"]:
        if version not in path.read_text(encoding="utf-8"):
            errors.append(f"{path}: release version {version} not present")
    if not release_metadata.get("startup_update_check_supported"):
        errors.append("release-metadata.json should expose startup update checking as a supported capability")
    return errors

def check_no_literal_crlf_markers(repo_root: Path):
    path = repo_root / "top" / "validation" / "output-rules.md"
    text = path.read_text(encoding="utf-8")
    return [f"{path}: contains literal `r`n markers"] if "`r`n" in text else []

def collect_repo_schema_results(repo_root: Path, schema_root: Path):
    results = {}
    results["root spec schema"] = validate_json_file(repo_root / "top" / "spec.json", schema_root / "spec.schema.json")
    results["root artifact manifest schema"] = validate_json_file(repo_root / "top" / "artifact-manifest.json", schema_root / "artifact-manifest.schema.json")
    results["release metadata schema"] = validate_json_file(repo_root / "release-metadata.json", schema_root / "release-metadata.schema.json")
    results["mode manifest schema"] = validate_json_file(repo_root / "top" / "modes" / "mode-manifest.json", schema_root / "mode-manifest.schema.json")
    example_errors = []
    for path in sorted((repo_root / "top" / "examples").glob("**/*.json")):
        schema_name = SCHEMA_BY_FILENAME.get(path.name)
        if schema_name:
            example_errors.extend(validate_json_file(path, schema_root / schema_name))
    results["example json schemas"] = example_errors
    return results

def collect_spec_reference_errors(repo_root: Path):
    errors = []
    spec = load_json(repo_root / "top" / "spec.json")
    def walk(node):
        if isinstance(node, dict):
            prompt = node.get("prompt")
            if prompt and not (repo_root / "top" / prompt).exists():
                errors.append(f"missing prompt reference: top/{prompt}")
            output_schema = node.get("output_schema")
            if output_schema and not (repo_root / "top" / output_schema).exists():
                errors.append(f"missing schema reference: top/{output_schema}")
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(spec.get("tree", {}))
    return errors

def check_mode_coverage(repo_root: Path):
    errors = []
    manifest = load_json(repo_root / "top" / "modes" / "mode-manifest.json")
    stable_modes = manifest.get("stable_release_scope", [])
    if stable_modes != list(STABLE_MODE_EXAMPLES.keys()):
        errors.append("mode-manifest stable_release_scope does not match validator stable mode map")
    for mode, example_dirs in STABLE_MODE_EXAMPLES.items():
        for example_dir in example_dirs:
            if not (repo_root / "top" / "examples" / example_dir).exists():
                errors.append(f"missing stable mode example for {mode}: {example_dir}")
    cli_text = (repo_root / "scripts" / "top_skill_factory_cli.py").read_text(encoding="utf-8")
    tests_text = (repo_root / "scripts" / "test_cli_workflows.py").read_text(encoding="utf-8")
    for command in STABLE_COMMANDS:
        if f'add_parser("{command}")' not in cli_text:
            errors.append(f"stable command missing in CLI: {command}")
        if command in {"validate", "check-output", "demo"}:
            continue
        if f'"{command}"' not in tests_text:
            errors.append(f"stable command missing in regression suite: {command}")
    return errors

def check_security_proof(repo_root: Path):
    errors = []
    example_root = repo_root / "top" / "examples" / "convert-sensitive-legacy-skill-blocked"
    if not example_root.exists():
        return ["missing security proof example: top/examples/convert-sensitive-legacy-skill-blocked"]
    for rel in ["legacy-skill-before.md", "sensitive-import-report.json", "final-decision.json", "README.md"]:
        if not (example_root / rel).exists():
            errors.append(f"security example missing artifact: {rel}")
    if not (repo_root / "scripts" / "test_sensitive_cases.py").exists():
        errors.append("missing scripts/test_sensitive_cases.py")
    report_path = example_root / "sensitive-import-report.json"
    if report_path.exists():
        text = report_path.read_text(encoding="utf-8")
        if "sk-live-SECRET" in text or "BEGIN PRIVATE KEY" in text:
            errors.append("security report echoes raw secret material")
    return errors

def workflow_bundle_roots(output_root: Path):
    candidates = []
    for pattern in ["generated-skill/top", "converted-skill/top", "updated-skill/top", "restored-skill/top", "merged-skill/top"]:
        candidate = output_root / pattern
        if candidate.exists():
            candidates.append(candidate)
    return candidates

def validate_evidence_paths(output_root: Path, evidence):
    errors = []
    for item in evidence:
        path = output_root / item
        if not path.exists():
            errors.append(f"{output_root}: missing evidence artifact {item}")
    return errors

def validate_bundle(top_dir: Path, schema_root: Path):
    errors = []
    manifest_path = top_dir / "artifact-manifest.json"
    if not manifest_path.exists():
        return [f"{top_dir}: missing artifact-manifest.json"]
    errors.extend(validate_json_file(manifest_path, schema_root / "artifact-manifest.schema.json"))
    manifest = load_json(manifest_path)
    contract = manifest["contracts"][0]
    for pattern in contract["required_artifacts"]:
        relative = pattern[4:] if pattern.startswith("top/") else pattern
        matches = list(top_dir.glob(relative)) if "*" in relative else [top_dir / relative]
        if not matches or not any(path.exists() for path in matches):
            errors.append(f"{top_dir}: missing required bundle artifact or pattern {relative}")
        for path in matches:
            if path.exists() and path.is_file() and path.stat().st_size == 0:
                errors.append(f"{top_dir}: empty required bundle artifact {path.relative_to(top_dir)}")
    spec_path = top_dir / "spec.json"
    if spec_path.exists():
        errors.extend(validate_json_file(spec_path, schema_root / "spec.schema.json"))
    else:
        errors.append(f"{top_dir}: missing spec.json")
    provenance_path = top_dir / "provenance.json"
    if provenance_path.exists():
        errors.extend(validate_json_file(provenance_path, schema_root / "provenance.schema.json"))
    return errors

def collect_output_schema_results(output_root: Path, repo_root: Path, schema_root: Path):
    results = {}
    final_decision_path = output_root / "final-decision.json"
    comparison_result_path = output_root / "final-comparison-result.json"
    bundle_roots = workflow_bundle_roots(output_root)
    final_data = None
    if final_decision_path.exists():
        errors = validate_json_file(final_decision_path, schema_root / "final-decision.schema.json")
        final_data = load_json(final_decision_path)
        errors.extend(validate_evidence_paths(output_root, final_data.get("evidence", [])))
        results["workflow final-decision schema"] = errors
    else:
        results["workflow final-decision schema"] = [] if comparison_result_path.exists() else [f"{output_root}: missing final-decision.json"]
    if comparison_result_path.exists():
        comparison_errors = validate_json_file(comparison_result_path, schema_root / "comparison-result.schema.json")
        comparison_data = load_json(comparison_result_path)
        comparison_errors.extend(validate_evidence_paths(output_root, comparison_data.get("evidence", [])))
        results["workflow comparison-result schema"] = comparison_errors
    else:
        results["workflow comparison-result schema"] = []
    for label, filename, schema_name in [
        ("workflow conversion-report schema", "conversion-report.json", "conversion-report.schema.json"),
        ("workflow blind-spot-report schema", "blind-spot-report.json", "blind-spot-report.schema.json"),
        ("workflow partial-output-package schema", "partial-output-package.json", "partial-output-package.schema.json"),
        ("workflow incompatibility-report schema", "incompatibility-report.json", "incompatibility-report.schema.json"),
        ("workflow rollback-record schema", "rollback-record.json", "rollback-record.schema.json"),
        ("workflow sensitive-import-report schema", "sensitive-import-report.json", "sensitive-import-report.schema.json"),
    ]:
        path = output_root / filename
        results[label] = validate_json_file(path, schema_root / schema_name) if path.exists() else []
    bundle_errors = []
    for top_dir in bundle_roots:
        bundle_errors.extend(validate_bundle(top_dir, schema_root))
    requires_bundle = not comparison_result_path.exists()
    if final_data and final_data.get("status") in {"failed", "blocked"} and final_data.get("artifact_contract") == "not_applicable":
        requires_bundle = False
    if requires_bundle and not bundle_roots:
        bundle_errors.append(f"{output_root}: no generated skill bundle found")
    results["workflow bundle artifacts"] = bundle_errors
    readme_path = output_root / "README.md"
    results["workflow readme"] = [] if readme_path.exists() and readme_path.stat().st_size > 0 else [f"{output_root}: missing or empty README.md"]
    return results

def build_report(results, title):
    total = sum(len(v) for v in results.values())
    lines = [f"# {title}", "", f"- Status: {'pass' if total == 0 else 'fail'}", f"- Total findings: {total}", "", "## Checks", ""]
    for name, findings in results.items():
        lines.append(f"### {name}")
        lines.extend([f"- {item}" for item in findings] or ["- pass"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--report", dest="report_path")
    parser.add_argument("--workflow-output", dest="workflow_output")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    schema_root = repo_root / "top" / "schemas"
    if args.workflow_output:
        output_root = Path(args.workflow_output).resolve()
        results = collect_output_schema_results(output_root, repo_root, schema_root)
        report = build_report(results, "Workflow Output Validation Report")
    else:
        results = collect_repo_schema_results(repo_root, schema_root)
        results["required full contract artifacts"] = check_required_artifacts(repo_root, repo_root / "top" / "artifact-manifest.json")
        results["markdown links"] = check_markdown_links(repo_root)
        results["artifact contract scope"] = check_contract_scopes(repo_root)
        results["release metadata consistency"] = check_release_metadata_consistency(repo_root)
        results["spec prompt references"] = collect_spec_reference_errors(repo_root)
        results["stable mode coverage"] = check_mode_coverage(repo_root)
        results["security proof"] = check_security_proof(repo_root)
        results["output-rules literal marker check"] = check_no_literal_crlf_markers(repo_root)
        report = build_report(results, "Schema Validation Report")
    if args.report_path:
        Path(args.report_path).write_text(report, encoding="utf-8")
    print(report)
    sys.exit(1 if any(results.values()) else 0)

if __name__ == "__main__":
    main()
