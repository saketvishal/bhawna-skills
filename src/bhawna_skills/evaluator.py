from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod

import httpx

from .models import (
    DecisionSet,
    EvaluationResult,
    ExceptionSet,
    Invariant,
    InvariantSet,
    RecordStatus,
    Verdict,
)
from .safety import safety_invariants


class Evaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        objective: str,
        constitution: str,
        invariants: InvariantSet,
        decisions: DecisionSet | None = None,
        exceptions: ExceptionSet | None = None,
    ) -> EvaluationResult:
        raise NotImplementedError


def enforced_invariants(
    invariants: InvariantSet,
    exceptions: ExceptionSet | None = None,
) -> list[Invariant]:
    excepted = {e.invariant_id for e in (exceptions.exceptions if exceptions else [])}
    rows = [i for i in invariants.invariants if i.id not in excepted]
    for extra in safety_invariants():
        if extra.id not in excepted:
            rows.append(extra)
    return rows


def decision_context(decisions: DecisionSet | None) -> str:
    if decisions is None:
        return ""
    lines: list[str] = []
    for rec in decisions.records:
        if rec.status is RecordStatus.accepted:
            lines.append(f"- [{rec.type.value}] {rec.id}: {rec.statement}")
    return "\n".join(lines)


class OpenAICompatibleEvaluator(Evaluator):
    """Semantic evaluator for any OpenAI-compatible chat-completions endpoint."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("BHAWNA_MODEL_URL", "").rstrip("/")
        self.api_key = os.environ.get("BHAWNA_API_KEY", "")
        self.model = os.environ.get("BHAWNA_MODEL", "")
        if not self.base_url or not self.model:
            raise RuntimeError(
                "Semantic evaluation requires BHAWNA_MODEL_URL and BHAWNA_MODEL. "
                "Set BHAWNA_API_KEY too when your provider requires authentication."
            )

    def evaluate(
        self,
        objective: str,
        constitution: str,
        invariants: InvariantSet,
        decisions: DecisionSet | None = None,
        exceptions: ExceptionSet | None = None,
    ) -> EvaluationResult:
        enforced = InvariantSet(
            project=invariants.project,
            version=invariants.version,
            invariants=enforced_invariants(invariants, exceptions),
        )
        invariant_json = enforced.model_dump_json(indent=2)
        accepted = decision_context(decisions)
        system = (
            "You are an architecture preflight reviewer. Detect whether a proposed "
            "engineering objective conflicts with CONFIRMED invariants and accepted "
            "project decisions. Do not invent requirements. Do not treat unresolved, "
            "deferred, rejected, or proposed records as blocking rules. Do not treat "
            "catalog suggestions as project law. Examples in an objective are evidence, "
            "not production rules unless the project explicitly says otherwise. "
            "Return JSON only."
        )
        schema = """{
  "verdict": "PASS|REVIEW|BLOCKED",
  "summary": "short summary",
  "findings": [
    {
      "invariant_id": "ID",
      "severity": "block|review|warn",
      "evidence": "quote or concise reference to the objective",
      "explanation": "why it conflicts",
      "recommendation": "minimal correction"
    }
  ],
  "evaluator": "semantic"
}"""
        user = (
            f"PROJECT CONSTITUTION\n{constitution}\n\n"
            f"CONFIRMED INVARIANTS AND SAFETY POLICY\n{invariant_json}\n\n"
            f"ACCEPTED DECISIONS (context, not unconfirmed)\n{accepted or '(none)'}\n\n"
            f"OBJECTIVE\n{objective}\n\n"
            f"Return this JSON shape exactly:\n{schema}"
        )

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        with httpx.Client(timeout=90) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            body = response.json()
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return EvaluationResult.model_validate(parsed)


class StaticPassEvaluator(Evaluator):
    """Useful for smoke tests and CI wiring; not a semantic safety gate."""

    def evaluate(
        self,
        objective: str,
        constitution: str,
        invariants: InvariantSet,
        decisions: DecisionSet | None = None,
        exceptions: ExceptionSet | None = None,
    ) -> EvaluationResult:
        del objective, constitution, invariants, decisions, exceptions
        return EvaluationResult(
            verdict=Verdict.pass_,
            summary="Configuration is valid. Semantic evaluation was not run.",
            findings=[],
            evaluator="static-pass",
        )
