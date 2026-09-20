from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .catalog_loader import load_catalog
from .config import (
    BHAWNA_DIR,
    CONSTITUTION_FILE,
    INVARIANTS_FILE,
    find_project_root,
    load_constitution,
    load_invariants,
    try_load_invariants,
)
from .discovery import discover
from .evaluator import OpenAICompatibleEvaluator, StaticPassEvaluator
from .knowledge import (
    load_decisions,
    load_exceptions,
    merge_record,
    save_decisions,
    supersede,
    unresolved_records,
    utc_now,
)
from .models import (
    KnowledgeRecord,
    KnowledgeType,
    RecordStatus,
    Verdict,
)
from .onboarding import load_answers_file, run_onboarding
from .routing import route_items

app = typer.Typer(
    help="Bhawna Skills — remember project decisions and check coding-agent objectives against them.",
    no_args_is_help=True,
)
decision_app = typer.Typer(help="Add, propose, or supersede decisions.")
app.add_typer(decision_app, name="decision")
console = Console()

DEFAULT_CONSTITUTION = """# Project Constitution

This file contains the durable engineering principles that objectives and plans must respect.

## Principles

1. Preserve explicit architectural decisions unless a new decision deliberately supersedes them.
2. Treat examples as evaluation fixtures, not implementation rules.
3. Prefer evidence over assumptions.
4. Do not declare work complete until required validation and integration gates pass.
5. Unconfirmed discoveries are candidates, not enforced rules.
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


def _emit(data: Any, as_json: bool) -> None:
    if as_json:
        console.print_json(json.dumps(data, indent=2, default=str))
        return
    if isinstance(data, str):
        console.print(data)


@app.command()
def init(
    path: Path = typer.Argument(Path.cwd(), help="Repository to initialize."),
    force: bool = typer.Option(False, "--force", help="Overwrite constitution/invariants templates."),
    mode: str = typer.Option(
        "discovery-only",
        "--mode",
        help="discovery-only | guided | quick",
    ),
    guided: bool = typer.Option(False, "--guided", help="Shortcut for --mode guided."),
    quick: bool = typer.Option(False, "--quick", help="Shortcut for --mode quick (CRITICAL/HIGH only)."),
    discovery_only: bool = typer.Option(
        False, "--discovery-only", help="Shortcut for --mode discovery-only."
    ),
    show_all: bool = typer.Option(False, "--all", help="Do not filter catalog by relevance."),
    answers: Path | None = typer.Option(None, "--answers", help="YAML map of catalog_id to answer/action."),
    json_out: bool = typer.Option(False, "--json", help="Machine-readable output."),
) -> None:
    """Initialize or refresh repository-owned decisions. Never auto-confirms discoveries."""
    root = path.resolve()
    target = root / BHAWNA_DIR
    target.mkdir(parents=True, exist_ok=True)
    constitution = target / CONSTITUTION_FILE
    invariants_path = target / INVARIANTS_FILE
    created: list[str] = []
    if constitution.exists() and not force:
        if not json_out:
            console.print(f"[yellow]Skipped[/yellow] {constitution} (already exists)")
    elif force or not constitution.exists():
        constitution.write_text(DEFAULT_CONSTITUTION, encoding="utf-8")
        created.append(str(constitution))
        if not json_out:
            console.print(f"[green]Created[/green] {constitution}")
    if invariants_path.exists() and not force:
        if not json_out:
            console.print(f"[yellow]Skipped[/yellow] {invariants_path} (already exists)")
    elif force or not invariants_path.exists():
        invariants_path.write_text(
            yaml.safe_dump(DEFAULT_INVARIANTS, sort_keys=False),
            encoding="utf-8",
        )
        created.append(str(invariants_path))
        if not json_out:
            console.print(f"[green]Created[/green] {invariants_path}")

    resolved_mode = mode
    if guided:
        resolved_mode = "guided"
    if quick:
        resolved_mode = "quick"
    if discovery_only:
        resolved_mode = "discovery-only"
    if resolved_mode not in {"guided", "quick", "discovery-only"}:
        raise typer.BadParameter("mode must be discovery-only, guided, or quick")

    answer_map = load_answers_file(answers)
    inv = try_load_invariants(root)
    result = run_onboarding(
        root,
        mode=resolved_mode,
        show_all=show_all,
        answers=answer_map if answer_map else None,
        invariants=inv,
        auto_confirm=False,
    )
    payload = result.model_dump(mode="json")
    payload["created"] = created
    payload["auto_confirm_semantic_decisions"] = False
    if json_out:
        _emit(payload, True)
        return
    console.print(
        Panel(
            f"mode={resolved_mode}\n"
            f"dimensions: {', '.join(result.discovery.dimensions) or '(none)'}\n"
            f"facts: {len(result.discovery.facts)}\n"
            f"relevant questions: {len(result.relevant_item_ids)}\n"
            f"candidates (PROPOSED): {len(result.candidates)}\n"
            f"accepted: {len(result.accepted)}\n"
            f"unresolved: {len(result.unresolved)}\n"
            f"conflicts: {len(result.conflicts)}\n"
            f"skipped secret paths: {', '.join(result.discovery.skipped_secret_paths) or '(none)'}",
            title="Bhawna onboarding",
        )
    )
    if result.relevant_item_ids:
        table = Table(title="Relevant decision areas (not yet enforced)")
        table.add_column("ID")
        table.add_column("Title")
        cat = load_catalog()
        for iid in result.relevant_item_ids[:40]:
            item = cat.item_by_id(iid)
            if item:
                table.add_row(item.id, item.title)
        console.print(table)
    for note in result.notes:
        console.print(f"[dim]{note}[/dim]")
    if result.conflicts:
        console.print("[red]DECISION CONFLICT[/red] — existing accepted records were kept.")
        for conflict in result.conflicts:
            console.print(f"  {conflict.catalog_id}: keep {conflict.existing_id}")


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
    decisions = load_decisions(root)
    checks.append(("decisions", True, f"{len(decisions.records)} records"))
    catalog = load_catalog()
    checks.append(("catalog", True, f"{len(catalog.all_items())} items"))

    table = Table(title="Bhawna doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for name, ok, detail in checks:
        table.add_row(name, "PASS" if ok else "FAIL", detail)
    console.print(table)
    if not all(ok for _, ok, _ in checks):
        raise typer.Exit(1)


@app.command("review")
def review_cmd(
    path: Path = typer.Argument(Path.cwd()),
    show_all: bool = typer.Option(False, "--all"),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Show relevant catalog areas and unresolved project questions."""
    root = find_project_root(path)
    report = discover(root)
    catalog = load_catalog()
    items = route_items(catalog, report, mode="guided", show_all=show_all)
    store = load_decisions(root)
    payload = {
        "dimensions": report.dimensions,
        "facts": [f.model_dump() for f in report.facts],
        "relevant": [{"id": i.id, "title": i.title, "importance": i.importance.value} for i in items],
        "unresolved": [r.model_dump() for r in unresolved_records(store)],
    }
    if json_out:
        _emit(payload, True)
        return
    console.print(f"Dimensions: {', '.join(report.dimensions)}")
    table = Table(title="Relevant areas")
    table.add_column("ID")
    table.add_column("Importance")
    table.add_column("Title")
    for item in items:
        table.add_row(item.id, item.importance.value, item.title)
    console.print(table)


@app.command("decisions")
def decisions_cmd(
    path: Path = typer.Argument(Path.cwd()),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """List recorded project knowledge."""
    root = find_project_root(path)
    store = load_decisions(root)
    if json_out:
        _emit(store.model_dump(mode="json"), True)
        return
    table = Table(title="Decisions")
    table.add_column("ID")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Statement")
    for rec in store.records:
        table.add_row(rec.id, rec.type.value, rec.status.value, rec.statement[:80])
    console.print(table)


@app.command()
def unresolved(
    path: Path = typer.Argument(Path.cwd()),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """List proposed, deferred, and undecided questions."""
    root = find_project_root(path)
    rows = unresolved_records(load_decisions(root))
    if json_out:
        _emit([r.model_dump(mode="json") for r in rows], True)
        return
    if not rows:
        console.print("No unresolved decisions.")
        return
    for rec in rows:
        console.print(f"[yellow]{rec.status.value}[/yellow] {rec.id}: {rec.title}")


@app.command()
def explain(
    rule_id: str,
    path: Path = typer.Argument(Path.cwd()),
) -> None:
    """Explain a confirmed invariant, safety rule, or catalog item."""
    from .safety import safety_invariants

    root = find_project_root(path)
    cat = load_catalog()
    item = cat.item_by_id(rule_id)
    if item:
        console.print(Panel(item.question, title=item.id))
        console.print(f"type={item.type.value} importance={item.importance.value} sources={item.sources}")
        return
    inv = try_load_invariants(root)
    for row in [*inv.invariants, *safety_invariants()]:
        if row.id == rule_id:
            console.print(Panel(row.statement, title=row.id))
            console.print(f"severity={row.severity.value} provenance={row.provenance} evidence={row.evidence}")
            console.print(f"confirmed_at={row.confirmed_at} catalog_id={row.catalog_id}")
            return
    raise typer.BadParameter(f"Unknown id {rule_id}")


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
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Check an objective against confirmed invariants (not unresolved catalog items)."""
    root = find_project_root(project)
    objective_text = objective.read_text(encoding="utf-8")
    invariants = load_invariants(root)
    constitution = load_constitution(root)
    decisions = load_decisions(root)
    exceptions = load_exceptions(root)
    evaluator = StaticPassEvaluator() if config_only else OpenAICompatibleEvaluator()
    result = evaluator.evaluate(
        objective_text,
        constitution,
        invariants,
        decisions=decisions,
        exceptions=exceptions,
    )
    if json_out:
        _emit(result.model_dump(mode="json"), True)
    else:
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


@decision_app.command("add")
def decision_add(
    catalog_id: str = typer.Option(..., "--id"),
    statement: str = typer.Option(..., "--statement"),
    knowledge_type: KnowledgeType = typer.Option(KnowledgeType.decision, "--type"),
    path: Path = typer.Option(Path.cwd(), "--project"),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Record an explicitly confirmed decision."""
    root = find_project_root(path)
    store = load_decisions(root)
    rec = KnowledgeRecord(
        id=catalog_id,
        catalog_id=catalog_id,
        type=knowledge_type,
        status=RecordStatus.accepted,
        title=catalog_id,
        statement=statement,
        confirmed_at=utc_now(),
        evidence=["explicit-cli"],
    )
    store, conflict = merge_record(store, rec)
    if conflict:
        console.print("[red]DECISION CONFLICT[/red] Use `bhawna decision supersede`.")
        raise typer.Exit(4)
    save_decisions(root, store)
    if json_out:
        _emit(rec.model_dump(mode="json"), True)
    else:
        console.print(f"[green]Accepted[/green] {rec.id}")


@decision_app.command("propose")
def decision_propose(
    catalog_id: str = typer.Option(..., "--id"),
    statement: str = typer.Option(..., "--statement"),
    path: Path = typer.Option(Path.cwd(), "--project"),
) -> None:
    """Submit a candidate (not enforced)."""
    root = find_project_root(path)
    store = load_decisions(root)
    rec = KnowledgeRecord(
        id=catalog_id,
        catalog_id=catalog_id,
        type=KnowledgeType.decision,
        status=RecordStatus.proposed,
        title=catalog_id,
        statement=statement,
        evidence=["agent-or-human-proposal"],
    )
    store, _conflict = merge_record(store, rec)
    save_decisions(root, store)
    console.print(f"[yellow]Proposed[/yellow] {rec.id} (not enforced)")


@decision_app.command("supersede")
def decision_supersede(
    existing: str = typer.Option(..., "--existing"),
    catalog_id: str = typer.Option(..., "--id"),
    statement: str = typer.Option(..., "--statement"),
    path: Path = typer.Option(Path.cwd(), "--project"),
) -> None:
    """Replace an accepted decision and keep history."""
    root = find_project_root(path)
    store = load_decisions(root)
    incoming = KnowledgeRecord(
        id=catalog_id,
        catalog_id=catalog_id,
        type=KnowledgeType.decision,
        status=RecordStatus.accepted,
        title=catalog_id,
        statement=statement,
        confirmed_at=utc_now(),
        evidence=["explicit-supersede"],
    )
    store = supersede(store, existing, incoming)
    save_decisions(root, store)
    console.print(f"[green]Superseded[/green] {existing} → {incoming.id}")


if __name__ == "__main__":
    app()
