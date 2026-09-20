from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    block = "block"
    review = "review"
    warn = "warn"


class Verdict(StrEnum):
    pass_ = "PASS"
    review = "REVIEW"
    blocked = "BLOCKED"


class KnowledgeType(StrEnum):
    decision = "DECISION"
    invariant = "INVARIANT"
    preference = "PREFERENCE"
    procedure = "PROCEDURE"
    deterministic_gate = "DETERMINISTIC_GATE"
    unresolved_decision = "UNRESOLVED_DECISION"


class RecordStatus(StrEnum):
    proposed = "PROPOSED"
    accepted = "ACCEPTED"
    superseded = "SUPERSEDED"
    rejected = "REJECTED"
    deprecated = "DEPRECATED"
    unresolved = "UNRESOLVED"
    deferred = "DEFERRED"
    not_applicable = "NOT_APPLICABLE"


class Importance(StrEnum):
    critical = "CRITICAL"
    high = "HIGH"
    medium = "MEDIUM"
    optional = "OPTIONAL"


class AnswerType(StrEnum):
    choice = "choice"
    multi = "multi"
    free_text = "free_text"
    confirm = "confirm"


class Invariant(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    rationale: str | None = None
    severity: Severity = Severity.block
    applies_to: list[str] = Field(default_factory=lambda: ["*"])
    forbidden: list[str] = Field(default_factory=list)
    required: list[str] = Field(default_factory=list)
    catalog_id: str | None = None
    knowledge_type: KnowledgeType = KnowledgeType.invariant
    provenance: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confirmed_at: str | None = None


class InvariantSet(BaseModel):
    project: str = "project"
    version: int = 1
    invariants: list[Invariant] = Field(default_factory=list)


class Finding(BaseModel):
    invariant_id: str
    severity: Severity
    evidence: str
    explanation: str
    recommendation: str | None = None


class EvaluationResult(BaseModel):
    verdict: Verdict
    summary: str
    findings: list[Finding] = Field(default_factory=list)
    evaluator: str


class SourceRef(BaseModel):
    id: str
    name: str
    url: str | None = None
    source_type: str = "guidance"
    concept: str | None = None
    retrieved: str | None = None
    notes: str | None = None


class DiscoveryHint(BaseModel):
    files: list[str] = Field(default_factory=list)
    globs: list[str] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)


class AppliesWhen(BaseModel):
    any_dimensions: list[str] = Field(default_factory=list)
    all_dimensions: list[str] = Field(default_factory=list)
    any_facts: list[str] = Field(default_factory=list)
    all_facts: list[str] = Field(default_factory=list)
    always: bool = False
    sparse_starter: bool = False


class FollowUp(BaseModel):
    id: str
    when_answer_in: list[str] = Field(default_factory=list)


class InvariantTemplate(BaseModel):
    title: str
    statement: str
    severity: Severity = Severity.block
    rationale: str | None = None


class CatalogItem(BaseModel):
    id: str
    title: str
    type: KnowledgeType
    category: str
    importance: Importance = Importance.medium
    question: str
    rationale: str | None = None
    applies_when: AppliesWhen = Field(default_factory=AppliesWhen)
    discovery_hints: DiscoveryHint = Field(default_factory=DiscoveryHint)
    answer_type: AnswerType = AnswerType.choice
    options: list[str] = Field(default_factory=list)
    follow_ups: list[FollowUp] = Field(default_factory=list)
    invariant_templates: list[InvariantTemplate] = Field(default_factory=list)
    confirmation_required: bool = True
    sources: list[str] = Field(default_factory=list)
    version: int = 1
    tags: list[str] = Field(default_factory=list)
    pack: str = ""


class CatalogPack(BaseModel):
    id: str
    title: str
    version: int = 1
    description: str = ""
    items: list[CatalogItem] = Field(default_factory=list)


class Catalog(BaseModel):
    version: str = "1"
    sources: dict[str, SourceRef] = Field(default_factory=dict)
    packs: list[CatalogPack] = Field(default_factory=list)

    def item_by_id(self, item_id: str) -> CatalogItem | None:
        for pack in self.packs:
            for item in pack.items:
                if item.id == item_id:
                    return item
        return None

    def all_items(self) -> list[CatalogItem]:
        items: list[CatalogItem] = []
        for pack in self.packs:
            for item in pack.items:
                items.append(item)
        return items


class DiscoveryFact(BaseModel):
    id: str
    kind: str
    detail: str
    dimensions: list[str] = Field(default_factory=list)


class DiscoveryReport(BaseModel):
    facts: list[DiscoveryFact] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)
    skipped_secret_paths: list[str] = Field(default_factory=list)


class KnowledgeRecord(BaseModel):
    id: str
    catalog_id: str | None = None
    type: KnowledgeType
    status: RecordStatus
    title: str
    statement: str
    importance: Importance = Importance.medium
    scope: list[str] = Field(default_factory=lambda: ["*"])
    answer: str | None = None
    rationale: str | None = None
    sources: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confirmed_at: str | None = None
    supersedes: list[str] = Field(default_factory=list)
    superseded_by: str | None = None
    pack: str | None = None


class DecisionSet(BaseModel):
    project: str = "project"
    version: int = 1
    records: list[KnowledgeRecord] = Field(default_factory=list)


class ExceptionRecord(BaseModel):
    invariant_id: str
    scope: list[str] = Field(default_factory=lambda: ["*"])
    rationale: str
    source: str | None = None
    expires: str | None = None
    created_at: str | None = None


class ExceptionSet(BaseModel):
    version: int = 1
    exceptions: list[ExceptionRecord] = Field(default_factory=list)


class Conflict(BaseModel):
    catalog_id: str
    existing_id: str
    existing_statement: str
    candidate_statement: str


class OnboardingResult(BaseModel):
    mode: str
    discovery: DiscoveryReport
    relevant_item_ids: list[str] = Field(default_factory=list)
    candidates: list[KnowledgeRecord] = Field(default_factory=list)
    accepted: list[KnowledgeRecord] = Field(default_factory=list)
    unresolved: list[KnowledgeRecord] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    promoted_invariants: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
