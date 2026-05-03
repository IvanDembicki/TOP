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
    "AI_PRELOAD_CONTEXT.md",
    "rules/skill-maintenance-rules.md",
    "canon/architectural-invariants.md",
    "canon/controller-content-rules.md",
    "canon/forbidden-confusions.md",
    "canon/validation-rules.md",
    "rules/violation-catalog.md",
    "rules/review-checklist.md",
    "rules/typing-checklist.md",
    "references/node-model.md",
    "references/code-generation.md",
    "references/node-validation-rules.md",
    "prompts/generate-top-node.md",
    "prompts/generate-top-tree.md",
    "prompts/refactor-to-top.md",
    "agents/migration-agent.md",
    "agents/target-adaptation-agent.md",
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

    return errors


def extract_version_from_markdown(text):
    match = re.search(r"\*\*Version:\*\*\s*([0-9]+\.[0-9]+\.[0-9]+)", text)
    return match.group(1) if match else None


def check_version_consistency(root):
    errors = []
    skill = load_json(root / "skill.json")
    release = load_json(root / "release-metadata.json")
    version = skill.get("version")

    if release.get("current_version") != version:
        errors.append("release-metadata.json current_version does not match skill.json version")

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
        ("SKILL.md", "Content/View constructor receives exactly one semantic argument"),
        ("SKILL.md", "RootContext"),
        ("SKILL.md", "TOP spec props are declarative metadata"),
        ("rules/skill-maintenance-rules.md", "No exhaustive-looking technology lists"),
        ("rules/skill-maintenance-rules.md", "Missed case feedback loop"),
        ("rules/violation-catalog.md", "CORE-026"),
        ("canon/architectural-invariants.md", "Objects are not assembled outside the tree and pushed inward"),
        ("canon/architectural-invariants.md", "Controller Role Purity Invariant"),
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
        (r"new\s+\w+Content\s*\([^)]*,", "extra Content constructor argument"),
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


def run(root):
    checks = [
        ("required paths", check_required_paths),
        ("json parse", check_json_parse),
        ("manifest references", check_manifest_references),
        ("version consistency", check_version_consistency),
        ("markdown links", check_markdown_links),
        ("required phrases", check_required_phrases),
        ("risky patterns", check_known_risky_patterns),
    ]
    all_errors = []
    for name, check in checks:
        errors = check(root)
        if errors:
            all_errors.append((name, errors))

    if all_errors:
        print("quick_validate: FAILED")
        for name, errors in all_errors:
            print(f"\n[{name}]")
            for error in errors:
                print(f"- {error}")
        return 1

    print("quick_validate: OK")
    print(f"validated: {root}")
    print(f"checks: {len(checks)}")
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
