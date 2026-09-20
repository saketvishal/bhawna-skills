from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .catalog_loader import load_catalog
from .config import save_invariants
from .discovery import discover
from .knowledge import (
    load_decisions,
    merge_record,
    promote_invariants,
    record_from_item,
    save_decisions,
    unresolved_records,
)
from .models import (
    CatalogItem,
    DiscoveryReport,
    InvariantSet,
    OnboardingResult,
    RecordStatus,
)
from .routing import route_items, walk_follow_ups

ACTION_ACCEPT = "accept"
ACTION_REJECT = "reject"
ACTION_DEFER = "defer"
ACTION_NA = "not_applicable"
ACTION_UNDECIDED = "undecided"


def _status_for_action(action: str) -> RecordStatus:
    mapping = {
        ACTION_ACCEPT: RecordStatus.accepted,
        ACTION_REJECT: RecordStatus.rejected,
        ACTION_DEFER: RecordStatus.deferred,
        ACTION_NA: RecordStatus.not_applicable,
        ACTION_UNDECIDED: RecordStatus.unresolved,
    }
    return mapping.get(action, RecordStatus.proposed)


def _evidence(report: DiscoveryReport, item: CatalogItem) -> list[str]:
    hints = set(item.discovery_hints.dimensions) | set(item.applies_when.any_dimensions)
    rows: list[str] = []
    for fact in report.facts:
        if set(fact.dimensions) & hints or fact.id in item.applies_when.any_facts:
            rows.append(f"{fact.id}: {fact.detail}")
    return rows[:8]


def load_answers_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return {}
    return data


def run_onboarding(
    root: Path,
    *,
    mode: str = "guided",
    show_all: bool = False,
    answers: dict[str, Any] | None = None,
    invariants: InvariantSet | None = None,
    auto_confirm: bool = False,
) -> OnboardingResult:
    if auto_confirm:
        raise ValueError("AUTO_CONFIRM_SEMANTIC_DECISIONS is forbidden")
    catalog = load_catalog()
    report = discover(root)
    relevant = route_items(catalog, report, mode=mode, show_all=show_all)
    answer_map: dict[str, str] = {}
    action_map: dict[str, str] = {}
    raw = answers or {}
    for key, value in raw.items():
        if isinstance(value, dict):
            action_map[key] = str(value.get("action", ACTION_ACCEPT if "answer" in value else ACTION_UNDECIDED))
            if "answer" in value:
                answer_map[key] = str(value["answer"])
        else:
            text = str(value)
            if text in {ACTION_REJECT, ACTION_DEFER, ACTION_NA, ACTION_UNDECIDED}:
                action_map[key] = text
            else:
                action_map[key] = ACTION_ACCEPT
                answer_map[key] = text

    visible = walk_follow_ups(relevant, answer_map)
    store = load_decisions(root)
    store.project = store.project or root.name
    inv = invariants or InvariantSet(project=store.project)
    result = OnboardingResult(mode=mode, discovery=report)
    result.relevant_item_ids = [i.id for i in visible]

    if mode == "discovery-only" or not raw:
        for item in visible:
            rec = record_from_item(
                item,
                status=RecordStatus.proposed,
                answer=None,
                evidence=_evidence(report, item),
            )
            store, conflict = merge_record(store, rec)
            if conflict:
                result.conflicts.append(conflict)
            else:
                result.candidates.append(rec)
        save_decisions(root, store)
        result.unresolved = unresolved_records(store)
        result.notes.append(
            "Candidates were recorded as PROPOSED. Nothing was auto-confirmed."
        )
        return result

    for item in visible:
        action = action_map.get(item.id, ACTION_UNDECIDED)
        answer = answer_map.get(item.id)
        status = _status_for_action(action)
        rec = record_from_item(
            item,
            status=status,
            answer=answer,
            evidence=_evidence(report, item),
        )
        store, conflict = merge_record(store, rec)
        if conflict:
            result.conflicts.append(conflict)
            continue
        if status is RecordStatus.accepted:
            result.accepted.append(rec)
            promoted = promote_invariants(item, rec, inv)
            result.promoted_invariants.extend(promoted)
        elif status in {RecordStatus.unresolved, RecordStatus.deferred, RecordStatus.proposed}:
            result.unresolved.append(rec)
        elif status is RecordStatus.rejected:
            pass
        else:
            result.unresolved.append(rec)

    save_decisions(root, store)
    if result.promoted_invariants:
        save_invariants(root, inv)
    result.unresolved = unresolved_records(store)
    return result



