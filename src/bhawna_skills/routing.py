from __future__ import annotations

from .models import Catalog, CatalogItem, DiscoveryReport, Importance

IMPORTANCE_RANK = {
    Importance.critical: 0,
    Importance.high: 1,
    Importance.medium: 2,
    Importance.optional: 3,
}


def item_is_relevant(
    item: CatalogItem,
    report: DiscoveryReport,
    *,
    show_all: bool = False,
) -> bool:
    if show_all or item.applies_when.always:
        return True
    dims = set(report.dimensions)
    facts = {f.id for f in report.facts}
    rule = item.applies_when
    if rule.sparse_starter and "sparse" in dims:
        return True
    has_constraint = bool(
        rule.any_dimensions or rule.all_dimensions or rule.any_facts or rule.all_facts
    )
    if not has_constraint:
        return bool(rule.sparse_starter and "sparse" in dims)
    if rule.all_dimensions and not set(rule.all_dimensions) <= dims:
        return False
    if rule.all_facts and not set(rule.all_facts) <= facts:
        return False
    if rule.any_dimensions and not (set(rule.any_dimensions) & dims):
        return False
    if rule.any_facts and not (set(rule.any_facts) & facts):
        return False
    return True


def route_items(
    catalog: Catalog,
    report: DiscoveryReport,
    *,
    mode: str = "guided",
    show_all: bool = False,
) -> list[CatalogItem]:
    selected = [
        item for item in catalog.all_items() if item_is_relevant(item, report, show_all=show_all)
    ]
    if mode == "quick":
        selected = [
            i for i in selected if i.importance in {Importance.critical, Importance.high}
        ]
    selected.sort(key=lambda i: (IMPORTANCE_RANK[i.importance], i.pack, i.id))
    return selected


def _follow_up_parents(items: list[CatalogItem]) -> dict[str, list[tuple[CatalogItem, list[str]]]]:
    parents: dict[str, list[tuple[CatalogItem, list[str]]]] = {}
    for item in items:
        for fu in item.follow_ups:
            parents.setdefault(fu.id, []).append((item, fu.when_answer_in or ["*"]))
    return parents


def walk_follow_ups(
    items: list[CatalogItem],
    answers: dict[str, str],
) -> list[CatalogItem]:
    parents = _follow_up_parents(items)
    visible: list[CatalogItem] = []
    for item in items:
        if item.id not in parents:
            visible.append(item)
            continue
        for parent, allowed in parents[item.id]:
            answer = answers.get(parent.id)
            if answer is None:
                continue
            if "*" in allowed or answer in allowed:
                visible.append(item)
                break
    return visible
