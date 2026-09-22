# Project decisions

Not every fact is an invariant. Bhawna types knowledge so coding-agent governance stays explainable.

## Types

| Type | Role |
| --- | --- |
| DECISION | A choice the project made |
| INVARIANT | A rule future work must not violate without superseding the decision |
| PREFERENCE | Overridable default |
| PROCEDURE | How a task is done |
| DETERMINISTIC_GATE | Often mechanically checkable requirement |
| UNRESOLVED_DECISION | Recognized question, not yet decided |

## Statuses

PROPOSED, ACCEPTED, SUPERSEDED, REJECTED, DEPRECATED, UNRESOLVED, DEFERRED, NOT_APPLICABLE.

Only **ACCEPTED** invariants (plus safety policy, scoped rules, and recorded exceptions) are enforced.

## Provenance

Records live in `.bhawna/decisions.yaml`. Sources, confirmation path, and supersede history stay in the repo so a later agent can explain *why* a check fired.

## Catalog

Versioned YAML packs ship with the package. They name **areas worth asking about** (architecture, dependencies, security, agents, and others). External standards listed as sources are guidance provenance, not universal requirements for every project.

## Commands

```bash
uv run bhawna decisions
uv run bhawna unresolved
uv run bhawna explain ID
uv run bhawna decision add
uv run bhawna decision propose
uv run bhawna decision supersede
```

Confirmations stay human-owned. See [guided onboarding](guided-onboarding.md).
