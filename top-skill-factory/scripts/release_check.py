#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=REPO)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    run([sys.executable, str(REPO / "scripts" / "validate_top_skill_factory.py"), str(REPO), "--report", str(REPO / "onboarding" / "schema-validation-report.md")])
    run([sys.executable, str(REPO / "scripts" / "test_cli_workflows.py")])
    run([sys.executable, str(REPO / "scripts" / "test_sensitive_cases.py")])
    print("Release check: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
