from __future__ import annotations

from importlib import resources
from typing import Any

import yaml

from .models import Catalog, CatalogItem, CatalogPack, SourceRef

CATALOG_PACKAGE = "bhawna_skills.catalog"


def _read_yaml(name: str) -> Any:
    root = resources.files(CATALOG_PACKAGE)
    data = (root / name).read_text(encoding="utf-8")
    return yaml.safe_load(data) or {}


def load_catalog() -> Catalog:
    raw_sources = _read_yaml("sources.yaml")
    sources: dict[str, SourceRef] = {}
    for item in raw_sources.get("sources", []):
        ref = SourceRef.model_validate(item)
        sources[ref.id] = ref

    packs: list[CatalogPack] = []
    pack_root = resources.files(CATALOG_PACKAGE) / "packs"
    names = sorted(p.name for p in pack_root.iterdir() if p.name.endswith(".yaml"))
    for name in names:
        payload = yaml.safe_load((pack_root / name).read_text(encoding="utf-8")) or {}
        pack = CatalogPack.model_validate(payload)
        for item in pack.items:
            item.pack = pack.id
            item.category = item.category or pack.id
        packs.append(pack)
    return Catalog(version="1", sources=sources, packs=packs)


def load_signals() -> list[dict[str, Any]]:
    raw = _read_yaml("signals.yaml")
    return list(raw.get("signals", []))


def catalog_item_count(catalog: Catalog | None = None) -> int:
    cat = catalog or load_catalog()
    return len(cat.all_items())


def format_item(item: CatalogItem) -> str:
    return f"{item.id}: {item.title} [{item.type.value}/{item.importance.value}]"
