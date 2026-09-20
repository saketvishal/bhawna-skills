from __future__ import annotations

import shutil
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import (
    BHAWNA_DIR,
    CONSTITUTION_FILE,
    INVARIANTS_FILE,
    find_project_root,
    load_constitution,
    load_invariants,
)
from .evaluator import OpenAICompatibleEvaluator, StaticPassEvaluator
from .models import Verdict

app = typer.Typer(
    help="Bhawna Skills — guardrails for reliable AI coding agents.",
    no_args_is_help=True,
)
console = Console()

DEFAULT_CONSTITUTION = """# Project Constitution

This file contains the durable engineering principles that objectives and plans must respect.

## Principles

1. Preserve explicit architectural decisions unless a new decision deliberately supersedes them.
2. Treat examples as evaluation fixtures, not implementation rules.
3. Prefer evidence over assumptions.
4. Do not declare work complete until required validation and integration gates pass.
"""

DEFAULT_INVARIANTS = {
    "project": "your-project",
    "version": 1,
    "invariants": [
        {
            "id": "ARCH-001",
            "title": "Examples are not production rules",
            "statement": (
                "Examples and observed failures must not become example-specific "
                "production logic."
            ),
            "rationale": "The implementation must generalize beyond known fixtures.",
            "severity": "block",
            "applies_to": ["*"],
        },
        {
            "id": "DONE-001",
            "title": "Completion requires validation",
            "statement": "An objective is not complete merely because implementation code exists.",
            "rationale": "Required tests, review, and integration gates determine completion.",
            "severity": "block",
            "applies_to": ["*"],
        },
    ],
}


@app.command()
def init(
    path: Path = typer.Argument(Path.cwd(), help="Repository to initialize."),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite existing Bhawna configuration.",
    ),
) -> None:
    """Initialize repository-owned preflight guardrails."""
    root = path.resolve()
    target = root / BHAWNA_DIR
    target.mkdir(parents=True, exist_ok=True)
    constitution = target / CONSTITUTION_FILE
    invariants = target / INVARIANTS_FILE
    for file in (constitution, invariants):
        if file.exists() and not force:
            console.print(f"[yellow]Skipped[/yellow] {file} (already exists)")
    if force or not constitution.exists():
        constitution.write_text(DEFAULT_CONSTITUTION, encoding="utf-8")
        console.print(f"[green]Created[/green] {constitution}")
    if force or not invariants.exists():
        invariants.write_text(
            yaml.safe_dump(DEFAULT_INVARIANTS, sort_keys=False),
            encoding="utf-8",
        )
        console.print(f"[green]Created[/green] {invariants}")


@app.command()
def doctor(path: Path = typer.Argument(Path.cwd(), help="Repository to inspect.")) -> None:
    """Validate Bhawna configuration and local runtime prerequisites."""
    root = find_project_root(path)
    checks: list[tuple[str, bool, str]] = []
    try:
        inv = load_invariants(root)
        checks.append(("invariants", True, f"{len(inv.invariants)} loaded"))
    except Exception as exc:  # noqa: BLE001
        checks.append(("invariants", False, str(exc)))
    constitution = root / BHAWNA_DIR / CONSTITUTION_FILE
    checks.append(("constitution", constitution.exists(), str(constitution)))
    git_path = shutil.which("git")
    checks.append(("git", git_path is not None, git_path or "not found"))

    table = Table(title="Bhawna doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for name, ok, detail in checks:
        table.add_row(name, "PASS" if ok else "FAIL", detail)
    console.print(table)
    if not all(ok for _, ok, _ in checks):
        raise typer.Exit(1)


@app.command()
def check(
    objective: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    project: Path = typer.Option(
        Path.cwd(),
        "--project",
        help="Project containing .bhawna/",
    ),
    config_only: bool = typer.Option(
        False,
        "--config-only",
        help="Validate configuration only; does not perform semantic preflight.",
    ),
) -> None:
    """Check an objective against the project's constitution and invariants."""
    root = find_project_root(project)
    objective_text = objective.read_text(encoding="utf-8")
    invariants = load_invariants(root)
    constitution = load_constitution(root)
    evaluator = StaticPassEvaluator() if config_only else OpenAICompatibleEvaluator()
    result = evaluator.evaluate(objective_text, constitution, invariants)

    styles = {
        Verdict.pass_: "green",
        Verdict.review: "yellow",
        Verdict.blocked: "red",
    }
    style = styles[result.verdict]
    console.print(Panel(result.summary, title=f"[{style}]{result.verdict.value}[/{style}]"))

    if result.findings:
        table = Table(title="Findings")
        table.add_column("Invariant")
        table.add_column("Severity")
        table.add_column("Evidence")
        table.add_column("Explanation")
        for finding in result.findings:
            table.add_row(
                finding.invariant_id,
                finding.severity.value,
                finding.evidence,
                finding.explanation,
            )
        console.print(table)

    if result.verdict is Verdict.blocked:
        raise typer.Exit(2)
    if result.verdict is Verdict.review:
        raise typer.Exit(3)


if __name__ == "__main__":
    app()
