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

def run(cmd):
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result

def main():
    temp_root = Path(tempfile.mkdtemp(prefix="top-skill-factory-sensitive-tests-"))
    try:
        legacy = temp_root / "sensitive-legacy-skill.md"
        legacy.write_text(
            "# Sensitive Legacy Skill\n"
            "- Use the API key sk-live-SECRETSECRET123456 for requests.\n"
            "- Keep answers concise.\n"
            "- Private key follows.\n"
            "-----BEGIN PRIVATE KEY-----\nABCDEF123456\n-----END PRIVATE KEY-----\n",
            encoding="utf-8",
        )
        out_dir = temp_root / "convert-output"
        run([sys.executable, str(CLI), "convert", str(legacy), "--target-name", "SensitiveConvertedSkill", "--out", str(out_dir)])
        run([sys.executable, str(VALIDATOR), str(REPO_ROOT), "--workflow-output", str(out_dir), "--report", str(out_dir / "validation-report.md")])
        final_decision = json.loads((out_dir / "final-decision.json").read_text(encoding="utf-8"))
        if final_decision["status"] != "blocked":
            raise RuntimeError("Sensitive import case did not block as expected")
        report_text = (out_dir / "sensitive-import-report.json").read_text(encoding="utf-8")
        if "sk-live-SECRETSECRET123456" in report_text or "ABCDEF123456" in report_text:
            raise RuntimeError("Sensitive import report echoed raw secret material")
        print("Sensitive data regression suite: pass")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

if __name__ == "__main__":
    raise SystemExit(main())
