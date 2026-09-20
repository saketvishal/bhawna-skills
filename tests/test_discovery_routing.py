from pathlib import Path

from bhawna_skills.catalog_loader import load_catalog
from bhawna_skills.discovery import discover
from bhawna_skills.routing import route_items, walk_follow_ups


def test_empty_repo_is_sparse(tmp_path: Path) -> None:
    report = discover(tmp_path)
    assert "sparse" in report.dimensions
    catalog = load_catalog()
    items = route_items(catalog, report, mode="quick")
    ids = {i.id for i in items}
    assert "CORE-LANG" in ids or "SEC-SECRETS" in ids
    assert "FE-FRAMEWORK" not in ids


def test_python_cli_does_not_ask_frontend(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="demo"\ndependencies=["typer"]\n',
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    report = discover(tmp_path)
    assert "python" in report.dimensions
    assert "uv" in report.dimensions
    catalog = load_catalog()
    items = route_items(catalog, report, mode="guided")
    ids = {i.id for i in items}
    assert "CORE-PKG" in ids
    assert "FE-FRAMEWORK" not in ids


def test_frontend_signal_activates_frontend_pack(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"dependencies":{"react":"18.0.0"}}', encoding="utf-8")
    report = discover(tmp_path)
    assert "frontend" in report.dimensions
    items = route_items(load_catalog(), report)
    assert any(i.id.startswith("FE-") for i in items)


def test_vector_and_sql_tokens(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies=["psycopg","qdrant-client","fastapi"]\n',
        encoding="utf-8",
    )
    report = discover(tmp_path)
    assert "vector-store" in report.dimensions
    assert "sql" in report.dimensions or "data" in report.dimensions
    items = route_items(load_catalog(), report)
    ids = {i.id for i in items}
    assert "DATA-PERSIST" in ids
    assert "DATA-VECTOR-ROLE" in ids


def test_follow_ups_require_parent_answer() -> None:
    catalog = load_catalog()
    persist = catalog.item_by_id("DATA-PERSIST")
    canonical = catalog.item_by_id("DATA-CANONICAL")
    assert persist and canonical
    hidden = walk_follow_ups([persist, canonical], {})
    assert canonical not in hidden
    shown = walk_follow_ups([persist, canonical], {"DATA-PERSIST": "yes"})
    assert canonical in shown


def test_secrets_are_not_read(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("BHAWNA_API_KEY=super-secret\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    report = discover(tmp_path)
    assert ".env" in report.skipped_secret_paths
    blob = " ".join(f.detail for f in report.facts)
    assert "super-secret" not in blob
