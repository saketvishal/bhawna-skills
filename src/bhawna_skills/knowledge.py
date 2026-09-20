from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml

from .models import (
    CatalogItem,
    Conflict,
    DecisionSet,
    ExceptionSet,
    Invariant,
    InvariantSet,
    KnowledgeRecord,
    KnowledgeType,
    RecordStatus,
)

DECISIONS_FILE = "decisions.yaml"
EXCEPTIONS_FILE = "exceptions.yaml"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_decisions(root: Path, bhawna_dir: str = ".bhawna") -> DecisionSet:
    path = root / bhawna_dir / DECISIONS_FILE
    if not path.exists():
        return DecisionSet(project=root.name)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return DecisionSet.model_validate(data)


def save_decisions(root: Path, store: DecisionSet, bhawna_dir: str = ".bhawna") -> Path:
    path = root / bhawna_dir / DECISIONS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(store.model_dump(mode="json"), sort_keys=False), encoding="utf-8")
    return path


def load_exceptions(root: Path, bhawna_dir: str = ".bhawna") -> ExceptionSet:
    path = root / bhawna_dir / EXCEPTIONS_FILE
    if not path.exists():
        return ExceptionSet()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ExceptionSet.model_validate(data)


def accepted_enforced(store: DecisionSet) -> list[KnowledgeRecord]:
    return [
        r
        for r in store.records
        if r.status is RecordStatus.accepted
        and r.type in {KnowledgeType.invariant, KnowledgeType.deterministic_gate}
    ]


def unresolved_records(store: DecisionSet) -> list[KnowledgeRecord]:
    return [
        r
        for r in store.records
        if r.status in {RecordStatus.unresolved, RecordStatus.deferred, RecordStatus.proposed}
    ]


def find_conflict(store: DecisionSet, catalog_id: str, statement: str) -> Conflict | None:
    for rec in store.records:
        if rec.catalog_id != catalog_id:
            continue
        if rec.status in {RecordStatus.superseded, RecordStatus.rejected, RecordStatus.deprecated}:
            continue
        if rec.status is RecordStatus.accepted and rec.statement.strip() != statement.strip():
            return Conflict(
                catalog_id=catalog_id,
                existing_id=rec.id,
                existing_statement=rec.statement,
                candidate_statement=statement,
            )
    return None


def record_from_item(
    item: CatalogItem,
    *,
    status: RecordStatus,
    answer: str | None,
    evidence: list[str],
    statement: str | None = None,
) -> KnowledgeRecord:
    text = statement or _statement_for(item, answer)
    return KnowledgeRecord(
        id=item.id,
        catalog_id=item.id,
        type=item.type
        if status is not RecordStatus.unresolved
        else KnowledgeType.unresolved_decision,
        status=status,
        title=item.title,
        statement=text,
        importance=item.importance,
        answer=answer,
        rationale=item.rationale,
        sources=list(item.sources),
        evidence=evidence,
        confirmed_at=utc_now() if status is RecordStatus.accepted else None,
        pack=item.pack,
    )


def _statement_for(item: CatalogItem, answer: str | None) -> str:
    if item.invariant_templates and answer:
        tmpl = item.invariant_templates[0].statement
        return tmpl.replace("{answer}", answer)
    if answer:
        return f"{item.title}: {answer}"
    return item.question


def merge_record(store: DecisionSet, incoming: KnowledgeRecord) -> tuple[DecisionSet, Conflict | None]:
    conflict = None
    if incoming.catalog_id:
        conflict = find_conflict(store, incoming.catalog_id, incoming.statement)
    if conflict:
        return store, conflict
    existing = next((r for r in store.records if r.id == incoming.id), None)
    if existing and existing.status is RecordStatus.accepted and incoming.status is not RecordStatus.accepted:
        return store, None
    if existing and existing.status is RecordStatus.accepted:
        return store, None
    records = [r for r in store.records if r.id != incoming.id]
    records.append(incoming)
    store.records = records
    return store, None


def supersede(store: DecisionSet, existing_id: str, incoming: KnowledgeRecord) -> DecisionSet:
    records: list[KnowledgeRecord] = []
    for rec in store.records:
        if rec.id == existing_id:
            records.append(
                rec.model_copy(
                    update={
                        "status": RecordStatus.superseded,
                        "superseded_by": incoming.id,
                    }
                )
            )
        elif rec.id != incoming.id:
            records.append(rec)
    incoming.supersedes = list({*incoming.supersedes, existing_id})
    incoming.status = RecordStatus.accepted
    incoming.confirmed_at = incoming.confirmed_at or utc_now()
    records.append(incoming)
    store.records = records
    return store


def promote_invariants(
    item: CatalogItem,
    record: KnowledgeRecord,
    inv: InvariantSet,
) -> list[str]:
    if record.status is not RecordStatus.accepted:
        return []
    if item.type not in {KnowledgeType.invariant, KnowledgeType.deterministic_gate}:
        if not item.invariant_templates:
            return []
    added: list[str] = []
    templates = item.invariant_templates
    if not templates:
        return []
    existing_ids = {i.id for i in inv.invariants}
    for index, tmpl in enumerate(templates):
        iid = f"{item.id}.INV{index + 1}"
        if iid in existing_ids:
            continue
        statement = tmpl.statement.replace("{answer}", record.answer or "")
        inv.invariants.append(
            Invariant(
                id=iid,
                title=tmpl.title,
                statement=statement,
                rationale=tmpl.rationale or item.rationale,
                severity=tmpl.severity,
                catalog_id=item.id,
                knowledge_type=KnowledgeType.invariant,
                provenance=list(item.sources),
                evidence=list(record.evidence),
                confirmed_at=record.confirmed_at,
            )
        )
        added.append(iid)
    return added
