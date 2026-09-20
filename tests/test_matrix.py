from pathlib import Path

from bhawna_skills.catalog_loader import load_catalog
from bhawna_skills.discovery import discover
from bhawna_skills.models import RecordStatus
from bhawna_skills.onboarding import run_onboarding
from bhawna_skills.routing import route_items


def _ids(tmp_path: Path, mode: str = "guided") -> set[str]:
    report = discover(tmp_path)
    return {i.id for i in route_items(load_catalog(), report, mode=mode)}


def test_python_api_fastapi(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies=["fastapi","uvicorn"]\n',
        encoding="utf-8",
    )
    ids = _ids(tmp_path)
    assert "API-STYLE" in ids
    assert "FE-FRAMEWORK" not in ids


def test_node_typescript_lockfile(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"devDependencies":{"typescript":"5.0.0"}}', encoding="utf-8")
    (tmp_path / "pnpm-lock.yaml").write_text("lockfileVersion: 9\n", encoding="utf-8")
    report = discover(tmp_path)
    assert "pnpm" in report.dimensions
    ids = _ids(tmp_path)
    assert "CORE-PKG" in ids


def test_fullstack(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\ndependencies=["fastapi"]\n', encoding="utf-8")
    (tmp_path / "package.json").write_text('{"dependencies":{"react":"18.2.0"}}', encoding="utf-8")
    ids = _ids(tmp_path)
    assert "API-STYLE" in ids
    assert "FE-FRAMEWORK" in ids


def test_existing_adrs(tmp_path: Path) -> None:
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0001.md").write_text("# ADR\n", encoding="utf-8")
    report = discover(tmp_path)
    assert "architecture" in report.dimensions
    assert "ARCH-ADR" in _ids(tmp_path)


def test_graph_plus_relational(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies=["neo4j","psycopg"]\n',
        encoding="utf-8",
    )
    report = discover(tmp_path)
    assert "graph" in report.dimensions
    assert "DATA-DERIVED" in _ids(tmp_path)


def test_not_applicable_and_defer(tmp_path: Path) -> None:
    result = run_onboarding(
        tmp_path,
        mode="guided",
        show_all=True,
        answers={
            "CORE-FORMAT": {"action": "not_applicable"},
            "CORE-LINT": {"action": "defer"},
        },
    )
    statuses = {r.id: r.status for r in result.unresolved}
    # not_applicable is not unresolved list - check store via candidates/accepted
    from bhawna_skills.knowledge import load_decisions

    store = load_decisions(tmp_path)
    by_id = {r.id: r.status for r in store.records}
    assert by_id.get("CORE-FORMAT") is RecordStatus.not_applicable
    assert by_id.get("CORE-LINT") is RecordStatus.deferred
    del statuses


def test_bhawnaignore(tmp_path: Path) -> None:
    (tmp_path / ".bhawnaignore").write_text("secret-notes.txt\n", encoding="utf-8")
    (tmp_path / "secret-notes.txt").write_text("token=abc\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='n'\n", encoding="utf-8")
    report = discover(tmp_path)
    details = " ".join(f.detail for f in report.facts)
    assert "token=abc" not in details


def test_repeated_init_does_not_clobber(tmp_path: Path) -> None:
    bh = tmp_path / ".bhawna"
    bh.mkdir()
    (bh / "constitution.md").write_text("KEEP-ME\n", encoding="utf-8")
    (bh / "invariants.yaml").write_text(
        "project: p\nversion: 1\ninvariants:\n- id: Z\n  title: Z\n  statement: z\n",
        encoding="utf-8",
    )
    run_onboarding(tmp_path, mode="discovery-only")
    run_onboarding(tmp_path, mode="discovery-only")
    assert "KEEP-ME" in (bh / "constitution.md").read_text(encoding="utf-8")
    assert "id: Z" in (bh / "invariants.yaml").read_text(encoding="utf-8")
