# Architecture

Public overview of how Bhawna Skills stores **project decisions** and enforces **architecture guardrails**. Product CLI: [Getting started](getting-started.md).

## Knowledge types

Bhawna does not treat every fact as an invariant.

| Type | Role |
| --- | --- |
| DECISION | A choice the project made |
| INVARIANT | A rule future work must not violate without superseding the decision |
| PREFERENCE | Overridable default |
| PROCEDURE | How a task is done |
| DETERMINISTIC_GATE | Often mechanically checkable requirement |
| UNRESOLVED_DECISION | Recognized question, not yet decided |

Statuses: PROPOSED, ACCEPTED, SUPERSEDED, REJECTED, DEPRECATED, UNRESOLVED, DEFERRED, NOT_APPLICABLE.

Unconfirmed semantic output never becomes an enforced invariant (`AUTO_CONFIRM_SEMANTIC_DECISIONS=NO`).

## Catalog

Versioned YAML packs ship in `bhawna_skills/catalog/`. Relevance comes from deterministic **signals** (files, globs, manifest tokens) plus `applies_when`. Follow-ups implement decision chains (e.g. persist → canonical store → derived role).

External standards are **guidance provenance**, not universal project requirements.

## Precedence (explainable)

1. Built-in Bhawna safety policy
2. Repository-wide confirmed invariant
3. Scoped confirmed rule (`applies_to` / `scope`)
4. Explicit recorded exception

Conflicts with an accepted record are reported; history is kept via supersede.

## v0.1 compatibility

Existing `.bhawna/constitution.md` and `invariants.yaml` still load. `init` without `--force` does not overwrite them.
