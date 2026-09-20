"""Deterministic demo of InvariantGate's configuration path.

Prints the sample project's invariants and a conflicting objective, then runs
`bhawna check --config-only`. That path validates files; it does not perform
semantic comparison. Semantic BLOCKED/PASS requires BHAWNA_MODEL_URL.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "sample-project"
OBJECTIVE = SAMPLE / "objectives" / "use-pip.md"
INVARIANTS = SAMPLE / ".bhawna" / "invariants.yaml"


def main() -> int:
    print("=== Sample invariants ===")
    print(INVARIANTS.read_text(encoding="utf-8"))
    print("=== Proposed objective ===")
    print(OBJECTIVE.read_text(encoding="utf-8"))
    print("=== bhawna check --config-only ===")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "bhawna_skills.cli",
            "check",
            str(OBJECTIVE),
            "--project",
            str(SAMPLE),
            "--config-only",
        ],
        cwd=ROOT,
        check=False,
    )
    print()
    print(
        "This demo is deterministic: --config-only reports that the "
        "guardrail files are valid. It does not claim the objective is safe."
    )
    print(
        "For semantic PASS/REVIEW/BLOCKED, set BHAWNA_MODEL_URL and "
        "BHAWNA_MODEL, then run without --config-only."
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
