#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = REPO_ROOT / "scripts" / "top_skill_factory_cli.py"
VALIDATOR = REPO_ROOT / "scripts" / "validate_top_skill_factory.py"


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate_output(root: Path, target: Path):
    report = target / "validation-report.md"
    run([sys.executable, str(VALIDATOR), str(root), "--workflow-output", str(target), "--report", str(report)])


def main():
    temp_root = Path(tempfile.mkdtemp(prefix="top-skill-factory-cli-tests-"))
    try:
        run([sys.executable, str(VALIDATOR), str(REPO_ROOT), "--report", str(temp_root / "repo-validation-report.md")])

        create_request = temp_root / "create-request.json"
        write(
            create_request,
            json.dumps(
                {
                    "goal": "Create a skill that turns a user goal into a concise action plan.",
                    "constraints": {"must_include_clarification_path": True, "max_modes": 1},
                },
                indent=2,
            )
            + "\n",
        )
        create_out = temp_root / "create-output"
        run([sys.executable, str(CLI), "create", str(create_request), "--target-name", "DemoCreateSkill", "--out", str(create_out)])
        validate_output(REPO_ROOT, create_out)

        compare_out = temp_root / "compare-output"
        run(
            [
                sys.executable,
                str(CLI),
                "compare",
                str(REPO_ROOT / "top" / "examples" / "compare-skill-end-to-end" / "skill-a"),
                str(REPO_ROOT / "top" / "examples" / "compare-skill-end-to-end" / "skill-b"),
                "--out",
                str(compare_out),
            ]
        )
        validate_output(REPO_ROOT, compare_out)

        legacy_skill = temp_root / "legacy-skill.md"
        write(
            legacy_skill,
            "# Legacy Skill\n- Keep answers concise.\n- Use bullet points.\n- Do your best with reasonable assumptions.\n",
        )
        convert_out = temp_root / "convert-output"
        run([sys.executable, str(CLI), "convert", str(legacy_skill), "--target-name", "DemoConvertedSkill", "--out", str(convert_out)])
        validate_output(REPO_ROOT, convert_out)

        update_req = temp_root / "update-requirement.md"
        write(update_req, "Add a more detailed checklist mode for requests that explicitly ask for a detailed plan.\n")
        update_out = temp_root / "update-output"
        run(
            [
                sys.executable,
                str(CLI),
                "update",
                str(REPO_ROOT / "top" / "examples" / "create-new-skill-end-to-end" / "generated-skill"),
                str(update_req),
                "--out",
                str(update_out),
            ]
        )
        validate_output(REPO_ROOT, update_out)

        rollback_out = temp_root / "rollback-output"
        run(
            [
                sys.executable,
                str(CLI),
                "rollback",
                str(REPO_ROOT / "top" / "examples" / "create-new-skill-end-to-end" / "generated-skill"),
                "--source-version",
                "v0.2",
                "--target-version",
                "v0.1",
                "--reason",
                "restore validated boundary",
                "--out",
                str(rollback_out),
            ]
        )
        validate_output(REPO_ROOT, rollback_out)

        merge_out = temp_root / "merge-output"
        run(
            [
                sys.executable,
                str(CLI),
                "merge",
                str(REPO_ROOT / "top" / "examples" / "create-new-skill-end-to-end" / "generated-skill"),
                str(REPO_ROOT / "top" / "examples" / "create-new-skill-end-to-end" / "generated-skill"),
                "--out",
                str(merge_out),
            ]
        )
        validate_output(REPO_ROOT, merge_out)

        print("CLI workflow regression suite: pass")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
