from __future__ import annotations

from .models import Invariant, KnowledgeType, Severity

# Built-in product safety only. Not technology opinions.
SAFETY_INVARIANTS: list[Invariant] = [
    Invariant(
        id="BHAWNA-SAFE-001",
        title="Discoveries are not automatically confirmed",
        statement=(
            "Semantic or heuristic discoveries must remain candidates until a human "
            "or explicit project confirmation accepts them. Unconfirmed output must "
            "not be enforced as an invariant."
        ),
        rationale="Suggestion is not a confirmed rule.",
        severity=Severity.block,
        knowledge_type=KnowledgeType.invariant,
        provenance=["bhawna"],
    ),
    Invariant(
        id="BHAWNA-SAFE-002",
        title="Provenance is retained",
        statement="Recorded decisions and invariants must retain source and evidence fields when known.",
        severity=Severity.warn,
        knowledge_type=KnowledgeType.invariant,
        provenance=["bhawna"],
    ),
    Invariant(
        id="BHAWNA-SAFE-003",
        title="Rejected rules are not enforced",
        statement=(
            "Rejected, deferred, not-applicable, and unresolved records must not be treated "
            "as blocking invariants."
        ),
        severity=Severity.block,
        knowledge_type=KnowledgeType.invariant,
        provenance=["bhawna"],
    ),
    Invariant(
        id="BHAWNA-SAFE-004",
        title="Do not fabricate validation status",
        statement="Configuration-only checks must not be reported as semantic safety reviews.",
        severity=Severity.block,
        knowledge_type=KnowledgeType.invariant,
        provenance=["bhawna"],
    ),
    Invariant(
        id="BHAWNA-SAFE-005",
        title="Do not silently overwrite confirmed configuration",
        statement=(
            "Existing accepted decisions and invariants must not be replaced without an "
            "explicit supersede action."
        ),
        severity=Severity.block,
        knowledge_type=KnowledgeType.invariant,
        provenance=["bhawna"],
    ),
]


def safety_invariants() -> list[Invariant]:
    return list(SAFETY_INVARIANTS)
