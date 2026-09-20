from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    block = "block"
    review = "review"
    warn = "warn"


class Verdict(str, Enum):
    pass_ = "PASS"
    review = "REVIEW"
    blocked = "BLOCKED"


class Invariant(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    rationale: str | None = None
    severity: Severity = Severity.block
    applies_to: list[str] = Field(default_factory=lambda: ["*"])
    forbidden: list[str] = Field(default_factory=list)
    required: list[str] = Field(default_factory=list)


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
