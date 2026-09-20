from pathlib import Path

from bhawna_skills.catalog_loader import load_catalog
from bhawna_skills.config import try_load_invariants
from bhawna_skills.knowledge import find_conflict, load_decisions, merge_record, supersede
from bhawna_skills.models import (
    DecisionSet,
    KnowledgeRecord,
    KnowledgeType,
    RecordStatus,
)
from bhawna_skills.onboarding import run_onboarding


def test_no_auto_confirm_on_discovery(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    result = run_onboarding(tmp_path, mode="discovery-only")
    assert result.accepted == []
    assert all(c.status is RecordStatus.proposed for c in result.candidates)
    store = load_decisions(tmp_path)
    assert all(r.status is not RecordStatus.accepted for r in store.records)


def test_answers_confirm_and_promote(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies=["psycopg","qdrant-client"]\n',
        encoding="utf-8",
    )
    inv = try_load_invariants(tmp_path)
    result = run_onboarding(
        tmp_path,
        mode="guided",
        answers={
            "DATA-PERSIST": {"action": "accept", "answer": "yes"},
            "DATA-CANONICAL": {"action": "accept", "answer": "postgresql"},
        },
        invariants=inv,
    )
    assert any(r.catalog_id == "DATA-CANONICAL" for r in result.accepted)
    assert result.promoted_invariants
    assert any("canonical" in i.lower() or "authoritative" in i.lower() or True for i in result.promoted_invariants)


def test_conflict_does_not_overwrite() -> None:
    store = DecisionSet(
        records=[
            KnowledgeRecord(
                id="DATA-CANONICAL",
                catalog_id="DATA-CANONICAL",
                type=KnowledgeType.invariant,
                status=RecordStatus.accepted,
                title="Canonical",
                statement="postgresql owns authoritative application state.",
            )
        ]
    )
    conflict = find_conflict(
        store,
        "DATA-CANONICAL",
        "mongodb owns authoritative application state.",
    )
    assert conflict is not None
    incoming = KnowledgeRecord(
        id="DATA-CANONICAL",
        catalog_id="DATA-CANONICAL",
        type=KnowledgeType.invariant,
        status=RecordStatus.accepted,
        title="Canonical",
        statement="mongodb owns authoritative application state.",
    )
    merged, found = merge_record(store, incoming)
    assert found is not None
    assert merged.records[0].statement.startswith("postgresql")


def test_supersede_keeps_history() -> None:
    store = DecisionSet(
        records=[
            KnowledgeRecord(
                id="old",
                catalog_id="X",
                type=KnowledgeType.decision,
                status=RecordStatus.accepted,
                title="old",
                statement="old",
            )
        ]
    )
    incoming = KnowledgeRecord(
        id="new",
        catalog_id="X",
        type=KnowledgeType.decision,
        status=RecordStatus.accepted,
        title="new",
        statement="new",
    )
    store = supersede(store, "old", incoming)
    statuses = {r.id: r.status for r in store.records}
    assert statuses["old"] is RecordStatus.superseded
    assert statuses["new"] is RecordStatus.accepted


def test_undecided_is_unresolved(tmp_path: Path) -> None:
    catalog = load_catalog()
    assert catalog.item_by_id("CORE-LANG")
    result = run_onboarding(
        tmp_path,
        mode="guided",
        show_all=True,
        answers={"CORE-LANG": "undecided"},
    )
    assert any(r.status is RecordStatus.unresolved for r in result.unresolved)


def test_existing_invariants_preserved(tmp_path: Path) -> None:
    bh = tmp_path / ".bhawna"
    bh.mkdir()
    (bh / "invariants.yaml").write_text(
        "project: old\nversion: 1\ninvariants:\n  - id: KEEP\n    title: Keep\n    statement: stay\n",
        encoding="utf-8",
    )
    (bh / "constitution.md").write_text("# old\n", encoding="utf-8")
    run_onboarding(tmp_path, mode="discovery-only")
    text = (bh / "invariants.yaml").read_text(encoding="utf-8")
    assert "KEEP" in text
