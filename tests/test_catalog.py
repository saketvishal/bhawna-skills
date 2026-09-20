from bhawna_skills.catalog_loader import load_catalog
from bhawna_skills.models import KnowledgeType


def test_catalog_loads_typed_items() -> None:
    catalog = load_catalog()
    items = catalog.all_items()
    assert len(items) >= 60
    ids = [i.id for i in items]
    assert len(ids) == len(set(ids))
    types = {i.type for i in items}
    assert KnowledgeType.decision in types
    assert KnowledgeType.invariant in types
    assert catalog.sources
    weak = [i.id for i in items if i.question.lower() in {"write clean code.", "use best practices."}]
    assert weak == []


def test_data_chain_follow_ups_exist() -> None:
    catalog = load_catalog()
    persist = catalog.item_by_id("DATA-PERSIST")
    assert persist is not None
    assert any(f.id == "DATA-CANONICAL" for f in persist.follow_ups)
