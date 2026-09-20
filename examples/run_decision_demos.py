"""Run discovery/guided demos against fixture projects (no LLM)."""

from __future__ import annotations

import json
from pathlib import Path

from bhawna_skills.onboarding import load_answers_file, run_onboarding

ROOT = Path(__file__).resolve().parents[1]


def run(name: str, rel: str, mode: str = "discovery-only", answers: Path | None = None) -> None:
    path = ROOT / rel
    result = run_onboarding(
        path,
        mode=mode,
        answers=load_answers_file(answers) or None,
    )
    print(f"=== {name} ===")
    print(
        json.dumps(
            {
                "dimensions": result.discovery.dimensions,
                "relevant": result.relevant_item_ids,
                "accepted": [r.id for r in result.accepted],
                "candidates": len(result.candidates),
                "unresolved": [r.id for r in result.unresolved],
                "promoted": result.promoted_invariants,
                "auto_confirm": False,
            },
            indent=2,
        )
    )


def main() -> None:
    run("simple", "examples/demo-simple")
    run("fullstack", "examples/demo-fullstack")
    run(
        "ai-guided",
        "examples/demo-ai",
        mode="guided",
        answers=ROOT / "examples/demo-ai/answers.yaml",
    )


if __name__ == "__main__":
    main()
